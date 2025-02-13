import unittest
from core.pokemon import Pokemon
from battle.battle_system import BattleSystem

class TestGameComponents(unittest.TestCase):
    def test_pokemon_load(self):
        # Verify that a known Pokémon loads correctly.
        pikachu = Pokemon("pikachu")
        self.assertTrue(pikachu.is_alive())
        self.assertGreater(pikachu.max_hp, 0)

    def test_battle_system(self):
        # Test a simple battle between two Pokémon.
        pikachu = Pokemon("pikachu")
        bulbasaur = Pokemon("bulbasaur")
        battle = BattleSystem()
        winner, loser = battle.start_battle(pikachu, bulbasaur)
        self.assertIn(winner.lower(), [pikachu.name, bulbasaur.name])
        self.assertIn(loser.lower(), [pikachu.name, bulbasaur.name])

if __name__ == "__main__":
    unittest.main()
