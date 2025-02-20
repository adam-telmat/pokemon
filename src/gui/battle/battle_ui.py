import pygame
import os

class BattleUI:
    def __init__(self, screen):
        self.screen = screen
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 144, 255)
        self.GRAY = (128, 128, 128)
        
        # Police
        try:
            font_path = os.path.join("src", "assets", "fonts", "pokemon.ttf")
            self.font = pygame.font.Font(font_path, 32)
        except:
            self.font = pygame.font.Font(None, 32)
        
        # Menu d'action
        self.action_options = ["ATTAQUE", "POKÉMON", "OBJETS", "FUITE"]
        self.selected_action = 0
        
        # Menu des attaques
        self.selected_move = 0
        
        # Zones de clic pour les menus
        self.action_rects = []
        self.move_rects = []
        
        # Dimensions des menus
        self.menu_height = 200
        self.menu_padding = 20
        
        # Initialiser les rectangles des menus
        self.init_menu_rects()

    def init_menu_rects(self):
        # Menu d'action (2x2 grid)
        button_width = (self.current_width // 2 - self.menu_padding * 3) // 2
        button_height = (self.menu_height - self.menu_padding * 3) // 2
        
        for i in range(4):
            row = i // 2
            col = i % 2
            x = self.current_width // 2 + col * (button_width + self.menu_padding) + self.menu_padding
            y = self.current_height - self.menu_height + row * (button_height + self.menu_padding) + self.menu_padding
            self.action_rects.append(pygame.Rect(x, y, button_width, button_height))

    def draw_action_menu(self):
        # Fond du menu
        menu_rect = pygame.Rect(self.current_width//2, self.current_height - self.menu_height,
                              self.current_width//2, self.menu_height)
        pygame.draw.rect(self.screen, self.BLACK, menu_rect)
        pygame.draw.rect(self.screen, self.WHITE, menu_rect, 2)
        
        # Options du menu
        for i, (option, rect) in enumerate(zip(self.action_options, self.action_rects)):
            color = self.BLUE if i == self.selected_action else self.WHITE
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=10)
            
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_move_menu(self, moves):
        # Fond du menu
        menu_rect = pygame.Rect(0, self.current_height - self.menu_height,
                              self.current_width, self.menu_height)
        pygame.draw.rect(self.screen, self.BLACK, menu_rect)
        pygame.draw.rect(self.screen, self.WHITE, menu_rect, 2)
        
        # Afficher les attaques (2x2 grid)
        self.move_rects = []
        button_width = (self.current_width - self.menu_padding * 3) // 2
        button_height = (self.menu_height - self.menu_padding * 3) // 2
        
        for i, move in enumerate(moves):
            row = i // 2
            col = i % 2
            x = col * (button_width + self.menu_padding) + self.menu_padding
            y = self.current_height - self.menu_height + row * (button_height + self.menu_padding) + self.menu_padding
            
            rect = pygame.Rect(x, y, button_width, button_height)
            self.move_rects.append(rect)
            
            # Dessiner le bouton
            color = self.BLUE if i == self.selected_move else self.WHITE
            pygame.draw.rect(self.screen, color, rect, 2, border_radius=10)
            
            # Nom de l'attaque
            text = self.font.render(move["name"], True, color)
            text_rect = text.get_rect(center=(rect.centerx, rect.centery - 10))
            self.screen.blit(text, text_rect)
            
            # PP de l'attaque
            pp_text = self.font.render(f"PP {move['pp']}/{move['max_pp']}", True, color)
            pp_rect = pp_text.get_rect(center=(rect.centerx, rect.centery + 20))
            self.screen.blit(pp_text, pp_rect)

    def handle_click(self, pos, state):
        """Gère les clics sur les menus"""
        if state == "CHOOSE_ACTION":
            for i, rect in enumerate(self.action_rects):
                if rect.collidepoint(pos):
                    return self.action_options[i]
        elif state == "CHOOSE_MOVE":
            for i, rect in enumerate(self.move_rects):
                if rect.collidepoint(pos):
                    return i
        return None 