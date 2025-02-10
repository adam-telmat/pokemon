import json
import os

class JsonManager:
    @staticmethod
    def load_json(file_path):
        if not os.path.exists(file_path):
            return []
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def add_pokemon_to_pokedex(pokemon, pokedex_path):
        pokedex = JsonManager.load_json(pokedex_path)
        # Vérification des doublons
        if not any(p['name'] == pokemon.name for p in pokedex):
            pokedex.append(pokemon.to_dict())
            JsonManager.save_json(pokedex_path, pokedex) 