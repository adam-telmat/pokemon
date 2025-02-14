import unittest
from core.pokemon import Pokemon
from battle.battle_system import BattleSystem

class TestGameComponents(unittest.TestCase):
    def test_pokemon_load(self):
        """
        Test that a known Pokémon (e.g., Pikachu) loads correctly
        and has valid stats.
        """
        pikachu = Pokemon("pikachu")
        self.assertTrue(pikachu.is_alive())
        self.assertGreater(pikachu.max_hp, 0)
        self.assertIsInstance(pikachu.types, list)
        self.assertGreater(len(pikachu.types), 0)

    def test_battle_system(self):
        """
        Simulate a simple battle between two Pokémon (Pikachu and Bulbasaur)
        and verify that the winner and loser are among these two.
        """
        pikachu = Pokemon("pikachu")
        bulbasaur = Pokemon("bulbasaur")
        battle = BattleSystem()
        winner, loser = battle.start_battle(pikachu, bulbasaur)
        self.assertIn(winner.lower(), [pikachu.name, bulbasaur.name])
        self.assertIn(loser.lower(), [pikachu.name, bulbasaur.name])

if __name__ == "__main__":
    unittest.main()
