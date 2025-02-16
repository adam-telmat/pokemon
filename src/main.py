from gui.menu.main_menu import MainMenu

def main():
    menu = MainMenu()
    choice = menu.run()
    
    if choice == "NEW_GAME":
        print("Démarrage nouvelle partie...")
    elif choice == "LOAD_GAME":
        print("Chargement partie...")
    elif choice == "OPTIONS":
        print("Options...")
    elif choice == "QUIT":
        print("Au revoir !")

if __name__ == "__main__":
    main() 