import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from models.Pokemon import Pokemon

class BattleTestWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Combat Pokémon")
        
        # Créer deux Pokémon pour le test
        self.pokemon1 = Pokemon("pikachu", ["electric"], 100, 5, 55, 40)
        self.pokemon2 = Pokemon("charizard", ["fire", "flying"], 120, 5, 60, 45)
        
        # Créer le canvas pour l'affichage
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        
        # Charger et afficher les sprites
        self.load_sprites()
        
        # Ajouter des boutons de test
        self.add_buttons()
        
    def load_sprites(self):
        # Charger les images depuis les URLs
        response1 = requests.get(self.pokemon1.back_sprite_url)
        response2 = requests.get(self.pokemon2.front_sprite_url)
        
        # Convertir en images Tkinter
        img1 = Image.open(BytesIO(response1.content))
        img2 = Image.open(BytesIO(response2.content))
        
        # Agrandir les images (×3)
        img1 = img1.resize((img1.width * 3, img1.height * 3))
        img2 = img2.resize((img2.width * 3, img2.height * 3))
        
        self.sprite1 = ImageTk.PhotoImage(img1)
        self.sprite2 = ImageTk.PhotoImage(img2)
        
        # Afficher les sprites
        self.canvas.create_image(200, 400, image=self.sprite1)  # Pokémon joueur
        self.canvas.create_image(600, 200, image=self.sprite2)  # Pokémon adversaire
        
        # Afficher les barres de vie
        self.draw_health_bars()
        
    def draw_health_bars(self):
        # Barre de vie Pokémon 1
        self.canvas.create_rectangle(100, 450, 300, 470, fill='white')
        self.canvas.create_rectangle(100, 450, 300 * (self.pokemon1.current_hp/self.pokemon1.max_hp), 470, fill='green')
        
        # Barre de vie Pokémon 2
        self.canvas.create_rectangle(500, 50, 700, 70, fill='white')
        self.canvas.create_rectangle(500, 50, 700 * (self.pokemon2.current_hp/self.pokemon2.max_hp), 70, fill='green')
        
    def add_buttons(self):
        # Bouton d'attaque
        attack_btn = tk.Button(self.root, text="Attaque Test", command=self.test_attack)
        attack_btn.pack(pady=10)
        
    def test_attack(self):
        # Simuler une attaque
        self.pokemon2.take_damage(20)
        # Redessiner les barres de vie
        self.draw_health_bars()

def main():
    root = tk.Tk()
    app = BattleTestWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 