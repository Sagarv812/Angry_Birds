import pygame, sys, time

size = width, height = 1920, 1080
flags = pygame.FULLSCREEN
black = 0, 0, 0
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
ifAudio = True
player1 = "Player 1"
player2 = "Player 2"
bigFont = pygame.font.Font("Media/angrybirds-regular.ttf", 100)
RED = (185,15,18)
YELLOW = (251,204,22)
BLUE = (11, 76, 227)
GREEN = (19, 212, 70)

def ScaleImage(image):
    return pygame.transform.scale(image,(50,50))

def ScaleBiggerImage(image):
    return pygame.transform.scale(image,(200,200))