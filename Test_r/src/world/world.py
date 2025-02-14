import random
from core.pokemon import Pokemon

class GymLeader:
    def __init__(self, name, main_pokemon):
        """
        Initialize a GymLeader with a name and a main Pokémon.
        """
        self.name = name
        self.main_pokemon = main_pokemon

class World:
    def __init__(self):
        """
        Initialize the game world.
        Currently, it contains a list of gym leaders.
        You can expand this to include routes, maps, and other world data.
        """
        self.gym_leaders = [
            GymLeader("Brock", Pokemon("onix")),
            GymLeader("Misty", Pokemon("staryu"))
        ]

    def get_gym_leader(self):
        """
        Return a random gym leader from the list.
        """
        return random.choice(self.gym_leaders)
