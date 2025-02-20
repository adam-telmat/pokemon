import pygame
import math
import os
from utils.ProfileManager import ProfileManager
from gui.battle.battle_scene import BattleScene
from utils.SpriteManager import SpriteManager
from gui.battle.arena_scenes.olga_arena import OlgaArena

class LeagueSelection:
    def __init__(self, screen):
        self.screen = screen
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        
        # Chemin de base pour les assets
        self.assets_path = os.path.join("src", "assets")
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.POKEMON_BLUE = (0, 144, 255)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        
        # Police
        try:
            font_path = os.path.join("src", "assets", "fonts", "pokemon.ttf")
            self.title_font = pygame.font.Font(font_path, 40)
            self.font = pygame.font.Font(font_path, 25)
        except:
            self.title_font = pygame.font.Font(None, 40)
            self.font = pygame.font.Font(None, 25)
        
        # Animation
        self.float_offset = 0
        self.float_speed = 0.03
        
        # Dresseurs de la ligue
        self.trainers = [
            {
                "name": "Olga",
                "title": "Maîtresse des Glaces",
                "description": "Ses Pokémon glacés vous gèleront sur place!",
                "sprite": self.load_trainer_sprite("lorelei")
            },
            {
                "name": "Aldo",
                "title": "Expert du Combat",
                "description": "Ses Pokémon sont entraînés pour la victoire!",
                "sprite": self.load_trainer_sprite("bruno")
            },
            {
                "name": "Agatha",
                "title": "Spécialiste Spectre",
                "description": "Ses spectres vous hanteront à jamais...",
                "sprite": self.load_trainer_sprite("agatha")
            },
            {
                "name": "Peter",
                "title": "Maître Dragon",
                "description": "Ses dragons sont imbattables!",
                "sprite": self.load_trainer_sprite("lance")
            },
            {
                "name": "Blue",
                "title": "Champion de la Ligue",
                "description": "Le plus grand dresseur de tous les temps!",
                "sprite": self.load_trainer_sprite("blue")
            }
        ]
        
        self.selected = 0
        
        # Charger le profil pour voir les dresseurs battus
        self.profile = ProfileManager.load_profile()
        
        # Ajouter les icônes
        self.LOCK_ICON = "🔒"
        self.CHECK_ICON = "✓"
        
        # Messages
        self.BLUE_LOCKED_MSG = "Battez les 4 dresseurs d'abord pour affronter Blue !"
        
        # Couleurs supplémentaires
        self.RED = (255, 0, 0)
        self.LOCKED_COLOR = (100, 100, 100)  # Gris plus foncé pour l'état verrouillé
        
        self.sprite_manager = SpriteManager()

    def load_trainer_sprite(self, trainer_name):
        # Mapping des noms de fichiers
        sprite_files = {
            "lorelei": "olga.png",
            "bruno": "Aldo.png",
            "agatha": "Agatha.png",
            "lance": "Peter.png",
            "blue": "Blue.png"
        }
        
        try:
            # Utiliser os.path.join pour créer le chemin
            filename = sprite_files[trainer_name]
            sprite_path = os.path.join(self.assets_path, filename)
            sprite = pygame.image.load(sprite_path).convert_alpha()
            return pygame.transform.scale(sprite, (150, 200))
        except Exception as e:
            print(f"Erreur lors du chargement du sprite de {trainer_name}: {e}")
            return None

    def load_trainer_pokemon(self, trainer_name):
        """Charge les sprites des Pokémon du dresseur"""
        trainer_team = TRAINER_TEAMS.get(trainer_name, [])
        pokemon_sprites = []
        
        for pokemon in trainer_team:
            sprite = self.sprite_manager.get_sprite(
                pokemon["name"],
                animated=False,  # Statique pour l'aperçu
                is_back=False
            )
            if sprite:
                pokemon_sprites.append({"name": pokemon["name"], "sprite": sprite})
        
        return pokemon_sprites

    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Animation de flottement
        self.float_offset += self.float_speed
        offset_y = math.sin(self.float_offset) * 10
        
        # Titre
        title = self.title_font.render("Ligue Pokémon", True, self.POKEMON_BLUE)
        title_rect = title.get_rect(center=(self.current_width//2, 50))
        self.screen.blit(title, title_rect)
        
        # Positions en utilisant toute la fenêtre
        positions = [
            {"x": 50, "y": 100},                    # Olga (en haut à gauche)
            {"x": self.current_width - 650, "y": 100},  # Aldo (décalé plus à gauche)
            {"x": self.current_width//2 - 250, "y": self.current_height//2 - 100},  # Agatha (centre)
            {"x": 50, "y": self.current_height - 250},  # Peter (en bas à gauche)
            {"x": self.current_width - 650, "y": self.current_height - 250}  # Blue (décalé plus à gauche)
        ]
        
        # Lignes de connexion (dessinées avant les dresseurs)
        for i in range(len(positions) - 1):
            start_pos = positions[i]
            end_pos = positions[i + 1]
            pygame.draw.line(self.screen, self.POKEMON_BLUE,
                           (start_pos["x"] + 250, start_pos["y"] + 70),
                           (end_pos["x"] + 50, end_pos["y"] + 30),
                           2)
        
        # Dessiner les dresseurs
        self.trainer_rects = []
        for i, trainer in enumerate(self.trainers):
            pos = positions[i]
            x_pos = pos["x"]
            y_pos = pos["y"] + (offset_y if i == self.selected else 0)
            
            # Zone cliquable plus large
            click_rect = pygame.Rect(x_pos - 20, y_pos - 20, 600, 160)  # Augmenté la largeur et hauteur
            self.trainer_rects.append(click_rect)
            
            # Gestion de Blue (dernier dresseur)
            is_blue = trainer["name"] == "Blue"
            blue_locked = is_blue and not ProfileManager.can_challenge_blue()
            
            # Couleur du texte
            if blue_locked:
                color = self.LOCKED_COLOR
            else:
                color = self.POKEMON_BLUE if i == self.selected else self.WHITE
            
            # Dessiner le cadre et le texte
            if blue_locked:
                # Effet de désactivation
                pygame.draw.rect(self.screen, (50, 50, 50), click_rect, border_radius=10)
            elif i == self.selected:
                pygame.draw.rect(self.screen, (0, 50, 100), click_rect, border_radius=10)
                pygame.draw.rect(self.screen, self.POKEMON_BLUE, click_rect, 3, border_radius=10)
            
            # Sprite et texte
            if trainer["sprite"]:
                sprite_rect = trainer["sprite"].get_rect(midleft=(x_pos, y_pos + 60))
                sprite = trainer["sprite"].copy()
                if blue_locked:
                    # Assombrir le sprite si verrouillé
                    dark = pygame.Surface(sprite.get_size()).convert_alpha()
                    dark.fill((0, 0, 0, 128))
                    sprite.blit(dark, (0, 0))
                self.screen.blit(sprite, sprite_rect)
            
            # Nom et description
            name = self.font.render(f"{trainer['name']} - {trainer['title']}", True, color)
            desc = self.font.render(trainer['description'], True, color)
            
            # Ajuster la position du texte
            text_x = x_pos + 170  # Un peu plus à droite du sprite
            name_rect = name.get_rect(x=text_x, y=y_pos + 10)
            desc_rect = desc.get_rect(x=text_x, y=y_pos + 50)
            
            # Vérifier si le texte dépasse
            if name_rect.right > click_rect.right - 10:
                name = self.font.render(f"{trainer['name']}", True, color)  # Afficher juste le nom si trop long
                title = self.font.render(trainer['title'], True, color)
                self.screen.blit(name, (text_x, y_pos + 10))
                self.screen.blit(title, (text_x, y_pos + 35))
                self.screen.blit(desc, (text_x, y_pos + 80))
            else:
                self.screen.blit(name, name_rect)
                self.screen.blit(desc, desc_rect)
            
            # Indicateurs
            if self.profile:
                if blue_locked:
                    # Cadenas pour Blue si verrouillé
                    lock = self.font.render(self.LOCK_ICON, True, self.RED)
                    self.screen.blit(lock, (text_x - 30, y_pos))
                elif self.profile["defeated_trainers"][trainer["name"]]:
                    # Coche verte pour les dresseurs battus
                    check = self.font.render(self.CHECK_ICON, True, self.GREEN)
                    self.screen.blit(check, (text_x - 30, y_pos))
            
            # Message pour Blue
            if i == self.selected and blue_locked:
                msg_text = self.font.render(self.BLUE_LOCKED_MSG, True, self.RED)
                msg_rect = msg_text.get_rect(center=(self.current_width//2, self.current_height - 50))
                # Fond semi-transparent pour le message
                msg_bg = pygame.Surface((msg_rect.width + 20, msg_rect.height + 10))
                msg_bg.fill(self.BLACK)
                msg_bg.set_alpha(200)
                self.screen.blit(msg_bg, (msg_rect.x - 10, msg_rect.y - 5))
                self.screen.blit(msg_text, msg_rect)
            
            # Griser les dresseurs non disponibles
            if trainer["name"] == "Blue" and not ProfileManager.can_challenge_blue():
                color = self.GRAY  # Griser Blue si pas encore disponible

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        mouse_pos = pygame.mouse.get_pos()
                        # Vérifier si on clique sur un dresseur
                        for i, rect in enumerate(self.trainer_rects):
                            if rect.collidepoint(mouse_pos):
                                self.selected = i
                                trainer = self.trainers[i]
                                
                                if trainer["name"] == "Olga":
                                    profile = ProfileManager.load_profile()
                                    if profile and "current_team" in profile and profile["current_team"]:  # Vérifier que l'équipe n'est pas vide
                                        print(f"Équipe chargée : {profile['current_team']}")
                                        arena = OlgaArena(self.screen, profile["current_team"])
                                        result = arena.run()
                                        return "BACK"
                                    else:
                                        print("Erreur : Vous devez d'abord sélectionner une équipe !")
                                        return "POKEMON_SELECTION"  # Rediriger vers la sélection des Pokémon
                
                elif event.type == pygame.MOUSEMOTION:
                    # Surbrillance au survol
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(self.trainer_rects):
                        if rect.collidepoint(mouse_pos):
                            self.selected = i
                            break
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "BACK"
                    elif event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.trainers)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.trainers)
            
            self.draw()
            pygame.display.flip() 