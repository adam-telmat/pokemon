#!/usr/bin/env python3
from __future__ import annotations
import logging
logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

import pygame
import random
import math
import requests
from io import BytesIO
from functools import lru_cache
import time
import os
import json

### GLOBAL SETTINGS
DEBUG_MODE = True

# ---------------------- GLOBAL CONFIGURATION ----------------------
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30
DEFAULT_LEVEL = 50
EXP_CURVE = [0, 100, 250, 500, 900, 1400, 2000, 2700, 3500, 4400, 5400]
POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

session = requests.Session()

# ---------------------- HELPER FUNCTION ----------------------
def fit_text(font, text, max_width):
    """Ensures that the given text fits within max_width by appending an ellipsis if needed."""
    if font.size(text)[0] <= max_width:
        return text
    else:
        while font.size(text + "...")[0] > max_width and len(text) > 0:
            text = text[:-1]
        return text + "..."

# ---------------------- GAME PERSISTENCE ----------------------
LEADERBOARD_FILE = "leaderboard.json"
player_name: str | None = None

def load_leaderboard() -> list:
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            try:
                data = json.load(f)
                return data
            except Exception as e:
                logger.error("Error loading leaderboard: " + str(e))
                return []
    return []

def save_leaderboard(leaderboard: list):
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(leaderboard, f)
    except Exception as e:
        logger.error("Error saving leaderboard: " + str(e))

# ---------------------- CONSTANTS ----------------------
TYPE_MATCHUPS = {
    ("fire", "grass"): 2.0,
    ("grass", "water"): 2.0,
    ("water", "fire"): 2.0,
    ("electric", "water"): 2.0,
    ("ground", "electric"): 2.0,
    ("rock", "fire"): 2.0
}

# ---------------------- FULL 24+ POKÉMON DATABASE ----------------------
SPECIES_DATA = {
    "pikachu": {"name": "Pikachu", "types": ["electric"], "level": 50, "max_hp": 120,
                "attack": 55, "defense": 40, "special_attack": 50, "special_defense": 50,
                "speed": 90, "moves": ["thunder-shock", "quick-attack", "iron-tail", "electro-ball"]},
    "charmander": {"name": "Charmander", "types": ["fire"], "level": 50, "max_hp": 118,
                   "attack": 52, "defense": 43, "special_attack": 60, "special_defense": 50,
                   "speed": 65, "moves": ["scratch", "ember", "growl", "flamethrower"]},
    "bulbasaur": {"name": "Bulbasaur", "types": ["grass"], "level": 50, "max_hp": 125,
                  "attack": 49, "defense": 49, "special_attack": 65, "special_defense": 65,
                  "speed": 45, "moves": ["tackle", "vine-whip", "razor-leaf", "growl"]},
    "squirtle": {"name": "Squirtle", "types": ["water"], "level": 50, "max_hp": 127,
                 "attack": 48, "defense": 65, "special_attack": 50, "special_defense": 64,
                 "speed": 43, "moves": ["tackle", "water-gun", "bubble", "bite"]},
    "onix": {"name": "Onix", "types": ["rock", "ground"], "level": 50, "max_hp": 130,
             "attack": 45, "defense": 160, "special_attack": 30, "special_defense": 45,
             "speed": 70, "moves": ["tackle", "rock-throw", "harden", "earthquake"]},
    "staryu": {"name": "Staryu", "types": ["water"], "level": 50, "max_hp": 115,
               "attack": 45, "defense": 55, "special_attack": 70, "special_defense": 55,
               "speed": 85, "moves": ["tackle", "water-gun", "swift", "recover"]},
    "butterfree": {"name": "Butterfree", "types": ["bug", "flying"], "level": 50, "max_hp": 130,
                   "attack": 45, "defense": 50, "special_attack": 80, "special_defense": 80,
                   "speed": 70, "moves": ["gust", "confusion", "psybeam", "silver-wind"]},
    "beedrill": {"name": "Beedrill", "types": ["bug", "poison"], "level": 50, "max_hp": 125,
                 "attack": 80, "defense": 40, "special_attack": 45, "special_defense": 80,
                 "speed": 75, "moves": ["fury-attack", "twineedle", "poison-sting", "rage"]},
    "pidgey": {"name": "Pidgey", "types": ["normal", "flying"], "level": 50, "max_hp": 110,
               "attack": 45, "defense": 40, "special_attack": 35, "special_defense": 35,
               "speed": 56, "moves": ["tackle", "gust", "quick-attack", "sand-attack"]},
    "rattata": {"name": "Rattata", "types": ["normal"], "level": 50, "max_hp": 105,
                "attack": 56, "defense": 35, "special_attack": 25, "special_defense": 35,
                "speed": 72, "moves": ["tackle", "quick-attack", "bite", "focus-energy"]},
    "spearow": {"name": "Spearow", "types": ["normal", "flying"], "level": 50, "max_hp": 105,
                "attack": 60, "defense": 30, "special_attack": 31, "special_defense": 31,
                "speed": 70, "moves": ["peck", "growl", "leer", "fury-attack"]},
    "ekans": {"name": "Ekans", "types": ["poison"], "level": 50, "max_hp": 115,
              "attack": 60, "defense": 44, "special_attack": 40, "special_defense": 54,
              "speed": 55, "moves": ["wrap", "poison-sting", "bite", "glare"]},
    "sandshrew": {"name": "Sandshrew", "types": ["ground"], "level": 50, "max_hp": 125,
                  "attack": 75, "defense": 85, "special_attack": 20, "special_defense": 30,
                  "speed": 40, "moves": ["scratch", "defense-curl", "sand-attack", "poison-sting"]},
    "clefairy": {"name": "Clefairy", "types": ["fairy"], "level": 50, "max_hp": 130,
                 "attack": 45, "defense": 48, "special_attack": 60, "special_defense": 65,
                 "speed": 35, "moves": ["pound", "sing", "doubleslap", "growl"]},
    "vulpix": {"name": "Vulpix", "types": ["fire"], "level": 50, "max_hp": 115,
               "attack": 41, "defense": 40, "special_attack": 50, "special_defense": 65,
               "speed": 65, "moves": ["ember", "tail-whip", "quick-attack", "flamethrower"]},
    "jigglypuff": {"name": "Jigglypuff", "types": ["normal", "fairy"], "level": 50, "max_hp": 160,
                   "attack": 45, "defense": 20, "special_attack": 45, "special_defense": 25,
                   "speed": 20, "moves": ["pound", "sing", "defense-curl", "doubleslap"]},
    "zubat": {"name": "Zubat", "types": ["poison", "flying"], "level": 50, "max_hp": 105,
              "attack": 45, "defense": 35, "special_attack": 30, "special_defense": 40,
              "speed": 55, "moves": ["leech-life", "supersonic", "bite", "wing-attack"]},
    "oddish": {"name": "Oddish", "types": ["grass", "poison"], "level": 50, "max_hp": 120,
              "attack": 50, "defense": 55, "special_attack": 75, "special_defense": 65,
              "speed": 30, "moves": ["absorb", "poison-powder", "acid", "sleep-powder"]},
    "paras": {"name": "Paras", "types": ["bug", "grass"], "level": 50, "max_hp": 115,
              "attack": 70, "defense": 55, "special_attack": 45, "special_defense": 55,
              "speed": 25, "moves": ["scratch", "stun-spore", "leech-life", "spore"]},
    "venonat": {"name": "Venonat", "types": ["bug", "poison"], "level": 50, "max_hp": 125,
                "attack": 55, "defense": 50, "special_attack": 40, "special_defense": 55,
                "speed": 45, "moves": ["tackle", "disable", "confusion", "poison-powder"]},
    "diglett": {"name": "Diglett", "types": ["ground"], "level": 50, "max_hp": 90,
                "attack": 55, "defense": 25, "special_attack": 35, "special_defense": 45,
                "speed": 95, "moves": ["scratch", "sand-attack", "growl", "dig"]},
    "meowth": {"name": "Meowth", "types": ["normal"], "level": 50, "max_hp": 110,
               "attack": 45, "defense": 35, "special_attack": 40, "special_defense": 40,
               "speed": 90, "moves": ["scratch", "bite", "pay-day", "growl"]},
    "psyduck": {"name": "Psyduck", "types": ["water"], "level": 50, "max_hp": 120,
                "attack": 52, "defense": 48, "special_attack": 65, "special_defense": 50,
                "speed": 55, "moves": ["scratch", "water-gun", "confusion", "disable"]},
    "mankey": {"name": "Mankey", "types": ["fighting"], "level": 50, "max_hp": 115,
               "attack": 80, "defense": 35, "special_attack": 35, "special_defense": 45,
               "speed": 70, "moves": ["scratch", "karate-chop", "low-kick", "focus-energy"]},
    "growlithe": {"name": "Growlithe", "types": ["fire"], "level": 50, "max_hp": 115,
                  "attack": 70, "defense": 45, "special_attack": 60, "special_defense": 50,
                  "speed": 60, "moves": ["bite", "ember", "roar", "flamethrower"]},
    "poliwag": {"name": "Poliwag", "types": ["water"], "level": 50, "max_hp": 105,
                "attack": 50, "defense": 40, "special_attack": 55, "special_defense": 45,
                "speed": 90, "moves": ["bubble", "water-gun", "hypnosis", "double-slap"]},
    "abra": {"name": "Abra", "types": ["psychic"], "level": 50, "max_hp": 100,
             "attack": 30, "defense": 30, "special_attack": 90, "special_defense": 55,
             "speed": 105, "moves": ["teleport", "psycho-cut", "confusion", "disable"]},
    "machop": {"name": "Machop", "types": ["fighting"], "level": 50, "max_hp": 115,
               "attack": 80, "defense": 70, "special_attack": 35, "special_defense": 45,
               "speed": 55, "moves": ["karate-chop", "low-kick", "fury-swipes", "focus-energy"]},
    "geodude": {"name": "Geodude", "types": ["rock", "ground"], "level": 50, "max_hp": 120,
                "attack": 80, "defense": 100, "special_attack": 30, "special_defense": 30,
                "speed": 20, "moves": ["tackle", "rock-throw", "selfdestruct", "earthquake"]},
    "ponyta": {"name": "Ponyta", "types": ["fire"], "level": 50, "max_hp": 115,
               "attack": 75, "defense": 55, "special_attack": 65, "special_defense": 60,
               "speed": 90, "moves": ["tackle", "ember", "flame-wheel", "stomp"]}
}

# ---------------------- MOVES DATA (fallback if needed) ----------------------
MOVES_DATA = {
    "thunder-shock": {"name": "thunder-shock", "power": 40, "accuracy": 100, "type": "electric", "damage_class": "special"},
    "quick-attack":  {"name": "quick-attack",  "power": 40, "accuracy": 100, "type": "normal", "damage_class": "physical"},
    "iron-tail":     {"name": "iron-tail",     "power": 100, "accuracy": 75,  "type": "steel", "damage_class": "physical"},
    "electro-ball":  {"name": "electro-ball",  "power": 60, "accuracy": 100, "type": "electric", "damage_class": "special"},
    "scratch":       {"name": "scratch",       "power": 40, "accuracy": 100, "type": "normal", "damage_class": "physical"},
    "ember":         {"name": "ember",         "power": 40, "accuracy": 100, "type": "fire", "damage_class": "special"},
    "growl":         {"name": "growl",         "power": 0,  "accuracy": 100, "type": "normal", "damage_class": "status"},
    "flamethrower":  {"name": "flamethrower",  "power": 90, "accuracy": 100, "type": "fire", "damage_class": "special"},
    "tackle":        {"name": "tackle",        "power": 40, "accuracy": 100, "type": "normal", "damage_class": "physical"},
    "vine-whip":     {"name": "vine-whip",     "power": 45, "accuracy": 100, "type": "grass", "damage_class": "physical"},
    "razor-leaf":    {"name": "razor-leaf",    "power": 55, "accuracy": 95,  "type": "grass", "damage_class": "physical"},
    "water-gun":     {"name": "water-gun",     "power": 40, "accuracy": 100, "type": "water", "damage_class": "special"},
    "bubble":        {"name": "bubble",        "power": 40, "accuracy": 100, "type": "water", "damage_class": "special"},
    "bite":          {"name": "bite",          "power": 60, "accuracy": 100, "type": "dark", "damage_class": "physical"},
    "rock-throw":    {"name": "rock-throw",    "power": 50, "accuracy": 90,  "type": "rock", "damage_class": "physical"},
    "earthquake":    {"name": "earthquake",    "power": 100, "accuracy": 100, "type": "ground", "damage_class": "physical"}
}

# ---------------------- POKEAPI EXTENSIONS ----------------------
class PokeAPIExtensions:
    @staticmethod
    @lru_cache(maxsize=32)
    def get_all_locations():
        url = f"{POKEAPI_BASE_URL}location?limit=100"
        response = session.get(url)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
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

# ---------------------- PLAYER SETUP & LEADERBOARD ----------------------
class PlayerSetup:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont("Arial", 48)
        self.font_md = pygame.font.SysFont("Arial", 36)
        self.font_sm = pygame.font.SysFont("Arial", 24)
        self.input_text = ""
        self.leaderboard = load_leaderboard()

    def handle(self):
        global player_name
        self.screen.fill((200, 230, 255))
        title = "Enter Your Name"
        title_surf = self.font_big.render(title, True, (0, 0, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 50))
        input_prompt = "Name: " + self.input_text
        input_surf = self.font_md.render(input_prompt, True, (0, 0, 0))
        self.screen.blit(input_surf, (WINDOW_WIDTH//2 - input_surf.get_width()//2, 150))
        leaderboard_title = "Top 3 Players"
        lb_title_surf = self.font_sm.render(leaderboard_title, True, (0, 0, 0))
        self.screen.blit(lb_title_surf, (50, 250))
        sorted_lb = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)[:3]
        y = 280
        for entry in sorted_lb:
            line = f'{entry["name"]}: {entry["score"]}'
            line_surf = self.font_sm.render(line, True, (0, 0, 0))
            self.screen.blit(line_surf, (50, y))
            y += 30
        instructions = "Press ENTER to confirm or type a new name"
        instr_surf = self.font_sm.render(instructions, True, (0, 0, 0))
        self.screen.blit(instr_surf, (WINDOW_WIDTH//2 - instr_surf.get_width()//2, 400))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.input_text != "":
                        player_name = self.input_text
                        if not any(entry["name"] == player_name for entry in self.leaderboard):
                            self.leaderboard.append({"name": player_name, "score": 0})
                            save_leaderboard(self.leaderboard)
                        return True
                    else:
                        if player_name:
                            return True
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
        return None

class LeaderboardScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont("Arial", 48)
        self.font_md = pygame.font.SysFont("Arial", 36)
        self.font_sm = pygame.font.SysFont("Arial", 24)
        self.leaderboard = load_leaderboard()

    def handle(self):
        self.screen.fill((255, 255, 240))
        title = "Leaderboard"
        title_surf = self.font_big.render(title, True, (0, 0, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 50))
        sorted_lb = sorted(self.leaderboard, key=lambda x: x["score"], reverse=True)
        y = 150
        rank = 1
        for entry in sorted_lb[:10]:
            line = f"{rank}. {entry['name']} - {entry['score']}"
            line_surf = self.font_md.render(line, True, (0, 0, 0))
            self.screen.blit(line_surf, (WINDOW_WIDTH//2 - line_surf.get_width()//2, y))
            y += 50
            rank += 1
        instr = "Press ESC to return to Main Menu"
        instr_surf = self.font_sm.render(instr, True, (0, 0, 0))
        self.screen.blit(instr_surf, (WINDOW_WIDTH//2 - instr_surf.get_width()//2, WINDOW_HEIGHT - 80))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        return None

# ---------------------- GUI CLASS ----------------------
class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.font_lg = pygame.font.SysFont("Arial", 48)
        self.font_md = pygame.font.SysFont("Arial", 36)
        self.font_sm = pygame.font.SysFont("Arial", 20)
        self.small_font = pygame.font.SysFont("Arial", 16)
        self.bg_animation_offset = 0
        self.bg_animation_speed = 0.5
        self.team_hovered_index = None
        self.selection_scroll_offset = 0

    def draw_nav_icons(self):
        pause_rect = pygame.Rect(WINDOW_WIDTH - 60, 10, 50, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), pause_rect)
        pause_text = self.font_sm.render("Pause", True, (255, 255, 255))
        self.screen.blit(pause_text, pause_text.get_rect(center=pause_rect.center))
        return pause_rect

    def draw_gradient_background(self, start_color, end_color):
        for y in range(WINDOW_HEIGHT):
            ratio = y / WINDOW_HEIGHT
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (WINDOW_WIDTH, y))

    def draw_main_menu_buttons(self, button_labels: list):
        button_rects = []
        start_y = 140
        mx, my = pygame.mouse.get_pos()
        for i, label in enumerate(button_labels):
            rect = pygame.Rect(WINDOW_WIDTH // 2 - 120, start_y + i * 55, 240, 50)
            color = (50, 150, 220) if rect.collidepoint(mx, my) else (70, 170, 240)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, (20, 20, 20), rect, 2)
            text = fit_text(self.font_md, label, rect.width - 10)
            text_surf = self.font_md.render(text, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            button_rects.append((rect, label))
        return button_rects

    def draw_battle_scene(self, player: Pokemon, opponent: Pokemon, battle_log: list, move_menu: list = None, selected_index: int = 0):
        self.screen.fill((245, 245, 245))
        self.draw_battle_sprite(opponent, (int(WINDOW_WIDTH * 0.55), 100), flipped=True)
        self.draw_hp_bar(opponent, (int(WINDOW_WIDTH * 0.55 - 50), 70))
        self.draw_battle_sprite(player, (int(WINDOW_WIDTH * 0.1), 280))
        self.draw_hp_bar(player, (int(WINDOW_WIDTH * 0.1 - 50), 260))
        y_log = 420
        for line in reversed(battle_log[-4:] if battle_log else []):
            log_surf = self.font_sm.render(line, True, (10, 10, 10))
            log_rect = log_surf.get_rect(midright=(WINDOW_WIDTH - 50, y_log))
            self.screen.blit(log_surf, log_rect)
            y_log += 26
        if move_menu:
            self.draw_move_menu(move_menu, selected_index)
        self.draw_nav_icons()

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
                raise Exception("Sprite missing")
        except Exception:
            color = (150, 150, 250) if not flipped else (250, 150, 150)
            rect = pygame.Rect(pos[0], pos[1], 160, 160)
            pygame.draw.rect(self.screen, color, rect)
            name_surf = self.font_sm.render(pkmn.name.capitalize(), True, (0, 0, 0))
            self.screen.blit(name_surf, (pos[0], pos[1] - 20))

    def draw_hp_bar(self, pkmn: Pokemon, pos):
        max_bar_width = 250
        bar_height = 25
        ratio = pkmn.current_hp / pkmn.max_hp if pkmn.max_hp else 0
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

    def draw_attack_effects(self):
        for effect in Game.attack_effects:
            t = effect["progress"]
            start_x, start_y = effect["start"]
            end_x, end_y = effect["end"]
            if effect.get("effect_type") == "fire":
                size = 8 + int(4 * math.sin(math.pi * t * 10))
                points = [
                    (int(start_x + (end_x - start_x) * t), int(start_y + (end_y - start_y) * t - size)),
                    (int(start_x + (end_x - start_x) * t - size), int(start_y + (end_y - start_y) * t + size)),
                    (int(start_x + (end_x - start_x) * t + size), int(start_y + (end_y - start_y) * t + size))
                ]
                pygame.draw.polygon(self.screen, effect["color"], points)
            elif effect.get("effect_type") == "water":
                width = 10
                height = 14
                cx = int(start_x + (end_x - start_x) * t)
                cy = int(start_y + (end_y - start_y) * t)
                rect = pygame.Rect(cx - width//2, cy - height//2, width, height)
                pygame.draw.ellipse(self.screen, effect["color"], rect)
            elif effect.get("effect_type") == "electric":
                points = []
                num_points = 5
                for i in range(num_points):
                    xi = start_x + (end_x - start_x) * (i / (num_points - 1)) + random.randint(-5, 5)
                    yi = start_y + (end_y - start_y) * (i / (num_points - 1)) + random.randint(-5, 5)
                    points.append((int(xi), int(yi)))
                pygame.draw.lines(self.screen, effect["color"], False, points, 3)
            else:
                current_x = start_x + (end_x - start_x) * t
                current_y = start_y + (end_y - start_y) * t
                radius = 8 + int(4 * math.sin(math.pi * t * 10))
                pygame.draw.circle(self.screen, effect["color"], (int(current_x), int(current_y)), radius)
                pygame.draw.circle(self.screen, effect["color"], (int(current_x), int(current_y)), radius//2)

    def draw_result_screen(self, message: str):
        self.draw_gradient_background((220, 230, 255), (160, 190, 230))
        for particle in Game.result_particles:
            pygame.draw.circle(self.screen, particle["color"], (int(particle["x"]), int(particle["y"])), int(particle["radius"]))
        result_title = "You Won!" if "win" in message.lower() or "caught" in message.lower() else "You Lost!"
        title_surf = self.font_lg.render(result_title, True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)
        msg_surf = self.font_md.render(message, True, (10, 10, 0))
        msg_rect = msg_surf.get_rect(center=(WINDOW_WIDTH // 2, 220))
        self.screen.blit(msg_surf, msg_rect)
        if "win" in message.lower() or "caught" in message.lower():
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
        title_surf = self.font_lg.render("Your Pokédex", True, (10, 10, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width()//2, 20))
        y = 100
        for key, entry in pokedex_entries.items():
            sprite = entry.get("sprite")
            if sprite:
                self.screen.blit(sprite, (50, y))
            line = f"{entry['name'].capitalize()} - HP: {entry['hp']}, Types: {', '.join(entry['types'])}"
            text_surf = self.font_sm.render(line, True, (10, 10, 0))
            self.screen.blit(text_surf, (140, y + 20))
            y += 100
        team_title = self.font_md.render("Your Team:", True, (10, 10, 0))
        self.screen.blit(team_title, (50, WINDOW_HEIGHT - 120))
        x = 200
        for pkmn in team_pokemon:
            if pkmn.sprite:
                self.screen.blit(pkmn.sprite, (x, WINDOW_HEIGHT - 140))
            x += 90

    def draw_evolution_chain(self, chain_data, font):
        self.screen.fill((240, 240, 255))
        title = "Evolution Chain"
        title_surf = font.render(title, True, (10, 10, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width()//2, 20))
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
            text_surf = self.font_sm.render(line, True, (10, 10, 0))
            self.screen.blit(text_surf, (50, y))
            y += 30

    def draw_item_screen(self, item: Item):
        self.screen.fill((250, 240, 230))
        title_surf = self.font_lg.render("Item Usage", True, (10, 10, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width()//2, 20))
        if item:
            self.screen.blit(item.sprite, (50, 100))
            draw_text(self.screen, f"{item.name.capitalize()}", (120, 110), self.font_md, (10, 10, 0))
        else:
            draw_text(self.screen, "No item data available.", (50, 100), self.font_md, (10, 10, 0))
        draw_text(self.screen, "Press any key to return to the main menu...", (50, 200), self.font_sm, (10, 10, 0))

    def draw_team_selection(self, available_pokemon: list, selected_indices: set):
        self.screen.fill((220, 240, 255))
        title_surf = self.font_lg.render("Select Your 6 Pokémon", True, (10, 10, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width()//2, 10))
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
            cell_rect = pygame.Rect(col * cell_width + 10, grid_y + row * cell_height - self.selection_scroll_offset,
                                      cell_width - 20, cell_height - 10)
            if cell_rect.collidepoint(mx, my):
                self.team_hovered_index = idx
            if idx in selected_indices:
                pygame.draw.rect(self.screen, (144, 238, 144), cell_rect)
            else:
                pygame.draw.rect(self.screen, (245, 245, 245), cell_rect)
            pygame.draw.rect(self.screen, (10, 10, 0), cell_rect, 2)
            if pkmn.sprite:
                self.screen.blit(pkmn.sprite, (x, y))
            name_text = self.font_sm.render(pkmn.name.capitalize(), True, (10, 10, 0))
            self.screen.blit(name_text, (x, y + 70))
        # Draw a Back button for navigation
        back_rect = pygame.Rect(10, WINDOW_HEIGHT - 60, 120, 40)
        pygame.draw.rect(self.screen, (200, 100, 100), back_rect)
        back_text = self.font_sm.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=back_rect.center))
        if 1 <= len(selected_indices) <= 6:
            btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 70, 200, 50)
            pygame.draw.rect(self.screen, (70, 130, 180), btn_rect)
            pygame.draw.rect(self.screen, (10, 10, 0), btn_rect, 2)
            btn_text = self.font_md.render("Confirm Selection", True, (255, 255, 255))
            btn_text_rect = btn_text.get_rect(center=btn_rect.center)
            self.screen.blit(btn_text, btn_text_rect)
            Game.selection_confirm_button = btn_rect
        else:
            Game.selection_confirm_button = None

    def draw_active_selection(self, team: list):
        if not team:
            logger.error("Team order is empty in draw_active_selection.")
            return
        self.screen.fill((240, 255, 240))
        title = "Order Your Team"
        title_surf = self.font_lg.render(title, True, (10, 10, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 10))
        instructions = self.font_sm.render("Use LEFT/RIGHT to reorder; press ENTER or click Confirm Order", True, (0, 0, 0))
        self.screen.blit(instructions, (WINDOW_WIDTH//2 - instructions.get_width()//2, 60))
        grid_cols = len(team)
        cell_width = WINDOW_WIDTH // grid_cols
        cell_height = 200
        for idx, pkmn in enumerate(team):
            x = idx * cell_width + 20
            y = 80
            cell_rect = pygame.Rect(idx * cell_width + 10, 80, cell_width - 20, cell_height - 10)
            pygame.draw.rect(self.screen, (245, 245, 245), cell_rect)
            pygame.draw.rect(self.screen, (10, 10, 0), cell_rect, 2)
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
                info_surf = self.font_sm.render(line, True, (10, 10, 0))
                self.screen.blit(info_surf, (x, dy))
                dy += 20
            if idx == Game.active_selection_index:
                pointer_x = x + (cell_width - 20) // 2
                pointer_y = 70
                point_list = [(pointer_x, pointer_y), (pointer_x - 10, pointer_y + 10), (pointer_x + 10, pointer_y + 10)]
                pygame.draw.polygon(self.screen, (255, 0, 0), point_list)
        btn_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 70, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), btn_rect)
        pygame.draw.rect(self.screen, (10, 10, 0), btn_rect, 2)
        btn_text = self.font_md.render("Confirm Order", True, (255, 255, 255))
        btn_text_rect = btn_text.get_rect(center=btn_rect.center)
        self.screen.blit(btn_text, btn_text_rect)
        Game.active_confirm_button = btn_rect

# ---------------------- POKÉMON CLASS ----------------------
class Pokemon:
    def __init__(self, name: str, level=DEFAULT_LEVEL):
        self.name = name.lower()
        self.level = level
        self.exp = 0
        self.status = None
        self.shake_offset = 0
        if not self.load_from_api():
            fallback = SPECIES_DATA.get(self.name)
            if fallback:
                self.load_fallback_data(fallback)
            else:
                raise Exception(f"Unable to load data for {name}")
        self.sprite = self.load_sprite_image()
        self.debug("Initialized Pokémon.")

    def debug(self, message):
        print(f"[DEBUG][{self.name.capitalize()}]: {message}")
        logger.debug(f"[DEBUG][{self.name.capitalize()}]: {message}")

    def load_fallback_data(self, data_dict):
        self.debug("Using fallback data.")
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
        self.debug("Fallback data loaded.")

    def load_from_api(self) -> bool:
        try:
            url = f"{POKEAPI_BASE_URL}pokemon/{self.name}"
            self.debug(f"Fetching API data from {url}")
            response = session.get(url)
            if response.status_code != 200:
                self.debug("API call failed.")
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
            self.debug("API data loaded successfully.")
            return True
        except Exception as e:
            self.debug(f"Exception during API load: {e}")
            return False

    def load_sprite_image(self):
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
            self.debug(f"Error loading sprite: {e}")
            placeholder = pygame.Surface((80, 80))
            placeholder.fill((200, 200, 200))
            return placeholder

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def take_damage(self, damage: int):
        if self.status == "burn":
            damage = int(damage * 0.5)
        actual = max(1, damage)
        self.current_hp = max(0, self.current_hp - actual)
        self.debug(f"Took {actual} damage. Remaining HP: {self.current_hp}.")

    def heal(self):
        self.current_hp = self.max_hp
        self.status = None
        self.debug("Healed to full HP.")

    def get_evolution_chain(self):
        try:
            species_url = f"{POKEAPI_BASE_URL}pokemon-species/{self.name}/"
            response = session.get(species_url)
            if response.status_code != 200:
                self.debug("Failed to load species data for evolution chain.")
                return None
            species_data = response.json()
            evolution_url = species_data.get("evolution_chain", {}).get("url")
            if evolution_url:
                evo_response = session.get(evolution_url)
                if evo_response.status_code == 200:
                    self.debug("Evolution chain data loaded.")
                    return evo_response.json()
            return None
        except Exception as e:
            self.debug(f"Error fetching evolution chain: {e}")
            return None

    def gain_exp(self, amount: int):
        self.exp += amount
        self.debug(f"Gained {amount} EXP; total EXP is now {self.exp}.")
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
        self.debug(f"Leveled up to {self.level}!")

    def display_stats(self):
        stats = (f"{self.name.capitalize()} | LV: {self.level} | HP: {self.current_hp}/{self.max_hp} | "
                 f"ATK: {self.attack} | DEF: {self.defense} | Sp. Atk: {self.special_attack} | "
                 f"Sp. Def: {self.special_defense} | SPD: {self.speed}")
        print(stats)

# ---------------------- BATTLE CLASS ----------------------
class Battle:
    def __init__(self, pkmn1: Pokemon, pkmn2: Pokemon, is_trainer_battle: bool = False):
        self.p1 = pkmn1
        self.p2 = pkmn2
        self.turn = 1
        self.battle_log = []
        self.is_trainer_battle = is_trainer_battle

    def log(self, message: str):
        self.battle_log.append(message)
        print(f"[BATTLE] {message}")

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
        if random.randint(1, 100) <= move["accuracy"]:
            dmg = self.calculate_damage(attacker, defender, move)
            defender.take_damage(dmg)
            self.log(f"It dealt {dmg} damage to {defender.name.capitalize()}!")
            attacker.shake_offset = 5
            pygame.time.set_timer(pygame.USEREVENT + 1, 300)
            effect_type = move["type"]
            effect_color = (255, 215, 0) if move["name"] == "electro-ball" else ((255, 69, 0) if move["name"] in ["ember", "flamethrower"] else random.choice([(30,144,255), (138,43,226)]))
            Game.create_attack_effect(attacker, defender, effect_color, effect_type)
        else:
            self.log(f"{attacker.name.capitalize()}'s attack missed!")

    def next_turn(self, p1_move_index: int, p2_move_index: int) -> bool:
        current_time = pygame.time.get_ticks()
        if current_time - Game.last_attack_time < 2000:
            return True
        Game.last_attack_time = current_time
        if self.p1.speed >= self.p2.speed:
            self.do_move(self.p1, self.p2, self.p1.moves[p1_move_index])
            if not self.p2.is_alive():
                self.log(f"{self.p2.name.capitalize()} fainted!")
                bonus = (self.p2.attack + self.p2.defense + self.p2.special_attack + self.p2.special_defense + self.p2.speed) // 5
                Game.score += 20 + bonus
                if not self.is_trainer_battle:
                    self.p1.gain_exp(100)
                return False
            self.do_move(self.p2, self.p1, self.p2.moves[p2_move_index])
            if not self.p1.is_alive():
                self.log(f"{self.p1.name.capitalize()} fainted! Auto-switching...")
                return False
        else:
            self.do_move(self.p2, self.p1, self.p2.moves[p2_move_index])
            if not self.p1.is_alive():
                self.log(f"{self.p1.name.capitalize()} fainted! Auto-switching...")
                return False
            self.do_move(self.p1, self.p2, self.p1.moves[p1_move_index])
            if not self.p2.is_alive():
                self.log(f"{self.p2.name.capitalize()} fainted!")
                bonus = (self.p2.attack + self.p2.defense + self.p2.special_attack + self.p2.special_defense + self.p2.speed) // 5
                Game.score += 20 + bonus
                if not self.is_trainer_battle:
                    self.p1.gain_exp(100)
                return False
        self.turn += 1
        return True

# ---------------------- EVOLUTION VIEWER CLASS ----------------------
class EvolutionViewer:
    def __init__(self, pokemon: Pokemon):
        self.pokemon = pokemon
        self.chain_data = pokemon.get_evolution_chain()
    
    def render_chain(self, surface, font):
        self.screen = surface
        if not self.chain_data:
            self.screen.blit(font.render("No evolution chain data available.", True, (0, 0, 0)), (50, 50))
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
        self.screen.blit(font.render("Evolution Chain:", True, (0, 0, 0)), (50, y))
        y += 40
        for name in species_names:
            self.screen.blit(font.render(name, True, (0, 0, 0)), (50, y))
            y += 30

# ---------------------- ITEM CLASS ----------------------
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
            print(f"[ITEM ERROR] {e}")
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
            print(f"[ITEM SPRITE ERROR] {e}")
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((220, 220, 220))
            return placeholder

# ---------------------- GAME CLASS ----------------------
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
    pokedex = {}  # Captured Pokémon
    score = 0

    @staticmethod
    def create_attack_effect(attacker, defender, color, effect_type):
        start = (int(WINDOW_WIDTH * 0.1 + 80), int(280 + 40))
        end = (int(WINDOW_WIDTH * 0.55 + 80), int(100 + 40))
        effect = {
            "start": start,
            "end": end,
            "progress": 0,
            "color": color,
            "effect_type": effect_type
        }
        Game.attack_effects.append(effect)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pokémon Adventure")
        self.clock = pygame.time.Clock()
        self.gui = GUI(self.screen)
        self.font_lg = pygame.font.SysFont("Arial", 48)
        self.font_md = pygame.font.SysFont("Arial", 36)
        self.font_sm = pygame.font.SysFont("Arial", 24)
        self.state = "LOADING"
        self.pause_already = False
        self.previous_state = None
        self.loading_step = 0
        self.load_progress = 0
        self.player_pokemon = None
        self.opponent_pokemon = None
        self.battle = None
        self.selected_move_index = 0
        self.result_message = ""
        self.player_team = []
        self.gym_leaders = [Pokemon(name) for name in ["onix", "staryu"]]
        self.default_wild_pool = list(SPECIES_DATA.keys())
        self.demo_item = None
        self.all_pokemon = None
        self.selected_team_indices = set()
        self.api_locations = []
        self.selected_overworlds = []
        self.current_overworld_index = 0
        self.current_wild_pool = []
        self.default_escape_time = 500
        self.trainer_sprite = self.load_trainer_image()
        self.trainer_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
        self.trainer_speed = 5
        self.adv_wilds = []
        self.adv_obstacles = []
        self.advanced_captured = []
        self.advanced_overworlds_completed = 0
        self.team_order = []
        self.generate_triangle_labyrinth_overworld()
        logger.debug("[GAME INIT] Game initialized successfully.")
        self.leaderboard = load_leaderboard()
        self.player_setup = PlayerSetup(self.screen)

    def load_trainer_image(self):
        url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/trainers/ash.png"
        try:
            response = session.get(url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                sprite = pygame.image.load(image_data).convert_alpha()
                sprite = pygame.transform.scale(sprite, (40, 40))
                logger.debug("[TRAINER] Trainer image loaded from API.")
                return sprite
        except Exception as e:
            logger.error(f"[TRAINER ERROR] {e}")
        sprite = pygame.Surface((40, 40))
        sprite.fill((255, 0, 0))
        return sprite

    def generate_triangle_labyrinth_overworld(self):
        logger.debug("Advanced Mode: Generating triangle labyrinth overworld.")
        self.trainer_pos = [WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT - 100]
        self.adv_wilds = []
        available_choices = list(set(self.current_wild_pool) - set([p.name for p in self.advanced_captured]))
        if len(available_choices) < 2:
            available_choices = list(set(self.default_wild_pool) - set([p.name for p in self.advanced_captured]))
            if len(available_choices) < 2:
                available_choices = self.default_wild_pool
        wild_choices = random.sample(available_choices, 2)
        wild1 = Pokemon(wild_choices[0])
        wild2 = Pokemon(wild_choices[1])
        self.adv_wilds.append({"pokemon": wild1, "pos": [50, 50], "captured": False, "escape_timer": self.default_escape_time})
        self.adv_wilds.append({"pokemon": wild2, "pos": [WINDOW_WIDTH - 90, 50], "captured": False, "escape_timer": self.default_escape_time})
        self.adv_obstacles = []
        num_obs = random.randint(10, 15)
        attempts = 0
        while len(self.adv_obstacles) < num_obs and attempts < 50:
            w = random.randint(20, 40)
            h = random.randint(20, 40)
            x = random.randint(0, WINDOW_WIDTH - w)
            y = random.randint(100, WINDOW_HEIGHT - 200)
            new_obs = pygame.Rect(x, y, w, h)
            corridor1 = pygame.Rect(WINDOW_WIDTH//2 - 10, WINDOW_HEIGHT - 100, 20, 150)
            corridor2 = pygame.Rect(WINDOW_WIDTH//2 - 10, 50, 20, 150)
            if new_obs.colliderect(corridor1) or new_obs.colliderect(corridor2):
                attempts += 1
                continue
            self.adv_obstacles.append(new_obs)
            attempts += 1
        logger.debug(f"[ADV MODE] Triangle labyrinth generated with {len(self.adv_obstacles)} obstacles.")

    def load_game_data(self):
        logger.debug(f"[LOAD DATA] Step: {self.loading_step}")
        # Fast start (0->10%), slow middle (10->90%), fast finish (90->100%)
        if self.loading_step == 0:
            time.sleep(0.1)
            self.loading_step += 1
            self.load_progress = 10
            return
        if self.loading_step == 1:
            time.sleep(0.5)
            self.loading_step += 1
            self.load_progress = 50
            return
        if self.loading_step == 2:
            time.sleep(0.5)
            self.loading_step += 1
            self.load_progress = 90
            return
        if self.loading_step == 3:
            time.sleep(0.1)
            self.loading_step += 1
            self.all_pokemon = [Pokemon(name) for name in SPECIES_DATA.keys()]
            self.demo_item = Item(1)
            self.selected_team_indices = set()
            self.load_progress = 100
            return

    def update_attack_effects(self):
        for effect in Game.attack_effects:
            effect["progress"] += 0.03
        Game.attack_effects[:] = [e for e in Game.attack_effects if e["progress"] < 1]

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
                "color": random.choice([(255, 69, 0), (255, 215, 0), (30, 144, 255)])
            })

    # ------------------ LOADING ------------------
    def handle_loading(self):
        self.screen.fill((0, 0, 0))
        loading_text = self.font_md.render("Loading game data...", True, (255, 255, 255))
        self.screen.blit(loading_text, (WINDOW_WIDTH//2 - loading_text.get_width()//2, WINDOW_HEIGHT//2 - 40))
        bar_width = 400
        bar_height = 30
        progress_ratio = self.load_progress / 100.0
        pygame.draw.rect(self.screen, (100, 100, 100), (WINDOW_WIDTH//2 - bar_width//2, WINDOW_HEIGHT//2, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (WINDOW_WIDTH//2 - bar_width//2, WINDOW_HEIGHT//2, int(bar_width * progress_ratio), bar_height))
        self.load_game_data()
        if self.load_progress >= 100:
            # Ensure the 100% bar is visible for a moment
            pygame.display.flip()
            time.sleep(0.5)
            self.state = "PLAYER_SETUP"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def handle_pause(self):
        pause_running = True
        while pause_running:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            pause_text = self.font_lg.render("Game Paused", True, (255, 255, 255))
            self.screen.blit(pause_text, (WINDOW_WIDTH//2 - pause_text.get_width()//2, WINDOW_HEIGHT//2 - 50))
            instr_text = self.font_md.render("Press R to Resume, M for Main Menu", True, (255, 255, 255))
            self.screen.blit(instr_text, (WINDOW_WIDTH//2 - instr_text.get_width()//2, WINDOW_HEIGHT//2 + 10))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.state = self.previous_state if self.previous_state is not None else "MAIN_MENU"
                        pause_running = False
                    elif event.key == pygame.K_m:
                        self.state = "MAIN_MENU"
                        pause_running = False
        return True

    def handle_main_menu(self):
        self.screen.fill((240, 240, 240))
        title_surf = self.gui.font_lg.render("Pokémon Adventure", True, (10, 10, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 40))
        buttons = self.gui.draw_main_menu_buttons(["How to Play", "Basic", "Advanced", "Leaderboard", "Pokedex", "Exit"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for rect, label in buttons:
                    if rect.collidepoint(mx, my):
                        logger.debug(f"[MAIN MENU] {label} pressed.")
                        if label == "Exit":
                            return False
                        elif label == "How to Play":
                            self.state = "HOW_TO_PLAY"
                        elif label == "Basic":
                            self.state = "BASIC_TEAM_SELECT"
                        elif label == "Advanced":
                            self.api_locations = PokeAPIExtensions.get_all_locations()
                            if len(self.api_locations) > 12:
                                self.api_locations = random.sample(self.api_locations, 12)
                            self.selected_overworlds = []
                            self.current_overworld_index = 0
                            self.state = "ADV_OVERWORLD_SELECT"
                        elif label == "Leaderboard":
                            self.state = "LEADERBOARD"
                        elif label == "Pokedex":
                            self.state = "POKEDEX"
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p] and not self.pause_already:
                self.pause_already = True
                self.previous_state = self.state
                self.state = "PAUSED"
            if not keys[pygame.K_p]:
                self.pause_already = False
        return True

    def handle_how_to_play(self):
        self.screen.fill((255, 250, 240))
        title = "How to Play"
        title_surf = self.font_lg.render(title, True, (10, 10, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 20))
        instructions = [
            "Welcome to Pokémon Adventure!",
            "",
            "Basic Mode:",
            "  - Choose 6 Pokémon and then order their passage (use arrow keys & ENTER).",
            "  - Use the BACK button to return to the main menu.",
            "",
            "Advanced Mode:",
            "  - 12 overworlds are fetched from the PokéAPI.",
            "  - Choose 3 overworlds. In non-City modes, a labyrinth is generated.",
            "  - Wild Pokémon may try to escape if you delay your catch.",
            "",
            "Pokedex:",
            "  - View captured Pokémon and press ESC to return to the main menu.",
            "",
            "Leaderboard:",
            "  - View the top players and your best score.",
            "",
            "Game Progress:",
            "  - Capture 4 Pokémon in your Pokédex to win and see your final score.",
            "  - If all your team faint, you lose.",
            "",
            "Press ESC to return to the Main Menu."
        ]
        y = 80
        for line in instructions:
            inst_surf = self.gui.small_font.render(line, True, (10, 10, 0))
            self.screen.blit(inst_surf, (50, y))
            y += 30
        back_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 80, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), back_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), back_rect, 2)
        back_text = self.font_md.render("Main Menu", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=back_rect.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(pygame.mouse.get_pos()):
                    self.state = "MAIN_MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_basic_team_select(self):
        self.gui.draw_team_selection(self.all_pokemon, self.selected_team_indices)
        back_rect = pygame.Rect(10, WINDOW_HEIGHT - 60, 120, 40)
        pygame.draw.rect(self.screen, (200, 100, 100), back_rect)
        back_text = self.font_sm.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, back_text.get_rect(center=back_rect.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
            elif event.type == pygame.MOUSEWHEEL:
                self.gui.selection_scroll_offset = max(0, self.gui.selection_scroll_offset - event.y * 20)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if back_rect.collidepoint(mx, my):
                    self.state = "MAIN_MENU"
                    return True
                grid_cols = 4
                cell_width = WINDOW_WIDTH // grid_cols
                cell_height = 90
                grid_y = 80
                for idx, pkmn in enumerate(self.all_pokemon):
                    col = idx % grid_cols
                    row = idx // grid_cols
                    cell_rect = pygame.Rect(
                        col * cell_width + 10,
                        grid_y + row * cell_height - self.gui.selection_scroll_offset,
                        cell_width - 20,
                        cell_height - 10
                    )
                    if cell_rect.collidepoint(mx, my):
                        if idx in self.selected_team_indices:
                            self.selected_team_indices.remove(idx)
                        else:
                            if len(self.selected_team_indices) < 6:
                                self.selected_team_indices.add(idx)
                if Game.selection_confirm_button and Game.selection_confirm_button.collidepoint(mx, my):
                    if len(self.selected_team_indices) > 0:
                        self.player_team = [self.all_pokemon[i] for i in self.selected_team_indices]
                        self.team_order = self.player_team.copy()
                        self.state = "TEAM_ORDER"
                        self.selected_team_indices = set()
                        self.gui.selection_scroll_offset = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_team_order(self):
        if not self.team_order:
            logger.error("Team order is empty, returning to team selection.")
            self.state = "BASIC_TEAM_SELECT"
            return True
        self.gui.draw_active_selection(self.team_order)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if Game.active_selection_index > 0:
                        self.team_order[Game.active_selection_index], self.team_order[Game.active_selection_index - 1] = self.team_order[Game.active_selection_index - 1], self.team_order[Game.active_selection_index]
                        Game.active_selection_index -= 1
                elif event.key == pygame.K_RIGHT:
                    if Game.active_selection_index < len(self.team_order) - 1:
                        self.team_order[Game.active_selection_index], self.team_order[Game.active_selection_index + 1] = self.team_order[Game.active_selection_index + 1], self.team_order[Game.active_selection_index]
                        Game.active_selection_index += 1
                elif event.key == pygame.K_RETURN:
                    self.player_team = self.team_order.copy()
                    self.player_pokemon = self.player_team[0]
                    self.start_wild_encounter()
                    self.state = "BATTLE"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if Game.active_confirm_button and Game.active_confirm_button.collidepoint(mx, my):
                    self.player_team = self.team_order.copy()
                    self.player_pokemon = self.player_team[0]
                    self.start_wild_encounter()
                    self.state = "BATTLE"
        return True

    def start_wild_encounter(self):
        self.player_pokemon.heal()
        wild_choice = random.choice(self.default_wild_pool)
        self.opponent_pokemon = Pokemon(wild_choice)
        self.opponent_pokemon.heal()
        self.battle = Battle(self.player_pokemon, self.opponent_pokemon)
        self.selected_move_index = 0
        logger.debug(f"[WILD] {self.player_pokemon.name.capitalize()} vs. {self.opponent_pokemon.name.capitalize()}")

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
                        if not self.player_pokemon.is_alive():
                            remaining = [p for p in self.player_team if p.is_alive()]
                            if remaining:
                                self.battle.log(f"{self.player_pokemon.name.capitalize()} fainted! Auto-switching to next Pokémon.")
                                self.player_team.remove(self.player_pokemon)
                                self.player_pokemon = remaining[0]
                                self.battle = Battle(self.player_pokemon, self.opponent_pokemon, self.battle.is_trainer_battle)
                            else:
                                self.result_message = f"All your Pokémon fainted!"
                                self.state = "GAME_OVER"
                        else:
                            self.result_message = f"You won! {self.opponent_pokemon.name.capitalize()} fainted."
                            bonus = (self.opponent_pokemon.attack + self.opponent_pokemon.defense +
                                     self.opponent_pokemon.special_attack + self.opponent_pokemon.special_defense +
                                     self.opponent_pokemon.speed) // 5
                            self.score += 20 + bonus
                            # Check win condition: capturing 4 Pokémon in the Pokédex
                            if len(Game.pokedex) >= 4:
                                self.state = "WIN"
                            else:
                                self.state = "CATCH"
                        return True
            elif event.type == pygame.USEREVENT + 1:
                if hasattr(self.player_pokemon, "shake_offset"):
                    self.player_pokemon.shake_offset = 0
                if hasattr(self.opponent_pokemon, "shake_offset"):
                    self.opponent_pokemon.shake_offset = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
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
                    catch_chance = 1 - (self.opponent_pokemon.current_hp / self.opponent_pokemon.max_hp)
                    if random.random() < catch_chance:
                        self.result_message = f"You caught {self.opponent_pokemon.name.capitalize()}!"
                        Game.pokedex[self.opponent_pokemon.name] = {
                            "name": self.opponent_pokemon.name,
                            "hp": self.opponent_pokemon.max_hp,
                            "types": self.opponent_pokemon.types,
                            "sprite": self.opponent_pokemon.sprite
                        }
                        bonus = self.opponent_pokemon.attack // 2
                        self.score += 10 + bonus
                        if len(Game.pokedex) >= 4:
                            self.state = "WIN"
                            continue
                    else:
                        self.result_message = f"{self.opponent_pokemon.name.capitalize()} escaped!"
                    self.create_particles()
                    Game.attack_effects = []
                    self.state = "RESULT"
                elif cancel_rect.collidepoint(mx, my):
                    self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_result(self):
        self.update_particles()
        self.gui.draw_result_screen(self.result_message + f"   Score: {self.score}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if "win" in self.result_message.lower() or "caught" in self.result_message.lower():
                    if len(Game.pokedex) < 4:
                        self.start_wild_encounter()
                        self.state = "BATTLE"
                    else:
                        self.state = "WIN"
                else:
                    self.state = "MAIN_MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_win(self):
        self.screen.fill((0, 100, 0))
        win_text = self.font_lg.render("Congratulations, You Win!", True, (255, 215, 0))
        self.screen.blit(win_text, (WINDOW_WIDTH//2 - win_text.get_width()//2, 150))
        score_text = self.font_md.render(f"Final Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 250))
        btn_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 100, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), btn_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), btn_rect, 2)
        btn_text = self.font_md.render("Main Menu", True, (255, 255, 255))
        self.screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))
        global player_name
        leaderboard = load_leaderboard()
        found = False
        for entry in leaderboard:
            if entry["name"] == player_name:
                if self.score > entry["score"]:
                    entry["score"] = self.score
                found = True
        if not found:
            leaderboard.append({"name": player_name, "score": self.score})
        save_leaderboard(leaderboard)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    self.state = "MAIN_MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_game_over(self):
        self.screen.fill((100, 0, 0))
        over_text = self.font_lg.render("Game Over!", True, (255, 255, 255))
        self.screen.blit(over_text, (WINDOW_WIDTH//2 - over_text.get_width()//2, 150))
        score_text = self.font_md.render(f"Final Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 250))
        btn_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 100, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), btn_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), btn_rect, 2)
        btn_text = self.font_md.render("Main Menu", True, (255, 255, 255))
        self.screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    self.state = "MAIN_MENU"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_pokedex(self):
        self.gui.draw_pokedex(Game.pokedex, self.player_team)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_evolution(self):
        self.screen.fill((240, 240, 255))
        if not self.player_team:
            self.screen.blit(self.gui.small_font.render("No Pokémon in your team to show evolution.", True, (0, 0, 0)), (50, 50))
        else:
            self.screen.blit(self.font_md.render(f"Evolution Chain for {self.player_team[0].name.capitalize()}:", True, (0, 0, 0)), (50, 50))
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
                    self.screen.blit(self.gui.small_font.render(name, True, (0, 0, 0)), (50, y))
                    y += 30
            else:
                self.screen.blit(self.gui.small_font.render("No Evolution data available.", True, (0, 0, 0)), (50, 120))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_item(self):
        self.gui.draw_item_screen(self.demo_item)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_adv_overworld_select(self):
        logger.debug("Advanced Mode: Entering ADV_OVERWORLD_SELECT state.")
        self.screen.fill((245, 245, 245))
        title_surf = self.font_md.render("Select 3 Overworlds", True, (0, 0, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 20))
        if not self.api_locations:
            self.api_locations = PokeAPIExtensions.get_all_locations()
            if len(self.api_locations) > 12:
                self.api_locations = random.sample(self.api_locations, 12)
        rects = []
        cols = 4
        spacing_x = WINDOW_WIDTH // cols
        spacing_y = 80
        for idx, loc in enumerate(self.api_locations):
            col = idx % cols
            row = idx // cols
            x = col * spacing_x + 20
            y = 80 + row * spacing_y
            rect = pygame.Rect(x, y, spacing_x - 40, 50)
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            text = fit_text(self.font_sm, loc["name"].capitalize(), rect.width - 10)
            text_surf = self.font_sm.render(text, True, (0, 0, 0))
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
            rects.append((rect, loc))
        info = "Click a location to select/deselect (3 required)."
        info_surf = self.font_sm.render(info, True, (0, 0, 0))
        self.screen.blit(info_surf, (20, WINDOW_HEIGHT - 120))
        for sel in self.selected_overworlds:
            for rect, loc in rects:
                if loc["name"] == sel["name"]:
                    pygame.draw.rect(self.screen, (255, 215, 0), rect, 4)
        confirm_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 80, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), confirm_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), confirm_rect, 2)
        confirm_text = self.font_md.render("Confirm", True, (255, 255, 255))
        self.screen.blit(confirm_text, confirm_text.get_rect(center=confirm_rect.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if confirm_rect.collidepoint(mx, my):
                    if len(self.selected_overworlds) == 3:
                        logger.debug("Advanced Mode: 3 overworlds selected. Transitioning to ADV_OVERWORLD.")
                        self.current_overworld_index = 0
                        self.setup_current_overworld()
                        self.state = "ADV_OVERWORLD"
                else:
                    for rect, loc in rects:
                        if rect.collidepoint(mx, my):
                            exists = any(sel["name"] == loc["name"] for sel in self.selected_overworlds)
                            if exists:
                                self.selected_overworlds = [sel for sel in self.selected_overworlds if sel["name"] != loc["name"]]
                            else:
                                if len(self.selected_overworlds) < 3:
                                    self.selected_overworlds.append(loc)
                            break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def setup_current_overworld(self):
        logger.debug("Advanced Mode: In setup_current_overworld.")
        current_loc = self.selected_overworlds[self.current_overworld_index]
        try:
            response = session.get(current_loc["url"])
            if response.status_code == 200:
                loc_detail = response.json()
                encounters = loc_detail.get("pokemon_encounters", [])
                self.current_wild_pool = [enc["pokemon"]["name"] for enc in encounters if "name" in enc["pokemon"]]
                if not self.current_wild_pool:
                    self.current_wild_pool = self.default_wild_pool
                self.current_overworld_name = current_loc["name"].capitalize()
                logger.debug(f"Advanced Mode: Overworld '{self.current_overworld_name}' loaded with wild pool: {self.current_wild_pool}")
            else:
                self.current_wild_pool = self.default_wild_pool
                self.current_overworld_name = current_loc["name"].capitalize()
        except Exception as e:
            logger.error(f"[ADV MODE] Error fetching location detail: {e}")
            self.current_wild_pool = self.default_wild_pool
            self.current_overworld_name = current_loc["name"].capitalize()
        if self.current_overworld_name.lower() == "city":
            self.generate_city_overworld()
        else:
            self.generate_triangle_labyrinth_overworld()

    def generate_city_overworld(self):
        logger.debug("Advanced Mode: Generating city overworld.")
        self.adv_obstacles = []
        self.trainer_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
        logger.debug("[ADV MODE] City overworld placeholder generated.")

    def handle_adv_overworld(self):
        logger.debug("Advanced Mode: Entering ADV_OVERWORLD state.")
        if self.current_overworld_name.lower() == "city":
            self.screen.fill((34, 139, 34))
        else:
            self.screen.fill((100, 150, 100))
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -self.trainer_speed
        if keys[pygame.K_RIGHT]:
            dx = self.trainer_speed
        if keys[pygame.K_UP]:
            dy = -self.trainer_speed
        if keys[pygame.K_DOWN]:
            dy = self.trainer_speed
        new_x = self.trainer_pos[0] + dx
        new_y = self.trainer_pos[1] + dy
        new_rect = pygame.Rect(new_x, new_y, 40, 40)
        collision = any(new_rect.colliderect(obs) for obs in self.adv_obstacles)
        if not collision:
            self.trainer_pos[0] = new_x
            self.trainer_pos[1] = new_y
        for obs in self.adv_obstacles:
            if self.current_overworld_name.lower() == "city":
                pygame.draw.rect(self.screen, (80, 80, 80), obs)
            else:
                pygame.draw.rect(self.screen, (150, 75, 0), obs)
        trainer_rect = pygame.Rect(self.trainer_pos[0], self.trainer_pos[1], 40, 40)
        self.screen.blit(self.trainer_sprite, trainer_rect)
        for wild in self.adv_wilds:
            if not wild["captured"]:
                wild["escape_timer"] -= 1
                if wild["escape_timer"] <= 0:
                    wild["captured"] = True
                    logger.debug(f"[ADV MODE] {wild['pokemon'].name.capitalize()} escaped!")
                else:
                    wild["pos"][0] += random.randint(-1, 1)
                    wild["pos"][1] += random.randint(-1, 1)
                self.screen.blit(wild["pokemon"].sprite, wild["pos"])
        if all(w["captured"] for w in self.adv_wilds):
            complete_text = self.font_md.render("Overworld Complete! Press ENTER to continue.", True, (255, 255, 255))
            self.screen.blit(complete_text, (WINDOW_WIDTH//2 - complete_text.get_width()//2, WINDOW_HEIGHT//2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if all(w["captured"] for w in self.adv_wilds):
                        for wild in self.adv_wilds:
                            self.advanced_captured.append(wild["pokemon"])
                            self.score += 10 + (wild["pokemon"].attack // 2)
                        self.advanced_overworlds_completed += 1
                        logger.debug(f"[ADV MODE] Overworld completed. Count: {self.advanced_overworlds_completed}")
                        if self.advanced_overworlds_completed < 3:
                            self.current_overworld_index += 1
                            self.setup_current_overworld()
                            self.state = "ADV_OVERWORLD"
                        else:
                            self.state = "ADV_READY"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        for wild in self.adv_wilds:
            if not wild["captured"]:
                wild_rect = pygame.Rect(wild["pos"][0], wild["pos"][1], 80, 80)
                if trainer_rect.colliderect(wild_rect):
                    wild["captured"] = True
                    logger.debug(f"[ADV MODE] Captured {wild['pokemon'].name.capitalize()}!")
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_adv_ready(self):
        logger.debug("Advanced Mode: Entering ADV_READY state.")
        self.screen.fill((50, 50, 100))
        title = "Advanced Adventure Complete!"
        title_surf = self.font_lg.render(title, True, (255, 215, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 100))
        info = "You captured 6 Pokémon. Press 'Proceed' to order your team for battle."
        info_surf = self.font_md.render(info, True, (255, 255, 255))
        self.screen.blit(info_surf, (WINDOW_WIDTH//2 - info_surf.get_width()//2, 200))
        btn_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 100, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), btn_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), btn_rect, 2)
        btn_text = self.font_md.render("Proceed", True, (255, 255, 255))
        self.screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    self.player_team = self.advanced_captured.copy()
                    self.team_order = self.player_team.copy()
                    self.state = "TEAM_ORDER"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_player_setup(self):
        result = self.player_setup.handle()
        if result is True:
            self.state = "MAIN_MENU"
        elif result is False:
            return False
        return True

    def handle_leaderboard(self):
        lb_screen = LeaderboardScreen(self.screen)
        result = lb_screen.handle()
        if result is True:
            self.state = "MAIN_MENU"
        elif result is False:
            return False
        return None

    def run(self):
        global player_name
        while True:
            self.clock.tick(FPS)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p] and not self.pause_already and self.state not in ["MAIN_MENU", "PLAYER_SETUP", "LEADERBOARD"]:
                self.pause_already = True
                self.previous_state = self.state
                self.state = "PAUSED"
            if not keys[pygame.K_p]:
                self.pause_already = False
            if self.state == "LOADING":
                if not self.handle_loading():
                    break
            elif self.state == "PLAYER_SETUP":
                if not self.handle_player_setup():
                    break
            elif self.state == "MAIN_MENU":
                if not self.handle_main_menu():
                    break
            elif self.state == "HOW_TO_PLAY":
                if not self.handle_how_to_play():
                    break
            elif self.state == "BASIC_TEAM_SELECT":
                if not self.handle_basic_team_select():
                    break
            elif self.state == "TEAM_ORDER":
                if not self.handle_team_order():
                    break
            elif self.state == "BATTLE":
                if not self.handle_battle():
                    break
            elif self.state == "CATCH":
                if not self.handle_catch():
                    break
            elif self.state == "RESULT":
                if not self.handle_result():
                    break
            elif self.state == "POKEDEX":
                if not self.handle_pokedex():
                    break
            elif self.state == "EVOLUTION":
                if not self.handle_evolution():
                    break
            elif self.state == "ITEM":
                if not self.handle_item():
                    break
            elif self.state == "ADV_OVERWORLD_SELECT":
                if not self.handle_adv_overworld_select():
                    break
            elif self.state == "ADV_OVERWORLD":
                if not self.handle_adv_overworld():
                    break
            elif self.state == "ADV_READY":
                if not self.handle_adv_ready():
                    break
            elif self.state == "LEADERBOARD":
                if not self.handle_leaderboard():
                    break
            elif self.state == "WIN":
                # When 4 Pokémon have been captured in the Pokédex, display final score.
                if not self.handle_win():
                    break
            elif self.state == "GAME_OVER":
                if not self.handle_game_over():
                    break
            elif self.state == "PAUSED":
                if not self.handle_pause():
                    break
            else:
                break
            self.update_attack_effects()
            self.gui.draw_attack_effects()
            pygame.display.flip()
        pygame.quit()
        logger.debug("[GAME] Game terminated.")

if __name__ == "__main__":
    game = Game()
    game.run()
