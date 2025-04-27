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
PINK = (245, 174, 183)
WOOD_BROWN = (193,107,30)
STONE_GRAY = (161,153,140)
ICE_BLUE = (119,209,244)
DARK_GRAY = (31,31,31)
ROPE_BROWN = (48,22,8)
state = "select"
winner = "PLAYER1"
pauseTime = 0

sfxVolume = 0.75
musicVolume = 0.75

clock = pygame.time.Clock()

bg = pygame.image.load("Media/Menu_background.jpg")

bg1 = pygame.image.load("Media/background1.jpg")

red = pygame.image.load("Media/Birds/red1.png")
chuck = pygame.image.load("Media/Birds/chuck1.png")
bomb = pygame.image.load("Media/Birds/bomb1.png")
blue = pygame.image.load("Media/Birds/blue1.png")
stella = pygame.image.load("Media/Birds/stella1.png")

WOOD = [
    pygame.image.load("Media/Blocks/woodblock1.png"),
    pygame.image.load("Media/Blocks/woodblock2.png"),
    pygame.image.load("Media/Blocks/woodblock4.png"),
    pygame.image.load("Media/Blocks/woodblock5.png"),
    pygame.image.load("Media/Blocks/wood_3.png")
]

ICE = [
    pygame.image.load("Media/Blocks/iceblock1.png"),
    pygame.image.load("Media/Blocks/iceblock2.png"),
    pygame.image.load("Media/Blocks/iceblock3.png"),
    pygame.image.load("Media/Blocks/iceblock4.png"),
    pygame.image.load("Media/Blocks/iceblock5.png")
]

STONE = [
    pygame.image.load("Media/Blocks/stone1.png"),
    pygame.image.load("Media/Blocks/stone2.png"),
    pygame.image.load("Media/Blocks/stone3.png"),
    pygame.image.load("Media/Blocks/stone4.png"),
    pygame.image.load("Media/Blocks/stone5.png")
]


buttonHoverSound = pygame.mixer.Sound("Media/audio/button_hover.mp3")
buttonClickSound = pygame.mixer.Sound("Media/audio/button_click1.mp3")
menu_bg = pygame.image.load("Media/banner.png")

def ScaleImage(image):
    return pygame.transform.scale(image,(50,50))

def ScaleBiggerImage(image):
    return pygame.transform.scale(image,(200,200))