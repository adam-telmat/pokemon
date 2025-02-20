"""
Équipes des maîtres de la Ligue Pokémon
Chaque maître a une équipe thématique avec des stats et mouvements équilibrés
"""

# Olga - Spécialiste Glace/Eau (2 Pokémon)
OLGA_TEAM = [
    {
        "name": "Lokhlass",
        "types": ["water", "ice"],
        "level": 52,
        "max_hp": 180,
        "current_hp": 180,
        "attack": 85,
        "defense": 80,
        "special_attack": 85,
        "special_defense": 95,
        "speed": 60,
        "moves": [
            {"name": "Ice Beam", "type": "ice", "category": "special", "power": 90, "accuracy": 100, "pp": 10, "max_pp": 10},
            {"name": "Surf", "type": "water", "category": "special", "power": 95, "accuracy": 100, "pp": 15, "max_pp": 15},
            {"name": "Body Slam", "type": "normal", "category": "physical", "power": 85, "accuracy": 100, "pp": 15, "max_pp": 15},
            {"name": "Blizzard", "type": "ice", "category": "special", "power": 120, "accuracy": 70, "pp": 5, "max_pp": 5}
        ]
    },
    {
        "name": "Artikodin",
        "types": ["ice", "flying"],
        "level": 54,
        "max_hp": 190,
        "current_hp": 190,
        "attack": 85,
        "defense": 100,
        "special_attack": 95,
        "special_defense": 125,
        "speed": 85,
        "moves": [
            {"name": "Blizzard", "type": "ice", "category": "special", "power": 120, "accuracy": 70, "pp": 5, "max_pp": 5},
            {"name": "Ice Beam", "type": "ice", "category": "special", "power": 90, "accuracy": 100, "pp": 10, "max_pp": 10},
            {"name": "Sky Attack", "type": "flying", "category": "physical", "power": 140, "accuracy": 90, "pp": 5, "max_pp": 5},
            {"name": "Agility", "type": "psychic", "category": "status", "power": 0, "accuracy": 100, "pp": 30, "max_pp": 30}
        ]
    }
]

# Aldo - Spécialiste Combat (3 Pokémon)
ALDO_TEAM = [
    {
        "name": "Mackogneur",
        "types": ["fighting"],
        "stats": {
            "hp": 90,
            "attack": 130,
            "defense": 80,
            "special_attack": 65,
            "special_defense": 85,
            "speed": 55
        },
        "moves": [
            {"name": "Dynamic Punch", "type": "fighting", "power": 100, "accuracy": 50, "pp": 5, "category": "physical"},
            {"name": "Rock Slide", "type": "rock", "power": 75, "accuracy": 90, "pp": 10, "category": "physical"},
            {"name": "Earthquake", "type": "ground", "power": 100, "accuracy": 100, "pp": 10, "category": "physical"},
            {"name": "Cross Chop", "type": "fighting", "power": 100, "accuracy": 80, "pp": 5, "category": "physical"}
        ]
    },
    {
        "name": "Tygnon",
        "types": ["fighting"],
        "stats": {
            "hp": 50,
            "attack": 105,
            "defense": 79,
            "special_attack": 35,
            "special_defense": 110,
            "speed": 76
        },
        "moves": [
            {"name": "Thunder Punch", "type": "electric", "power": 75, "accuracy": 100, "pp": 15, "category": "physical"},
            {"name": "Ice Punch", "type": "ice", "power": 75, "accuracy": 100, "pp": 15, "category": "physical"},
            {"name": "Fire Punch", "type": "fire", "power": 75, "accuracy": 100, "pp": 15, "category": "physical"},
            {"name": "Mega Punch", "type": "normal", "power": 80, "accuracy": 85, "pp": 20, "category": "physical"}
        ]
    },
    {
        "name": "Onix",
        "types": ["rock", "ground"],
        "stats": {
            "hp": 35,
            "attack": 45,
            "defense": 160,
            "special_attack": 30,
            "special_defense": 45,
            "speed": 70
        },
        "moves": [
            {"name": "Rock Slide", "type": "rock", "power": 75, "accuracy": 90, "pp": 10, "category": "physical"},
            {"name": "Earthquake", "type": "ground", "power": 100, "accuracy": 100, "pp": 10, "category": "physical"},
            {"name": "Dig", "type": "ground", "power": 80, "accuracy": 100, "pp": 10, "category": "physical"},
            {"name": "Bind", "type": "normal", "power": 15, "accuracy": 85, "pp": 20, "category": "physical"}
        ]
    }
]

# Agatha - Spécialiste Spectre/Poison (4 Pokémon)
AGATHA_TEAM = [
    {
        "name": "Ectoplasma",
        "types": ["ghost", "poison"],
        "stats": {
            "hp": 60,
            "attack": 65,
            "defense": 60,
            "special_attack": 130,
            "special_defense": 75,
            "speed": 110
        },
        "moves": [
            {"name": "Shadow Ball", "type": "ghost", "power": 80, "accuracy": 100, "pp": 15, "category": "special"},
            {"name": "Psychic", "type": "psychic", "power": 90, "accuracy": 100, "pp": 10, "category": "special"},
            {"name": "Hypnosis", "type": "psychic", "power": 0, "accuracy": 60, "pp": 20, "category": "status"},
            {"name": "Dream Eater", "type": "psychic", "power": 100, "accuracy": 100, "pp": 15, "category": "special"}
        ]
    },
    {
        "name": "Arbok",
        "types": ["poison"],
        "stats": {
            "hp": 60,
            "attack": 95,
            "defense": 69,
            "special_attack": 65,
            "special_defense": 79,
            "speed": 80
        },
        "moves": [
            {"name": "Poison Fang", "type": "poison", "power": 50, "accuracy": 100, "pp": 15, "category": "physical"},
            {"name": "Wrap", "type": "normal", "power": 15, "accuracy": 90, "pp": 20, "category": "physical"},
            {"name": "Glare", "type": "normal", "power": 0, "accuracy": 100, "pp": 30, "category": "status"},
            {"name": "Earthquake", "type": "ground", "power": 100, "accuracy": 100, "pp": 10, "category": "physical"}
        ]
    },
    {
        "name": "Nosferalto",
        "types": ["poison", "flying"],
        "stats": {
            "hp": 75,
            "attack": 80,
            "defense": 70,
            "special_attack": 65,
            "special_defense": 75,
            "speed": 90
        },
        "moves": [
            {"name": "Air Cutter", "type": "flying", "power": 60, "accuracy": 95, "pp": 25, "category": "special"},
            {"name": "Toxic", "type": "poison", "power": 0, "accuracy": 90, "pp": 10, "category": "status"},
            {"name": "Confuse Ray", "type": "ghost", "power": 0, "accuracy": 100, "pp": 10, "category": "status"},
            {"name": "Bite", "type": "dark", "power": 60, "accuracy": 100, "pp": 25, "category": "physical"}
        ]
    },
    {
        "name": "Spectrum",
        "types": ["ghost", "poison"],
        "stats": {
            "hp": 45,
            "attack": 50,
            "defense": 45,
            "special_attack": 115,
            "special_defense": 55,
            "speed": 95
        },
        "moves": [
            {"name": "Shadow Ball", "type": "ghost", "power": 80, "accuracy": 100, "pp": 15, "category": "special"},
            {"name": "Sludge Bomb", "type": "poison", "power": 90, "accuracy": 100, "pp": 10, "category": "special"},
            {"name": "Hypnosis", "type": "psychic", "power": 0, "accuracy": 60, "pp": 20, "category": "status"},
            {"name": "Dream Eater", "type": "psychic", "power": 100, "accuracy": 100, "pp": 15, "category": "special"}
        ]
    }
]

# Peter - Spécialiste Dragon (5 Pokémon)
PETER_TEAM = [
    {
        "name": "Dracolosse",
        "types": ["dragon", "flying"],
        "stats": {
            "hp": 91,
            "attack": 134,
            "defense": 95,
            "special_attack": 100,
            "special_defense": 100,
            "speed": 80
        },
        "moves": [
            {"name": "Outrage", "type": "dragon", "power": 120, "accuracy": 100, "pp": 10, "category": "physical"},
            {"name": "Wing Attack", "type": "flying", "power": 60, "accuracy": 100, "pp": 35, "category": "physical"},
            {"name": "Thunder Wave", "type": "electric", "power": 0, "accuracy": 90, "pp": 20, "category": "status"},
            {"name": "Hyper Beam", "type": "normal", "power": 150, "accuracy": 90, "pp": 5, "category": "special"}
        ]
    },
    {
        "name": "Leviator",
        "types": ["water", "flying"],
        "stats": {
            "hp": 95,
            "attack": 125,
            "defense": 79,
            "special_attack": 60,
            "special_defense": 100,
            "speed": 81
        },
        "moves": [
            {"name": "Hydro Pump", "type": "water", "power": 110, "accuracy": 80, "pp": 5, "category": "special"},
            {"name": "Dragon Rage", "type": "dragon", "power": 40, "accuracy": 100, "pp": 10, "category": "special"},
            {"name": "Ice Beam", "type": "ice", "power": 90, "accuracy": 100, "pp": 10, "category": "special"},
            {"name": "Hyper Beam", "type": "normal", "power": 150, "accuracy": 90, "pp": 5, "category": "special"}
        ]
    },
    {
        "name": "Dracaufeu",
        "types": ["fire", "flying"],
        "stats": {
            "hp": 78,
            "attack": 84,
            "defense": 78,
            "special_attack": 109,
            "special_defense": 85,
            "speed": 100
        },
        "moves": [
            {"name": "Flamethrower", "type": "fire", "power": 90, "accuracy": 100, "pp": 15, "category": "special"},
            {"name": "Wing Attack", "type": "flying", "power": 60, "accuracy": 100, "pp": 35, "category": "physical"},
            {"name": "Fire Spin", "type": "fire", "power": 35, "accuracy": 85, "pp": 15, "category": "special"},
            {"name": "Slash", "type": "normal", "power": 70, "accuracy": 100, "pp": 20, "category": "physical"}
        ]
    },
    {
        "name": "Ptera",
        "types": ["rock", "flying"],
        "stats": {
            "hp": 80,
            "attack": 105,
            "defense": 65,
            "special_attack": 60,
            "special_defense": 75,
            "speed": 130
        },
        "moves": [
            {"name": "Rock Slide", "type": "rock", "power": 75, "accuracy": 90, "pp": 10, "category": "physical"},
            {"name": "Wing Attack", "type": "flying", "power": 60, "accuracy": 100, "pp": 35, "category": "physical"},
            {"name": "Earthquake", "type": "ground", "power": 100, "accuracy": 100, "pp": 10, "category": "physical"},
            {"name": "Hyper Beam", "type": "normal", "power": 150, "accuracy": 90, "pp": 5, "category": "special"}
        ]
    },
    {
        "name": "Dracolosse",
        "types": ["dragon", "flying"],
        "stats": {
            "hp": 91,
            "attack": 134,
            "defense": 95,
            "special_attack": 100,
            "special_defense": 100,
            "speed": 80
        },
        "moves": [
            {"name": "Thunder", "type": "electric", "power": 110, "accuracy": 70, "pp": 10, "category": "special"},
            {"name": "Blizzard", "type": "ice", "power": 110, "accuracy": 70, "pp": 5, "category": "special"},
            {"name": "Fire Blast", "type": "fire", "power": 110, "accuracy": 85, "pp": 5, "category": "special"},
            {"name": "Hyper Beam", "type": "normal", "power": 150, "accuracy": 90, "pp": 5, "category": "special"}
        ]
    }
]

# Blue - Champion (6 Pokémon)
BLUE_TEAM = [
    {
        "name": "Roucarnage",
        "types": ["normal", "flying"],
        "stats": {
            "hp": 83,
            "attack": 80,
            "defense": 75,
            "special_attack": 70,
            "special_defense": 70,
            "speed": 101
        },
        "moves": [
            {"name": "Sky Attack", "type": "flying", "power": 140, "accuracy": 90, "pp": 5, "category": "physical"},
            {"name": "Double Edge", "type": "normal", "power": 120, "accuracy": 100, "pp": 15, "category": "physical"},
            {"name": "Mirror Move", "type": "flying", "power": 0, "accuracy": 100, "pp": 20, "category": "status"},
            {"name": "Hyper Beam", "type": "normal", "power": 150, "accuracy": 90, "pp": 5, "category": "special"}
        ]
    },
    {
        "name": "Alakazam",
        "types": ["psychic"],
        "stats": {
            "hp": 55,
            "attack": 50,
            "defense": 45,
            "special_attack": 135,
            "special_defense": 95,
            "speed": 120
        },
        "moves": [
            {"name": "Psychic", "type": "psychic", "power": 90, "accuracy": 100, "pp": 10, "category": "special"},
            {"name": "Thunder Wave", "type": "electric", "power": 0, "accuracy": 90, "pp": 20, "category": "status"},
            {"name": "Recover", "type": "normal", "power": 0, "accuracy": 100, "pp": 10, "category": "status"},
            {"name": "Reflect", "type": "psychic", "power": 0, "accuracy": 100, "pp": 20, "category": "status"}
        ]
    },
    {
        "name": "Arcanin",
        "types": ["fire"],
        "stats": {
            "hp": 90,
            "attack": 110,
            "defense": 80,
            "special_attack": 100,
            "special_defense": 80,
            "speed": 95
        },
        "moves": [
            {"name": "Flamethrower", "type": "fire", "power": 90, "accuracy": 100, "pp": 15, "category": "special"},
            {"name": "Extreme Speed", "type": "normal", "power": 80, "accuracy": 100, "pp": 5, "category": "physical"},
            {"name": "Crunch", "type": "dark", "power": 80, "accuracy": 100, "pp": 15, "category": "physical"},
            {"name": "Fire Blast", "type": "fire", "power": 110, "accuracy": 85, "pp": 5, "category": "special"}
        ]
    },
    {
        "name": "Exeggutor",
        "types": ["grass", "psychic"],
        "stats": {
            "hp": 95,
            "attack": 95,
            "defense": 85,
            "special_attack": 125,
            "special_defense": 75,
            "speed": 55
        },
        "moves": [
            {"name": "Solar Beam", "type": "grass", "power": 120, "accuracy": 100, "pp": 10, "category": "special"},
            {"name": "Psychic", "type": "psychic", "power": 90, "accuracy": 100, "pp": 10, "category": "special"},
            {"name": "Sleep Powder", "type": "grass", "power": 0, "accuracy": 75, "pp": 15, "category": "status"},
            {"name": "Egg Bomb", "type": "normal", "power": 100, "accuracy": 75, "pp": 10, "category": "physical"}
        ]
    },
    {
        "name": "Tortank",
        "types": ["water"],
        "stats": {
            "hp": 79,
            "attack": 83,
            "defense": 100,
            "special_attack": 85,
            "special_defense": 105,
            "speed": 78
        },
        "moves": [
            {"name": "Hydro Pump", "type": "water", "power": 110, "accuracy": 80, "pp": 5, "category": "special"},
            {"name": "Ice Beam", "type": "ice", "power": 90, "accuracy": 100, "pp": 10, "category": "special"},
            {"name": "Skull Bash", "type": "normal", "power": 130, "accuracy": 100, "pp": 10, "category": "physical"},
            {"name": "Rain Dance", "type": "water", "power": 0, "accuracy": 100, "pp": 5, "category": "status"}
        ]
    },
    {
        "name": "Ronflex",
        "types": ["normal"],
        "stats": {
            "hp": 160,
            "attack": 110,
            "defense": 65,
            "special_attack": 65,
            "special_defense": 110,
            "speed": 30
        },
        "moves": [
            {"name": "Body Slam", "type": "normal", "power": 85, "accuracy": 100, "pp": 15, "category": "physical"},
            {"name": "Earthquake", "type": "ground", "power": 100, "accuracy": 100, "pp": 10, "category": "physical"},
            {"name": "Rest", "type": "psychic", "power": 0, "accuracy": 100, "pp": 10, "category": "status"},
            {"name": "Snore", "type": "normal", "power": 50, "accuracy": 100, "pp": 15, "category": "special"}
        ]
    }
]

# Dictionnaire pour accéder facilement aux équipes
TRAINER_TEAMS = {
    "Olga": OLGA_TEAM,
    "Aldo": ALDO_TEAM,
    "Agatha": AGATHA_TEAM,
    "Peter": PETER_TEAM,
    "Blue": BLUE_TEAM
} 