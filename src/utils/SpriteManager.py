import pygame
import os
from PIL import Image

class SpriteManager:
    def __init__(self):
        # Chemins des dossiers de sprites
        self.STATIC_FOLDER = os.path.join("src", "assets", "sprites", "static")
        self.ANIMATED_FOLDER = os.path.join("src", "assets", "sprites", "animated")
        
        # Cache en mémoire
        self.sprite_cache = {}
    
    def get_sprite(self, pokemon_name, animated=False, is_back=False):
        """Point d'entrée unique pour obtenir un sprite"""
        cache_key = f"{pokemon_name}_{'animated' if animated else 'static'}_{'back' if is_back else 'front'}"
        
        # Vérifier le cache en mémoire
        if cache_key in self.sprite_cache:
            return self.sprite_cache[cache_key]
        
        # Obtenir l'ID du Pokémon
        pokemon_id = self.get_pokemon_id(pokemon_name)
        
        # Construire le chemin du fichier
        if animated:
            # Utiliser le bon format de nom de fichier pour les GIFs
            path = os.path.join(self.ANIMATED_FOLDER, f"{pokemon_id}_{'back' if is_back else 'front'}.gif")
            print(f"Chargement du sprite: {path}")  # Debug
            sprite = self._load_animated_sprite(path)
        else:
            # Pour les sprites statiques
            path = os.path.join(self.STATIC_FOLDER, f"{pokemon_id}_{'back' if is_back else 'front'}.png")
            sprite = self._load_static_sprite(path)
        
        if sprite:
            self.sprite_cache[cache_key] = sprite
        
        return sprite
    
    def _load_static_sprite(self, path):
        """Charge un sprite statique"""
        try:
            sprite = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(sprite, (sprite.get_width() * 3, sprite.get_height() * 3))
        except Exception as e:
            print(f"Erreur lors du chargement du sprite statique: {e}")
            return None
    
    def _load_animated_sprite(self, path):
        """Charge un sprite animé depuis un GIF"""
        try:
            # Ouvrir le GIF
            gif = Image.open(path)
            frames = []
            
            # Extraire chaque frame
            for frame_index in range(gif.n_frames):
                gif.seek(frame_index)
                # Convertir la frame en surface pygame
                frame_surface = pygame.image.fromstring(
                    gif.convert("RGBA").tobytes(),
                    gif.size,
                    "RGBA"
                )
                # Redimensionner si nécessaire
                frame_surface = pygame.transform.scale(frame_surface, (200, 200))
                frames.append(frame_surface)
            
            return frames
            
        except Exception as e:
            print(f"Erreur lors du chargement du sprite animé: {e}")
            return None
    
    def get_pokemon_id(self, name):
        """Mapping des noms français vers les IDs"""
        ids = {
            # Pokémon disponibles pour le joueur
            "Pikachu": 25,
            "Salamèche": 4,
            "Bulbizarre": 1,
            "Carapuce": 7,
            "Onix": 95,
            "Staross": 120,
            "Psykokwak": 54,
            "Férosinge": 56,
            "Rondoudou": 39,
            "Miaouss": 52,
            "Roucool": 16,
            "Rattata": 19,
            "Piafabec": 21,
            "Abo": 23,
            "Sabelette": 27,
            "Mélofée": 35,
            "Goupix": 37,
            "Taupiqueur": 50,
            "Machoc": 66,
            "Racaillou": 74,
            "Fantominus": 92,
            "Krabby": 98,
            "Machopeur": 67,
            "Tentacool": 72,
            "Voltorbe": 100,
            "Mystherbe": 43,
            "Paras": 46,
            "Venonat": 48,
            
            # Équipes des dresseurs
            "Lokhlass": 131,
            "Artikodin": 144,
            "Mackogneur": 68,
            "Tygnon": 107,
            "Ectoplasma": 94,
            "Arbok": 24,
            "Nosferalto": 42,
            "Spectrum": 93,
            "Dracolosse": 149,
            "Leviator": 130,
            "Dracaufeu": 6,
            "Ptera": 142,
            "Roucarnage": 18,
            "Alakazam": 65,
            "Arcanin": 59,
            "Exeggutor": 103,
            "Tortank": 9,
            "Ronflex": 143
        }
        return ids.get(name, 1)  # Bulbizarre par défaut 

    def get_trainer_sprite(self, trainer_name):
        """Charge le sprite d'un dresseur"""
        try:
            path = f"src/assets/trainers/{trainer_name}.png"
            sprite = pygame.image.load(path)
            return pygame.transform.scale(sprite, (200, 300))  # Ajuster la taille selon besoin
        except:
            print(f"Erreur: Impossible de charger le sprite du dresseur {trainer_name}")
            return None 