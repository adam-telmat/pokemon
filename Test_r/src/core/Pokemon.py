import requests
from config import POKEAPI_BASE_URL

class Pokemon:
    """
    Represents a single Pokémon with stats, moves, sprites, and more
    loaded from the PokéAPI.
    """
    def __init__(self, name):
        self.name = name.lower()
        self.status_condition = None
        self.level = 50  # Default level if you want to integrate with the official damage formula
        if not self.load_from_api():
            raise Exception(f"Unable to load Pokémon data for {name}")

    def load_from_api(self):
        """
        Fetch Pokémon data from the PokéAPI, storing stats, moves,
        sprites, abilities, and species info (like habitat or legendary status).
        """
        try:
            response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{self.name}")
            if response.status_code != 200:
                return False
            data = response.json()

            self.pokedex_id = data.get("id")
            self.height = data.get("height", 0) / 10
            self.weight = data.get("weight", 0) / 10

            # Extract stats
            stats = {s['stat']['name']: s['base_stat'] for s in data.get("stats", [])}
            self.max_hp = stats.get("hp", 50)
            self.current_hp = self.max_hp
            self.attack = stats.get("attack", 50)
            self.defense = stats.get("defense", 50)
            self.special_attack = stats.get("special-attack", 50)
            self.special_defense = stats.get("special-defense", 50)
            self.speed = stats.get("speed", 50)

            # Types
            self.types = [t["type"]["name"] for t in data.get("types", [])]

            # Moves (limit to first 4 for simplicity)
            self.moves = []
            for move in data.get("moves", [])[:4]:
                move_url = move["move"]["url"]
                move_resp = requests.get(move_url)
                if move_resp.status_code == 200:
                    move_data = move_resp.json()
                    self.moves.append({
                        "name": move_data["name"],
                        "power": move_data.get("power", 0),
                        "accuracy": move_data.get("accuracy", 100),
                        "pp": move_data.get("pp", 0),
                        "type": move_data["type"]["name"],
                        "damage_class": move_data["damage_class"]["name"]
                    })

            # Sprites
            sprites = data.get("sprites", {})
            versions = sprites.get("versions", {})
            gen5 = versions.get("generation-v", {}).get("black-white", {})
            self.animated_front = gen5.get("animated", {}).get("front_default")
            self.animated_back = gen5.get("animated", {}).get("back_default")
            self.front_sprite_url = sprites.get("front_default")
            self.back_sprite_url = sprites.get("back_default")

            # Abilities
            self.abilities = [a["ability"]["name"] for a in data.get("abilities", [])]

            # Species details
            species_url = data.get("species", {}).get("url")
            if species_url:
                species_resp = requests.get(species_url)
                if species_resp.status_code == 200:
                    species_data = species_resp.json()
                    self.growth_rate = species_data.get("growth_rate", {}).get("name", "medium")
                    self.habitat = species_data.get("habitat", {}).get("name", "unknown")
                    self.is_legendary = species_data.get("is_legendary", False)
                    self.is_mythical = species_data.get("is_mythical", False)

            return True
        except Exception as e:
            print(f"Error loading Pokémon data: {e}")
            return False

    def is_alive(self):
        """Returns True if the Pokémon has HP left."""
        return self.current_hp > 0

    def take_damage(self, damage):
        """
        Reduces the Pokémon's HP by 'damage', clamped so that HP
        can't drop below 0. Returns the actual damage inflicted.
        """
        # Simple defense-based reduction, ensuring at least 1 damage
        actual_damage = max(1, int(damage))
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage
