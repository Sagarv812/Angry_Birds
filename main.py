import pygame, numpy, sys, time
import Modules.birds as bird
import Modules.flying_mechanism as fly
import Modules.settings as settings
import Modules.loading_screen as load

pygame.init()


size = width, height = 1920, 1080
speed = [10,-10]
black = 0, 0, 0
screen = pygame.display.set_mode((1920,1080), settings.flags)
pygame.display.set_caption("ANGRY BIRDS")
# red = pygame.image.load(bird.birds["Red"][0])
# red = ScaleImage(red)
# birdrect = red.get_rect()
# birdrect.topleft = (500,500)

# clock = pygame.time.Clock()

load.loadScreen(screen)



