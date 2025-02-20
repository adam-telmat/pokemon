# Données des 28 Pokémon du jeu
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
    "psyduck": {"name": "Psyduck", "types": ["water"], "level": 50, "max_hp": 120,
                "attack": 50, "defense": 45, "special_attack": 60, "special_defense": 55,
                "speed": 55, "moves": ["tackle", "water-gun", "confusion", "disable"]},
    "mankey": {"name": "Mankey", "types": ["fighting"], "level": 50, "max_hp": 115,
               "attack": 80, "defense": 35, "special_attack": 35, "special_defense": 45,
               "speed": 70, "moves": ["scratch", "karate-chop", "low-kick", "focus-energy"]},
    "jigglypuff": {"name": "Jigglypuff", "types": ["normal", "fairy"], "level": 50, "max_hp": 160,
                   "attack": 45, "defense": 20, "special_attack": 45, "special_defense": 25,
                   "speed": 20, "moves": ["pound", "sing", "defense-curl", "doubleslap"]},
    "meowth": {"name": "Meowth", "types": ["normal"], "level": 50, "max_hp": 110,
               "attack": 45, "defense": 35, "special_attack": 40, "special_defense": 40,
               "speed": 90, "moves": ["scratch", "bite", "pay-day", "growl"]},
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
    "diglett": {"name": "Diglett", "types": ["ground"], "level": 50, "max_hp": 90,
                "attack": 55, "defense": 25, "special_attack": 35, "special_defense": 45,
                "speed": 95, "moves": ["scratch", "sand-attack", "growl", "dig"]},
    "machop": {"name": "Machop", "types": ["fighting"], "level": 50, "max_hp": 110,
               "attack": 70, "defense": 50, "special_attack": 35, "special_defense": 35,
               "speed": 45, "moves": ["karate-chop", "low-kick", "focus-energy", "seismic-toss"]},
    "geodude": {"name": "Geodude", "types": ["rock", "ground"], "level": 50, "max_hp": 115,
                "attack": 80, "defense": 100, "special_attack": 30, "special_defense": 30,
                "speed": 20, "moves": ["tackle", "rock-throw", "harden", "earthquake"]},
    "gastly": {"name": "Gastly", "types": ["ghost", "poison"], "level": 50, "max_hp": 100,
               "attack": 35, "defense": 30, "special_attack": 100, "special_defense": 35,
               "speed": 80, "moves": ["lick", "spite", "shadow-ball", "hypnosis"]},
    "krabby": {"name": "Krabby", "types": ["water"], "level": 50, "max_hp": 110,
               "attack": 70, "defense": 50, "special_attack": 40, "special_defense": 40,
               "speed": 50, "moves": ["bubble", "vice-grip", "mud-slap", "crabhammer"]},
    "machoke": {"name": "Machoke", "types": ["fighting"], "level": 50, "max_hp": 115,
                "attack": 80, "defense": 60, "special_attack": 40, "special_defense": 40,
                "speed": 50, "moves": ["karate-chop", "low-kick", "seismic-toss", "bulk-up"]},
    "tentacool": {"name": "Tentacool", "types": ["water", "poison"], "level": 50, "max_hp": 105,
                  "attack": 40, "defense": 35, "special_attack": 50, "special_defense": 100,
                  "speed": 70, "moves": ["acid", "bubble", "wrap", "water-gun"]},
    "voltorb": {"name": "Voltorb", "types": ["electric"], "level": 50, "max_hp": 105,
                "attack": 50, "defense": 40, "special_attack": 55, "special_defense": 55,
                "speed": 100, "moves": ["tackle", "spark", "electro-ball", "swift"]},
    "oddish": {"name": "Oddish", "types": ["grass", "poison"], "level": 50, "max_hp": 120,
               "attack": 50, "defense": 55, "special_attack": 75, "special_defense": 65,
               "speed": 30, "moves": ["absorb", "poison-powder", "acid", "sleep-powder"]},
    "paras": {"name": "Paras", "types": ["bug", "grass"], "level": 50, "max_hp": 115,
              "attack": 70, "defense": 55, "special_attack": 45, "special_defense": 55,
              "speed": 25, "moves": ["scratch", "stun-spore", "leech-life", "spore"]},
    "venonat": {"name": "Venonat", "types": ["bug", "poison"], "level": 50, "max_hp": 125,
                "attack": 55, "defense": 50, "special_attack": 40, "special_defense": 55,
                "speed": 45, "moves": ["tackle", "disable", "confusion", "poison-powder"]}
}

# Dictionnaire pour les noms français
POKEMON_NAMES_FR = {
    "pikachu": "Pikachu",
    "charmander": "Salamèche",
    "bulbasaur": "Bulbizarre",
    "squirtle": "Carapuce",
    "onix": "Onix",
    "staryu": "Staross",
    "psyduck": "Psykokwak",
    "mankey": "Férosinge",
    "jigglypuff": "Rondoudou",
    "meowth": "Miaouss",
    "pidgey": "Roucool",
    "rattata": "Rattata",
    "spearow": "Piafabec",
    "ekans": "Abo",
    "sandshrew": "Sabelette",
    "clefairy": "Mélofée",
    "vulpix": "Goupix",
    "diglett": "Taupiqueur",
    "machop": "Machoc",
    "geodude": "Racaillou",
    "gastly": "Fantominus",
    "krabby": "Krabby",
    "machoke": "Machopeur",
    "tentacool": "Tentacool",
    "voltorb": "Voltorbe",
    "oddish": "Mystherbe",
    "paras": "Paras",
    "venonat": "Mimitoss"
}

# Dictionnaire pour les attaques en français
MOVE_NAMES_FR = {
    # Attaques Normal
    "tackle": "Charge",
    "scratch": "Griffe",
    "quick-attack": "Vive-Attaque",
    "pound": "Écras'Face",
    "growl": "Rugissement",
    "defense-curl": "Boul'Armure",
    "doubleslap": "Double-Claque",
    "bite": "Morsure",
    "sand-attack": "Jet de Sable",
    "leer": "Regard Médusant",
    "fury-attack": "Furie",
    "focus-energy": "Puissance",
    "swift": "Météores",
    "vice-grip": "Force Poigne",
    
    # Attaques Électrik
    "thunder-shock": "Éclair",
    "electro-ball": "Boule Élek",
    "spark": "Étincelle",
    
    # Attaques Feu
    "ember": "Flammèche",
    "flamethrower": "Lance-Flammes",
    
    # Attaques Plante
    "vine-whip": "Fouet Lianes",
    "razor-leaf": "Tranch'Herbe",
    "absorb": "Vol-Vie",
    "stun-spore": "Para-Spore",
    "sleep-powder": "Poudre Dodo",
    "leech-life": "Vampirisme",
    "spore": "Spore",
    
    # Attaques Eau
    "water-gun": "Pistolet à O",
    "bubble": "Écume",
    "crabhammer": "Pince-Masse",
    
    # Attaques Combat
    "karate-chop": "Poing-Karaté",
    "low-kick": "Balayage",
    "seismic-toss": "Frappe Atlas",
    "bulk-up": "Gonflette",
    
    # Attaques Poison
    "poison-sting": "Dard-Venin",
    "acid": "Acide",
    "poison-powder": "Poudre Toxik",
    
    # Attaques Sol/Roche
    "rock-throw": "Jet-Pierres",
    "earthquake": "Séisme",
    "mud-slap": "Coud'Boue",
    "dig": "Tunnel",
    
    # Attaques Spectre/Psy
    "lick": "Léchouille",
    "spite": "Dépit",
    "shadow-ball": "Ball'Ombre",
    "hypnosis": "Hypnose",
    "confusion": "Choc Mental",
    "disable": "Entrave",
    
    # Autres
    "iron-tail": "Queue de Fer",
    "pay-day": "Jackpot",
    "wrap": "Ligotage",
    "glare": "Intimidation",
    "tail-whip": "Mimi-Queue",
    "harden": "Armure"
}

# Dictionnaire pour les types en français
TYPE_NAMES_FR = {
    "normal": "Normal",
    "fire": "Feu",
    "water": "Eau",
    "grass": "Plante",
    "electric": "Électrik",
    "ice": "Glace",
    "fighting": "Combat",
    "poison": "Poison",
    "ground": "Sol",
    "flying": "Vol",
    "psychic": "Psy",
    "bug": "Insecte",
    "rock": "Roche",
    "ghost": "Spectre",
    "dragon": "Dragon",
    "dark": "Ténèbres",
    "steel": "Acier",
    "fairy": "Fée"
}

# Il faut ajouter un dictionnaire de correspondance nom français -> nom anglais
POKEMON_NAMES = {
    "Salamèche": "Charmander",
    "Carapuce": "Squirtle",
    "Bulbizarre": "Bulbasaur",
    "Paras": "Paras",  # Celui-ci marche car même nom
    "Tentacool": "Tentacool",  # Celui-ci devrait marcher aussi car même nom
    # etc...
} 