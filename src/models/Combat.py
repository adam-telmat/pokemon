import random

class Combat:
    def __init__(self, player_pokemon, opponent_pokemon):
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon
        self.winner = None
        self.loser = None

    def calculate_damage(self, attacker, defender):
        # Chance de rater l'attaque (20%)
        if random.random() < 0.2:
            return 0

        base_damage = attacker.attack
        type_multiplier = self.get_type_effectiveness(attacker.types[0], defender.types[0])
        return base_damage * type_multiplier

    def get_type_effectiveness(self, attacker_type, defender_type):
        # À implémenter avec le tableau des efficacités
        return 1.0

    def execute_turn(self, attacker, defender):
        damage = self.calculate_damage(attacker, defender)
        if damage > 0:
            actual_damage = defender.take_damage(damage)
            return f"{attacker.name} inflige {actual_damage} dégâts à {defender.name}!"
        return f"{attacker.name} rate son attaque!"

    def check_winner(self):
        if not self.player_pokemon.is_alive():
            self.winner = self.opponent_pokemon
            self.loser = self.player_pokemon
            return True
        elif not self.opponent_pokemon.is_alive():
            self.winner = self.player_pokemon
            self.loser = self.opponent_pokemon
            return True
        return False 