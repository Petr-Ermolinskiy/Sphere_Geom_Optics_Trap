import os
import pygame
from pygame_ui.menu import Menu

from constants import WIDTH, HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sphere in the Optical Trap: Geometrical Optics")
    
    # set the icon logo
    icon = pygame.image.load(os.path.join(os.getcwd(), "logo.png"))
    pygame.display.set_icon(icon)

    # Create and run the menu
    menu = Menu(screen)
    menu.run_menu()

if __name__ == "__main__":
    main()
