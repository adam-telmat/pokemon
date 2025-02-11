import requests
from enum import Enum

class PokemonTypeUtils:
    BASE_API_URL = "https://pokeapi.co/api/v2/type/"
    
    @staticmethod
    def get_all_types():
        """Récupère tous les types depuis l'API"""
        try:
            response = requests.get(PokemonTypeUtils.BASE_API_URL)
            if response.status_code == 200:
                data = response.json()
                return [type_data['name'] for type_data in data['results']]
            else:
                raise Exception("Impossible de récupérer les types")
        except Exception as e:
            print(f"Erreur lors de la récupération des types: {e}")
            return []

    @staticmethod
    def get_type_effectiveness(attack_type, defense_type):
        """Récupère les multiplicateurs de dégâts entre types"""
        try:
            response = requests.get(f"{PokemonTypeUtils.BASE_API_URL}{attack_type}")
            if response.status_code == 200:
                data = response.json()
                damage_relations = data['damage_relations']
                
                # Vérifier les différentes relations de dégâts
                if defense_type in [t['name'] for t in damage_relations['double_damage_to']]:
                    return 2.0
                elif defense_type in [t['name'] for t in damage_relations['half_damage_to']]:
                    return 0.5
                elif defense_type in [t['name'] for t in damage_relations['no_damage_to']]:
                    return 0.0
                return 1.0
            else:
                return 1.0
        except Exception as e:
            print(f"Erreur lors de la récupération des efficacités: {e}")
            return 1.0

class PokemonType(Enum):
    NORMAL = "Normal"
    FEU = "Feu"
    EAU = "Eau"
    PLANTE = "Plante"
    ELECTRIK = "Electrik"
    GLACE = "Glace"
    COMBAT = "Combat"
    POISON = "Poison"
    SOL = "Sol"
    VOL = "Vol"
    PSY = "Psy"
    INSECTE = "Insecte"
    ROCHE = "Roche"
    SPECTRE = "Spectre"
    DRAGON = "Dragon"
    TENEBRES = "Ténèbres"
    ACIER = "Acier"
    FEE = "Fée" 