import pygame
import sys
import math
import random

class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
        pygame.display.set_caption("Pokémon Game")
        
        # Tailles de l'écran
        self.current_width = 1920
        self.current_height = 1080
        
        try:
            # Charger l'image de fond sans modification
            self.background = pygame.image.load("src/assets/pokemon_backgroundfinale.jpg").convert_alpha()
            self.background = pygame.transform.scale(self.background, (1920, 1080))
            
            # Charger le Pokémon 3D avec transparence
            self.pokemon_3d = pygame.image.load("src/assets/pokemon3D2.png").convert_alpha()
            # Nouvelle taille : plus large (800) et moins haut (400)
            self.pokemon_3d = pygame.transform.scale(self.pokemon_3d, (800, 400))
            
            # Position ajustée : plus haut et centré
            self.pokemon_pos = [1920//2 - 400, -20]  # Centré horizontalement avec la nouvelle largeur
            self.pokemon_float = 0
            self.pokemon_float_speed = 0.05
            
        except Exception as e:
            print(f"Erreur lors du chargement des images: {e}")
            self.background = None
            self.pokemon_3d = None
        
        # Uniquement les couleurs emblématiques Pokémon
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.POKEMON_YELLOW = (255, 236, 0)      # Jaune vif actuel (parfait)
        self.POKEMON_BLUE = (0, 144, 255)        # Bleu plus électrique
        self.POKEMON_BLUE_LIGHT = (30, 170, 255)  # Version plus claire pour la sélection
        
        # Options du menu
        self.options = [
            "Nouvelle Partie",
            "Charger Partie",
            "Options",
            "Quitter"
        ]
        self.selected = 0
        
        # Police
        self.font = pygame.font.Font(None, 96)
        
        # Effets visuels
        self.glow_color = (0, 255, 255)  # Cyan pour l'effet cyberpunk
        self.glow_alpha = 0  # Pour l'effet de pulsation
        self.glow_direction = 1
        self.glow_speed = 3
        
        # Logo 3D (on peut utiliser une image de Pokémon en 3D)
        try:
            self.logo = pygame.image.load("src/assets/images/pokemon_logo_3d.png")
            self.logo = pygame.transform.scale(self.logo, (600, 300))
            self.logo_pos = (self.current_width//2 - 300, 50)
            self.logo_offset = 0
            self.logo_direction = 1
        except:
            self.logo = None
        
        # Effets d'animation avancés
        self.pokemon_rotation = 0  # Rotation du Pokémon
        self.pokemon_scale = 1.0   # Pour l'effet de "respiration"
        self.particle_list = []    # Particules autour du Pokémon
        self.glow_radius = 50      # Halo lumineux
        
        # Couleurs pour les effets
        self.GLOW_COLOR = (0, 255, 255, 100)  # Cyan transparent
        self.PARTICLE_COLORS = [
            (0, 255, 255),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 128)   # Vert néon
        ]
        
    def draw_cyberpunk_box(self, surface, rect, color, glow=False):
        """Dessine une boîte style cyberpunk"""
        # Contour principal
        pygame.draw.rect(surface, color, rect, border_radius=10)
        
        # Effet de coin cyberpunk
        corner_size = 20
        line_color = (0, 255, 255) if glow else (100, 100, 100)
        
        # Coins supérieurs
        pygame.draw.line(surface, line_color, (rect.left, rect.top + corner_size),
                        (rect.left, rect.top), 3)
        pygame.draw.line(surface, line_color, (rect.left, rect.top),
                        (rect.left + corner_size, rect.top), 3)
        
        pygame.draw.line(surface, line_color, (rect.right - corner_size, rect.top),
                        (rect.right, rect.top), 3)
        pygame.draw.line(surface, line_color, (rect.right, rect.top),
                        (rect.right, rect.top + corner_size), 3)

    def create_particle(self):
        """Crée une particule d'effet"""
        return {
            'pos': [self.pokemon_pos[0] + self.pokemon_size[0]//2,
                    self.pokemon_pos[1] + self.pokemon_size[1]//2],
            'vel': [random.uniform(-2, 2), random.uniform(-2, 2)],
            'timer': random.uniform(0, 100),
            'color': random.choice(self.PARTICLE_COLORS),
            'size': random.randint(2, 6)
        }

    def draw(self):
        # Afficher le fond
        if self.background:
            self.screen.blit(self.background, (0, 0))
            
            # Animer et afficher le Pokémon 3D
            if self.pokemon_3d:
                self.pokemon_float += self.pokemon_float_speed
                offset_y = math.sin(self.pokemon_float) * 20
                pokemon_y = self.pokemon_pos[1] + offset_y
                self.screen.blit(self.pokemon_3d, (self.pokemon_pos[0], pokemon_y))
        
        # Dessiner les options du menu
        for i, option in enumerate(self.options):
            # Texte en bleu Pokémon
            color = self.POKEMON_BLUE_LIGHT if i == self.selected else self.POKEMON_BLUE
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.current_width//2, 600 + i * 120))
            
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
        
        pygame.display.flip()
        
    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            # Passer en plein écran
            self.screen = pygame.display.set_mode((self.current_width, self.current_height), pygame.FULLSCREEN)
        else:
            # Revenir en mode fenêtré
            self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
        # Redimensionner le background
        self.background = pygame.transform.scale(self.background, 
            (self.current_width if self.is_fullscreen else 1920, 
             self.current_height if self.is_fullscreen else 1080))
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                    
                # Gérer le redimensionnement
                elif event.type == pygame.VIDEORESIZE:
                    # S'assurer que la fenêtre ne soit pas plus petite que le minimum
                    width = max(self.min_width, event.w)
                    height = max(self.min_height, event.h)
                    self.current_width = width
                    self.current_height = height
                    self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
                    # Redimensionner le background
                    self.background = pygame.transform.scale(self.background, (width, height))
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:  # F11 pour basculer plein écran
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected == 0:
                            return "NEW_GAME"
                        elif self.selected == 1:
                            return "LOAD_GAME"
                        elif self.selected == 2:
                            return "OPTIONS"
                        elif self.selected == 3:
                            return "QUIT"
            
            self.draw() 