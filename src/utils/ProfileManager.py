import json
import os

class ProfileManager:
    SAVE_FILE = "save_data.json"
    
    @staticmethod
    def save_profile(data):
        try:
            with open(ProfileManager.SAVE_FILE, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    @staticmethod
    def load_profile():
        try:
            if os.path.exists(ProfileManager.SAVE_FILE):
                with open(ProfileManager.SAVE_FILE, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return None
            
    @staticmethod
    def create_new_profile(trainer_name):
        data = {
            "trainer_name": trainer_name,
            "pokedex": {},
            "score": 0
        }
        return ProfileManager.save_profile(data) 