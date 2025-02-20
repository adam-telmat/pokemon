import pygame
import os

class BattleSounds:
    def __init__(self):
        self.sounds = {}
        self.load_sounds()
    
    def load_sounds(self):
        """Charge tous les sons du combat"""
        sound_dir = os.path.join("src", "assets", "sounds")
        try:
            self.sounds = {
                "hit": pygame.mixer.Sound(os.path.join(sound_dir, "hit.wav")),
                "critical": pygame.mixer.Sound(os.path.join(sound_dir, "critical.wav")),
                "miss": pygame.mixer.Sound(os.path.join(sound_dir, "miss.wav")),
                "victory": pygame.mixer.Sound(os.path.join(sound_dir, "victory.wav")),
                "defeat": pygame.mixer.Sound(os.path.join(sound_dir, "defeat.wav"))
            }
        except Exception as e:
            print(f"Erreur lors du chargement des sons: {e}") 