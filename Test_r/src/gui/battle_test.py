import pygame
import requests
from io import BytesIO
import sys
import os
import random

# Ajouter le dossier src au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.Pokemon import Pokemon
from utils.PokemonTypeUtils import PokemonTypeUtils

class BattleWindow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pokémon Battle Test")
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        
        # Créer les Pokémon avec toutes leurs stats
        self.pokemon1 = Pokemon("pikachu")  # Plus besoin de spécifier les stats
        self.pokemon2 = Pokemon("charizard")
        
        # Charger les sprites
        self.load_sprites()
        
        # Police
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Variables pour l'animation
        self.is_attacking = False
        self.attack_frame = 0
        self.original_pos1 = (100, 300)  # Position initiale de Pikachu
        self.original_pos2 = (500, 100)  # Position initiale de Dracaufeu
        self.current_pos1 = self.original_pos1
        self.current_pos2 = self.original_pos2
        
        # Clock pour contrôler la vitesse d'animation
        self.clock = pygame.time.Clock()
        
        self.selected_move = 0  # Index du move sélectionné
        
    def load_sprites(self):
        try:
            # Essayer de charger les sprites animés
            if self.pokemon1.animated_back:
                response1 = requests.get(self.pokemon1.animated_back)
            else:
                response1 = requests.get(self.pokemon1.back_sprite_url)
                
            if self.pokemon2.animated_front:
                response2 = requests.get(self.pokemon2.animated_front)
            else:
                response2 = requests.get(self.pokemon2.front_sprite_url)
            
            # Convertir en images Pygame
            img1 = BytesIO(response1.content)
            img2 = BytesIO(response2.content)
            
            self.sprite1 = pygame.image.load(img1)
            self.sprite2 = pygame.image.load(img2)
            
            # Agrandir les sprites (×3)
            size1 = self.sprite1.get_size()
            size2 = self.sprite2.get_size()
            self.sprite1 = pygame.transform.scale(self.sprite1, (size1[0] * 3, size1[1] * 3))
            self.sprite2 = pygame.transform.scale(self.sprite2, (size2[0] * 3, size2[1] * 3))
        except Exception as e:
            print(f"Erreur: {e}")
        
    def draw_health_bar(self, x, y, health, max_health):
        bar_width = 200
        bar_height = 20
        fill_width = int(bar_width * (health / max_health))
        
        # Fond blanc
        pygame.draw.rect(self.screen, self.WHITE, (x, y, bar_width, bar_height))
        # Barre verte
        pygame.draw.rect(self.screen, self.GREEN, (x, y, fill_width, bar_height))
        # Contour noir
        pygame.draw.rect(self.screen, self.BLACK, (x, y, bar_width, bar_height), 2)
        
        # Texte PV
        text = self.font.render(f"PV: {health}/{max_health}", True, self.BLACK)
        self.screen.blit(text, (x, y + 25))
        
    def draw_pokemon_info(self, pokemon, x, y, is_player):
        # Nom et niveau
        text = self.font.render(f"{pokemon.name.upper()} Nv.50", True, self.BLACK)
        self.screen.blit(text, (x, y))
        
        # Types
        types_text = self.small_font.render(f"Types: {', '.join(pokemon.types)}", True, self.BLACK)
        self.screen.blit(types_text, (x, y + 30))
        
        # Stats
        stats_text = self.small_font.render(
            f"ATK: {pokemon.attack} DEF: {pokemon.defense} SPD: {pokemon.speed}", 
            True, self.BLACK
        )
        self.screen.blit(stats_text, (x, y + 60))
        
        # Afficher les moves avec leurs détails
        y_offset = y + 90
        for move in pokemon.moves:
            move_text = self.small_font.render(
                f"{move['name']} - PWR:{move['power']} ACC:{move['accuracy']} PP:{move['pp']}", 
                True, self.BLACK
            )
            self.screen.blit(move_text, (x, y_offset))
            y_offset += 20
        
        # Afficher les infos supplémentaires
        if hasattr(pokemon, 'habitat'):
            info_text = self.small_font.render(
                f"Habitat: {pokemon.habitat} {'⭐' if pokemon.is_legendary else ''}", 
                True, self.BLACK
            )
            self.screen.blit(info_text, (x, y_offset + 20))
        
        # Afficher le statut
        if pokemon.status_condition:
            status_text = self.small_font.render(
                f"Status: {pokemon.status_condition['name'].upper()}", 
                True, self.RED
            )
            self.screen.blit(status_text, (x, y + 120))

    def animate_attack(self):
        if self.is_attacking:
            # Animation de Pikachu qui avance pour attaquer
            if self.attack_frame < 5:
                self.current_pos1 = (
                    self.original_pos1[0] + (self.attack_frame * 20),
                    self.original_pos1[1]
                )
            # Animation de Pikachu qui recule
            elif self.attack_frame < 10:
                self.current_pos1 = (
                    self.original_pos1[0] + ((10 - self.attack_frame) * 20),
                    self.original_pos1[1]
                )
            # Animation de Dracaufeu qui tremble quand il est touché
            if 5 <= self.attack_frame < 8:
                self.current_pos2 = (
                    self.original_pos2[0] + ((-1)**(self.attack_frame) * 10),
                    self.original_pos2[1]
                )
            else:
                self.current_pos2 = self.original_pos2
                
            self.attack_frame += 1
            if self.attack_frame >= 10:
                self.is_attacking = False
                self.attack_frame = 0
                self.current_pos1 = self.original_pos1
                self.current_pos2 = self.original_pos2

    def use_move(self):
        move = self.pokemon1.moves[self.selected_move]
        
        # Calculer les dégâts selon le type d'attaque
        if move['damage_class'] == 'physical':
            base_damage = move['power'] * (self.pokemon1.attack / self.pokemon2.defense)
        else:  # special
            base_damage = move['power'] * (self.pokemon1.special_attack / self.pokemon2.special_defense)
            
        # Appliquer le multiplicateur de type
        type_multiplier = PokemonTypeUtils.get_type_effectiveness(move['type'], self.pokemon2.types[0])
        final_damage = int(base_damage * type_multiplier)
        
        # Vérifier la précision
        accuracy_check = random.randint(1, 100)
        if accuracy_check <= move['accuracy']:
            self.pokemon2.take_damage(final_damage)
            return True, f"{move['name']} inflige {final_damage} dégâts!"
        else:
            return False, f"{move['name']} rate sa cible!"

    def run(self):
        running = True
        while running:
            self.clock.tick(30)  # 30 FPS
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        # Sélectionner le move (1-4)
                        self.selected_move = event.key - pygame.K_1
                        if self.selected_move < len(self.pokemon1.moves):
                            hit, message = self.use_move()
                            if hit:
                                self.is_attacking = True
                    elif event.key == pygame.K_r:
                        self.pokemon1.current_hp = self.pokemon1.max_hp
                        self.pokemon2.current_hp = self.pokemon2.max_hp
            
            # Animer l'attaque
            self.animate_attack()
            
            # Dessiner
            self.screen.fill(self.WHITE)
            
            # Dessiner les sprites aux positions actuelles
            self.screen.blit(self.sprite1, self.current_pos1)
            self.screen.blit(self.sprite2, self.current_pos2)
            
            # Dessiner les infos des Pokémon
            self.draw_pokemon_info(self.pokemon1, 50, 400, True)
            self.draw_pokemon_info(self.pokemon2, 450, 50, False)
            
            # Dessiner les barres de vie
            self.draw_health_bar(100, 450, self.pokemon1.current_hp, self.pokemon1.max_hp)
            self.draw_health_bar(500, 50, self.pokemon2.current_hp, self.pokemon2.max_hp)
            
            # Instructions
            instructions = self.font.render("1-4 pour sélectionner un move, R pour reset", True, self.BLACK)
            self.screen.blit(instructions, (200, 550))
            
            pygame.display.flip()
            
        pygame.quit()

def main():
    game = BattleWindow()
    game.run()

if __name__ == "__main__":
    main() 