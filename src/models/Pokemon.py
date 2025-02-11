import requests
from PIL import Image
from io import BytesIO

class Pokemon:
    BASE_API_URL = "https://pokeapi.co/api/v2/pokemon/"

    def __init__(self, name, types, hp, level, attack, defense):
        self.name = name.lower()
        self.types = types
        self.max_hp = hp
        self.current_hp = hp
        self.level = level
        self.attack = attack
        self.defense = defense
        
        # Récupérer les données de l'API
        self.load_sprites_from_api()

    def load_sprites_from_api(self):
        """Charge les sprites depuis PokeAPI"""
        try:
            response = requests.get(f"{self.BASE_API_URL}{self.name}")
            if response.status_code == 200:
                data = response.json()
                self.front_sprite_url = data['sprites']['front_default']
                self.back_sprite_url = data['sprites']['back_default']
                
                # Charger les images
                self.front_sprite = self.load_sprite(self.front_sprite_url)
                self.back_sprite = self.load_sprite(self.back_sprite_url)
            else:
                raise Exception(f"Pokémon {self.name} non trouvé")
        except Exception as e:
            print(f"Erreur lors du chargement des sprites: {e}")
            
    def load_sprite(self, url):
        """Charge une image depuis une URL"""
        response = requests.get(url)
        return Image.open(BytesIO(response.content))

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def get_sprite(self, is_player=True):
        """Retourne le sprite approprié"""
        return self.back_sprite if is_player else self.front_sprite 