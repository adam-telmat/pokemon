import random

class BattleLogic:
    def __init__(self):
        self.TYPE_CHART = {
            # Notre tableau complet des types qu'on vient de définir
        }
    
    def calculate_damage(self, move, attacker, defender):
        # Base damage formula
        if move["category"] == "physical":
            attack = attacker["attack"]
            defense = defender["defense"]
        else:  # Special
            attack = attacker["special_attack"]
            defense = defender["special_defense"]
        
        base_damage = ((2 * attack + 10) / (defense + 10)) * move["power"]
        
        # Type multiplier
        type_multiplier = self.get_type_multiplier(move["type"], defender["types"])
        
        # Random factor (0.85 to 1.0)
        random_factor = random.uniform(0.85, 1.0)
        
        final_damage = base_damage * type_multiplier * random_factor
        return max(1, int(final_damage))
    
    def get_type_multiplier(self, move_type, defender_types):
        multiplier = 1.0
        for def_type in defender_types:
            if def_type in self.TYPE_CHART[move_type]:
                multiplier *= self.TYPE_CHART[move_type][def_type]
        return multiplier
    
    def determine_first(self, pokemon1, pokemon2):
        return pokemon1 if pokemon1["speed"] > pokemon2["speed"] else pokemon2 