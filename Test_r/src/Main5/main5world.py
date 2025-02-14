#!/usr/bin/env python3
"""
Advanced Pokémon Game Using PokeAPI – Ultimate Edition
======================================================
This enhanced version adds a "World/Location" selection system before wild battles.
You can "Explore Worlds" to pick a Region and a specific Location from the PokeAPI,
and then do wild encounters using that location’s real Pokémon data.

The rest of the original game features remain:
  - Turn-based battles with a 2-second delay between moves,
  - Detailed Pokedex storing captured Pokémon,
  - Team selection & active Pokémon selection,
  - Evolution chain viewer,
  - Item usage screen,
  - Difficulty modes (EASY / HARD),
  - Animated thrown-object effects in battle,
  - And more!

Dependencies:
    pip install pygame requests
To run:
    python advanced_pokemon_game_full.py
"""

# ---------------------- IMPORTS ----------------------
import pygame
import random
import math
import requests
from io import BytesIO
import threading
from functools import lru_cache
import time

# ---------------------- GLOBAL CONFIGURATION ----------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30
DEFAULT_LEVEL = 50
EXP_CURVE = [0, 100, 250, 500, 900, 1400, 2000, 2700, 3500, 4400, 5400]
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

session = requests.Session()

# ---------------------- SPECIES DATA (24 Pokémon) ----------------------
# Fallback local data for if we can't get certain Pokémon from the API, or for quick reference.
SPECIES_DATA = {
    "pikachu": {"name": "Pikachu", "types": ["electric"], "level": 50, "max_hp": 120, "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50, "speed": 90, "moves": ["thunder-shock", "quick-attack", "iron-tail", "electro-ball"]},
    "charmander": {"name": "Charmander", "types": ["fire"], "level": 50, "max_hp": 118, "attack": 52, "defense": 43, "special_attack": 60, "special_defense": 50, "speed": 65, "moves": ["scratch", "ember", "growl", "flamethrower"]},
    "bulbasaur": {"name": "Bulbasaur", "types": ["grass"], "level": 50, "max_hp": 125, "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65, "speed": 45, "moves": ["tackle", "vine-whip", "razor-leaf", "growl"]},
    "squirtle": {"name": "Squirtle", "types": ["water"], "level": 50, "max_hp": 127, "attack": 48, "defense": 65, "special_attack": 50, "special_defense": 64, "speed": 43, "moves": ["tackle", "water-gun", "bubble", "bite"]},
    "onix": {"name": "Onix", "types": ["rock", "ground"], "level": 50, "max_hp": 130, "attack": 45, "defense": 160, "special_attack": 30, "special_defense": 45, "speed": 70, "moves": ["tackle", "rock-throw", "harden", "earthquake"]},
    "staryu": {"name": "Staryu", "types": ["water"], "level": 50, "max_hp": 115, "attack": 45, "defense": 55, "special_attack": 70, "special_defense": 55, "speed": 85, "moves": ["tackle", "water-gun", "swift", "recover"]},
    "butterfree": {"name": "Butterfree", "types": ["bug", "flying"], "level": 50, "max_hp": 130, "attack": 45, "defense": 50, "special_attack": 80, "special_defense": 80, "speed": 70, "moves": ["gust", "confusion", "psybeam", "silver-wind"]},
    "beedrill": {"name": "Beedrill", "types": ["bug", "poison"], "level": 50, "max_hp": 125, "attack": 80, "defense": 40, "special_attack": 45, "special_defense": 80, "speed": 75, "moves": ["fury-attack", "twineedle", "poison-sting", "rage"]},
    "pidgey": {"name": "Pidgey", "types": ["normal", "flying"], "level": 50, "max_hp": 110, "attack": 45, "defense": 40, "special_attack": 35, "special_defense": 35, "speed": 56, "moves": ["tackle", "gust", "quick-attack", "sand-attack"]},
    "rattata": {"name": "Rattata", "types": ["normal"], "level": 50, "max_hp": 105, "attack": 56, "defense": 35, "special_attack": 25, "special_defense": 35, "speed": 72, "moves": ["tackle", "quick-attack", "bite", "focus-energy"]},
    "spearow": {"name": "Spearow", "types": ["normal", "flying"], "level": 50, "max_hp": 105, "attack": 60, "defense": 30, "special_attack": 31, "special_defense": 31, "speed": 70, "moves": ["peck", "growl", "leer", "fury-attack"]},
    "ekans": {"name": "Ekans", "types": ["poison"], "level": 50, "max_hp": 115, "attack": 60, "defense": 44, "special_attack": 40, "special_defense": 54, "speed": 55, "moves": ["wrap", "poison-sting", "bite", "glare"]},
    "sandshrew": {"name": "Sandshrew", "types": ["ground"], "level": 50, "max_hp": 125, "attack": 75, "defense": 85, "special_attack": 20, "special_defense": 30, "speed": 40, "moves": ["scratch", "defense-curl", "sand-attack", "poison-sting"]},
    "clefairy": {"name": "Clefairy", "types": ["fairy"], "level": 50, "max_hp": 130, "attack": 45, "defense": 48, "special_attack": 60, "special_defense": 65, "speed": 35, "moves": ["pound", "sing", "doubleslap", "growl"]},
    "vulpix": {"name": "Vulpix", "types": ["fire"], "level": 50, "max_hp": 115, "attack": 41, "defense": 40, "special_attack": 50, "special_defense": 65, "speed": 65, "moves": ["ember", "tail-whip", "quick-attack", "flamethrower"]},
    "jigglypuff": {"name": "Jigglypuff", "types": ["normal", "fairy"], "level": 50, "max_hp": 160, "attack": 45, "defense": 20, "special_attack": 45, "special_defense": 25, "speed": 20, "moves": ["pound", "sing", "defense-curl", "doubleslap"]},
    "zubat": {"name": "Zubat", "types": ["poison", "flying"], "level": 50, "max_hp": 105, "attack": 45, "defense": 35, "special_attack": 30, "special_defense": 40, "speed": 55, "moves": ["leech-life", "supersonic", "bite", "wing-attack"]},
    "oddish": {"name": "Oddish", "types": ["grass", "poison"], "level": 50, "max_hp": 120, "attack": 50, "defense": 55, "special_attack": 75, "special_defense": 65, "speed": 30, "moves": ["absorb", "poison-powder", "acid", "sleep-powder"]},
    "paras": {"name": "Paras", "types": ["bug", "grass"], "level": 50, "max_hp": 115, "attack": 70, "defense": 55, "special_attack": 45, "special_defense": 55, "speed": 25, "moves": ["scratch", "stun-spore", "leech-life", "spore"]},
    "venonat": {"name": "Venonat", "types": ["bug", "poison"], "level": 50, "max_hp": 125, "attack": 55, "defense": 50, "special_attack": 40, "special_defense": 55, "speed": 45, "moves": ["tackle", "disable", "confusion", "poison-powder"]},
    "diglett": {"name": "Diglett", "types": ["ground"], "level": 50, "max_hp": 90, "attack": 55, "defense": 25, "special_attack": 35, "special_defense": 45, "speed": 95, "moves": ["scratch", "sand-attack", "growl", "dig"]},
    "meowth": {"name": "Meowth", "types": ["normal"], "level": 50, "max_hp": 110, "attack": 45, "defense": 35, "special_attack": 40, "special_defense": 40, "speed": 90, "moves": ["scratch", "bite", "pay-day", "growl"]},
    "psyduck": {"name": "Psyduck", "types": ["water"], "level": 50, "max_hp": 120, "attack": 52, "defense": 48, "special_attack": 65, "special_defense": 50, "speed": 55, "moves": ["scratch", "water-gun", "confusion", "disable"]},
    "mankey": {"name": "Mankey", "types": ["fighting"], "level": 50, "max_hp": 115, "attack": 80, "defense": 35, "special_attack": 35, "special_defense": 45, "speed": 70, "moves": ["scratch", "karate-chop", "low-kick", "focus-energy"]}
}

# ---------------------- MOVES DATA ----------------------
MOVES_DATA = {
    "thunder-shock": {"name": "Thunder Shock", "power": 40, "type": "electric", "damage_class": "special", "accuracy": 100},
    "quick-attack": {"name": "Quick Attack", "power": 40, "type": "normal", "damage_class": "physical", "accuracy": 100},
    "iron-tail": {"name": "Iron Tail", "power": 100, "type": "steel", "damage_class": "physical", "accuracy": 75},
    "electro-ball": {"name": "Electro Ball", "power": 60, "type": "electric", "damage_class": "special", "accuracy": 100},
    "scratch": {"name": "Scratch", "power": 40, "type": "normal", "damage_class": "physical", "accuracy": 100},
    "ember": {"name": "Ember", "power": 40, "type": "fire", "damage_class": "special", "accuracy": 100},
    "growl": {"name": "Growl", "power": 0, "type": "normal", "damage_class": "status", "accuracy": 100},
    "flamethrower": {"name": "Flamethrower", "power": 90, "type": "fire", "damage_class": "special", "accuracy": 100},
    "tackle": {"name": "Tackle", "power": 40, "type": "normal", "damage_class": "physical", "accuracy": 100},
    # Add more moves as desired...
}

# ---------------------- TYPE MATCHUPS ----------------------
# Basic example multipliers
TYPE_MATCHUPS = {
    ("fire", "grass"): 2.0,
    ("grass", "water"): 2.0,
    ("water", "fire"): 2.0,
    ("electric", "water"): 2.0,
    ("ground", "electric"): 2.0,
    ("rock", "fire"): 2.0
}

# ---------------------------------------------------------
#  POKEMON CLASS
# ---------------------------------------------------------
class Pokemon:
    """
    Represents a Pokémon with live data fetched from the PokeAPI.
    Loads stats, types, moves, sprite URLs, and dynamically loads its sprite image.
    Provides methods for healing, taking damage, EXP/leveling, etc.
    """

    def __init__(self, name: str, level=DEFAULT_LEVEL):
        self.name = name.lower()
        self.level = level
        self.exp = 0
        self.status = None
        self.shake_offset = 0
        if not self.load_from_api():
            # If the API fails, try fallback from SPECIES_DATA
            fallback = SPECIES_DATA.get(self.name)
            if fallback:
                self.load_fallback_data(fallback)
            else:
                raise Exception(f"Unable to load data for {name}")
        self.sprite = self.load_sprite_image()

    def load_fallback_data(self, data_dict):
        """
        Fallback if the real PokeAPI call fails or the Pokémon doesn't exist in the PokeAPI.
        """
        self.pokedex_id = 99999
        self.height = 1
        self.weight = 1
        self.max_hp = data_dict["max_hp"]
        self.current_hp = self.max_hp
        self.attack = data_dict["attack"]
        self.defense = data_dict["defense"]
        self.special_attack = data_dict["special_attack"]
        self.special_defense = data_dict["special_defense"]
        self.speed = data_dict["speed"]
        self.types = data_dict["types"]
        self.moves = []
        for move_name in data_dict["moves"]:
            # If we have local info in MOVES_DATA, use it:
            move_obj = MOVES_DATA.get(move_name, None)
            if move_obj:
                self.moves.append({
                    "name": move_obj["name"],
                    "power": move_obj["power"],
                    "accuracy": move_obj["accuracy"],
                    "pp": 25,
                    "type": move_obj["type"],
                    "damage_class": move_obj["damage_class"]
                })

    def load_from_api(self) -> bool:
        try:
            url = f"{POKEAPI_BASE_URL}pokemon/{self.name}"
            response = session.get(url)
            if response.status_code != 200:
                return False

            data = response.json()
            self.pokedex_id = data.get("id")
            self.height = data.get("height", 0) / 10
            self.weight = data.get("weight", 0) / 10

            stats = {s["stat"]["name"]: s["base_stat"] for s in data.get("stats", [])}
            self.max_hp = stats.get("hp", 50) + self.level
            self.current_hp = self.max_hp
            self.attack = stats.get("attack", 50)
            self.defense = stats.get("defense", 50)
            self.special_attack = stats.get("special-attack", 50)
            self.special_defense = stats.get("special-defense", 50)
            self.speed = stats.get("speed", 50)

            self.types = [t["type"]["name"] for t in data.get("types", [])]

            # Limit to 4 moves for brevity:
            self.moves = []
            for move in data.get("moves", [])[:4]:
                move_url = move["move"]["url"]
                move_resp = session.get(move_url)
                if move_resp.status_code == 200:
                    move_data = move_resp.json()
                    self.moves.append({
                        "name": move_data["name"],
                        "power": move_data.get("power") or 0,
                        "accuracy": move_data.get("accuracy") or 100,
                        "pp": move_data.get("pp") or 0,
                        "type": move_data["type"]["name"],
                        "damage_class": move_data["damage_class"]["name"]
                    })

            sprites = data.get("sprites", {})
            self.front_sprite_url = sprites.get("front_default")
            self.back_sprite_url = sprites.get("back_default")
            return True

        except Exception:
            return False

    def load_sprite_image(self):
        """
        Loads the Pokémon's front sprite into a Pygame Surface (scaled).
        If unavailable, returns a placeholder surface.
        """
        try:
            if hasattr(self, "front_sprite_url") and self.front_sprite_url:
                response = session.get(self.front_sprite_url)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    sprite_image = pygame.image.load(image_data).convert_alpha()
                    self.original_sprite = sprite_image.copy()
                    sprite_image = pygame.transform.scale(sprite_image, (80, 80))
                    return sprite_image
            placeholder = pygame.Surface((80, 80))
            placeholder.fill((200, 200, 200))
            return placeholder
        except Exception as e:
            print(f"Error loading sprite for {self.name}: {e}")
            placeholder = pygame.Surface((80, 80))
            placeholder.fill((200, 200, 200))
            return placeholder

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, damage: int):
        # If you want status-based modifications, do so here.
        if self.status == "burn":
            damage = int(damage * 0.5)
        actual = max(1, damage)
        self.current_hp = max(0, self.current_hp - actual)

    def heal(self):
        self.current_hp = self.max_hp
        self.status = None

    def get_evolution_chain(self):
        """
        Returns the entire evolution chain from the PokeAPI.
        """
        try:
            species_url = f"{POKEAPI_BASE_URL}pokemon-species/{self.name}/"
            response = session.get(species_url)
            if response.status_code != 200:
                return None
            species_data = response.json()
            evolution_url = species_data.get("evolution_chain", {}).get("url")
            if evolution_url:
                evo_response = session.get(evolution_url)
                if evo_response.status_code == 200:
                    return evo_response.json()
            return None
        except Exception as e:
            print(f"Error fetching evolution chain for {self.name}: {e}")
            return None

    def gain_exp(self, amount: int):
        self.exp += amount
        if self.level < len(EXP_CURVE) and self.exp >= EXP_CURVE[self.level]:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.exp = 0
        self.max_hp += 5
        self.attack += 2
        self.defense += 2
        self.special_attack += 2
        self.special_defense += 2
        self.speed += 1
        self.heal()
        print(f"{self.name.capitalize()} leveled up to {self.level}!")

# ---------------------------------------------------------
# BATTLE SYSTEM
# ---------------------------------------------------------
class Battle:
    """
    Implements a turn-based battle between two Pokémon, including advanced thrown-object effects.
    """
    def __init__(self, pkmn1: Pokemon, pkmn2: Pokemon, is_trainer_battle=False):
        self.p1 = pkmn1
        self.p2 = pkmn2
        self.turn = 1
        self.battle_log = []
        self.is_trainer_battle = is_trainer_battle

    def log(self, message: str):
        self.battle_log.append(message)
        print(message)

    def get_type_multiplier(self, attack_type: str, defender_types: list) -> float:
        multiplier = 1.0
        for d_type in defender_types:
            if (attack_type, d_type) in TYPE_MATCHUPS:
                multiplier *= TYPE_MATCHUPS[(attack_type, d_type)]
        return multiplier

    def calculate_damage(self, attacker: Pokemon, defender: Pokemon, move: dict) -> int:
        power = move["power"]
        if power <= 0:
            return 0
        if move["damage_class"] == "physical":
            A = attacker.attack
            D = defender.defense
        else:
            A = attacker.special_attack
            D = defender.special_defense

        level = attacker.level
        base = (((2 * level) / 5) + 2) * power * (A / D) / 50 + 2
        random_factor = random.uniform(0.85, 1.0)
        stab = 1.5 if move["type"] in attacker.types else 1.0
        type_multiplier = self.get_type_multiplier(move["type"], defender.types)
        critical = 2.0 if random.random() < 0.0625 else 1.0
        modifier = random_factor * stab * type_multiplier * critical
        damage = int(base * modifier)
        return max(1, damage)

    def do_move(self, attacker: Pokemon, defender: Pokemon, move: dict):
        self.log(f"{attacker.name.capitalize()} used {move['name'].capitalize()}!")
        # Check accuracy:
        if random.randint(1, 100) <= move["accuracy"]:
            dmg = self.calculate_damage(attacker, defender, move)
            defender.take_damage(dmg)
            self.log(f"It dealt {dmg} damage to {defender.name.capitalize()}!")
            attacker.shake_offset = 5
            pygame.time.set_timer(pygame.USEREVENT + 1, 300)  # shake timer

            # Add a nice projectile effect:
            effect_color = None
            if move["name"] == "electro-ball":
                effect_color = (255, 215, 0)
            elif move["name"] in ["ember", "flamethrower"]:
                effect_color = (255, 69, 0)
            else:
                effect_color = random.choice([(30,144,255), (138,43,226)])

            Game.create_attack_effect(attacker, defender, effect_color)

        else:
            self.log(f"{attacker.name.capitalize()}'s attack missed!")

    def next_turn(self, p1_move_index: int, p2_move_index: int) -> bool:
        current_time = pygame.time.get_ticks()
        if current_time - Game.last_attack_time < 2000:
            # Enforce 2-second delay
            return True

        Game.last_attack_time = current_time

        # Speed determines who attacks first:
        if self.p1.speed >= self.p2.speed:
            self.do_move(self.p1, self.p2, self.p1.moves[p1_move_index])
            if not self.p2.is_alive():
                self.log(f"{self.p2.name.capitalize()} fainted!")
                if not self.is_trainer_battle:
                    self.p1.gain_exp(100)
                return False

            self.do_move(self.p2, self.p1, self.p2.moves[p2_move_index])
            if not self.p1.is_alive():
                self.log(f"{self.p1.name.capitalize()} fainted!")
                return False
        else:
            self.do_move(self.p2, self.p1, self.p2.moves[p2_move_index])
            if not self.p1.is_alive():
                self.log(f"{self.p1.name.capitalize()} fainted!")
                return False

            self.do_move(self.p1, self.p2, self.p1.moves[p1_move_index])
            if not self.p2.is_alive():
                self.log(f"{self.p2.name.capitalize()} fainted!")
                if not self.is_trainer_battle:
                    self.p1.gain_exp(100)
                return False

        self.turn += 1
        return True

# ---------------------------------------------------------
# EVOLUTION VIEWER
# ---------------------------------------------------------
class EvolutionViewer:
    def __init__(self, pokemon: Pokemon):
        self.pokemon = pokemon
        self.chain_data = pokemon.get_evolution_chain()
    
    def render_chain(self, surface, font):
        if not self.chain_data:
            draw_text(surface, "No evolution chain data available.", (50, 50), font, (0, 0, 0))
            return
        chain = self.chain_data.get("chain", {})
        species_names = []
        def traverse(chain_node):
            if chain_node:
                species_names.append(chain_node.get("species", {}).get("name", "Unknown").capitalize())
                for evo in chain_node.get("evolves_to", []):
                    traverse(evo)
        traverse(chain)
        y = 50
        draw_text(surface, "Evolution Chain:", (50, y), font, (0, 0, 0))
        y += 40
        for name in species_names:
            draw_text(surface, name, (50, y), font, (0, 0, 0))
            y += 30

# ---------------------------------------------------------
# ITEM CLASS
# ---------------------------------------------------------
class Item:
    def __init__(self, item_id: int):
        self.item_id = item_id
        self.data = self.load_item_data()
        self.name = self.data.get("name") if self.data else "unknown"
        self.sprite = self.load_item_sprite()

    def load_item_data(self):
        try:
            url = f"{POKEAPI_BASE_URL}item/{self.item_id}/"
            response = session.get(url)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error loading item data: {e}")
            return None

    def load_item_sprite(self):
        try:
            if self.data and self.data.get("sprites") and self.data["sprites"].get("default"):
                url = self.data["sprites"]["default"]
                response = session.get(url)
                if response.status_code == 200:
                    image_data = BytesIO(response.content)
                    sprite = pygame.image.load(image_data).convert_alpha()
                    sprite = pygame.transform.scale(sprite, (50, 50))
                    return sprite
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((220, 220, 220))
            return placeholder
        except Exception as e:
            print(f"Error loading item sprite: {e}")
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((220, 220, 220))
            return placeholder

# ---------------------------------------------------------
# EXTENDED POKEAPI EXTENSIONS (CACHED)
# ---------------------------------------------------------
class PokeAPIExtensions:
    @staticmethod
    @lru_cache(maxsize=32)
    def get_berry(berry_id):
        url = f"{POKEAPI_BASE_URL}berry/{berry_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    @lru_cache(maxsize=32)
    def get_contest_type(contest_type_id):
        url = f"{POKEAPI_BASE_URL}contest-type/{contest_type_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    def get_encounter(pokemon_id):
        # Example usage: /pokemon/{id}/encounters
        url = f"{POKEAPI_BASE_URL}pokemon/{pokemon_id}/encounters/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    def get_evolution_chain(chain_id):
        url = f"{POKEAPI_BASE_URL}evolution-chain/{chain_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    @lru_cache(maxsize=32)
    def get_game(game_id):
        url = f"{POKEAPI_BASE_URL}game/{game_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    @lru_cache(maxsize=32)
    def get_generation(generation_id):
        url = f"{POKEAPI_BASE_URL}generation/{generation_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    @lru_cache(maxsize=32)
    def get_pokedex(pokedex_id):
        url = f"{POKEAPI_BASE_URL}pokedex/{pokedex_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    @lru_cache(maxsize=32)
    def get_version(version_id):
        url = f"{POKEAPI_BASE_URL}version/{version_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    @lru_cache(maxsize=32)
    def get_item(item_id):
        url = f"{POKEAPI_BASE_URL}item/{item_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    @staticmethod
    @lru_cache(maxsize=32)
    def get_location(location_id):
        url = f"{POKEAPI_BASE_URL}location/{location_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

    # -----------------------------------------------------
    # NEW: Region and Location fetch methods
    # -----------------------------------------------------
    @staticmethod
    @lru_cache(maxsize=1)
    def get_all_regions():
        """
        Fetch a list of all Regions from the PokeAPI.
        Returns a list of dicts with minimal info: { 'name': 'kanto', 'url': '...' }
        """
        # You can limit or offset if you like:
        response = session.get(f"{POKEAPI_BASE_URL}region?limit=100")
        if response.status_code == 200:
            return response.json().get("results", [])
        return []

    @staticmethod
    @lru_cache(maxsize=32)
    def get_region(name_or_id):
        """
        Returns region detail for the given region name (e.g., 'kanto') or id.
        Typically includes "locations" referencing the location resources.
        """
        url = f"{POKEAPI_BASE_URL}region/{name_or_id}/"
        response = session.get(url)
        return response.json() if response.status_code == 200 else None

# ---------------------------------------------------------
# GUI HELPER
# ---------------------------------------------------------
def draw_text(surface, text, pos, font, color):
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

# ---------------------------------------------------------
# GUI CLASS
# ---------------------------------------------------------
class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.font_lg = pygame.font.SysFont("Arial", 36)
        self.font_md = pygame.font.SysFont("Arial", 28)
        self.font_sm = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 14)
        self.bg_animation_offset = 0
        self.bg_animation_speed = 0.5
        self.team_hovered_index = None
        self.selection_scroll_offset = 0

    def draw_gradient_background(self, start_color, end_color):
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def draw_main_menu(self, button_labels: list):
        self.draw_gradient_background((240, 220, 200), (180, 200, 240))
        title_surf = self.font_lg.render("Main Menu", True, (10, 10, 10))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 70))
        self.screen.blit(title_surf, title_rect)
        button_rects = []
        start_y = 140
        mx, my = pygame.mouse.get_pos()

        for i, label in enumerate(button_labels):
            rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, start_y + i * 55, 240, 50)
            color = (50, 150, 220) if rect.collidepoint(mx, my) else (70, 170, 240)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (20, 20, 20), rect, 2)
            text_surf = self.font_md.render(label, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            button_rects.append((rect, label))

        self.bg_animation_offset = (self.bg_animation_offset + self.bg_animation_speed) % WINDOW_WIDTH
        for i in range(0, WINDOW_WIDTH, 20):
            pygame.draw.line(self.screen, (220, 220, 220), (i + self.bg_animation_offset, WINDOW_HEIGHT - 10), (i + self.bg_animation_offset - 10, WINDOW_HEIGHT), 2)

        return button_rects

    def draw_battle_scene(self, player: Pokemon, opponent: Pokemon, battle_log: list, move_menu: list = None, selected_index: int = 0):
        self.screen.fill((245, 245, 245))
        # Opponent sprite
        self.draw_battle_sprite(opponent, (WINDOW_WIDTH * 0.55, 100), flipped=True)
        self.draw_battle_sprite(player, (WINDOW_WIDTH * 0.1, 280))
        self.draw_hp_bar(opponent, (WINDOW_WIDTH * 0.55 - 50, 70))
        self.draw_hp_bar(player, (WINDOW_WIDTH * 0.1 - 50, 260))

        # Battle log
        y_log = 420
        for line in reversed(battle_log[-4:]):
            log_surf = self.font_sm.render(line, True, (10, 10, 10))
            log_rect = log_surf.get_rect(midright=(WINDOW_WIDTH - 50, y_log))
            self.screen.blit(log_surf, log_rect)
            y_log += 26

        # Moves
        if move_menu:
            self.draw_move_menu(move_menu, selected_index)

        # If difficulty is EASY, show opponent details
        if Game.difficulty == "EASY":
            self.draw_opponent_details(opponent)

    def draw_battle_sprite(self, pkmn: Pokemon, pos, flipped=False):
        try:
            if pkmn.sprite:
                sprite = pygame.transform.flip(pkmn.sprite, True, False) if flipped else pkmn.sprite
                if hasattr(pkmn, "original_sprite"):
                    sprite = pygame.transform.scale(pkmn.original_sprite, (160, 160))
                else:
                    sprite = pygame.transform.scale(sprite, (160, 160))
                self.screen.blit(sprite, pos)
            else:
                raise Exception("No sprite available")
        except Exception:
            color = (150, 150, 250) if not flipped else (250, 150, 150)
            rect = pygame.Rect(pos[0], pos[1], 160, 160)
            pygame.draw.rect(self.screen, color, rect)
            name_surf = self.font_sm.render(pkmn.name.capitalize(), True, (0, 0, 0))
            self.screen.blit(name_surf, (pos[0], pos[1] - 20))

    def draw_hp_bar(self, pkmn: Pokemon, pos):
        max_bar_width = 250
        bar_height = 25
        ratio = pkmn.current_hp / pkmn.max_hp
        current_width = int(max_bar_width * ratio)
        pygame.draw.rect(self.screen, (20, 20, 20), (pos[0], pos[1], max_bar_width, bar_height), 2)
        pygame.draw.rect(self.screen, (0, 220, 0), (pos[0], pos[1], current_width, bar_height))

    def draw_move_menu(self, moves: list, selected_index: int):
        menu_x = 50
        menu_y = 500
        box_width = 300
        box_height = 120
        pygame.draw.rect(self.screen, (220, 220, 220), (menu_x, menu_y, box_width, box_height))
        pygame.draw.rect(self.screen, (20, 20, 20), (menu_x, menu_y, box_width, box_height), 2)
        for i, move in enumerate(moves):
            y_pos = menu_y + 10 + i * 26
            color = (220, 50, 50) if i == selected_index else (20, 20, 20)
            move_str = f"{move['name'].capitalize()} (Pow: {move['power']}, {move['type']})"
            text_surf = self.font_sm.render(move_str, True, color)
            self.screen.blit(text_surf, (menu_x + 10, y_pos))

    def draw_opponent_details(self, opponent: Pokemon):
        panel_rect = pygame.Rect(WINDOW_WIDTH - 250, 10, 240, 140)
        s = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 150))
        self.screen.blit(s, panel_rect.topleft)
        details = [
            f"{opponent.name.capitalize()} Details:",
            f"LV: {opponent.level}",
            f"HP: {opponent.current_hp}/{opponent.max_hp}",
            f"ATK: {opponent.attack}",
            f"DEF: {opponent.defense}",
            f"Sp. Atk: {opponent.special_attack}",
            f"Sp. Def: {opponent.special_defense}",
            f"SPD: {opponent.speed}",
            f"Types: {', '.join(opponent.types)}"
        ]
        y = panel_rect.top + 5
        for line in details:
            detail_surf = self.small_font.render(line, True, (255, 255, 255))
            self.screen.blit(detail_surf, (panel_rect.left + 5, y))
            y += 16

    def draw_result_screen(self, message: str):
        self.draw_gradient_background((220, 230, 255), (160, 190, 230))
        for particle in Game.result_particles:
            pygame.draw.circle(self.screen, particle["color"], (int(particle["x"]), int(particle["y"])), int(particle["radius"]))

        result_title = "You Won!" if "won" in message.lower() or "caught" in message.lower() else "You Lost!"
        title_surf = self.font_lg.render(result_title, True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)

        msg_surf = self.font_md.render(message, True, (10, 10, 10))
        msg_rect = msg_surf.get_rect(center=(WINDOW_WIDTH // 2, 220))
        self.screen.blit(msg_surf, msg_rect)

        if "won" in message.lower() or "caught" in message.lower():
            play_again_rect = pygame.Rect(WINDOW_WIDTH // 2 - 220, 300, 200, 50)
            main_menu_rect = pygame.Rect(WINDOW_WIDTH // 2 + 20, 300, 200, 50)
            pygame.draw.rect(self.screen, (34, 139, 34), play_again_rect)
            pygame.draw.rect(self.screen, (20, 20, 20), play_again_rect, 2)
            pygame.draw.rect(self.screen, (70, 130, 180), main_menu_rect)
            pygame.draw.rect(self.screen, (20, 20, 20), main_menu_rect, 2)
            pa_text = self.font_md.render("Play Again", True, (255, 255, 255))
            mm_text = self.font_md.render("Main Menu", True, (255, 255, 255))
            self.screen.blit(pa_text, pa_text.get_rect(center=play_again_rect.center))
            self.screen.blit(mm_text, mm_text.get_rect(center=main_menu_rect.center))
            Game.result_back_button = main_menu_rect
            Game.play_again_button = play_again_rect
        else:
            btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, 300, 240, 50)
            pygame.draw.rect(self.screen, (50, 205, 50), btn_rect)
            pygame.draw.rect(self.screen, (20, 20, 20), btn_rect, 2)
            btn_text = self.font_md.render("Back to Main Menu", True, (255, 255, 255))
            self.screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))
            Game.result_back_button = btn_rect

    def draw_pokedex(self, pokedex_entries: dict, team_pokemon: list):
        self.screen.fill((255, 255, 240))
        title_surf = self.font_lg.render("Your Pokédex", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 20))
        y = 100
        for key, entry in pokedex_entries.items():
            sprite = entry.get("sprite")
            if sprite:
                self.screen.blit(sprite, (50, y))
            line = f"{entry['name'].capitalize()} - HP: {entry['hp']}, Types: {', '.join(entry['types'])}"
            text_surf = self.font_sm.render(line, True, (10, 10, 10))
            self.screen.blit(text_surf, (140, y + 20))
            y += 100

        team_title = self.font_md.render("Your Team:", True, (10, 10, 10))
        self.screen.blit(team_title, (50, WINDOW_HEIGHT - 120))
        x = 200
        for pkmn in team_pokemon:
            if pkmn.sprite:
                self.screen.blit(pkmn.sprite, (x, WINDOW_HEIGHT - 140))
            x += 90

    def draw_evolution_chain(self, chain_data, font):
        self.screen.fill((240, 240, 255))
        title = "Evolution Chain"
        title_surf = font.render(title, True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 20))

        y = 100
        species_names = []
        def traverse(chain_node):
            if chain_node:
                species_names.append(chain_node.get("species", {}).get("name", "Unknown").capitalize())
                for evo in chain_node.get("evolves_to", []):
                    traverse(evo)
        if chain_data:
            traverse(chain_data.get("chain", {}))

        for name in species_names:
            line = f"{name}"
            text_surf = self.font_sm.render(line, True, (10, 10, 10))
            self.screen.blit(text_surf, (50, y))
            y += 30

    def draw_item_screen(self, item: Item):
        self.screen.fill((250, 240, 230))
        title_surf = self.font_lg.render("Item Usage", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 20))
        if item:
            self.screen.blit(item.sprite, (50, 100))
            draw_text(self.screen, f"{item.name.capitalize()}", (120, 110), self.font_md, (10, 10, 10))
        else:
            draw_text(self.screen, "No item data available.", (50, 100), self.font_md, (10, 10, 10))
        draw_text(self.screen, "Press any key to return to the main menu...", (50, 200), self.font_sm, (10, 10, 10))

    def draw_team_selection(self, available_pokemon: list, selected_indices: set):
        self.screen.fill((220, 240, 255))
        title_surf = self.font_lg.render("Select Your 6 Pokémon", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 10))

        grid_cols = 4
        cell_width = WINDOW_WIDTH // grid_cols
        cell_height = 90
        grid_y = 80
        mx, my = pygame.mouse.get_pos()
        self.team_hovered_index = None

        for idx, pkmn in enumerate(available_pokemon):
            col = idx % grid_cols
            row = idx // grid_cols
            x = col * cell_width + 20
            y = grid_y + row * cell_height - self.selection_scroll_offset
            cell_rect = pygame.Rect(col * cell_width + 10, grid_y + row * cell_height - self.selection_scroll_offset, cell_width - 20, cell_height - 10)

            if cell_rect.collidepoint(mx, my):
                self.team_hovered_index = idx

            if idx in selected_indices:
                pygame.draw.rect(self.screen, (144, 238, 144), cell_rect)
            else:
                pygame.draw.rect(self.screen, (245, 245, 245), cell_rect)

            pygame.draw.rect(self.screen, (10, 10, 10), cell_rect, 2)
            if pkmn.sprite:
                self.screen.blit(pkmn.sprite, (x, y))
            name_text = self.font_sm.render(pkmn.name.capitalize(), True, (10, 10, 10))
            self.screen.blit(name_text, (x, y + 70))

        # Hover details:
        if self.team_hovered_index is not None:
            hovered_pkmn = available_pokemon[self.team_hovered_index]
            panel_rect = pygame.Rect(WINDOW_WIDTH - 250, grid_y, 230, 200)
            pygame.draw.rect(self.screen, (255, 255, 255), panel_rect)
            pygame.draw.rect(self.screen, (10, 10, 10), panel_rect, 2)
            details = [
                f"Name: {hovered_pkmn.name.capitalize()}",
                f"HP: {hovered_pkmn.max_hp}",
                f"ATK: {hovered_pkmn.attack}",
                f"DEF: {hovered_pkmn.defense}",
                f"Sp. Atk: {hovered_pkmn.special_attack}",
                f"Sp. Def: {hovered_pkmn.special_defense}",
                f"Speed: {hovered_pkmn.speed}",
                f"Types: {', '.join(hovered_pkmn.types)}"
            ]
            dy = panel_rect.top + 10
            for line in details:
                detail_surf = self.font_sm.render(line, True, (10, 10, 10))
                self.screen.blit(detail_surf, (panel_rect.left + 10, dy))
                dy += 25

        if 1 <= len(selected_indices) <= 6:
            btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 70, 200, 50)
            pygame.draw.rect(self.screen, (70, 130, 180), btn_rect)
            pygame.draw.rect(self.screen, (10, 10, 10), btn_rect, 2)
            btn_text = self.font_md.render("Confirm Selection", True, (255, 255, 255))
            btn_text_rect = btn_text.get_rect(center=btn_rect.center)
            self.screen.blit(btn_text, btn_text_rect)
            Game.selection_confirm_button = btn_rect
        else:
            Game.selection_confirm_button = None

    def draw_active_selection(self, team: list):
        self.screen.fill((240, 255, 240))
        title_surf = self.font_lg.render("Choose Your Active Pokémon", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 10))

        grid_cols = len(team)
        cell_width = WINDOW_WIDTH // grid_cols
        cell_height = 200

        for idx, pkmn in enumerate(team):
            x = idx * cell_width + 20
            y = 80
            cell_rect = pygame.Rect(idx * cell_width + 10, 80, cell_width - 20, cell_height - 10)
            pygame.draw.rect(self.screen, (245, 245, 245), cell_rect)
            pygame.draw.rect(self.screen, (10, 10, 10), cell_rect, 2)

            if pkmn.sprite:
                offset = -8 * math.sin(pygame.time.get_ticks() * 0.005) if idx == Game.active_selection_index else 0
                self.screen.blit(pkmn.sprite, (x, 80 + offset))

            info = [
                f"{pkmn.name.capitalize()}",
                f"HP: {pkmn.max_hp}",
                f"ATK: {pkmn.attack}",
                f"DEF: {pkmn.defense}",
                f"SPD: {pkmn.speed}"
            ]
            dy = 160
            for line in info:
                info_surf = self.font_sm.render(line, True, (10, 10, 10))
                self.screen.blit(info_surf, (x, dy))
                dy += 20

            if idx == Game.active_selection_index:
                pointer_x = x + (cell_width - 20) // 2
                pointer_y = 70
                point_list = [(pointer_x, pointer_y), (pointer_x - 10, pointer_y + 10), (pointer_x + 10, pointer_y + 10)]
                pygame.draw.polygon(self.screen, (255, 0, 0), point_list)

        btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 70, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), btn_rect)
        pygame.draw.rect(self.screen, (10, 10, 10), btn_rect, 2)
        btn_text = self.font_md.render("Confirm Active", True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=btn_rect.center)
        self.screen.blit(btn_text, btn_text_rect)
        Game.active_confirm_button = btn_rect

    def draw_how_to_play(self):
        self.draw_gradient_background((255, 250, 240), (240, 230, 140))
        title_surf = self.font_lg.render("How to Play", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 10))
        instructions = [
            "Welcome to Pokémon Adventure!",
            "",
            "Controls:",
            "  - UP/DOWN or W/S: Navigate menus & moves.",
            "  - ENTER: Confirm selection.",
            "  - Mouse: Click to select/deselect.",
            "  - Mouse Wheel: Scroll in team selection.",
            "  - ESC: Return to previous menu.",
            "  - D: From main menu, open Difficulty selection.",
            "",
            "Team Selection:",
            "  - Choose up to 6 Pokémon from the grid.",
            "  - Hover over a Pokémon to view details.",
            "",
            "Active Selection:",
            "  - Click a team member to select your active Pokémon.",
            "",
            "Battle Damage Formula:",
            "  Damage = ((((2*Lv)/5+2)*Pow*(A/D))/50+2) * Modifier",
            "    Modifier = rand * STAB * Type * Crit",
            "    (STAB=1.5 if move matches type; Crit=2x, ~6.25% chance)",
            "",
            "New Features:",
            "  - Thrown-object effects in battles.",
            "  - 2-second delay enforced between moves.",
            "  - Catch wild Pokémon if you defeat them!",
            "  - EASY mode shows opponent details; HARD hides them.",
            "  - Explore worlds to pick real-locations for random encounters!",
            "",
            "All captured Pokémon are stored in your Pokédex.",
            "",
            "Press any key or click 'Back to Main Menu' to return."
        ]
        y = 80
        for line in instructions:
            inst_surf = self.small_font.render(line, True, (10, 10, 10))
            self.screen.blit(inst_surf, (50, y))
            y += 18

        btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 70, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), btn_rect)
        pygame.draw.rect(self.screen, (10, 10, 10), btn_rect, 2)
        btn_text = self.font_md.render("Back to Main Menu", True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=btn_rect.center)
        self.screen.blit(btn_text, btn_text_rect)
        Game.howto_back_button = btn_rect

# ---------------------------------------------------------
# MAIN GAME CLASS
# ---------------------------------------------------------
class Game:
    result_particles = []
    attack_effects = []
    result_back_button = None
    selection_confirm_button = None
    active_confirm_button = None
    howto_back_button = None
    play_again_button = None
    catch_confirm_button = None
    active_selection_index = 0
    difficulty = "HARD"
    last_attack_time = 0
    pokedex = {}  # Stores captured Pokémon (name -> dict)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pokémon Adventure")
        self.clock = pygame.time.Clock()
        self.gui = GUI(self.screen)

        # Game states:
        #   MENU, DIFFICULTY, HOW_TO_PLAY, SELECTION, ACTIVE_SELECT, BATTLE,
        #   CATCH, RESULT, POKEDEX, EVOLUTION, ITEM,
        #   REGION_SELECT, LOCATION_SELECT
        self.state = "MENU"

        self.font_md = pygame.font.Font(None, 36)
        self.font_sm = pygame.font.Font(None, 28)

        # The player's chosen Pokémon for battle
        self.player_pokemon = None
        self.opponent_pokemon = None
        self.battle = None
        self.selected_move_index = 0
        self.result_message = ""

        # The player's entire selected team
        self.player_team = []

        # Some gym leader or boss Pokémon
        self.gym_leaders = [Pokemon(name) for name in ["onix", "staryu"]]

        # Default wild pool if no location is set:
        self.default_wild_pool = list(SPECIES_DATA.keys())

        # A dynamic wild pool that changes if user picks a location from the API:
        self.world_wild_pool = None  # If set, we use this instead of default_wild_pool

        # A sample item for demonstration
        self.demo_item = Item(1)

        # All available Pokémon for selection
        self.all_pokemon = [Pokemon(name) for name in SPECIES_DATA.keys()]
        self.selected_team_indices = set()

        # For "Explore Worlds" feature:
        self.available_regions = []
        self.selected_region = None
        self.available_locations = []
        self.selected_location = None

        # Attempt to fetch the region list once at initialization:
        self.fetch_regions()

        # For "scrolling" or other expansions, etc.

    @staticmethod
    def create_attack_effect(attacker: Pokemon, defender: Pokemon, color=None):
        # Original logic for thrown objects
        start = (int(WINDOW_WIDTH * 0.1 + 80), int(280 + 40))
        end = (int(WINDOW_WIDTH * 0.55 + 80), int(100 + 40))
        effect = {
            "start": start,
            "end": end,
            "progress": 0,
            "color": color if color else random.choice([(255,69,0), (255,215,0), (30,144,255)]),
            "trajectory": random.choice(["parabola", "zigzag", "linear"])
        }
        Game.attack_effects.append(effect)

    def update_attack_effects(self):
        for effect in Game.attack_effects:
            effect["progress"] += 0.03
        Game.attack_effects[:] = [e for e in Game.attack_effects if e["progress"] < 1]

    def draw_attack_effects(self):
        for effect in Game.attack_effects:
            t = effect["progress"]
            start_x, start_y = effect["start"]
            end_x, end_y = effect["end"]
            if effect["trajectory"] == "parabola":
                current_x = start_x + (end_x - start_x) * t
                current_y = start_y + (end_y - start_y) * t - 80 * math.sin(math.pi * t)
            elif effect["trajectory"] == "zigzag":
                current_x = start_x + (end_x - start_x) * t + 20 * math.sin(10 * math.pi * t)
                current_y = start_y + (end_y - start_y) * t
            else:  # linear
                current_x = start_x + (end_x - start_x) * t
                current_y = start_y + (end_y - start_y) * t

            pygame.draw.circle(self.screen, effect["color"], (int(current_x), int(current_y)), 8)
            pygame.draw.circle(self.screen, effect["color"], (int(current_x), int(current_y)), 4)

    def update_particles(self):
        for particle in Game.result_particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            particle["radius"] = max(0, particle["radius"] - 0.1)
        Game.result_particles[:] = [p for p in Game.result_particles if p["life"] > 0]

    def create_particles(self):
        for _ in range(50):
            Game.result_particles.append({
                "x": WINDOW_WIDTH // 2,
                "y": WINDOW_HEIGHT // 2,
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-3, 3),
                "radius": random.uniform(3, 6),
                "life": random.randint(30, 60),
                "color": random.choice([(255,69,0), (255,215,0), (30,144,255)])
            })

    # ---------------------------
    # Methods for "Explore Worlds"
    # ---------------------------
    def fetch_regions(self):
        """
        Fetch a list of all available regions from the PokeAPI,
        store them in self.available_regions as [ { 'name': 'kanto', 'url': ... }, ... ].
        """
        self.available_regions = PokeAPIExtensions.get_all_regions()

    def fetch_locations_for_region(self, region_name):
        """
        Using the region detail, load all associated 'locations' from that region.
        Store in self.available_locations as [ { 'name': 'viridian-forest', 'url': ... }, ... ].
        """
        region_data = PokeAPIExtensions.get_region(region_name)
        if not region_data:
            self.available_locations = []
            return

        # region_data typically has "locations": [ { 'name': 'viridian-forest', 'url': ... }, ... ]
        self.available_locations = region_data.get("locations", [])

    def build_wild_pool_from_location(self, location_name):
        """
        For the chosen location, fetch real 'pokemon_encounters' from /api/v2/location/<location_name>.
        Build a custom 'world_wild_pool' which is a list of Pokémon names available in that location.
        """
        # Example: https://pokeapi.co/api/v2/location/viridian-forest
        # JSON has "pokemon_encounters": [ { 'pokemon': { 'name': 'caterpie', ... }, ... } ]
        url = f"{POKEAPI_BASE_URL}location/{location_name}"
        response = session.get(url)
        if response.status_code != 200:
            self.world_wild_pool = None
            return

        loc_data = response.json()
        encounters = loc_data.get("pokemon_encounters", [])
        # We'll collect all the encountered Pokémon names:
        pkmn_names = [enc["pokemon"]["name"] for enc in encounters]
        if pkmn_names:
            self.world_wild_pool = pkmn_names
        else:
            self.world_wild_pool = None

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            if self.state == "MENU":
                running = self.handle_menu()
            elif self.state == "DIFFICULTY":
                running = self.handle_difficulty()
            elif self.state == "HOW_TO_PLAY":
                running = self.handle_how_to_play()
            elif self.state == "SELECTION":
                running = self.handle_selection()
            elif self.state == "ACTIVE_SELECT":
                running = self.handle_active_select()
            elif self.state == "BATTLE":
                running = self.handle_battle()
            elif self.state == "CATCH":
                running = self.handle_catch()
            elif self.state == "RESULT":
                running = self.handle_result()
            elif self.state == "POKEDEX":
                running = self.handle_pokedex()
            elif self.state == "EVOLUTION":
                running = self.handle_evolution()
            elif self.state == "ITEM":
                running = self.handle_item()
            elif self.state == "REGION_SELECT":
                running = self.handle_region_select()
            elif self.state == "LOCATION_SELECT":
                running = self.handle_location_select()
            else:
                running = False

            self.update_attack_effects()
            self.draw_attack_effects()
            pygame.display.flip()

        pygame.quit()

    # ----------------------------------
    # Different state handling below
    # ----------------------------------
    def handle_menu(self):
        buttons = self.gui.draw_main_menu([
            "Wild Encounter",
            "Gym Battle",
            "Select Team",
            "How to Play",
            "View Pokédex",
            "View Evolution",
            "Use Item",
            "Explore Worlds",
            "Exit"
        ])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for rect, label in buttons:
                    if rect.collidepoint(mx, my):
                        if label == "Exit":
                            return False
                        elif label == "Wild Encounter":
                            if not self.player_team:
                                self.state = "SELECTION"
                            else:
                                self.state = "ACTIVE_SELECT"
                                Game.active_selection_index = 0
                        elif label == "Gym Battle":
                            if not self.player_team:
                                self.state = "SELECTION"
                            else:
                                # Instead of random wild, do a gym battle.
                                self.state = "ACTIVE_SELECT"
                                Game.active_selection_index = 0
                        elif label == "Select Team":
                            self.state = "SELECTION"
                        elif label == "How to Play":
                            self.state = "HOW_TO_PLAY"
                        elif label == "View Pokédex":
                            self.state = "POKEDEX"
                        elif label == "View Evolution":
                            self.state = "EVOLUTION"
                        elif label == "Use Item":
                            self.state = "ITEM"
                        elif label == "Explore Worlds":
                            self.state = "REGION_SELECT"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_d:
                    self.state = "DIFFICULTY"
        return True

    def handle_difficulty(self):
        self.screen.fill((240, 240, 240))
        prompt = "Select Difficulty Mode:"
        prompt_surf = self.font_md.render(prompt, True, (0, 0, 0))
        self.screen.blit(prompt_surf, (WINDOW_WIDTH//2 - prompt_surf.get_width()//2, 150))

        easy_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, 250, 200, 50)
        hard_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, 320, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), easy_rect)
        pygame.draw.rect(self.screen, (220, 50, 50), hard_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), easy_rect, 2)
        pygame.draw.rect(self.screen, (0, 0, 0), hard_rect, 2)

        easy_text = self.font_md.render("Easy Mode", True, (255, 255, 255))
        hard_text = self.font_md.render("Hard Mode", True, (255, 255, 255))
        self.screen.blit(easy_text, easy_text.get_rect(center=easy_rect.center))
        self.screen.blit(hard_text, hard_text.get_rect(center=hard_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if easy_rect.collidepoint(mx, my):
                    Game.difficulty = "EASY"
                    self.state = "MENU"
                elif hard_rect.collidepoint(mx, my):
                    Game.difficulty = "HARD"
                    self.state = "MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
        return True

    def handle_how_to_play(self):
        self.gui.draw_how_to_play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if Game.howto_back_button and Game.howto_back_button.collidepoint(mx, my):
                    self.state = "MENU"
            elif event.type == pygame.KEYDOWN:
                self.state = "MENU"
        return True

    def handle_selection(self):
        self.gui.draw_team_selection(self.all_pokemon, self.selected_team_indices)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEWHEEL:
                self.gui.selection_scroll_offset = max(0, self.gui.selection_scroll_offset - event.y * 20)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                grid_cols = 4
                cell_width = WINDOW_WIDTH // grid_cols
                cell_height = 90
                for idx, pkmn in enumerate(self.all_pokemon):
                    col = idx % grid_cols
                    row = idx // grid_cols
                    cell_rect = pygame.Rect(col * cell_width + 10, 80 + row * cell_height - self.gui.selection_scroll_offset,
                                            cell_width - 20, cell_height - 10)
                    if cell_rect.collidepoint(mx, my):
                        if idx in self.selected_team_indices:
                            self.selected_team_indices.remove(idx)
                        else:
                            if len(self.selected_team_indices) < 6:
                                self.selected_team_indices.add(idx)

                if Game.selection_confirm_button and Game.selection_confirm_button.collidepoint(mx, my):
                    if len(self.selected_team_indices) == 0:
                        pass  # do nothing, must select at least 1
                    else:
                        self.player_team = [self.all_pokemon[i] for i in self.selected_team_indices]
                        self.selected_team_indices = set()
                        self.gui.selection_scroll_offset = 0
                        self.state = "MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
        return True

    def handle_active_select(self):
        self.gui.draw_active_selection(self.player_team)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                grid_cols = len(self.player_team)
                cell_width = WINDOW_WIDTH // grid_cols
                cell_height = 200
                for idx, pkmn in enumerate(self.player_team):
                    cell_rect = pygame.Rect(idx * cell_width + 10, 80, cell_width - 20, cell_height - 10)
                    if cell_rect.collidepoint(mx, my):
                        Game.active_selection_index = idx

                if Game.active_confirm_button and Game.active_confirm_button.collidepoint(mx, my):
                    self.player_pokemon = self.player_team[Game.active_selection_index]
                    # Distinguish if it was "Wild" or "Gym" (based on the last button pressed in the menu, if we track it).
                    # For simplicity, let's always do a "wild" encounter unless we code a separate path:
                    if self.state == "ACTIVE_SELECT":
                        # Start whichever battle is relevant:
                        # If we want a wild encounter:
                        if self.world_wild_pool:
                            self.start_world_wild_encounter()
                        else:
                            # Default wild pool
                            self.start_wild_encounter()
                    else:
                        # Or a Gym battle
                        self.start_gym_battle()

                    self.state = "BATTLE"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
        return True

    def start_wild_encounter(self):
        self.player_pokemon.heal()
        wild_choice = random.choice(self.default_wild_pool)
        self.opponent_pokemon = Pokemon(wild_choice)
        self.opponent_pokemon.heal()
        self.battle = Battle(self.player_pokemon, self.opponent_pokemon)
        self.selected_move_index = 0

    def start_world_wild_encounter(self):
        """
        Starts a wild encounter using the currently selected location's 'world_wild_pool' if set.
        """
        self.player_pokemon.heal()
        if not self.world_wild_pool:
            # fallback to default
            wild_choice = random.choice(self.default_wild_pool)
        else:
            wild_choice = random.choice(self.world_wild_pool)
        self.opponent_pokemon = Pokemon(wild_choice)
        self.opponent_pokemon.heal()
        self.battle = Battle(self.player_pokemon, self.opponent_pokemon)
        self.selected_move_index = 0

    def start_gym_battle(self):
        self.player_pokemon.heal()
        self.opponent_pokemon = random.choice(self.gym_leaders)
        self.opponent_pokemon.heal()
        self.battle = Battle(self.player_pokemon, self.opponent_pokemon, is_trainer_battle=True)
        self.selected_move_index = 0

    def handle_battle(self):
        self.gui.draw_battle_scene(
            self.player_pokemon,
            self.opponent_pokemon,
            self.battle.battle_log,
            self.player_pokemon.moves,
            self.selected_move_index
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_w):
                    self.selected_move_index = (self.selected_move_index - 1) % len(self.player_pokemon.moves)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    self.selected_move_index = (self.selected_move_index + 1) % len(self.player_pokemon.moves)
                elif event.key == pygame.K_RETURN:
                    opp_move_index = random.randint(0, len(self.opponent_pokemon.moves) - 1)
                    continue_battle = self.battle.next_turn(self.selected_move_index, opp_move_index)
                    self.selected_move_index = 0
                    if not continue_battle:
                        if self.player_pokemon.is_alive():
                            self.result_message = f"You won! {self.opponent_pokemon.name.capitalize()} fainted."
                            # If it was a wild Pokémon from either default or world pool, we can catch:
                            # is_trainer_battle is false => means wild
                            if not self.battle.is_trainer_battle:
                                self.state = "CATCH"
                                return True
                        else:
                            self.result_message = f"You lost! {self.player_pokemon.name.capitalize()} fainted."
                        self.create_particles()
                        Game.attack_effects = []
                        self.state = "RESULT"
            elif event.type == pygame.USEREVENT + 1:
                if hasattr(self.player_pokemon, "shake_offset"):
                    self.player_pokemon.shake_offset = 0
                if hasattr(self.opponent_pokemon, "shake_offset"):
                    self.opponent_pokemon.shake_offset = 0
        return True

    def handle_catch(self):
        self.screen.fill((230, 255, 230))
        prompt = "Attempt to Catch Wild " + self.opponent_pokemon.name.capitalize() + "?"
        prompt_surf = self.font_md.render(prompt, True, (0, 0, 0))
        self.screen.blit(prompt_surf, (WINDOW_WIDTH//2 - prompt_surf.get_width()//2, 150))

        catch_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, 250, 200, 50)
        cancel_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, 320, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), catch_rect)
        pygame.draw.rect(self.screen, (70, 130, 180), cancel_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), catch_rect, 2)
        pygame.draw.rect(self.screen, (0, 0, 0), cancel_rect, 2)

        catch_text = self.font_md.render("Catch", True, (255, 255, 255))
        cancel_text = self.font_md.render("Cancel", True, (255, 255, 255))
        self.screen.blit(catch_text, catch_text.get_rect(center=catch_rect.center))
        self.screen.blit(cancel_text, cancel_text.get_rect(center=cancel_rect.center))

        Game.catch_confirm_button = catch_rect

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if catch_rect.collidepoint(mx, my):
                    # Catch chance = 1 - (current_hp / max_hp)
                    catch_chance = 1 - (self.opponent_pokemon.current_hp / self.opponent_pokemon.max_hp)
                    if random.random() < catch_chance:
                        self.result_message = f"You caught {self.opponent_pokemon.name.capitalize()}!"
                        # Add to your Pokedex
                        Game.pokedex[self.opponent_pokemon.name] = {
                            "name": self.opponent_pokemon.name,
                            "hp": self.opponent_pokemon.max_hp,
                            "types": self.opponent_pokemon.types,
                            "sprite": self.opponent_pokemon.sprite
                        }
                        # Also optionally add to your team if < 6
                        if len(self.player_team) < 6:
                            self.player_team.append(self.opponent_pokemon)
                    else:
                        self.result_message = f"{self.opponent_pokemon.name.capitalize()} escaped!"
                    self.create_particles()
                    Game.attack_effects = []
                    self.state = "RESULT"
                elif cancel_rect.collidepoint(mx, my):
                    self.state = "MENU"
        return True

    def handle_result(self):
        self.update_particles()
        self.gui.draw_result_screen(self.result_message)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if "won" in self.result_message.lower() or "caught" in self.result_message.lower():
                    if hasattr(Game, "play_again_button") and Game.play_again_button and Game.play_again_button.collidepoint(mx, my):
                        # Replay with a new wild encounter
                        if self.world_wild_pool:
                            self.start_world_wild_encounter()
                        else:
                            self.start_wild_encounter()
                        self.state = "BATTLE"
                    elif Game.result_back_button and Game.result_back_button.collidepoint(mx, my):
                        self.state = "MENU"
                        self.battle.battle_log.clear()
                        Game.result_particles = []
                else:
                    if Game.result_back_button and Game.result_back_button.collidepoint(mx, my):
                        self.state = "MENU"
                        self.battle.battle_log.clear()
                        Game.result_particles = []
            elif event.type == pygame.KEYDOWN:
                self.state = "MENU"
                self.battle.battle_log.clear()
                Game.result_particles = []
        return True

    def handle_pokedex(self):
        self.gui.draw_pokedex(Game.pokedex, self.player_team)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                # Return to menu
                self.state = "MENU"
        return True

    def handle_evolution(self):
        self.screen.fill((240, 240, 255))
        if not self.player_team:
            draw_text(self.screen, "No Pokémon in your team to show evolution.", (50, 50), self.font_sm, (0, 0, 0))
        else:
            draw_text(self.screen, f"Evolution Chain for {self.player_team[0].name.capitalize()}:", (50, 50), self.font_md, (0, 0, 0))
            evo_chain = self.player_team[0].get_evolution_chain()
            if evo_chain:
                species_names = []
                def traverse(chain_node):
                    if chain_node:
                        species_names.append(chain_node.get("species", {}).get("name", "Unknown").capitalize())
                        for evo in chain_node.get("evolves_to", []):
                            traverse(evo)
                traverse(evo_chain.get("chain", {}))
                y = 120
                for name in species_names:
                    draw_text(self.screen, name, (50, y), self.font_sm, (0, 0, 0))
                    y += 30
            else:
                draw_text(self.screen, "No Evolution data available.", (50, 120), self.font_sm, (0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.state = "MENU"
        return True

    def handle_item(self):
        self.gui.draw_item_screen(self.demo_item)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.state = "MENU"
        return True

    # ------------------------------------------------
    #   NEW STATES for "Explore Worlds"
    # ------------------------------------------------
    def handle_region_select(self):
        """
        Presents a list of all fetched regions from the PokeAPI.
        Clicking one sets self.selected_region and transitions to LOCATION_SELECT.
        """
        self.screen.fill((255, 250, 240))
        title_surf = self.font_md.render("Select a Region to Explore", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 20))

        # We can just draw them in a column:
        mx, my = pygame.mouse.get_pos()
        y_pos = 100
        region_rects = []

        for region in self.available_regions:
            region_name = region["name"]
            rect = pygame.Rect(100, y_pos, 200, 30)
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            pygame.draw.rect(self.screen, (10, 10, 10), rect, 2)
            txt_surf = self.font_sm.render(region_name.capitalize(), True, (0, 0, 0))
            self.screen.blit(txt_surf, (rect.x + 10, rect.y + 5))
            region_rects.append((rect, region_name))
            y_pos += 40

        # Back button
        back_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 60, 200, 40)
        pygame.draw.rect(self.screen, (70, 130, 180), back_rect)
        pygame.draw.rect(self.screen, (10, 10, 10), back_rect, 2)
        back_txt = self.font_sm.render("Back to Main Menu", True, (255, 255, 255))
        self.screen.blit(back_txt, back_txt.get_rect(center=back_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    self.state = "MENU"
                else:
                    for rect, r_name in region_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_region = r_name
                            self.fetch_locations_for_region(r_name)
                            self.state = "LOCATION_SELECT"
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
        return True

    def handle_location_select(self):
        """
        Lists all the region’s locations. Selecting one sets self.selected_location
        and calls build_wild_pool_from_location to create a dynamic pool for wild battles.
        Then returns to main menu after selection.
        """
        self.screen.fill((255, 255, 240))
        if not self.selected_region:
            draw_text(self.screen, "No region selected. Press ESC to return.", (50, 50), self.font_sm, (10, 10, 10))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
            return True

        region_text = f"Locations in {self.selected_region.capitalize()}"
        title_surf = self.font_md.render(region_text, True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width() // 2, 20))

        mx, my = pygame.mouse.get_pos()
        y_pos = 100
        location_rects = []

        for location in self.available_locations:
            loc_name = location["name"]
            rect = pygame.Rect(100, y_pos, 250, 30)
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            pygame.draw.rect(self.screen, (10, 10, 10), rect, 2)
            txt_surf = self.font_sm.render(loc_name.capitalize().replace("-", " "), True, (0, 0, 0))
            self.screen.blit(txt_surf, (rect.x + 10, rect.y + 5))
            location_rects.append((rect, loc_name))
            y_pos += 35

        # Back to main menu:
        back_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 60, 200, 40)
        pygame.draw.rect(self.screen, (70, 130, 180), back_rect)
        pygame.draw.rect(self.screen, (10, 10, 10), back_rect, 2)
        back_txt = self.font_sm.render("Back to Main Menu", True, (255, 255, 255))
        self.screen.blit(back_txt, back_txt.get_rect(center=back_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    self.state = "MENU"
                else:
                    for rect, name in location_rects:
                        if rect.collidepoint(event.pos):
                            self.selected_location = name
                            # Build the new wild pool:
                            self.build_wild_pool_from_location(name)
                            self.state = "MENU"
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MENU"
        return True


# ---------------------- ENTRY POINT ----------------------
if __name__ == "__main__":
    # (Optional) Print filler or do something before launching
    game = Game()
    game.run()

    # After closing, you could demo the extended API usage if desired:
    # demo_api_extensions()
