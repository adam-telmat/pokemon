import requests
from PIL import Image
import pygame
from io import BytesIO

class ResourceManager:
    # API pour les sprites animés
    POKEMON_GIF_API = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/"
    
    @staticmethod
    def load_pokemon_gif(pokemon_id, is_back=False):
        """Charge le GIF animé d'un Pokémon"""
        try:
            # Format: 25.gif pour Pikachu face, back/25.gif pour dos
            url = f"{ResourceManager.POKEMON_GIF_API}{'back/' if is_back else ''}{pokemon_id}.gif"
            response = requests.get(url)
            
            if response.status_code == 200:
                # Charger le GIF
                gif = Image.open(BytesIO(response.content))
                frames = []
                
                # Extraire chaque frame
                for frame in range(gif.n_frames):
                    gif.seek(frame)
                    # Convertir en surface Pygame
                    frame_surface = pygame.image.fromstring(
                        gif.convert("RGBA").tobytes(),
                        gif.size,
                        "RGBA"
                    )
                    frames.append(frame_surface)
                    
                return frames
            else:
                print(f"Erreur: GIF non trouvé pour le Pokémon {pokemon_id}")
                return None
                
        except Exception as e:
            print(f"Erreur lors du chargement du GIF: {e}")
            return None

    @staticmethod
    def get_all_pokemon_list():
        """Récupère la liste de tous les Pokémon disponibles"""
        try:
            response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=898")  # Tous les Pokémon
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        'id': i + 1,
                        'name': pokemon['name'],
                        'url': pokemon['url']
                    }
                    for i, pokemon in enumerate(data['results'])
                ]
            return []
        except Exception as e:
            print(f"Erreur lors de la récupération de la liste: {e}")
            return [] 