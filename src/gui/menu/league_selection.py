import pygame
import math

class LeagueSelection:
    def __init__(self, screen):
        self.screen = screen
        
        # Utiliser les dimensions de l'écran existant
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        
        # Fond noir simple
        self.background = pygame.Surface((self.current_width, self.current_height))
        self.background.fill((0, 0, 0))
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.GOLD = (255, 215, 0)      # Pour le champion
        self.BLUE = (30, 144, 255)     # Pour la sélection
        
        # Police
        self.font = pygame.font.Font(None, 96)
        self.title_font = pygame.font.Font(None, 120)
        
        # Dresseurs de la ligue
        self.trainers = [
            {
                "name": "Olga",
                "title": "Maîtresse des Glaces",
                "difficulty": "★★★☆☆",
                "description": "Ses Pokémon glacés vous gèleront sur place!"
            },
            {
                "name": "Aldo",
                "title": "Expert du Combat",
                "difficulty": "★★★★☆",
                "description": "Ses Pokémon sont entraînés pour la victoire!"
            },
            {
                "name": "Agatha",
                "title": "Spécialiste Spectre",
                "difficulty": "★★★★☆",
                "description": "Ses spectres vous hanteront à jamais..."
            },
            {
                "name": "Peter",
                "title": "Maître Dragon",
                "difficulty": "★★★★★",
                "description": "Ses dragons sont imbattables!"
            },
            {
                "name": "Blue",
                "title": "Champion de la Ligue",
                "difficulty": "★★★★★",
                "description": "Le plus grand dresseur de tous les temps!",
                "is_champion": True
            }
        ]
        
        self.selected = 0
        self.float_offset = 0
        self.float_speed = 0.03

    def draw(self):
        # Fond noir
        self.screen.blit(self.background, (0, 0))
        
        # Titre
        title = self.title_font.render("LIGUE POKEMON", True, self.WHITE)
        title_rect = title.get_rect(center=(self.current_width//2, 100))
        self.screen.blit(title, title_rect)
        
        # Animation de flottement
        self.float_offset += self.float_speed
        offset_y = math.sin(self.float_offset) * 10
        
        # Dessiner les dresseurs
        for i, trainer in enumerate(self.trainers):
            # Couleur selon sélection et statut
            if trainer.get('is_champion'):
                color = self.GOLD if i == self.selected else (200, 170, 0)
            else:
                color = self.BLUE if i == self.selected else self.WHITE
            
            # Nom et titre
            text = f"{trainer['name']} - {trainer['title']}"
            text_surface = self.font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.current_width//2, 300 + i * 150))
            
            # Difficulté et description
            if i == self.selected:
                diff_text = f"Difficulté: {trainer['difficulty']}"
                desc_text = trainer['description']
                
                diff_surface = self.font.render(diff_text, True, color)
                desc_surface = self.font.render(desc_text, True, color)
                
                self.screen.blit(diff_surface, (100, 900))
                self.screen.blit(desc_surface, (100, 980))
            
            # Dessiner le texte avec effet de flottement si sélectionné
            if i == self.selected:
                text_rect.y += offset_y
            self.screen.blit(text_surface, text_rect)
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "BACK"
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.trainers)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.trainers)
                    elif event.key == pygame.K_RETURN:
                        return f"BATTLE_{self.trainers[self.selected]['name'].upper()}"
                
                # Gestion de la souris
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        mouse_pos = pygame.mouse.get_pos()
                        for i, trainer in enumerate(self.trainers):
                            text_rect = self.font.render(f"{trainer['name']} - {trainer['title']}", True, (0,0,0)).get_rect(
                                center=(self.current_width//2, 300 + i * 150))
                            if text_rect.collidepoint(mouse_pos):
                                return f"BATTLE_{trainer['name'].upper()}"
                
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, trainer in enumerate(self.trainers):
                        text_rect = self.font.render(f"{trainer['name']} - {trainer['title']}", True, (0,0,0)).get_rect(
                            center=(self.current_width//2, 300 + i * 150))
                        if text_rect.collidepoint(mouse_pos):
                            self.selected = i
                            break
            
            self.draw() 