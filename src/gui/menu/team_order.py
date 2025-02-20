import pygame
import os
from utils.SpriteManager import SpriteManager
from utils.ProfileManager import ProfileManager

class TeamOrderMenu:
    def __init__(self, screen, selected_pokemon):
        self.screen = screen
        self.current_width = screen.get_width()
        self.current_height = screen.get_height()
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.POKEMON_BLUE = (0, 144, 255)
        self.GRAY = (100, 100, 100)
        
        # Police
        try:
            self.title_font = pygame.font.Font("src/assets/fonts/pokemon.ttf", 40)
            self.font = pygame.font.Font("src/assets/fonts/pokemon.ttf", 25)
        except:
            self.title_font = pygame.font.Font(None, 40)
            self.font = pygame.font.Font(None, 25)
        
        # Initialiser le sprite manager
        self.sprite_manager = SpriteManager()
        
        # Pokémon sélectionnés
        self.team = []
        for pokemon_name in selected_pokemon:  # selected_pokemon est déjà une liste de noms
            sprite = self.sprite_manager.get_sprite(
                pokemon_name,  # On utilise directement le nom
                animated=False,
                is_back=False
            )
            self.team.append({
                "name": pokemon_name,  # Garder le vrai nom !
                "sprite": sprite
            })
        self.selected_index = None
        self.dragging = False
        self.drag_pokemon = None
        self.drag_pos = None
        
        # Bouton de confirmation
        self.confirm_button = pygame.Rect(
            self.current_width//2 - 100,
            self.current_height - 60,
            200,
            50
        )
        
        # On n'a plus besoin de recharger les sprites car ils sont déjà là !
        # Supprimer tout le code de chargement des sprites ici

    def draw(self):
        self.screen.fill(self.BLACK)
        
        # Titre
        title = self.title_font.render("Organisez votre équipe", True, self.POKEMON_BLUE)
        title_rect = title.get_rect(center=(self.current_width//2, 50))
        self.screen.blit(title, title_rect)
        
        # Instructions
        instructions = self.font.render("Glissez-déposez les Pokémon pour changer leur ordre", True, self.WHITE)
        inst_rect = instructions.get_rect(center=(self.current_width//2, 100))
        self.screen.blit(instructions, inst_rect)
        
        # Afficher les emplacements numérotés
        for i in range(6):
            x = (self.current_width // 6) * i + 100
            y = self.current_height // 2
            
            # Cadre
            frame_rect = pygame.Rect(x - 50, y - 80, 100, 160)
            pygame.draw.rect(self.screen, self.GRAY, frame_rect, border_radius=10)
            
            # Numéro de position
            pos_text = self.font.render(f"#{i+1}", True, self.WHITE)
            pos_rect = pos_text.get_rect(center=(x, y - 60))
            self.screen.blit(pos_text, pos_rect)
            
            # Pokémon
            if i < len(self.team) and (not self.dragging or i != self.selected_index):
                pokemon = self.team[i]
                # Sprite
                sprite_rect = pokemon['sprite'].get_rect(center=(x, y))
                self.screen.blit(pokemon['sprite'], sprite_rect)
                # Nom
                name = self.font.render(pokemon['name'], True, self.WHITE)
                name_rect = name.get_rect(center=(x, y + 50))
                self.screen.blit(name, name_rect)
        
        # Afficher le Pokémon en cours de déplacement
        if self.dragging and self.drag_pokemon and self.drag_pos:
            sprite_rect = self.drag_pokemon['sprite'].get_rect(center=self.drag_pos)
            self.screen.blit(self.drag_pokemon['sprite'], sprite_rect)
        
        # Bouton de confirmation
        pygame.draw.rect(self.screen, self.POKEMON_BLUE, self.confirm_button, border_radius=10)
        confirm_text = self.font.render("Confirmer l'ordre", True, self.WHITE)
        text_rect = confirm_text.get_rect(center=self.confirm_button.center)
        self.screen.blit(confirm_text, text_rect)

    def save_team(self):
        """Sauvegarde l'équipe complète avec stats et mouvements"""
        from data.pokemon_data import SPECIES_DATA
        
        # Dictionnaire de conversion des noms
        name_conversion = {
            "Salamèche": "charmander",
            "Psykokwak": "psyduck",
            "Roucool": "pidgey",
            "Staross": "staryu",
            "Abo": "ekans",
            "Sabelette": "sandshrew"
            # Ajouter les autres conversions ici
        }
        
        # Dictionnaire des types d'attaques
        move_types = {
            "scratch": "normal",
            "ember": "fire",
            "growl": "normal",
            "flamethrower": "fire",
            "tackle": "normal",
            "water-gun": "water",
            "confusion": "psychic",
            "disable": "normal",
            "wrap": "normal",
            "poison-sting": "poison",
            "bite": "dark",
            "glare": "normal",
            "defense-curl": "normal",
            "sand-attack": "ground"
        }

        profile = ProfileManager.load_profile()
        if profile:
            complete_team = []
            print("Sauvegarde de l'équipe :")
            for pokemon in self.team:
                # Convertir le nom en version anglaise pour la recherche
                english_name = name_conversion.get(pokemon["name"], pokemon["name"].lower())
                pokemon_data = SPECIES_DATA.get(english_name, {})
                print(f"Pokemon: {pokemon['name']} ({english_name}), Data: {pokemon_data}")
                
                if pokemon_data:
                    team_pokemon = {
                        "name": pokemon["name"],
                        "types": pokemon_data["types"],  # Ajouter les types !
                        "level": pokemon_data["level"],
                        "max_hp": pokemon_data["max_hp"],
                        "current_hp": pokemon_data["max_hp"],
                        "attack": pokemon_data["attack"],
                        "defense": pokemon_data["defense"],
                        "special_attack": pokemon_data["special_attack"],
                        "special_defense": pokemon_data["special_defense"],
                        "speed": pokemon_data["speed"],
                        "moves": []
                    }
                    
                    # Ajouter les mouvements avec leurs vrais types
                    for move_name in pokemon_data["moves"]:
                        move = {
                            "name": move_name,
                            "type": move_types.get(move_name, "normal"),  # Utiliser le vrai type
                            "category": "special" if move_types.get(move_name) in ["fire", "water", "electric", "psychic"] else "physical",
                            "power": 40,
                            "pp": 30,
                            "max_pp": 30
                        }
                        team_pokemon["moves"].append(move)
                    
                    complete_team.append(team_pokemon)
            
            print(f"Équipe complète à sauvegarder : {complete_team}")
            profile["current_team"] = complete_team
            ProfileManager.save_profile(profile)
    
    def get_pokemon_moves(self, pokemon_name):
        """Récupère les mouvements d'un Pokémon depuis les données"""
        from data.pokemon_data import SPECIES_DATA
        pokemon_data = SPECIES_DATA.get(pokemon_name.lower(), {})
        moves = pokemon_data.get("moves", [])
        return [{"name": move, "pp": 30, "max_pp": 30} for move in moves]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "QUIT"
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Si on clique sur le bouton de confirmation
                        if self.confirm_button.collidepoint(mouse_pos):
                            self.save_team()  # Utiliser la nouvelle méthode
                            return "BACK"
                        
                        # Vérifier si on clique sur un Pokémon
                        for i in range(len(self.team)):
                            x = (self.current_width // 6) * i + 100
                            y = self.current_height // 2
                            rect = pygame.Rect(x - 50, y - 80, 100, 160)
                            
                            if rect.collidepoint(mouse_pos):
                                self.dragging = True
                                self.selected_index = i
                                self.drag_pokemon = self.team[i]
                                self.drag_pos = mouse_pos
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1 and self.dragging:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Vérifier sur quel emplacement on relâche
                        for i in range(6):
                            x = (self.current_width // 6) * i + 100
                            y = self.current_height // 2
                            rect = pygame.Rect(x - 50, y - 80, 100, 160)
                            
                            if rect.collidepoint(mouse_pos):
                                # Échanger les positions
                                self.team[self.selected_index], self.team[i] = self.team[i], self.team[self.selected_index]
                                break
                        
                        self.dragging = False
                        self.selected_index = None
                        self.drag_pokemon = None
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        self.drag_pos = event.pos
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "BACK"
            
            self.draw()
            pygame.display.flip() 