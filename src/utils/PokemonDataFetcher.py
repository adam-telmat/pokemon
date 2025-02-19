import requests
from typing import Dict, Any

class PokemonDataFetcher:
    # URLs
    POKEAPI_URL = "https://pokeapi.co/api/v2/"
    SHOWDOWN_SPRITE_URL = "https://play.pokemonshowdown.com/sprites/ani/"
    SHOWDOWN_DATA_URL = "https://play.pokemonshowdown.com/data/"

    def __init__(self):
        self.cache = {}

    def get_pokemon_data(self, name: str) -> Dict[str, Any]:
        """Récupère les données complètes d'un Pokémon"""
        # D'abord vérifier le cache
        if name in self.cache:
            return self.cache[name]

        # Données de base de PokéAPI
        pokeapi_data = self._fetch_pokeapi_data(name)
        
        # Sprites HD de Showdown
        sprites = {
            'front_animated': f"{self.SHOWDOWN_SPRITE_URL}{name}.gif",
            'back_animated': f"{self.SHOWDOWN_SPRITE_URL}back/{name}.gif",
            'front_shiny': f"{self.SHOWDOWN_SPRITE_URL}shiny/{name}.gif"
        }

        # Combiner les données
        pokemon_data = {
            **pokeapi_data,
            'sprites': sprites,
            'showdown_data': self._fetch_showdown_data(name)
        }

        # Mettre en cache
        self.cache[name] = pokemon_data
        return pokemon_data

    def _fetch_pokeapi_data(self, name: str) -> Dict[str, Any]:
        """Récupère les données depuis PokéAPI"""
        response = requests.get(f"{self.POKEAPI_URL}pokemon/{name}")
        if response.status_code == 200:
            return response.json()
        return {}

    def _fetch_showdown_data(self, name: str) -> Dict[str, Any]:
        """Récupère les données depuis Showdown"""
        response = requests.get(f"{self.SHOWDOWN_DATA_URL}pokedex.json")
        if response.status_code == 200:
            data = response.json()
            return data.get(name, {})
        return {} 