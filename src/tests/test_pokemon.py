import sys
import os

# Ajouter le dossier src au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.Pokemon import Pokemon
from models.PokemonType import PokemonType, PokemonTypeUtils

def test_pokemon():
    # Créer un Pokémon
    pikachu = Pokemon("pikachu", ["electric"], 100, 5, 55, 40)
    
    # Vérifier que les sprites sont chargés
    print("\nTest des sprites:")
    print(f"Sprite avant: {pikachu.front_sprite_url}")
    print(f"Sprite arrière: {pikachu.back_sprite_url}")

    # Tester les types
    print("\nTest des types:")
    types = PokemonTypeUtils.get_all_types()
    print(f"Types disponibles: {types}")

    # Tester les efficacités
    print("\nTest des efficacités:")
    effectiveness = PokemonTypeUtils.get_type_effectiveness("electric", "water")
    print(f"Efficacité Électrique vs Eau: {effectiveness}")

    # Tester les dégâts
    print("\nTest des dégâts:")
    damage = pikachu.take_damage(20)
    print(f"Dégâts subis: {damage}")
    print(f"PV restants: {pikachu.current_hp}")

if __name__ == "__main__":
    test_pokemon() 