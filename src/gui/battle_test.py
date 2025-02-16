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
        
        # Positions initiales (AVANT load_sprites)
        self.original_pos1 = (100, 300)  # Position initiale de Pikachu
        self.original_pos2 = (500, 100)  # Position initiale de Dracaufeu
        self.current_pos1 = self.original_pos1
        self.current_pos2 = self.original_pos2
        
        # Créer les Pokémon
        self.pokemon1 = Pokemon("pikachu")
        self.pokemon2 = Pokemon("charizard")
        
        # Variables pour l'animation
        self.is_attacking = False
        self.attack_frame = 0
        
        # Variables pour l'animation des ailes
        self.wing_angle = 0
        self.wing_speed = 0.5
        self.wing_max_angle = 8
        self.wing_direction = 1
        
        # Variables pour l'animation idle
        self.idle_frame = 0
        self.idle_direction = 1
        self.idle_offset = 0
        self.idle_max_offset = 10
        self.idle_speed = 0.5
        
        # Référence au sprite original
        self.original_sprite2 = None
        
        # APRÈS avoir initialisé toutes les positions
        self.load_sprites()
        
        # Police
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Clock
        self.clock = pygame.time.Clock()
        
        self.selected_move = 0
        
    def load_sprites(self):
        try:
            print("Début du chargement des sprites...")  # Debug
            
            # Charger les sprites
            response1 = requests.get(self.pokemon1.back_sprite_url)
            response2 = requests.get(self.pokemon2.front_sprite_url)
            
            if response1.status_code != 200 or response2.status_code != 200:
                raise Exception("Erreur lors du téléchargement des sprites")
            
            # Convertir en images Pygame
            img1 = BytesIO(response1.content)
            img2 = BytesIO(response2.content)
            
            # Charger les sprites
            self.sprite1 = pygame.image.load(img1)
            self.sprite2 = pygame.image.load(img2)
            
            if not self.sprite1 or not self.sprite2:
                raise Exception("Erreur lors du chargement des images")
            
            # Agrandir les sprites
            size1 = self.sprite1.get_size()
            size2 = self.sprite2.get_size()
            self.sprite1 = pygame.transform.scale(self.sprite1, (size1[0] * 3, size1[1] * 3))
            self.sprite2 = pygame.transform.scale(self.sprite2, (size2[0] * 3, size2[1] * 3))
            
            print("Sprites chargés et redimensionnés")  # Debug
            
            # Créer la copie et vérifier qu'elle est valide
            self.original_sprite2 = self.sprite2.copy()
            if not self.original_sprite2:
                raise Exception("Erreur lors de la copie du sprite")
            
            print("Copie du sprite créée")  # Debug
            
            # Initialiser le rectangle
            self.sprite2_rect = self.sprite2.get_rect()
            self.sprite2_rect.center = self.current_pos2
            
            print("Chargement des sprites terminé avec succès")  # Debug
            
        except Exception as e:
            print(f"Erreur détaillée lors du chargement des sprites: {e}")
            # Initialiser avec des valeurs par défaut en cas d'erreur
            self.original_sprite2 = self.sprite2
            self.sprite2_rect = self.sprite2.get_rect(center=self.current_pos2)
        
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

    def animate_idle(self):
        """Animation de flottement et des ailes pour Dracaufeu"""
        if not self.is_attacking:
            # Flottement vertical
            self.idle_offset += self.idle_direction * self.idle_speed
            if abs(self.idle_offset) >= self.idle_max_offset:
                self.idle_direction *= -1
            
            # Animation des ailes
            self.wing_angle += self.wing_direction * self.wing_speed
            if abs(self.wing_angle) >= self.wing_max_angle:
                self.wing_direction *= -1
            
            # Créer une copie rotative du sprite
            rotated = pygame.transform.rotate(self.original_sprite2, self.wing_angle)
            
            # Obtenir le rectangle pour centrer la rotation
            rect = rotated.get_rect(center=self.current_pos2)
            
            # Mettre à jour la position et le sprite
            self.current_pos2 = (
                self.original_pos2[0],
                self.original_pos2[1] + self.idle_offset
            )
            self.sprite2 = rotated
            self.sprite2_rect = rect

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
            
            # Animer l'attaque ou l'idle
            if self.is_attacking:
                self.animate_attack()
            else:
                self.animate_idle()
            
            # Dessiner
            self.screen.fill(self.WHITE)
            
            # Dessiner les sprites
            self.screen.blit(self.sprite1, self.current_pos1)
            if hasattr(self, 'sprite2_rect'):
                self.screen.blit(self.sprite2, self.sprite2_rect)
            else:
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