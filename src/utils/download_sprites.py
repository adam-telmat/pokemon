import requests
import os
import shutil

def download_sprites():
    # Supprimer le dossier sprites s'il existe
    if os.path.exists("src/assets/sprites"):
        shutil.rmtree("src/assets/sprites")
    
    # Créer les nouveaux dossiers
    os.makedirs("src/assets/sprites/static", exist_ok=True)
    os.makedirs("src/assets/sprites/animated", exist_ok=True)
    
    # Liste des IDs à télécharger
    pokemon_ids = [
        # Pokémon disponibles pour le joueur (28 Pokémon)
        25, 4, 1, 7,      # Pikachu, Salamèche, Bulbizarre, Carapuce
        95, 120, 54, 56,  # Onix, Staross, Psykokwak, Férosinge
        39, 52, 16, 19,   # Rondoudou, Miaouss, Roucool, Rattata
        21, 23, 27, 35,   # Piafabec, Abo, Sabelette, Mélofée
        37, 50, 66, 74,   # Goupix, Taupiqueur, Machoc, Racaillou
        92, 98, 67, 72,   # Fantominus, Krabby, Machopeur, Tentacool
        100, 43, 46, 48,  # Voltorbe, Mystherbe, Paras, Venonat

        # Olga (2 Pokémon)
        131, 144,  # Lokhlass, Artikodin

        # Aldo (3 Pokémon)
        68, 107, 95,  # Mackogneur, Tygnon, Onix

        # Agatha (4 Pokémon)
        94, 24, 42, 93,  # Ectoplasma, Arbok, Nosferalto, Spectrum

        # Peter (5 Pokémon)
        149, 130, 6, 142, 149,  # Dracolosse, Leviator, Dracaufeu, Ptera, Dracolosse

        # Blue (6 Pokémon)
        18, 65, 59, 103, 9, 143  # Roucarnage, Alakazam, Arcanin, Exeggutor, Tortank, Ronflex
    ]
    
    total = len(pokemon_ids) * 4  # 4 sprites par Pokémon
    current = 0
    
    for pokemon_id in pokemon_ids:
        # URLs des sprites
        urls = {
            f"src/assets/sprites/static/{pokemon_id}_front.png": 
                f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png",
            f"src/assets/sprites/static/{pokemon_id}_back.png":
                f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/{pokemon_id}.png",
            f"src/assets/sprites/animated/{pokemon_id}_front.gif":
                f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/{pokemon_id}.gif",
            f"src/assets/sprites/animated/{pokemon_id}_back.gif":
                f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/back/{pokemon_id}.gif"
        }
        
        for save_path, url in urls.items():
            try:
                current += 1
                print(f"Téléchargement {current}/{total} : {save_path}")
                
                response = requests.get(url)
                if response.status_code == 200:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                else:
                    print(f"Erreur {response.status_code} pour {url}")
                    
            except Exception as e:
                print(f"Erreur lors du téléchargement de {url}: {e}")

if __name__ == "__main__":
    download_sprites() 