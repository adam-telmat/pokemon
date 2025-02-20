import pygame
import os
from .battle_logic import BattleLogic
from .battle_ui import BattleUI
from .battle_animations import BattleAnimations
from utils.SpriteManager import SpriteManager

class BattleScene:
    def __init__(self, screen, player_team, opponent):
        self.screen = screen
        self.sprite_manager = SpriteManager()
        
        # Convertir la liste de noms en Pokémon avec sprites
        self.player_team = []
        for pokemon_name in player_team:
            sprite = self.sprite_manager.get_sprite(
                pokemon_name,
                animated=True,
                is_back=True
            )
            self.player_team.append({
                "name": pokemon_name,
                "sprite": sprite
            })
        
        # Fond noir simple
        self.screen.fill((0, 0, 0))
        
        # Positions des Pokémon
        self.player_pos = (200, screen.get_height() - 200)  # Pokémon du joueur
        self.opponent_pos = (screen.get_width() - 200, 200)  # Pokémon d'Olga

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "BACK"
            
            # Dessiner la scène
            self.screen.fill((0, 0, 0))
            
            # Dessiner les Pokémon (pour l'instant juste des rectangles)
            pygame.draw.rect(self.screen, (255, 0, 0), (*self.player_pos, 100, 100))
            pygame.draw.rect(self.screen, (0, 0, 255), (*self.opponent_pos, 100, 100))
            
            pygame.display.flip()

    def load_pokemon_sprites(self):
        # Sprite animé du Pokémon du joueur (de dos)
        self.player_sprite = self.sprite_manager.get_sprite(
            self.current_pokemon["name"],
            animated=True,   # Animé pour le combat
            is_back=True     # De dos pour le joueur
        )
        
        # Sprite animé du Pokémon adverse (de face)
        self.opponent_sprite = self.sprite_manager.get_sprite(
            self.opponent_pokemon["name"],
            animated=True,   # Animé pour le combat
            is_back=False    # De face pour l'adversaire
        ) 