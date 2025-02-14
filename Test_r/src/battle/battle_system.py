import random
from core.pokemon import Pokemon
from Test_r.src.config import POKEAPI_BASE_URL

class BattleSystem:
    def __init__(self):
        # Define some example type relationships for damage multipliers.
        self.type_chart = {
            ("water", "ground"): 0.5,
            ("fire", "grass"): 2.0,
            # Extend with additional type matchups as needed...
        }

    def get_type_multiplier(self, attack_type, defender_types):
        # Default multiplier is 1.0; multiply for each defender type.
        multiplier = 1.0
        for d_type in defender_types:
            multiplier *= self.type_chart.get((attack_type, d_type), 1.0)
        return multiplier

    def calculate_damage(self, attacker, defender, move):
        """
        Calculate damage using the official Pokémon damage formula.
        
        Formula:
            Damage = (((((2 * Level) / 5 + 2) * Power * (A / D)) / 50) + 2) * Modifier
        where Modifier includes:
            - Random factor: a random number between 0.85 and 1.0.
            - STAB: 1.5 if the move's type matches one of the attacker's types, else 1.0.
            - Type multiplier: effectiveness of move's type against the defender's types.
            - Critical: 2.0 if a critical hit occurs (6.25% chance), else 1.0.
        """
        # Use the attacker's level if available; default to level 50.
        level = getattr(attacker, "level", 50)
        power = move["power"]

        # Choose the appropriate attacking and defending stat.
        if move["damage_class"] == "physical":
            A = attacker.attack
            D = defender.defense
        else:
            A = attacker.special_attack
            D = defender.special_defense

        # Base damage calculation (ignoring modifiers).
        base = (((2 * level) / 5 + 2) * power * (A / D)) / 50 + 2

        # Modifier components.
        random_factor = random.uniform(0.85, 1.0)
        stab = 1.5 if move["type"] in attacker.types else 1.0
        type_multiplier = self.get_type_multiplier(move["type"], defender.types)
        # 6.25% chance for a critical hit.
        critical = 2.0 if random.random() < 0.0625 else 1.0

        modifier = random_factor * stab * type_multiplier * critical
        damage = int(base * modifier)

        return max(1, damage)

    def start_battle(self, player_pokemon: Pokemon, opponent_pokemon: Pokemon):
        print(f"A battle starts between {player_pokemon.name.capitalize()} and {opponent_pokemon.name.capitalize()}!")
        # Determine turn order based on speed.
        if player_pokemon.speed >= opponent_pokemon.speed:
            turn_order = [("player", player_pokemon, opponent_pokemon), ("opponent", opponent_pokemon, player_pokemon)]
        else:
            turn_order = [("opponent", opponent_pokemon, player_pokemon), ("player", player_pokemon, opponent_pokemon)]
        
        # Battle loop.
        while player_pokemon.is_alive() and opponent_pokemon.is_alive():
            for role, attacker, defender in turn_order:
                if not attacker.is_alive() or not defender.is_alive():
                    break
                if attacker.moves:
                    move = random.choice(attacker.moves)
                    print(f"{attacker.name.capitalize()} uses {move['name']}!")
                    if random.randint(1, 100) <= move.get("accuracy", 100):
                        damage = self.calculate_damage(attacker, defender, move)
                        defender.take_damage(damage)
                        print(f"It deals {damage} damage to {defender.name.capitalize()}!")
                    else:
                        print(f"{attacker.name.capitalize()}'s attack missed!")
                if not defender.is_alive():
                    print(f"{defender.name.capitalize()} fainted!")
                    winner = attacker.name
                    loser = defender.name
                    return winner, loser
        # In a tie scenario, return player's Pokémon as winner.
        return player_pokemon.name, opponent_pokemon.name
