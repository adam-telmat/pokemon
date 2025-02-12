import pygame

from game import Game
import os


print("Répertoire courant :", os.getcwd())


pygame.init()

if __name__ == "__main__":
    game = Game()
    game.run()