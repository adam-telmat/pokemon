import requests
from PIL import Image
from io import BytesIO
import random

class Pokemon:
    BASE_API_URL = "https://pokeapi.co/api/v2/pokemon/"
    MOVE_API = "https://pokeapi.co/api/v2/move/"
    AILMENT_API = "https://pokeapi.co/api/v2/move-ailment/"
    CATEGORY_API = "https://pokeapi.co/api/v2/move-category/"
    DAMAGE_CLASS_API = "https://pokeapi.co/api/v2/move-damage-class/"

    def __init__(self, name):
        self.name = name.lower()
        self.status_condition = None  # Pour les effets d'état
        self.load_from_api()  # On charge tout depuis l'API

    def load_from_api(self):
        try:
            # Données de base du Pokémon
            response = requests.get(f"{self.BASE_API_URL}{self.name}")
            if response.status_code == 200:
                data = response.json()
                
                # Infos de base
                self.pokedex_id = data['id']
                self.height = data['height'] / 10
                self.weight = data['weight'] / 10
                
                # Stats depuis l'API
                stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
                self.max_hp = stats['hp']
                self.current_hp = stats['hp']
                self.attack = stats['attack']
                self.defense = stats['defense']
                self.special_attack = stats['special-attack']
                self.special_defense = stats['special-defense']
                self.speed = stats['speed']
                
                # Types et mouvements
                self.types = [t['type']['name'] for t in data['types']]
                self.moves = []
                for move in data['moves'][:4]:  # On prend les 4 premiers moves
                    move_url = move['move']['url']
                    move_response = requests.get(move_url)
                    if move_response.status_code == 200:
                        move_data = move_response.json()
                        self.moves.append({
                            'name': move_data['name'],
                            'power': move_data.get('power', 0),
                            'accuracy': move_data.get('accuracy', 100),
                            'pp': move_data.get('pp', 0),
                            'type': move_data['type']['name'],
                            'damage_class': move_data['damage_class']['name']  # physical/special
                        })
                
                # Sprites animés (Gen 5)
                sprites = data['sprites']
                versions = sprites.get('versions', {})
                bw = versions.get('generation-v', {}).get('black-white', {})
                
                self.animated_front = bw.get('animated', {}).get('front_default')
                self.animated_back = bw.get('animated', {}).get('back_default')
                
                # Sprites statiques (fallback)
                self.front_sprite_url = sprites['front_default']
                self.back_sprite_url = sprites['back_default']
                
                # Capacités
                self.abilities = [a['ability']['name'] for a in data['abilities']]
                
                # Récupérer les lieux où trouver le Pokémon
                species_url = data['species']['url']
                species_response = requests.get(species_url)
                if species_response.status_code == 200:
                    species_data = species_response.json()
                    
                    # Récupérer les encounters
                    encounters_url = f"https://pokeapi.co/api/v2/pokemon/{self.pokedex_id}/encounters"
                    encounters_response = requests.get(encounters_url)
                    if encounters_response.status_code == 200:
                        encounters_data = encounters_response.json()
                        self.locations = []
                        for encounter in encounters_data:
                            self.locations.append({
                                'location': encounter['location_area']['name'],
                                'version': [v['version']['name'] for v in encounter['version_details']],
                                'chance': encounter['version_details'][0]['max_chance']
                            })
                    
                    # Informations supplémentaires de l'espèce
                    self.growth_rate = species_data['growth_rate']['name']
                    self.habitat = species_data.get('habitat', {}).get('name', 'unknown')
                    self.is_legendary = species_data['is_legendary']
                    self.is_mythical = species_data['is_mythical']
                
                return True
        except Exception as e:
            print(f"Erreur: {e}")
            return False

    def is_alive(self):
        return self.current_hp > 0

    def take_damage(self, damage):
        actual_damage = max(1, damage - self.defense)
        self.current_hp = max(0, self.current_hp - actual_damage)
        return actual_damage

    def load_move_with_effects(self, move_name):
        """Charge une attaque avec tous ses effets"""
        response = requests.get(f"{self.MOVE_API}{move_name}")
        if response.status_code == 200:
            move_data = response.json()
            
            # Données de base
            move = {
                'name': move_data['name'],
                'power': move_data.get('power', 0),
                'accuracy': move_data.get('accuracy', 100),
                'pp': move_data.get('pp', 0),
                'type': move_data['type']['name'],
                'damage_class': move_data['damage_class']['name'],
                
                # Effets secondaires
                'effect_chance': move_data.get('effect_chance', 0),
                'ailment': move_data.get('meta', {}).get('ailment', {}).get('name', None),
                'ailment_chance': move_data.get('meta', {}).get('ailment_chance', 0),
                
                # Cibles
                'target': move_data['target']['name'],
                
                # Description
                'effect': next((e['effect'] for e in move_data['effect_entries'] 
                              if e['language']['name'] == 'en'), '')
            }
            return move
        return None

    def apply_status_condition(self, ailment, chance):
        """Applique un effet d'état (paralysie, poison, etc.)"""
        if random.randint(1, 100) <= chance:
            # Charger les détails de l'effet
            response = requests.get(f"{self.AILMENT_API}{ailment}")
            if response.status_code == 200:
                ailment_data = response.json()
                self.status_condition = {
                    'name': ailment,
                    'description': ailment_data.get('description', ''),
                    'turns': random.randint(2, 5)  # Durée aléatoire
                }
                return True
        return False

    def process_status_effects(self):
        """Applique les effets des statuts à chaque tour"""
        if not self.status_condition:
            return
        
        if self.status_condition['name'] == 'paralysis':
            if random.randint(1, 4) == 1:  # 25% de chance d'être paralysé
                return "est paralysé et ne peut pas attaquer!"
            
        elif self.status_condition['name'] == 'poison':
            damage = max(1, self.max_hp // 8)  # 1/8 des PV max
            self.take_damage(damage)
            return "subit les effets du poison!"
        
        elif self.status_condition['name'] == 'burn':
            damage = max(1, self.max_hp // 16)  # 1/16 des PV max
            self.take_damage(damage)
            return "subit les effets de la brûlure!"
        
        self.status_condition['turns'] -= 1
        if self.status_condition['turns'] <= 0:
            status = self.status_condition['name']
            self.status_condition = None
            return f"n'est plus {status}!"

    def use_move(self, move_index, target):
        """Utilise une attaque avec tous ses effets"""
        if move_index >= len(self.moves):
            return False, "Cette attaque n'existe pas!"
        
        move = self.moves[move_index]
        
        # Vérifier la paralysie
        if self.status_condition and self.status_condition['name'] == 'paralysis':
            if random.randint(1, 4) == 1:
                return False, f"{self.name} est paralysé et ne peut pas attaquer!"
        
        # Vérifier les PP
        if move['pp'] <= 0:
            return False, "Plus de PP!"
        
        move['pp'] -= 1
        
        # Vérifier la précision
        if random.randint(1, 100) > move['accuracy']:
            return False, "L'attaque a échoué!"
        
        # Calculer les dégâts
        if move['power'] > 0:
            # Obtenir la catégorie de dégâts
            damage_class_response = requests.get(f"{self.DAMAGE_CLASS_API}{move['damage_class']}")
            if damage_class_response.status_code == 200:
                damage_class_data = damage_class_response.json()
                
                # Calculer les dégâts selon la classe
                if move['damage_class'] == 'physical':
                    base_damage = move['power'] * (self.attack / target.defense)
                else:
                    base_damage = move['power'] * (self.special_attack / target.special_defense)
                    
                # Appliquer les effets d'état
                if move.get('ailment'):
                    target.apply_status_condition(move['ailment'], move['ailment_chance'])
                    
                return True, f"{self.name} utilise {move['name']}!"
        
        return True, f"{self.name} utilise {move['name']}!" 