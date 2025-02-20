import pygame
import math
import os
from gui.menu.pokemon_selection import PokemonSelection
from gui.menu.team_order import TeamOrderMenu
from gui.menu.league_selection import LeagueSelection

class GameMenu:
    def __init__(self, screen, sprite_manager, profile=None):
        self.screen = screen
        self.sprite_manager = sprite_manager
        self.profile = profile
        
        # Utiliser les dimensions de l'écran existant
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        
        # Chemin de base pour les assets
        self.assets_path = os.path.join("src", "assets")
        
        try:
            # Charger et redimensionner l'image de fond
            background_path = os.path.join(self.assets_path, "pokemon_backgroundfinale.jpg")
            self.background = pygame.image.load(background_path).convert_alpha()
            self.background = pygame.transform.scale(self.background, (self.current_width, self.current_height))
            
        except Exception as e:
            print(f"Erreur lors du chargement de l'image de fond: {e}")
            self.background = pygame.Surface((self.current_width, self.current_height))
            self.background.fill((0, 0, 0))
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.POKEMON_YELLOW = (255, 236, 0)      # Jaune vif
        self.POKEMON_BLUE = (0, 144, 255)        # Bleu de base
        self.POKEMON_BLUE_LIGHT = (0, 90, 255)   # Bleu plus foncé pour la sélection
        
        # Même police
        self.font = pygame.font.Font(None, 96)
        
        # Animation
        self.float_offset = 0
        self.float_speed = 0.03

        self.options = [
            "Pokémon",    # Équipe
            "Pokédex",    # Pokédex
            "Sac",        # Inventaire
            "Mode Combat", # Nouveau !
            "Options",    # Options
            "Retour"      # Retour
        ]
        self.selected = 0
        self.selected_team = None  # Pour stocker l'équipe de Pokémon

    def draw(self):
        # Fond
        self.screen.blit(self.background, (0, 0))
        
        # Animation de flottement
        self.float_offset += self.float_speed
        offset_y = math.sin(self.float_offset) * 10
        
        # Dessiner les options du menu
        for i, option in enumerate(self.options):
            # Texte en bleu Pokémon
            color = self.POKEMON_BLUE_LIGHT if i == self.selected else self.POKEMON_BLUE
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.current_width//2, 300 + i * 120))
            
            # Rectangle jaune Pokémon
            box_rect = text_rect.inflate(60, 40)
            if i == self.selected:
                box_rect = text_rect.inflate(80, 50)
                pygame.draw.rect(self.screen, self.POKEMON_YELLOW, box_rect, border_radius=15)
                pygame.draw.rect(self.screen, self.POKEMON_BLUE_LIGHT, box_rect, 3, border_radius=15)
            else:
                pygame.draw.rect(self.screen, self.POKEMON_YELLOW, box_rect, border_radius=10)
            
            # Afficher le texte
            self.screen.blit(text, text_rect)
        
        # Si une équipe est sélectionnée, on peut activer le mode combat
        if self.selected_team is None:
            # Griser l'option "Mode Combat"
            pass
        else:
            # Activer l'option "Mode Combat"
            pass
        
        pygame.display.flip() 

    def handle_pokemon_selection(self):
        """Gère la sélection et l'ordre des Pokémon"""
        pokemon_selection = PokemonSelection(self.screen)
        pokemon_names = pokemon_selection.run()
        
        if pokemon_names and pokemon_names != "BACK":
            team_order = TeamOrderMenu(self.screen, pokemon_names)
            order_result = team_order.run()
            if order_result == "BACK":  # Changé de ORDER_CONFIRMED à BACK
                self.selected_team = team_order.team  # Sauvegarder l'équipe ordonnée
        return None

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        mouse_pos = pygame.mouse.get_pos()
                        for i, option in enumerate(self.options):
                            text_rect = self.font.render(option, True, (0,0,0)).get_rect(center=(self.current_width//2, 300 + i * 120))
                            box_rect = text_rect.inflate(60, 40)
                            if box_rect.collidepoint(mouse_pos):
                                if option == "Pokémon":
                                    self.handle_pokemon_selection()
                                elif option == "Mode Combat":
                                    # Ouvrir directement la sélection de la ligue
                                    league_screen = LeagueSelection(self.screen)
                                    league_result = league_screen.run()
                                    if league_result == "BACK":
                                        continue  # Retour au menu de jeu
                                    elif isinstance(league_result, dict):
                                        return league_result  # Retourner le résultat au main.py
                                elif option == "Retour":
                                    return "BACK"
                
                # Survol de la souris
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, option in enumerate(self.options):
                        text_rect = self.font.render(option, True, (0,0,0)).get_rect(center=(self.current_width//2, 300 + i * 120))
                        box_rect = text_rect.inflate(60, 40)
                        if box_rect.collidepoint(mouse_pos):
                            self.selected = i
                            break
                
                # Contrôle clavier
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "BACK"
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected == 0:  # Pokémon
                            return self.handle_pokemon_selection()
                        elif self.selected == 1:  # Pokédex
                            return "POKEDEX"
                        elif self.selected == 2:  # Sac
                            return "BAG"
                        elif self.selected == 3:  # Mode Combat
                            return self.open_battle_menu()
                        elif self.selected == 4:  # Options
                            return "OPTIONS"
                        elif self.selected == 5:  # Retour
                            return "BACK"
            
            self.draw()

    def open_battle_menu(self):
        """Ouvre le menu de la ligue"""
        from gui.menu.league_selection import LeagueSelection
        league_menu = LeagueSelection(self.screen)
        return league_menu.run()

    def open_pokemon_selection(self):
        from gui.menu.pokemon_selection import PokemonSelection
        pokemon_selection = PokemonSelection(self.screen)
        result = pokemon_selection.run()
        
        if result == "ORDER_CONFIRMED":
            # Stocker l'équipe ordonnée et continuer dans le menu de jeu
            self.selected_team = pokemon_selection.get_ordered_team()
            return None  # Reste dans le menu de jeu
        elif result == "BACK":
            return None  # Reste dans le menu de jeu
        elif result == "QUIT":
            return "QUIT"
        
        return None 