import pygame, numpy, sys, time
import Modules.birds as bird
import Modules.flying_mechanism as fly
import Modules.settings as settings
import Modules.loading_screen as load
import Modules.player_names as Players
import Main_Menu as menu
import Modules.bird_select as selection
import random

pygame.init()


size = width, height = 1920, 1080
speed = [10,-10]
black = 0, 0, 0
screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("ANGRY BIRDS")
# red = pygame.image.load(bird.birds["Red"][0])
# red = ScaleImage(red)
# birdrect = red.get_rect()
# birdrect.topleft = (500,500)

clock = pygame.time.Clock()

while True:

    if settings.state == "load":
        load.loadScreen(screen)
    elif settings.state == "menu":
        menu.menu(screen)
    elif settings.state == "naming":
        Players.naming(screen)
    elif settings.state == "select": 
        for i in range(1,3):
            selection.chooseBird(screen, i)
            if settings.state == "naming":
                break
    else:
        break


