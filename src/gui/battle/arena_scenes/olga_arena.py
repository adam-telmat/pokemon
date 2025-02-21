import pygame
import math
import random
import copy
from data.trainer_teams import OLGA_TEAM
from utils.SpriteManager import SpriteManager
from utils.ProfileManager import ProfileManager

class OlgaArena:
    def __init__(self, screen, player_team):
        # Initialisation de base
        self.screen = screen
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        
        # Équipes
        self.player_team = player_team
        self.opponent_team = copy.deepcopy(OLGA_TEAM)
        
        # Debug: vérifier les PV
        for pokemon in self.opponent_team:
            print(f"PV de {pokemon['name']}: {pokemon['current_hp']}/{pokemon['max_hp']}")
        
        # États du combat
        self.current_pokemon = 0
        self.opponent_pokemon = 0
        self.battle_state = "INTRO"
        self.battle_menu_state = "MAIN"
        self.selected_option = 0
        self.selected_move = 0
        
        # Menu de combat (en bas de l'écran)
        self.menu_options = ["ATTAQUE", "POKEMON", "SAC", "FUITE"]
        self.menu_rect = pygame.Rect(0, self.current_height - 150, self.current_width, 150)  # Ajout ici !
        
        # Sprite Manager
        self.sprite_manager = SpriteManager()
        
        # État de l'intro
        self.intro_state = "TRAINER_APPEAR"
        self.intro_timer = pygame.time.get_ticks()
        self.intro_duration = 2000
        
        # Charger le sprite d'Olga
        try:
            self.trainer_sprite = pygame.image.load("src/assets/olga.png").convert_alpha()
            self.trainer_sprite = pygame.transform.scale(self.trainer_sprite, (300, 450))
            print("Sprite d'Olga chargé avec succès")
        except Exception as e:
            print(f"Erreur lors du chargement du sprite d'Olga: {e}")
            self.trainer_sprite = None
        
        # Position d'Olga
        self.trainer_pos = (self.current_width//2 - 100, self.current_height//2 - 100)
        
        # Positions des Pokémon
        self.player_pokemon_pos = (self.current_width//4, self.current_height - 300)
        self.opponent_pokemon_pos = (3*self.current_width//4, 200)
        
        # Initialiser le son
        self.battle_music = pygame.mixer.Sound("src/assets/sounds/111_battlezik.wav")
        self.battle_music_channel = None
        
        # Message de fuite
        self.escape_message = None
        self.message_timer = 0
        self.message_duration = 2000
        
        # Charger les sprites des Pokémon
        self.load_pokemon_sprites()  # Maintenant ça devrait marcher !
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.ICE_BLUE = (150, 200, 255)
        
        # Police
        try:
            font_path = "src/assets/fonts/pokemon.ttf"
            self.font = pygame.font.Font(font_path, 36)
            self.olga_font = pygame.font.Font(font_path, 48)  # Police plus grande pour Olga !
        except:
            self.font = pygame.font.Font(None, 36)
            self.olga_font = pygame.font.Font(None, 48)
        
        # Animation des sprites
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_delay = 200  # Délai entre les frames en millisecondes
        
        # Ajouter des variables pour gérer les messages de tour
        self.battle_message = None
        self.message_timer = pygame.time.get_ticks()
        self.message_duration = 1500  # Durée d'affichage des messages (1.5 secondes)
        self.waiting_for_opponent = False  # Pour gérer le tour de l'adversaire
        
        # Ajouter des variables pour l'animation d'attaque
        self.attacking = False
        self.attack_animation_start = 0
        self.attack_animation_duration = 1000  # 1 seconde pour l'animation complète
        self.attacker_original_pos = None
        self.attack_target_pos = None
        self.current_attacker_pos = None
        self.is_player_attacking = False
    
    def load_pokemon_sprites(self):
        """Charge les sprites des Pokémon actuels"""
        player_pokemon = self.player_team[self.current_pokemon]
        opponent_pokemon = self.opponent_team[self.opponent_pokemon]
        
        # Charger les sprites animés
        self.player_sprite = self.sprite_manager.get_sprite(
            player_pokemon["name"],
            animated=True,
            is_back=True  # Remis à True pour avoir le Pokémon de dos
        )
        print(f"Sprite joueur chargé: {self.player_sprite}")  # Debug
        
        self.opponent_sprite = self.sprite_manager.get_sprite(
            opponent_pokemon["name"],
            animated=True,
            is_back=False
        )
        print(f"Sprite adversaire chargé: {self.opponent_sprite}")  # Debug
    
    def draw_battle(self):
        """Affiche l'écran de combat"""
        # Fond
        self.screen.fill(self.ICE_BLUE)
        
        # Terrain
        pygame.draw.rect(self.screen, (180, 210, 235), (0, self.current_height//2 - 100, self.current_width, 200))
        
        # Animer les sprites
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.animation_frame = (self.animation_frame + 1) % 2
            self.animation_timer = current_time
        
        if self.attacking:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.attack_animation_start
            progress = min(1.0, elapsed / self.attack_animation_duration)
            
            if progress < 0.25:  # Aller vers la cible
                t = progress * 4
                x = self.attacker_original_pos[0] + (self.attack_target_pos[0] - self.attacker_original_pos[0]) * t
                y = self.attacker_original_pos[1] + (self.attack_target_pos[1] - self.attacker_original_pos[1]) * t
                self.current_attacker_pos = (x, y)
            elif progress < 0.5:  # Rester sur place pour "frapper"
                self.current_attacker_pos = self.attack_target_pos
            elif progress < 0.75:  # Retourner à la position initiale
                t = (progress - 0.5) * 4
                x = self.attack_target_pos[0] + (self.attacker_original_pos[0] - self.attack_target_pos[0]) * t
                y = self.attack_target_pos[1] + (self.attacker_original_pos[1] - self.attack_target_pos[1]) * t
                self.current_attacker_pos = (x, y)
            else:  # Animation terminée
                self.current_attacker_pos = self.attacker_original_pos
                self.attacking = False
                
                # Appliquer les dégâts après l'animation
                if self.is_player_attacking:
                    # Dégâts du joueur
                    player_pokemon = self.player_team[self.current_pokemon]
                    opponent_pokemon = self.opponent_team[self.opponent_pokemon]
                    damage = self.calculate_damage(self.current_move, player_pokemon, opponent_pokemon)
                    opponent_pokemon["current_hp"] = max(0, opponent_pokemon["current_hp"] - damage)
                    
                    # Vérifier si le Pokémon adverse est K.O.
                    if opponent_pokemon["current_hp"] <= 0:
                        self.battle_message = f"{opponent_pokemon['name']} est K.O. !"
                        if self.opponent_pokemon + 1 < len(self.opponent_team):
                            self.opponent_pokemon += 1
                            self.load_pokemon_sprites()
                        else:
                            self.show_battle_end("VICTORY")
                            return
                    
                    # Passer au tour d'Olga
                    self.waiting_for_opponent = True
                    self.message_timer = pygame.time.get_ticks()
                    self.battle_message = "Au tour d'Olga !"
                else:
                    # Dégâts d'Olga
                    opponent_pokemon = self.opponent_team[self.opponent_pokemon]
                    player_pokemon = self.player_team[self.current_pokemon]
                    damage = self.calculate_damage(self.current_move, opponent_pokemon, player_pokemon)
                    player_pokemon["current_hp"] = max(0, player_pokemon["current_hp"] - damage)
                    
                    # Vérifier si notre Pokémon est K.O.
                    if player_pokemon["current_hp"] <= 0:
                        self.battle_message = f"{player_pokemon['name']} est K.O. !"
                        # Chercher le prochain Pokémon non K.O.
                        next_pokemon_found = False
                        for i in range(self.current_pokemon + 1, len(self.player_team)):
                            if self.player_team[i]["current_hp"] > 0:
                                self.current_pokemon = i
                                next_pokemon_found = True
                                self.battle_message = f"À toi, {self.player_team[i]['name']} !"
                                self.load_pokemon_sprites()
                                break
                        
                        if not next_pokemon_found:
                            self.show_battle_end("DEFEAT")
                            return
                    
                    # Retour au menu principal
                    self.battle_menu_state = "MAIN"
                    self.selected_move = 0
        
        # Dessiner les sprites à leur position actuelle
        if self.attacking:
            if self.is_player_attacking:
                # Si c'est le joueur qui attaque
                self.draw_pokemon_sprite(self.opponent_sprite, self.opponent_pokemon_pos, False)
                self.draw_pokemon_sprite(self.player_sprite, self.current_attacker_pos, True)
            else:
                # Si c'est Olga qui attaque
                self.draw_pokemon_sprite(self.player_sprite, self.player_pokemon_pos, True)
                self.draw_pokemon_sprite(self.opponent_sprite, self.current_attacker_pos, False)
        else:
            # Position normale
            self.draw_pokemon_sprite(self.player_sprite, self.player_pokemon_pos, True)
            self.draw_pokemon_sprite(self.opponent_sprite, self.opponent_pokemon_pos, False)
        
        # Menu de combat et barres de vie
        self.draw_battle_menu()
        self.draw_health_bars()
        
        # Afficher le message de fuite s'il existe
        if self.escape_message and current_time - self.message_timer < self.message_duration:
            # Créer une surface semi-transparente pour le fond du message
            message_surface = pygame.Surface((self.current_width, 100))
            message_surface.set_alpha(200)
            message_surface.fill((0, 0, 0))  # Fond noir
            self.screen.blit(message_surface, (0, self.current_height//2 - 50))
            
            # Afficher le message
            text = self.font.render(self.escape_message, True, (255, 255, 255))  # Texte blanc
            text_rect = text.get_rect(center=(self.current_width//2, self.current_height//2))
            self.screen.blit(text, text_rect)
        elif self.escape_message:
            self.escape_message = None  # Effacer le message après la durée
        
        # Afficher le message de combat
        if self.battle_message and current_time - self.message_timer < self.message_duration:
            # Fond semi-transparent pour le message
            message_surface = pygame.Surface((self.current_width, 100))
            message_surface.set_alpha(200)
            message_surface.fill((0, 0, 0))
            self.screen.blit(message_surface, (0, self.current_height//2 - 50))
            
            # Afficher le message
            text = self.font.render(self.battle_message, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.current_width//2, self.current_height//2))
            self.screen.blit(text, text_rect)
        elif self.waiting_for_opponent and current_time - self.message_timer > self.message_duration:
            # Exécuter le tour de l'adversaire après l'affichage du message
            self.opponent_turn()
            self.waiting_for_opponent = False
            self.battle_menu_state = "MAIN"
            self.selected_move = 0
    
    def draw_battle_menu(self):
        """Affiche le menu de combat"""
        # Fond blanc semi-transparent
        menu_surface = pygame.Surface((self.menu_rect.width, self.menu_rect.height))
        menu_surface.set_alpha(200)  # 0 = transparent, 255 = opaque
        menu_surface.fill(self.WHITE)
        self.screen.blit(menu_surface, self.menu_rect)
        
        # Bordure noire
        pygame.draw.rect(self.screen, self.BLACK, self.menu_rect, 2)
        
        if self.battle_menu_state == "MAIN":
            # Afficher les 4 options principales
            for i, option in enumerate(self.menu_options):
                color = self.BLUE if i == self.selected_option else self.BLACK
                text = self.font.render(option, True, color)
                x = 50 + (i % 2) * 400
                y = self.current_height - 130 + (i // 2) * 50  # Ajusté pour le nouveau menu
                self.screen.blit(text, (x, y))
        
        elif self.battle_menu_state == "MOVES":
            # Afficher les attaques
            moves = self.player_team[self.current_pokemon]["moves"]
            for i, move in enumerate(moves):
                color = self.BLUE if i == self.selected_move else self.BLACK
                text = self.font.render(move["name"], True, color)
                x = 50 + (i % 2) * 400
                y = 475 + (i // 2) * 50
                self.screen.blit(text, (x, y))
    
    def draw_health_bars(self):
        """Dessine les barres de vie des Pokémon"""
        player_pokemon = self.player_team[self.current_pokemon]
        opponent_pokemon = self.opponent_team[self.opponent_pokemon]
        
        # Dessiner la barre de vie du joueur
        pygame.draw.rect(self.screen, self.WHITE, (50, 400, 300, 20), border_radius=5)
        pygame.draw.rect(self.screen, self.RED, (50, 400, 300 * player_pokemon.get("current_hp", 100) / player_pokemon.get("max_hp", 100), 20), border_radius=5)
        pygame.draw.rect(self.screen, self.BLACK, (50, 400, 300, 20), 2)
        
        # Dessiner la barre de vie d'Olga
        pygame.draw.rect(self.screen, self.WHITE, (550, 200, 300, 20), border_radius=5)
        pygame.draw.rect(self.screen, self.RED, (550, 200, 300 * opponent_pokemon.get("current_hp", 100) / opponent_pokemon.get("max_hp", 100), 20), border_radius=5)
        pygame.draw.rect(self.screen, self.BLACK, (550, 200, 300, 20), 2)
        
        # Texte des barres de vie
        player_health_text = self.font.render(f"{player_pokemon.get('current_hp', 0)}/{player_pokemon.get('max_hp', 0)}", True, self.BLACK)
        player_health_rect = player_health_text.get_rect(midleft=(50, 400))
        self.screen.blit(player_health_text, player_health_rect)
        
        opponent_health_text = self.font.render(f"{opponent_pokemon.get('current_hp', 0)}/{opponent_pokemon.get('max_hp', 0)}", True, self.BLACK)
        opponent_health_rect = opponent_health_text.get_rect(midright=(600, 200))
        self.screen.blit(opponent_health_text, opponent_health_rect)
    
    def handle_battle_input(self, event):
        """Gère les entrées pendant le combat"""
        if self.battle_state == "BATTLE":
            if self.battle_menu_state == "MAIN":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 2) % 4
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 2) % 4
                    elif event.key == pygame.K_LEFT:
                        self.selected_option = (self.selected_option - 1) % 4
                    elif event.key == pygame.K_RIGHT:
                        self.selected_option = (self.selected_option + 1) % 4
                    elif event.key == pygame.K_RETURN:
                        self.handle_menu_selection()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        mouse_pos = event.pos
                        # Vérifier sur quel bouton on a cliqué
                        button_width = (800 // 2 - 30) // 2
                        button_height = 150
                        
                        for i in range(4):
                            row = i // 2
                            col = i % 2
                            x = col * (button_width + 20) + 20
                            y = 475 + row * (button_height + 20)
                            
                            button_rect = pygame.Rect(x, y, button_width, button_height)
                            if button_rect.collidepoint(mouse_pos):
                                self.selected_option = i
                                self.handle_menu_selection()
            
            elif self.battle_menu_state == "MOVES":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.battle_menu_state = "MAIN"
                    elif event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        self.handle_move_selection(event.key)
                    elif event.key == pygame.K_RETURN:
                        self.execute_move()
    
    def handle_menu_selection(self):
        """Gère la sélection dans le menu"""
        if self.menu_options[self.selected_option] == "ATTAQUE":
            self.battle_menu_state = "MOVES"
        elif self.menu_options[self.selected_option] == "POKEMON":
            self.battle_menu_state = "POKEMON"
        elif self.menu_options[self.selected_option] == "SAC":
            # Pour l'instant, on ne fait rien avec le sac
            pass
        elif self.menu_options[self.selected_option] == "FUITE":
            # Afficher uniquement le message de fuite
            self.battle_message = None  # Effacer tout message de combat en cours
            self.waiting_for_opponent = False  # Ne pas déclencher le tour de l'adversaire
            self.escape_message = "Impossible de fuir un combat de dresseur !"
            self.message_timer = pygame.time.get_ticks()
            self.battle_menu_state = "MAIN"
    
    def handle_move_selection(self, key):
        """Gère la sélection des attaques"""
        moves = self.player_team[self.current_pokemon]["moves"]
        if key == pygame.K_UP:
            self.selected_move = (self.selected_move - 2) % len(moves)
        elif key == pygame.K_DOWN:
            self.selected_move = (self.selected_move + 2) % len(moves)
        elif key == pygame.K_LEFT:
            self.selected_move = (self.selected_move - 1) % len(moves)
        elif key == pygame.K_RIGHT:
            self.selected_move = (self.selected_move + 1) % len(moves)
    
    def execute_move(self):
        """Exécute l'attaque sélectionnée"""
        player_pokemon = self.player_team[self.current_pokemon]
        opponent_pokemon = self.opponent_team[self.opponent_pokemon]
        move = player_pokemon["moves"][self.selected_move]
        
        # Démarrer l'animation d'attaque
        self.attacking = True
        self.attack_animation_start = pygame.time.get_ticks()
        self.is_player_attacking = True
        self.attacker_original_pos = self.player_pokemon_pos
        self.attack_target_pos = self.opponent_pokemon_pos
        self.current_attacker_pos = self.player_pokemon_pos
        
        # Message d'attaque
        self.battle_message = f"{player_pokemon['name']} utilise {move['name']} !"
        self.message_timer = pygame.time.get_ticks()
        
        # Stocker le move pour l'utiliser après l'animation
        self.current_move = move

    def opponent_turn(self):
        """Gère le tour d'Olga"""
        opponent_pokemon = self.opponent_team[self.opponent_pokemon]
        player_pokemon = self.player_team[self.current_pokemon]
        
        # Choisir une attaque aléatoire
        move = random.choice(opponent_pokemon["moves"])
        
        # Démarrer l'animation d'attaque
        self.attacking = True
        self.attack_animation_start = pygame.time.get_ticks()
        self.is_player_attacking = False
        self.attacker_original_pos = self.opponent_pokemon_pos
        self.attack_target_pos = self.player_pokemon_pos
        self.current_attacker_pos = self.opponent_pokemon_pos
        
        # Message d'attaque
        self.battle_message = f"{opponent_pokemon['name']} utilise {move['name']} !"
        self.message_timer = pygame.time.get_ticks()
        
        # Stocker le move pour l'utiliser après l'animation
        self.current_move = move

    def calculate_damage(self, move, attacker, defender):
        """Calcule les dégâts selon la formule officielle Pokémon"""
        try:
            # Vérifier que toutes les stats nécessaires sont présentes
            required_stats = ["level", "attack", "defense", "special_attack", "special_defense", "types"]
            for stat in required_stats:
                if stat not in attacker or stat not in defender:
                    print(f"Erreur: stat {stat} manquante")
                    return 0

            # Vérifier les données du move
            if "category" not in move or "power" not in move or "type" not in move:
                print(f"Erreur: données d'attaque manquantes pour {move['name']}")
                return 0

            # Si c'est une attaque de statut (power = 0)
            if move["power"] == 0:
                return 0

            level = attacker["level"]
            
            # Attaque et défense selon le type de move
            if move["category"] == "physical":
                attack = attacker["attack"]
                defense = defender["defense"]
            else:  # special
                attack = attacker["special_attack"]
                defense = defender["special_defense"]
            
            power = move["power"]
            
            # STAB
            stab = 1.5 if move["type"] in attacker["types"] else 1.0
            
            # Type effectiveness
            type_multiplier = self.calculate_type_effectiveness(move["type"], defender["types"])
            
            # Coup critique (6.25% de chance)
            is_crit = random.random() < 0.0625
            crit_multiplier = 2 if is_crit else 1
            if is_crit:
                print("Coup critique !")
            
            # Random factor (85-100%)
            random_factor = random.randint(85, 100) / 100
            
            # Formule complète
            damage = (((2 * level / 5 + 2) * power * attack / defense) / 50 + 2) * \
                     stab * type_multiplier * crit_multiplier * random_factor
            
            # Afficher les détails du calcul en debug
            print(f"Dégâts calculés pour {move['name']}:")
            print(f"Base: {(((2 * level / 5 + 2) * power * attack / defense) / 50 + 2)}")
            print(f"STAB: {stab}")
            print(f"Type: {type_multiplier}")
            print(f"Crit: {crit_multiplier}")
            print(f"Random: {random_factor}")
            print(f"Total: {int(damage)}")
            
            return int(damage)
            
        except Exception as e:
            print(f"Erreur dans le calcul des dégâts: {e}")
            return 0

    def calculate_type_effectiveness(self, move_type, defender_types):
        """Calcule l'efficacité du type selon la table des types Pokémon"""
        type_chart = {
            "normal": {"rock": 0.5, "ghost": 0, "steel": 0.5},
            "fire": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2},
            "water": {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5},
            "electric": {"water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5},
            "grass": {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5},
            "ice": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5},
            "fighting": {"normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dark": 2, "steel": 2},
            "poison": {"grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0},
            "ground": {"fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2},
            "flying": {"electric": 0.5, "grass": 2, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5},
            "psychic": {"fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5},
            "bug": {"fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5, "dark": 2, "steel": 0.5},
            "rock": {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5},
            "ghost": {"normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5, "steel": 0.5},
            "dragon": {"dragon": 2, "steel": 0.5},
            "dark": {"fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "steel": 0.5},
            "steel": {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5}
        }
        
        multiplier = 1.0
        for def_type in defender_types:
            if move_type in type_chart and def_type in type_chart[move_type]:
                multiplier *= type_chart[move_type][def_type]
            
        return multiplier

    def draw_intro(self):
        """Affiche l'introduction du combat"""
        current_time = pygame.time.get_ticks()
        
        if self.intro_state == "TRAINER_APPEAR":
            # Fond glacé plus sombre pour plus de dramatisme
            self.screen.fill((100, 150, 200))
            
            # Effet de flash glacé
            if (current_time // 200) % 2:
                pygame.draw.rect(self.screen, (200, 220, 255), (0, 0, self.current_width, self.current_height//4))
            
            # Afficher Olga avec un effet d'apparition progressive
            if self.trainer_sprite:
                alpha = min(255, (current_time - self.intro_timer) // 3)
                sprite_copy = self.trainer_sprite.copy()
                sprite_copy.set_alpha(alpha)
                self.screen.blit(sprite_copy, self.trainer_pos)
            
            if current_time - self.intro_timer > self.intro_duration:
                self.intro_state = "TRAINER_SPEAK"
                self.intro_timer = current_time
        
        elif self.intro_state == "TRAINER_SPEAK":
            # Fond glacé
            self.screen.fill((100, 150, 200))
            
            # Afficher Olga
            if self.trainer_sprite:
                self.screen.blit(self.trainer_sprite, self.trainer_pos)
            
            # Messages plus intimidants avec animation
            messages = [
                "Je suis Olga, Maîtresse des Pokémon Glace !",
                "Dans mon arène, même les plus ardents",
                "combattants finissent gelés..."
            ]
            
            for i, message in enumerate(messages):
                text = self.olga_font.render(message, True, (220, 220, 255))
                shadow = self.olga_font.render(message, True, (0, 0, 100))
                pos_y = 50 + i * 60
                
                # Effet d'ombre
                self.screen.blit(shadow, (self.current_width//2 - text.get_width()//2 + 2, pos_y + 2))
                self.screen.blit(text, (self.current_width//2 - text.get_width()//2, pos_y))
            
            # Passer automatiquement à l'état suivant après la durée
            if current_time - self.intro_timer > self.intro_duration:
                self.intro_state = "BATTLE_START"
                self.intro_timer = current_time
        
        elif self.intro_state == "BATTLE_START":
            # Fond glacé
            self.screen.fill(self.ICE_BLUE)
            
            # Message de début de combat
            start_text = self.font.render("Que le combat commence !", True, self.BLACK)
            start_rect = start_text.get_rect(center=(self.current_width//2, self.current_height//2))
            self.screen.blit(start_text, start_rect)
            
            if current_time - self.intro_timer > self.intro_duration:
                self.battle_state = "BATTLE"

    def show_battle_end(self, result):
        """Affiche l'écran de fin de combat"""
        self.battle_state = "END"
        self.battle_result = result
        
        # Sauvegarder la victoire si applicable
        if result == "VICTORY":
            ProfileManager.update_defeated_trainer("Olga")

    def draw_battle_end(self):
        """Dessine l'écran de fin de combat"""
        # Fond
        self.screen.fill(self.ICE_BLUE)
        
        # Message de fin
        message = "Victoire !" if self.battle_result == "VICTORY" else "Défaite..."
        text = self.font.render(message, True, self.BLACK)
        text_rect = text.get_rect(center=(self.current_width//2, self.current_height//2 - 50))
        self.screen.blit(text, text_rect)
        
        # Bouton retour
        return_text = self.font.render("Appuyez sur ENTRÉE pour continuer", True, self.BLACK)
        return_rect = return_text.get_rect(center=(self.current_width//2, self.current_height//2 + 50))
        self.screen.blit(return_text, return_rect)

    def draw_pokemon_sprite(self, sprite, position, is_player):
        """Dessine un sprite de Pokémon à la position donnée"""
        if sprite and isinstance(sprite, list) and len(sprite) > 0:
            frame = sprite[self.animation_frame % len(sprite)]
            sprite_rect = frame.get_rect()
            sprite_rect.center = position
            self.screen.blit(frame, sprite_rect)

    def run(self):
        # Démarrer la musique en boucle
        self.battle_music_channel = self.battle_music.play(-1)  # -1 pour jouer en boucle
        
        running = True
        result = None
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Arrêter la musique avant de quitter
                    if self.battle_music_channel:
                        self.battle_music_channel.stop()
                    return "QUIT" if event.type == pygame.QUIT else "BACK"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.battle_state == "INTRO" and self.intro_state == "BATTLE_START":
                            self.battle_state = "BATTLE"
                        elif self.battle_state == "END":
                            result = self.battle_result
                            running = False
                
                # Si on est en combat, gérer les inputs du combat
                if self.battle_state == "BATTLE":
                    self.handle_battle_input(event)
            
            # Gérer les différents états
            if self.battle_state == "INTRO":
                self.draw_intro()
            elif self.battle_state == "BATTLE":
                self.draw_battle()
            elif self.battle_state == "END":
                self.draw_battle_end()
            
            pygame.display.flip()
        
        # Arrêter la musique avant de retourner au menu
        if self.battle_music_channel:
            self.battle_music_channel.stop()
        return result 