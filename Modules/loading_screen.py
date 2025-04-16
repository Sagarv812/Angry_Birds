import pygame as py, sys, time
import os
import Modules.settings as settings

clock = py.time.Clock()

def loadScreen(screen):
    
    logo = py.image.load("Media/logo.png")
    w = logo.get_width()
    h = logo.get_height()

    #Colors
    BG_COLOR = (30,30,30)
    BAR_COLOR = (0, 200, 0)
    BORDER_COLOUR = (255, 255, 255)

    #Positioning
    image_x = int(settings.width/2-w/2)
    image_y = int(settings.height/2-h/2)
    logo_rect = logo.get_rect()
    logo_rect.topleft = (image_x, image_y-150)
    bar_size = (500, 50)
    bar_position = (logo_rect.centerx-bar_size[0]/2, logo_rect.bottom+20)

    progress = 0
    while True:
        
        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()

        screen.fill(BG_COLOR)
        inner_width = int(bar_size[0]*progress/100)
        py.draw.rect(screen, BORDER_COLOUR, (*bar_position, *bar_size), 2)
        py.draw.rect(screen, BAR_COLOR, (bar_position[0]+1, bar_position[1]+1, inner_width-2, bar_size[1]-2))
        screen.blit(logo, logo_rect)

        progress += 1
        time.sleep(0.02)
        if progress >100:
            settings.state = "menu"
            break

        py.display.flip()
    