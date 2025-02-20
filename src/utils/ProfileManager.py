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
            "score": 0,
            "defeated_trainers": {
                "Olga": False,
                "Aldo": False,
                "Agatha": False,
                "Peter": False,
                "Blue": False
            },
            "current_team": [],  # Liste des Pokémon de l'équipe actuelle
            "badges": 0  # Nombre de badges (dresseurs battus)
        }
        return ProfileManager.save_profile(data)
    
    @staticmethod
    def update_defeated_trainer(trainer_name):
        """Met à jour le statut d'un dresseur battu"""
        profile = ProfileManager.load_profile()
        if profile:
            profile["defeated_trainers"][trainer_name] = True
            profile["badges"] += 1
            return ProfileManager.save_profile(profile)
        return False
    
    @staticmethod
    def get_next_trainer():
        """Retourne le prochain dresseur à affronter"""
        profile = ProfileManager.load_profile()
        if profile:
            trainer_order = ["Olga", "Aldo", "Agatha", "Peter", "Blue"]
            for trainer in trainer_order:
                if not profile["defeated_trainers"][trainer]:
                    return trainer
        return None
    
    @staticmethod
    def can_challenge_blue():
        """Vérifie si le joueur peut affronter Blue (tous les autres battus)"""
        profile = ProfileManager.load_profile()
        if profile:
            return all(profile["defeated_trainers"][t] for t in ["Olga", "Aldo", "Agatha", "Peter"])
        return False 