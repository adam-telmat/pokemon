#!/usr/bin/env python3
"""
Pokémon Adventure – Ultimate Edition (Extended & Updated)
==========================================================

This game offers two modes:

  ● Basic Mode:
      - Choose 6 Pokémon from a list (24 available in the database).
      - Engage in turn‐based battles using moves and stats.

  ● Advanced Mode:
      - The game imports 12 overworld “locations” from the PokéAPI.
      - Out of those 12, you pick 3 overworlds.
      - For each chosen overworld, a simple grid‐based labyrinth is generated.
      - Wild Pokémon for that labyrinth are taken from the API location’s 
        “pokemon_encounters” (if available) or from a default pool.
      - In each labyrinth, capture 2 wild Pokémon.
      - Earn bonus points based on opponent stats.
      - Win if your Pokédex reaches 4 Pokémon; lose if all 6 of your team faint.

Additional features:
  - A loading screen with a progress bar.
  - A Pokédex view accessible from the Main Menu.
  - Global pause functionality (press P to pause; then R to resume or M for Main Menu).
  - Navigation/back buttons on most screens.
  - An evolution chain viewer and item usage screen.
  - A scoring system that awards bonus points.

Dependencies:
    pip install pygame requests

To run:
    python advanced_pokemon_game_full.py
"""

import pygame
import random
import math
import requests
from io import BytesIO
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

# ---------------------- FALLBACK DATA: 24 POKÉMON ----------------------
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
               "speed": 70, "moves": ["scratch", "karate-chop", "low-kick", "focus-energy"]}
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

# ---------------------- GUI HELPER FUNCTION ----------------------
def draw_text(surface, text, pos, font, color):
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)

# ---------------------- GUI CLASS ----------------------
class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.font_lg = pygame.font.SysFont("Arial", 48)
        self.font_md = pygame.font.SysFont("Arial", 36)
        self.font_sm = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)
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

    def draw_main_menu_buttons(self, button_labels: list):
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
        return button_rects

    def draw_battle_scene(self, player: Pokemon, opponent: Pokemon, battle_log: list, move_menu: list = None, selected_index: int = 0):
        self.screen.fill((245, 245, 245))
        self.draw_battle_sprite(opponent, (int(WINDOW_WIDTH * 0.55), 100), flipped=True)
        self.draw_battle_sprite(player, (int(WINDOW_WIDTH * 0.1), 280))
        self.draw_hp_bar(opponent, (int(WINDOW_WIDTH * 0.55 - 50), 70))
        self.draw_hp_bar(player, (int(WINDOW_WIDTH * 0.1 - 50), 260))
        y_log = 420
        for line in reversed(battle_log[-4:] if battle_log else []):
            log_surf = self.font_sm.render(line, True, (10, 10, 10))
            log_rect = log_surf.get_rect(midright=(WINDOW_WIDTH - 50, y_log))
            self.screen.blit(log_surf, log_rect)
            y_log += 26
        if move_menu:
            self.draw_move_menu(move_menu, selected_index)
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
            else:
                current_x = start_x + (end_x - start_x) * t
                current_y = start_y + (end_y - start_y) * t
            pygame.draw.circle(self.screen, effect["color"], (int(current_x), int(current_y)), 8)
            pygame.draw.circle(self.screen, effect["color"], (int(current_x), int(current_y)), 4)

    def draw_result_screen(self, message: str):
        self.draw_gradient_background((220, 230, 255), (160, 190, 230))
        for particle in Game.result_particles:
            pygame.draw.circle(self.screen, particle["color"], (int(particle["x"]), int(particle["y"])), int(particle["radius"]))
        result_title = "You Won!" if "win" in message.lower() or "caught" in message.lower() else "You Lost!"
        title_surf = self.font_lg.render(result_title, True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)
        msg_surf = self.font_md.render(message, True, (10, 10, 10))
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
        title_surf = self.font_lg.render("Your Pokédex", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width()//2, 20))
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
            text_surf = self.font_sm.render(line, True, (10, 10, 10))
            self.screen.blit(text_surf, (50, y))
            y += 30

    def draw_item_screen(self, item: Item):
        self.screen.fill((250, 240, 230))
        title_surf = self.font_lg.render("Item Usage", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width()//2, 20))
        if item:
            self.screen.blit(item.sprite, (50, 100))
            draw_text(self.screen, f"{item.name.capitalize()}", (120, 110), self.font_md, (10, 10, 10))
        else:
            draw_text(self.screen, "No item data available.", (50, 100), self.font_md, (10, 10, 10))
        draw_text(self.screen, "Press any key to return to the main menu...", (50, 200), self.font_sm, (10, 10, 10))

    def draw_team_selection(self, available_pokemon: list, selected_indices: set):
        self.screen.fill((220, 240, 255))
        title_surf = self.font_lg.render("Select Your 6 Pokémon", True, (10, 10, 10))
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
            pygame.draw.rect(self.screen, (10, 10, 10), cell_rect, 2)
            if pkmn.sprite:
                self.screen.blit(pkmn.sprite, (x, y))
            name_text = self.font_sm.render(pkmn.name.capitalize(), True, (10, 10, 10))
            self.screen.blit(name_text, (x, y + 70))
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
        self.screen.blit(title_surf, (WINDOW_WIDTH // 2 - title_surf.get_width()//2, 10))
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
    pokedex = {}
    score = 0

    @staticmethod
    def create_attack_effect(attacker, defender, color):
        start = (int(WINDOW_WIDTH * 0.1 + 80), int(280 + 40))
        end = (int(WINDOW_WIDTH * 0.55 + 80), int(100 + 40))
        effect = {
            "start": start,
            "end": end,
            "progress": 0,
            "color": color,
            "trajectory": random.choice(["parabola", "zigzag", "linear"])
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
        self.load_progress = 0
        self.pause_already = False
        self.previous_state = None
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
        # Advanced mode variables:
        self.api_locations = []         # Will hold 12 API locations
        self.selected_overworlds = []   # 3 chosen overworlds (each from API)
        self.current_overworld_index = 0
        self.current_wild_pool = []     # Wild Pokémon names for current overworld
        self.trainer_sprite = self.load_trainer_image()
        self.trainer_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
        self.trainer_speed = 5
        self.adv_wilds = []
        self.adv_obstacles = []
        # Initially load all game data.
        self.load_game_data()
        print("[GAME INIT] Game initialized successfully.")

    def load_trainer_image(self):
        url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/other/official-artwork/charmander.png"
        try:
            response = session.get(url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                sprite = pygame.image.load(image_data).convert_alpha()
                sprite = pygame.transform.scale(sprite, (40, 40))
                print("[TRAINER] Trainer image loaded from API.")
                return sprite
        except Exception as e:
            print(f"[TRAINER ERROR] {e}")
        sprite = pygame.Surface((40, 40))
        sprite.fill((255, 0, 0))
        return sprite

    def load_game_data(self):
        print("[LOAD DATA] Collecting game data from API...")
        self.all_pokemon = [Pokemon(name) for name in SPECIES_DATA.keys()]
        self.demo_item = Item(1)
        self.selected_team_indices = set()
        print("[LOAD DATA] Game data collection complete.")

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

    def handle_loading(self):
        self.screen.fill((0, 0, 0))
        loading_text = self.font_md.render("Loading game data...", True, (255, 255, 255))
        self.screen.blit(loading_text, (WINDOW_WIDTH//2 - loading_text.get_width()//2, WINDOW_HEIGHT//2 - 40))
        bar_width = 400
        bar_height = 30
        progress = self.load_progress / 100.0
        pygame.draw.rect(self.screen, (100, 100, 100), (WINDOW_WIDTH//2 - bar_width//2, WINDOW_HEIGHT//2, bar_width, bar_height))
        pygame.draw.rect(self.screen, (0, 255, 0), (WINDOW_WIDTH//2 - bar_width//2, WINDOW_HEIGHT//2, int(bar_width * progress), bar_height))
        self.load_progress += 1
        if self.load_progress >= 100:
            self.state = "MAIN_MENU"
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
        title_surf = self.gui.font_lg.render("Pokémon Adventure", True, (10, 10, 10))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 40))
        buttons = self.gui.draw_main_menu_buttons(["How to Play", "Basic", "Advanced", "Pokedex", "Exit"])
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
                        print(f"[MAIN MENU] {label} pressed.")
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
                        elif label == "Pokedex":
                            self.state = "POKEDEX"
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p] and not self.pause_already:
                self.pause_already = True
                self.previous_state = self.state
                self.state = "PAUSED"
                return True
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
            "  - Select 6 Pokémon (from 24 available) and battle turn-based.",
            "",
            "Advanced Mode:",
            "  - 12 overworlds are imported from the PokéAPI.",
            "  - Choose 3 overworlds; for each, a labyrinth is generated.",
            "  - Wild Pokémon come from the API location's encounters (if available).",
            "  - Capture 2 wild Pokémon per overworld.",
            "",
            "Pokedex:",
            "  - View your captured Pokémon from the Main Menu.",
            "",
            "Pause:",
            "  - Press P to pause (R to resume, M for Main Menu).",
            "",
            "Scoring:",
            "  - Earn points for wins and captures; bonus points are added based on opponent stats.",
            "",
            "Press ESC to return to the Main Menu."
        ]
        y = 80
        for line in instructions:
            inst_surf = self.gui.small_font.render(line, True, (10, 10, 10))
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
            return True
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_basic_team_select(self):
        self.gui.draw_team_selection(self.all_pokemon, self.selected_team_indices)
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
                    if len(self.selected_team_indices) > 0:
                        self.player_team = [self.all_pokemon[i] for i in self.selected_team_indices]
                        self.selected_team_indices = set()
                        self.gui.selection_scroll_offset = 0
                        self.state = "ACTIVE_SELECT"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_active_select(self):
        self.gui.draw_active_selection(self.player_team)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
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
                    self.start_wild_encounter()
                    self.state = "BATTLE"
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def start_wild_encounter(self):
        self.player_pokemon.heal()
        wild_choice = random.choice(self.default_wild_pool)
        self.opponent_pokemon = Pokemon(wild_choice)
        self.opponent_pokemon.heal()
        self.battle = Battle(self.player_pokemon, self.opponent_pokemon)
        self.selected_move_index = 0
        print(f"[WILD] {self.player_pokemon.name.capitalize()} vs. {self.opponent_pokemon.name.capitalize()}")

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
                                self.player_team.remove(self.player_pokemon)
                                self.player_pokemon = remaining[0]
                                self.battle = Battle(self.player_pokemon, self.opponent_pokemon)
                                self.battle.log("Switched to next Pokémon!")
                            else:
                                self.result_message = "All your Pokémon fainted!"
                                self.state = "GAME_OVER"
                                continue
                        else:
                            self.result_message = f"You won! {self.opponent_pokemon.name.capitalize()} fainted."
                            bonus = (self.opponent_pokemon.attack + self.opponent_pokemon.defense +
                                     self.opponent_pokemon.special_attack + self.opponent_pokemon.special_defense +
                                     self.opponent_pokemon.speed) // 5
                            self.score += 20 + bonus
                            self.state = "CATCH"
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
                mx, my = pygame.mouse.get_pos()
                if "win" in self.result_message.lower() or "caught" in self.result_message.lower():
                    if Game.play_again_button and Game.play_again_button.collidepoint(mx, my):
                        self.start_wild_encounter()
                        self.state = "BATTLE"
                    elif Game.result_back_button and Game.result_back_button.collidepoint(mx, my):
                        self.state = "MAIN_MENU"
                        self.battle.battle_log.clear()
                        Game.result_particles = []
                else:
                    if Game.result_back_button and Game.result_back_button.collidepoint(mx, my):
                        self.state = "MAIN_MENU"
                        self.battle.battle_log.clear()
                        Game.result_particles = []
            elif event.type == pygame.KEYDOWN:
                self.state = "MAIN_MENU"
                self.battle.battle_log.clear()
                Game.result_particles = []
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

    # ------------------ Advanced Overworld Selection (API Import) ------------------
    def handle_adv_overworld_select(self):
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
            loc_name = loc["name"].capitalize()
            text_surf = self.font_sm.render(loc_name, True, (0, 0, 0))
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))
            rects.append((rect, loc))
        info = "Click on a location to select/deselect (3 required)."
        info_surf = self.font_sm.render(info, True, (0,0,0))
        self.screen.blit(info_surf, (20, WINDOW_HEIGHT - 120))
        for sel in self.selected_overworlds:
            for rect, loc in rects:
                if loc["name"] == sel["name"]:
                    pygame.draw.rect(self.screen, (255, 215, 0), rect, 4)
        confirm_rect = pygame.Rect(WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT - 80, 200, 50)
        pygame.draw.rect(self.screen, (70, 130, 180), confirm_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), confirm_rect, 2)
        confirm_text = self.font_md.render("Confirm", True, (255,255,255))
        self.screen.blit(confirm_text, confirm_text.get_rect(center=confirm_rect.center))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if confirm_rect.collidepoint(mx, my):
                    if len(self.selected_overworlds) == 3:
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
            else:
                self.current_wild_pool = self.default_wild_pool
                self.current_overworld_name = current_loc["name"].capitalize()
        except Exception as e:
            print(f"[ADV MODE] Error fetching location detail: {e}")
            self.current_wild_pool = self.default_wild_pool
            self.current_overworld_name = current_loc["name"].capitalize()
        self.generate_api_labyrinth_overworld()

    def generate_api_labyrinth_overworld(self):
        cols = 8
        rows = 6
        cell_w = WINDOW_WIDTH // cols
        cell_h = WINDOW_HEIGHT // rows
        free_cols = random.sample(range(cols), 2)
        self.adv_obstacles = []
        for c in range(cols):
            if c in free_cols:
                continue
            for r in range(rows):
                x = c * cell_w
                y = r * cell_h
                obstacle = pygame.Rect(x + 10, y + 10, cell_w - 20, cell_h - 20)
                self.adv_obstacles.append(obstacle)
        self.adv_wilds = []
        free_cells = []
        for c in free_cols:
            for r in range(rows):
                free_cells.append((c, r))
        random.shuffle(free_cells)
        for _ in range(2):
            if free_cells:
                c, r = free_cells.pop()
                if self.current_wild_pool:
                    wild_name = random.choice(self.current_wild_pool)
                else:
                    wild_name = random.choice(self.default_wild_pool)
                wild_pkmn = Pokemon(wild_name)
                x = c * cell_w + cell_w//2 + random.randint(-10, 10) - 40
                y = r * cell_h + cell_h//2 + random.randint(-10, 10) - 40
                self.adv_wilds.append({"pokemon": wild_pkmn, "pos": [x, y], "captured": False})
        start_col = free_cols[0]
        self.trainer_pos = [start_col * cell_w + cell_w//2 - 20, WINDOW_HEIGHT//2 - 20]
        print(f"[ADV MODE] {self.current_overworld_name} labyrinth generated. Free columns: {free_cols}.")

    def handle_adv_overworld(self):
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
        collision = False
        for obs in self.adv_obstacles:
            if new_rect.colliderect(obs):
                collision = True
                break
        if not collision:
            self.trainer_pos[0] = new_x
            self.trainer_pos[1] = new_y
        for obs in self.adv_obstacles:
            pygame.draw.rect(self.screen, (150, 75, 0), obs)
        trainer_rect = pygame.Rect(self.trainer_pos[0], self.trainer_pos[1], 40, 40)
        self.screen.blit(self.trainer_sprite, trainer_rect)
        for wild in self.adv_wilds:
            if not wild["captured"]:
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
                        self.current_overworld_index += 1
                        if self.current_overworld_index < len(self.selected_overworlds):
                            self.setup_current_overworld()
                            self.state = "ADV_OVERWORLD"
                        else:
                            self.state = "ADV_READY"
                elif event.key == pygame.K_ESCAPE:
                    self.state = "MAIN_MENU"
        trainer_rect = pygame.Rect(self.trainer_pos[0], self.trainer_pos[1], 40, 40)
        for wild in self.adv_wilds:
            if not wild["captured"]:
                wild_rect = pygame.Rect(wild["pos"][0], wild["pos"][1], 80, 80)
                if trainer_rect.colliderect(wild_rect):
                    wild["captured"] = True
                    print(f"[ADV MODE] Captured {wild['pokemon'].name.capitalize()}!")
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p] and not self.pause_already:
            self.pause_already = True
            self.previous_state = self.state
            self.state = "PAUSED"
        if not keys[pygame.K_p]:
            self.pause_already = False
        return True

    def handle_adv_ready(self):
        self.screen.fill((50, 50, 100))
        title = "Advanced Adventure Complete!"
        title_surf = self.font_lg.render(title, True, (255, 215, 0))
        self.screen.blit(title_surf, (WINDOW_WIDTH//2 - title_surf.get_width()//2, 100))
        info = "You captured 6 Pokémon. Press 'Proceed' to continue to battle."
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
                    self.state = "ACTIVE_SELECT"
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

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p] and not self.pause_already:
                self.pause_already = True
                self.previous_state = self.state
                self.state = "PAUSED"
            if not keys[pygame.K_p]:
                self.pause_already = False

            if self.state == "PAUSED":
                running = self.handle_pause()
            elif self.state == "LOADING":
                running = self.handle_loading()
            elif self.state == "MAIN_MENU":
                running = self.handle_main_menu()
            elif self.state == "HOW_TO_PLAY":
                running = self.handle_how_to_play()
            elif self.state == "BASIC_TEAM_SELECT":
                running = self.handle_basic_team_select()
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
            elif self.state == "ADV_OVERWORLD_SELECT":
                running = self.handle_adv_overworld_select()
            elif self.state == "ADV_OVERWORLD":
                running = self.handle_adv_overworld()
            elif self.state == "ADV_READY":
                running = self.handle_adv_ready()
            elif self.state == "WIN":
                running = self.handle_win()
            elif self.state == "GAME_OVER":
                running = self.handle_game_over()
            else:
                running = False

            self.update_attack_effects()
            self.gui.draw_attack_effects()
            pygame.display.flip()
        pygame.quit()
        print("[GAME] Game terminated.")

if __name__ == "__main__":
    game = Game()
    game.run()
