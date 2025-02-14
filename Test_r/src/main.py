import json
import os
import random
import pygame
from io import BytesIO

# Import modules from your project
from core.pokemon import Pokemon
from battle.battle_system import BattleSystem
from world.world import World
from pokedex.pokedex import Pokedex
from gui.gui import GUI
from Test_r.src.config import WINDOW_WIDTH, WINDOW_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pokémon Adventure")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True

        # Initialize subsystems
        self.world = World()
        self.pokedex = Pokedex()
        self.battle_system = BattleSystem()
        self.gui = GUI(self.screen)
        self.player_data = {}

        # Load existing data or start a new game
        self.load_player_data()
        if not self.player_data.get("team"):
            self.new_game()

    def load_player_data(self):
        os.makedirs("data", exist_ok=True)
        try:
            with open("data/player_data.json", "r") as f:
                self.player_data = json.load(f)
        except FileNotFoundError:
            # Initialize new player data if no file exists
            self.player_data = {"team": [], "pokedex": [], "badges": [], "money": 5000}
            self.save_player_data()

    def save_player_data(self):
        os.makedirs("data", exist_ok=True)
        with open("data/player_data.json", "w") as f:
            json.dump(self.player_data, f, indent=4)

    def new_game(self):
        # Reset player data for a new game
        self.player_data = {"team": [], "pokedex": [], "badges": [], "money": 5000}
        # Load available Pokémon names from data/pokemon.json (or use a default list)
        if os.path.exists("data/pokemon.json"):
            with open("data/pokemon.json", "r") as f:
                available_pokemon = json.load(f)
        else:
            available_pokemon = ["pikachu", "charmander", "bulbasaur", "squirtle"]
        print("Choose your starting Pokémon:")
        for idx, p in enumerate(available_pokemon, start=1):
            print(f"{idx}. {p.capitalize()}")
        try:
            choice = int(input("Enter the number of your choice: ")) - 1
            starter = available_pokemon[choice]
        except Exception as e:
            print(f"Invalid input ({e}). Defaulting to {available_pokemon[0].capitalize()}.")
            starter = available_pokemon[0]
        self.player_data["team"].append(starter)
        print(f"You have chosen {starter.capitalize()}!")
        self.save_player_data()

    def add_pokemon(self):
        # Let the player add a new Pokémon to their team.
        new_poke_name = input("Enter the name of the Pokémon to add: ").strip().lower()
        try:
            poke = Pokemon(new_poke_name)
            if poke:
                self.player_data["team"].append(new_poke_name)
                print(f"{new_poke_name.capitalize()} has been added to your team!")
                self.save_player_data()
            else:
                print("Invalid Pokémon name. Please try again.")
        except Exception as e:
            print(f"Error adding Pokémon: {e}")

    def view_pokedex(self):
        # Display the player's Pokédex
        pokedex_list = self.player_data.get("pokedex", [])
        if not pokedex_list:
            print("Your Pokédex is empty!")
        else:
            print("Your Pokédex:")
            unique_pokemon = list(set(pokedex_list))
            for p in unique_pokemon:
                count = pokedex_list.count(p)
                print(f"{p.capitalize()} - encountered {count} time{'s' if count > 1 else ''}")

    def start_battle(self, opponent_pokemon):
        if not self.player_data["team"]:
            print("No Pokémon in your team!")
            return
        player_pokemon = Pokemon(self.player_data["team"][0])
        winner, loser = self.battle_system.start_battle(player_pokemon, opponent_pokemon)
        if winner.lower() == player_pokemon.name.lower():
            # Add opponent to Pokédex without duplicates
            if opponent_pokemon.name not in self.player_data["pokedex"]:
                self.player_data["pokedex"].append(opponent_pokemon.name)
                self.pokedex.add_pokemon(opponent_pokemon)
            print(f"You won! {opponent_pokemon.name.capitalize()} has been recorded in your Pokédex.")
        else:
            print(f"You lost! {player_pokemon.name.capitalize()} fainted.")
        self.save_player_data()

    def encounter_wild_pokemon(self):
        # Random wild encounter from a predefined list
        wild_options = ["pikachu", "charmander", "bulbasaur", "squirtle", "eevee", "psyduck"]
        opponent = Pokemon(random.choice(wild_options))
        self.start_battle(opponent)

    def enter_gym_battle(self):
        # Retrieve a gym leader from the world module
        gym_leader = self.world.get_gym_leader()
        self.start_battle(gym_leader.main_pokemon)

    def buy_items(self):
        # Shop interface with item prices
        items = {"potion": 300, "super potion": 700, "revive": 1500}
        self.gui.display_shop(items, self.player_data["money"])
        # Assume GUI updates money as needed; then save
        self.save_player_data()

    def main_menu(self):
        while self.running:
            self.screen.fill((255, 255, 255))
            self.gui.draw_main_menu()  # Draw menu options on screen
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.encounter_wild_pokemon()
                    elif event.key == pygame.K_2:
                        self.enter_gym_battle()
                    elif event.key == pygame.K_3:
                        self.buy_items()
                    elif event.key == pygame.K_4:
                        self.add_pokemon()
                    elif event.key == pygame.K_5:
                        self.view_pokedex()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            self.clock.tick(30)
        pygame.quit()
        self.save_player_data()

    def run(self):
        self.main_menu()

if __name__ == "__main__":
    game = Game()
    game.run()
