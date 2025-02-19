from gui.menu.main_menu import MainMenu
from gui.menu.game_menu import GameMenu
from utils.ProfileManager import ProfileManager

def main():
    menu = MainMenu()
    running = True
    current_profile = None
    
    while running:
        choice = menu.run()
        
        if choice == "NEW_GAME":
            # Demander le pseudo
            trainer_name = menu.ask_trainer_name()
            if trainer_name:
                # Créer nouveau profil
                ProfileManager.create_new_profile(trainer_name)
                # Créer et lancer le sous-menu de jeu
                game_menu = GameMenu(menu.screen)
                game_choice = game_menu.run()
                
        elif choice == "LOAD_GAME":
            # Charger le profil existant
            current_profile = ProfileManager.load_profile()
            if current_profile:
                game_menu = GameMenu(menu.screen, current_profile)
                game_choice = game_menu.run()
            else:
                menu.show_message("Aucune sauvegarde trouvée !")
                
        elif choice == "QUIT":
            running = False

if __name__ == "__main__":
    main() 