import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import pygame
from data.pokemon_data import SPECIES_DATA, POKEMON_NAMES_FR, TYPE_NAMES_FR
from utils.SpriteManager import SpriteManager

class PokemonSelection:
    def __init__(self, screen):
        self.screen = screen
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        
        # Initialiser le gestionnaire de sprites
        self.sprite_manager = SpriteManager()
        
        # Chemin de base pour les assets
        self.assets_path = os.path.join("src", "assets")
        
        # Même style que nos autres menus
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.POKEMON_YELLOW = (255, 236, 0)
        self.POKEMON_BLUE = (0, 144, 255)
        self.POKEMON_BLUE_LIGHT = (0, 90, 255)
        
        # Police
        try:
            font_path = os.path.join("src", "assets", "fonts", "pokemon.ttf")
            self.font = pygame.font.Font(font_path, 36)
        except Exception as e:
            print(f"Erreur lors du chargement de la police: {e}")
            self.font = pygame.font.Font(None, 36)
        
        # Charger les données des Pokémon
        self.available_pokemon = []
        self.selected_pokemon = []
        self.load_pokemon_data()
        
        # Fond
        try:
            background_path = os.path.join(self.assets_path, "pokemon_backgroundfinale.jpg")
            self.background = pygame.image.load(background_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (self.current_width, self.current_height))
        except Exception as e:
            print(f"Erreur lors du chargement de l'image de fond: {e}")
            self.background = None
        
        # Ajout des variables pour le défilement
        self.scroll_y = 0
        self.scroll_speed = 30
        self.max_scroll = 0  # Sera calculé en fonction du nombre de Pokémon
        
        # Bouton de confirmation
        self.confirm_button = pygame.Rect(
            self.current_width//2 - 100,
            self.current_height - 60,
            200,
            50
        )
        
        # Police plus adaptée pour les stats
        try:
            self.title_font = pygame.font.Font(font_path, 40)
            self.stats_font = pygame.font.Font(font_path, 25)
        except Exception as e:
            print(f"Erreur lors du chargement de la police: {e}")
            self.title_font = pygame.font.Font(None, 40)
            self.stats_font = pygame.font.Font(None, 25)

    def load_pokemon_data(self):
        """Charge les données et sprites des Pokémon"""
        for name, data in SPECIES_DATA.items():
            try:
                # Utiliser le sprite statique pour la sélection
                sprite = self.sprite_manager.get_sprite(
                    POKEMON_NAMES_FR.get(name, name),
                    animated=False,
                    is_back=False
                )
                
                if sprite:
                    pokemon = {
                        'name': POKEMON_NAMES_FR.get(name, name),
                        'sprite': sprite,
                        'data': data
                    }
                    self.available_pokemon.append(pokemon)
                else:
                    print(f"Sprite non trouvé pour {name}")
                    
            except Exception as e:
                print(f"Erreur lors du chargement de {name}: {e}")

    def get_pokemon_id(self, name):
        """Retourne l'ID du Pokémon pour l'API"""
        pokemon_ids = {
            "pikachu": 25, "charmander": 4, "bulbasaur": 1, "squirtle": 7,
            "onix": 95, "staryu": 120, "psyduck": 54, "mankey": 56,
            "jigglypuff": 39, "meowth": 52, "pidgey": 16, "rattata": 19,
            "spearow": 21, "ekans": 23, "sandshrew": 27, "clefairy": 35,
            "vulpix": 37, "diglett": 50, "machop": 66, "geodude": 74,
            "gastly": 92, "krabby": 98, "machoke": 67, "tentacool": 72,
            "voltorb": 100, "oddish": 43, "paras": 46, "venonat": 48
        }
        return pokemon_ids.get(name, 1)

    def draw(self):
        # Fond noir
        self.screen.fill(self.BLACK)
        
        # Titre
        title = self.font.render("Sélectionnez 6 Pokémon", True, self.POKEMON_BLUE)
        title_rect = title.get_rect(center=(self.current_width//2, 50))
        self.screen.blit(title, title_rect)
        
        # Nombre de Pokémon sélectionnés
        selected_text = self.font.render(f"Sélectionnés: {len(self.selected_pokemon)}/6", True, self.WHITE)
        self.screen.blit(selected_text, (20, 20))
        
        # Afficher les Pokémon disponibles avec défilement
        for i, pokemon in enumerate(self.available_pokemon):
            x = (i % 4) * (self.current_width // 4) + 50
            y = (i // 4) * 200 + 100 + self.scroll_y
            
            # Ne dessiner que les Pokémon visibles
            if y + 180 > 0 and y < self.current_height - 100:
                # Cadre gris ou bleu clair si sélectionné
                frame_rect = pygame.Rect(x, y, (self.current_width // 4) - 60, 180)
                if pokemon in self.selected_pokemon:
                    pygame.draw.rect(self.screen, (50, 100, 150), frame_rect, border_radius=10)  # Bleu foncé
                    pygame.draw.rect(self.screen, self.POKEMON_BLUE, frame_rect, 3, border_radius=10)
                else:
                    pygame.draw.rect(self.screen, (100, 100, 100), frame_rect, border_radius=10)  # Gris foncé
                
                # Sprite
                if pokemon['sprite']:
                    sprite_rect = pokemon['sprite'].get_rect(center=(x + frame_rect.width//4, y + 60))
                    self.screen.blit(pokemon['sprite'], sprite_rect)
                
                # Stats complètes avec alignement
                name = self.title_font.render(pokemon['name'], True, self.WHITE)
                
                # Stats alignées
                types_formatted = ' / '.join(TYPE_NAMES_FR[t] for t in pokemon['data']['types'])
                left_column = [
                    f"Type: {types_formatted}",  # Première lettre en majuscule seulement
                    f"HP: {pokemon['data']['max_hp']}",
                    f"ATK: {pokemon['data']['attack']}",
                    f"DEF: {pokemon['data']['defense']}"
                ]
                
                right_column = [
                    f"Sp.ATK: {pokemon['data']['special_attack']}",
                    f"Sp.DEF: {pokemon['data']['special_defense']}",
                    f"SPD: {pokemon['data']['speed']}"
                ]
                
                # Position de départ pour les stats
                left_x = x + 10
                right_x = x + frame_rect.width//2 + 10
                stats_y = y + 80  # Commencer sous le sprite
                
                # Afficher le nom centré en haut
                name_rect = name.get_rect(centerx=x + frame_rect.width//2, y=y + 10)
                self.screen.blit(name, name_rect)
                
                # Afficher les colonnes de stats
                for i, text in enumerate(left_column):
                    stat = self.stats_font.render(text, True, self.WHITE)
                    self.screen.blit(stat, (left_x, stats_y + i * 25))
                
                for i, text in enumerate(right_column):
                    stat = self.stats_font.render(text, True, self.WHITE)
                    self.screen.blit(stat, (right_x, stats_y + i * 25))
        
        # Bouton de confirmation (visible seulement si 6 Pokémon sont sélectionnés)
        if len(self.selected_pokemon) == 6:
            pygame.draw.rect(self.screen, self.POKEMON_BLUE, self.confirm_button, border_radius=10)
            confirm_text = self.font.render("Confirmer l'équipe", True, self.WHITE)
            text_rect = confirm_text.get_rect(center=self.confirm_button.center)
            self.screen.blit(confirm_text, text_rect)

    def run(self):
        # Calculer le scroll maximum
        rows = (len(self.available_pokemon) + 3) // 4  # Nombre de lignes
        self.max_scroll = -(rows * 200 - (self.current_height - 200))  # Espace pour le bouton
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Vérifier le clic sur le bouton de confirmation
                        if len(self.selected_pokemon) == 6 and self.confirm_button.collidepoint(mouse_pos):
                            from gui.menu.team_order import TeamOrderMenu
                            # Passer uniquement les noms des Pokémon
                            pokemon_names = [pokemon["name"] for pokemon in self.selected_pokemon]
                            order_menu = TeamOrderMenu(self.screen, pokemon_names)
                            return order_menu.run()
                        
                        # Sélection/Désélection des Pokémon
                        for i, pokemon in enumerate(self.available_pokemon):
                            x = (i % 4) * (self.current_width // 4) + 50
                            y = (i // 4) * 200 + 100 + self.scroll_y
                            rect = pygame.Rect(x, y, (self.current_width // 4) - 60, 180)
                            
                            if rect.collidepoint(mouse_pos):
                                if pokemon not in self.selected_pokemon and len(self.selected_pokemon) < 6:
                                    self.selected_pokemon.append(pokemon)
                                elif pokemon in self.selected_pokemon:
                                    self.selected_pokemon.remove(pokemon)
                    
                    elif event.button == 4:  # Molette vers le haut
                        self.scroll_y = min(0, self.scroll_y + self.scroll_speed)
                    elif event.button == 5:  # Molette vers le bas
                        self.scroll_y = max(self.max_scroll, self.scroll_y - self.scroll_speed)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "BACK"
            
            self.draw()
            pygame.display.flip() 

    def get_ordered_team(self):
        return self.selected_pokemon 

    def get_selected_pokemon(self):
        """Retourne la liste des Pokémon sélectionnés avec leurs sprites"""
        selected = []
        for pokemon in self.selected_pokemon:
            pokemon_data = {
                "name": pokemon,
                "sprite": self.sprite_manager.get_sprite(pokemon)  # On garde le sprite
            }
            selected.append(pokemon_data)
        return selected 