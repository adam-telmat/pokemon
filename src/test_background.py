import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test Background")

try:
    # Utiliser le bon chemin et nom de fichier
    background = pygame.image.load("src/assets/pokemon_backgroundfinale.jpg")
    # Redimensionner l'image à la taille de la fenêtre
    background = pygame.transform.scale(background, (800, 600))
    print("✅ Image chargée avec succès!")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit()

# Afficher l'image
screen.blit(background, (0, 0))
pygame.display.flip()

# Boucle pour garder la fenêtre ouverte
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 