import pygame

class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

    def draw_main_menu(self):
        """
        Renders the main menu on the provided Pygame screen.
        Menu options include wild encounters, gym battles, buying items, adding Pokémon,
        viewing the Pokédex, and exiting the game.
        """
        menu_items = [
            "1. Wild Encounter",
            "2. Gym Battle",
            "3. Buy Items",
            "4. Add Pokémon",
            "5. View Pokédex",
            "ESC. Exit Game"
        ]
        # Fill the background with a light blue shade.
        self.screen.fill((200, 200, 255))
        # Draw each menu item with some spacing.
        for idx, item in enumerate(menu_items):
            text_surface = self.font_large.render(item, True, (0, 0, 0))
            self.screen.blit(text_surface, (50, 50 + idx * 60))

    def display_shop(self, items, money):
        """
        Displays a basic shop interface.
        Currently, this outputs to the console and pauses briefly, but you can expand it to include buttons,
        images, or more advanced UI elements.
        """
        print("Welcome to the Shop!")
        print(f"Your money: {money}")
        for item, price in items.items():
            print(f"{item.capitalize()}: {price} coins")
        # A simple delay to simulate a shop display.
        pygame.time.delay(1500)
