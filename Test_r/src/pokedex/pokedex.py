import json
import os

class Pokedex:
    """
    A comprehensive Pokédex that stores detailed Pokémon data.
    
    Each entry records stats, types, moves, abilities, species details,
    and sprite URLs. If a Pokémon is encountered more than once,
    its 'encounters' count is incremented.
    """
    def __init__(self):
        self.entries = {}
        self.filepath = os.path.join("data", "pokedex.json")
        self.load()

    def load(self):
        """
        Load the existing Pokédex data from pokedex.json.
        If the file does not exist, initialize with an empty dictionary.
        """
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                self.entries = json.load(f)
        else:
            self.entries = {}

    def save(self):
        """
        Save the current Pokédex entries to pokedex.json,
        ensuring the directory exists.
        """
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump(self.entries, f, indent=4)

    def add_pokemon(self, pokemon):
        """
        Add a Pokémon to the Pokédex.
        
        If the Pokémon already exists (based on its lowercase name),
        increment the 'encounters' count; otherwise, create a new entry
        with all relevant details.
        
        Parameters:
            pokemon: An instance of the Pokemon class.
        """
        name = pokemon.name.lower()
        if name in self.entries:
            self.entries[name]["encounters"] += 1
        else:
            self.entries[name] = {
                "name": pokemon.name,
                "pokedex_id": pokemon.pokedex_id,
                "types": pokemon.types,
                "max_hp": pokemon.max_hp,
                "attack": pokemon.attack,
                "defense": pokemon.defense,
                "special_attack": pokemon.special_attack,
                "special_defense": pokemon.special_defense,
                "speed": pokemon.speed,
                "moves": pokemon.moves,           # List of move dictionaries
                "abilities": pokemon.abilities,   # List of ability names
                "growth_rate": getattr(pokemon, "growth_rate", "unknown"),
                "habitat": getattr(pokemon, "habitat", "unknown"),
                "is_legendary": getattr(pokemon, "is_legendary", False),
                "is_mythical": getattr(pokemon, "is_mythical", False),
                "front_sprite_url": getattr(pokemon, "front_sprite_url", None),
                "back_sprite_url": getattr(pokemon, "back_sprite_url", None),
                "animated_front": getattr(pokemon, "animated_front", None),
                "animated_back": getattr(pokemon, "animated_back", None),
                "encounters": 1
            }
        self.save()

    def list_entries(self):
        """
        Return the entire dictionary of Pokédex entries.
        """
        return self.entries

    def get_entry(self, pokemon_name):
        """
        Retrieve a single Pokémon's entry by name (case-insensitive).
        
        Parameters:
            pokemon_name (str): The name of the Pokémon.
            
        Returns:
            The entry dictionary if found, or None if not.
        """
        return self.entries.get(pokemon_name.lower(), None)
