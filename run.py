import pygame
from pygame.locals import *

from earth_defense import *
from classes import *

if __name__ == '__main__':
    pygame.init()

    #game interface initialization
    DISPLAY_WIDTH = 900
    DISPLAY_HEIGHT = 600
    game_interface = Interface(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    #game_interface.set_background(main_menu_background)
    #game_interface.set_caption("Earth Defense")

    #Main initialization
    main_game = Main(game_interface)
    main_game.main_menu_screen()

    #exiting game
    pygame.quit()
    quit()

