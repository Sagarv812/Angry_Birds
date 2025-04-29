import pygame

pygame.init()

import Modules.settings as settings
import Modules.loading_screen as load
import Modules.player_names as Players
import Modules.Main_Menu as menu
import Modules.bird_select as selection
import Modules.play as Play
import Modules.winner as Winner
import Modules.theme_select as Theme


info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w,info.current_h),settings.flags) #Initializing Display
pygame.display.set_caption("ANGRY BIRDS")

clock = pygame.time.Clock()

while True:
    settings.width, settings.height = screen.get_size()

    if settings.state == "load":
        load.loadScreen(screen)
    elif settings.state == "menu":
        menu.menu(screen)
    elif settings.state == "naming":
        Players.naming(screen)
    elif settings.state == "theme":
        Theme.selectTheme(screen)
    elif settings.state == "select": 
        for i in range(1,3):
            selection.chooseBird(screen, i)
            if settings.state == "naming":
                break
    elif settings.state == "play":
        Play.playGame(screen)
    else:
        Winner.winnerAnimation(screen)
        break


