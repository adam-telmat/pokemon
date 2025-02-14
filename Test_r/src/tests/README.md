# Pokémon Game

This is a Python-based Pokémon game built using Pygame. The game features:
- A core module that loads Pokémon data via the PokéAPI.
- A turn-based battle system with type multipliers and dynamic damage calculation.
- A Pokédex that records encountered Pokémon and avoids duplicates.
- A simple, yet extensible GUI for menus and shop interfaces.
- A modular project structure using object-oriented programming principles.

## Project Structure

pokemon-game/ ├── assets/ # Images, sounds, and other assets ├── data/ # Data files (player_data.json, pokemon.json, pokedex.json) ├── gui/ # GUI-related modules ├── core/ # Core game logic (Pokémon, moves, stats) ├── battle/ # Battle system mechanics ├── pokedex/ # Pokédex functionality ├── world/ # World and gym leader information ├── develop/ # Experimental features ├── tests/ # Unit tests ├── config.py # Configuration settings ├── utils.py # Helper functions ├── main.py # Entry point of the game ├── requirements.txt # Dependencies ├── README.md # Project documentation └── .gitignore # Git ignore file

markdown
Copy

## How to Run

1. Install dependencies:  
   ```bash
   pip install -r requirements.txt
