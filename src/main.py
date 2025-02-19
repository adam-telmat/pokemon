from gui.menu.main_menu import MainMenu
from gui.menu.game_menu import GameMenu

def main():
    menu = MainMenu()
    running = True
    
    while running:
        choice = menu.run()
        
        if choice == "NEW_GAME":
            # Créer et lancer le sous-menu de jeu
            game_menu = GameMenu(menu.screen)
            game_choice = game_menu.run()
            
            # Gérer les choix du sous-menu
            if game_choice == "QUIT":
                running = False
            # On continue la boucle pour les autres choix
                
        elif choice == "LOAD_GAME":
            print("Chargement partie...")
        elif choice == "OPTIONS":
            print("Options...")
        elif choice == "QUIT":
            running = False

if __name__ == "__main__":
    main() 