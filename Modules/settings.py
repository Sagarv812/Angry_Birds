import pygame, sys, time

size = width, height = 1920, 1080
flags = pygame.FULLSCREEN
black = 0, 0, 0

def ScaleImage(image):
    return pygame.transform.scale(image,(50,50))

def ScaleBiggerImage(image):
    return pygame.transform.scale(image,(200,200))