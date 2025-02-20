from gui.menu.main_menu import MainMenu
from gui.menu.game_menu import GameMenu
from utils.ProfileManager import ProfileManager
from gui.menu.league_selection import LeagueSelection
from gui.menu.pokemon_selection import PokemonSelection
from gui.menu.team_order import TeamOrderMenu
from gui.battle.battle_scene import BattleScene
from utils.SpriteManager import SpriteManager

def main():
    # Initialiser le gestionnaire de sprites au démarrage
    sprite_manager = SpriteManager()
    
    menu = MainMenu()
    running = True
    current_profile = None
    current_menu = "MAIN"
    game_menu = None  # Pour garder une référence au menu de jeu
    selected_team = None  # Pour stocker l'équipe sélectionnée
    
    while running:
        if current_menu == "MAIN":
            choice = menu.run()
            
            if choice == "NEW_GAME":
                trainer_name = menu.ask_trainer_name()
                if trainer_name:
                    ProfileManager.create_new_profile(trainer_name)
                    game_menu = GameMenu(menu.screen, sprite_manager)
                    current_menu = "GAME"  # Passer au menu de jeu
                    
            elif choice == "LOAD_GAME":
                current_profile = ProfileManager.load_profile()
                if current_profile:
                    game_menu = GameMenu(menu.screen, sprite_manager, current_profile)
                    current_menu = "GAME"  # Passer au menu de jeu
                else:
                    menu.show_message("Aucune sauvegarde trouvée !")
            
            elif choice == "QUIT":
                running = False
        
        elif current_menu == "GAME":
            game_choice = game_menu.run()
            
            if game_choice == "BACK":
                current_menu = "MAIN"
            elif game_choice == "QUIT":
                running = False
            elif game_choice == "POKEMON_SELECTION":
                # Sélection des Pokémon
                pokemon_selection = PokemonSelection(menu.screen)
                pokemon_names = pokemon_selection.run()
                
                if pokemon_names and pokemon_names != "BACK":
                    # Ordre de l'équipe
                    team_order = TeamOrderMenu(menu.screen, pokemon_names)
                    order_result = team_order.run()
                    
                    if order_result == "BACK":
                        selected_team = team_order.team  # Sauvegarder l'équipe ordonnée
                        current_menu = "GAME"
            
            elif game_choice == "START_BATTLE":
                # Afficher d'abord la sélection des dresseurs
                league_screen = LeagueSelection(menu.screen)
                league_result = league_screen.run()
                
                if league_result == "BACK":
                    current_menu = "GAME"
                elif isinstance(league_result, dict):
                    # Un dresseur a été sélectionné
                    battle_scene = BattleScene(
                        screen=menu.screen,
                        player_team=[pokemon["name"] for pokemon in selected_team],
                        opponent=league_result["trainer"]
                    )
                    battle_result = battle_scene.run()
                    if battle_result == "BACK":
                        current_menu = "GAME"

        elif current_menu == "LEAGUE":
            result = league_screen.run()
            if isinstance(result, dict) and result["action"] == "POKEMON_SELECTION":
                # Aller à la sélection des Pokémon
                pokemon_selection = PokemonSelection(menu.screen)
                selected_pokemon = pokemon_selection.run()
                
                if selected_pokemon and selected_pokemon != "BACK":
                    # Aller à l'ordre de l'équipe
                    team_order = TeamOrderMenu(menu.screen, selected_pokemon)
                    order_result = team_order.run()
                    
                    if order_result == "ORDER_CONFIRMED":
                        # Lancer le combat
                        battle_scene = BattleScene(
                            screen=menu.screen,
                            player_team=selected_pokemon,
                            opponent=result["opponent"]
                        )
                        current_menu = battle_scene.run()
                    else:
                        current_menu = "LEAGUE"
                else:
                    current_menu = "LEAGUE"

if __name__ == "__main__":
    main() 