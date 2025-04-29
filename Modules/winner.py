import pygame as py, sys
import Modules.settings as settings

def winnerAnimation(screen):
    
    scale = 2
    winnerName = settings.bigFont.render(settings.winner+"  WINS!!",True,settings.RED)
    winnerName = py.transform.scale(winnerName, (settings.width/scale, settings.height/(scale*3.22)))
    winnerName_rect = winnerName.get_rect()
    bird = settings.red
    scale = 4
    bird = py.transform.scale(bird, (settings.width/scale,settings.height/(scale*0.58)))
    bird_rect = bird.get_rect()
    scale = 5
    crown = py.image.load("Media/crown.png")
    crown = py.transform.scale(crown, (settings.width/scale,settings.height/(scale*0.62)))
    crown_rect = crown.get_rect()
    confetti = py.image.load("Media/confetti.png")
    confetti_rect = confetti.get_rect()
    stars = py.image.load("Media/stars-edited.png")
    stars_rect = stars.get_rect()
    bg = py.transform.scale(settings.bg, screen.get_size())

    py.mixer.music.stop()
    py.mixer.music.load("Media/audio/game_complete.mp3")
    py.mixer.music.play(-1)
    py.mixer.music.set_volume(settings.musicVolume)

    bird_rect.center = (settings.width/2, settings.height/2)
    crown_rect.bottom = bird_rect.top+settings.height/6
    crown_rect.centerx = bird_rect.centerx+settings.width/70
    stars_rect.centerx = crown_rect.centerx
    winnerName_rect.centerx = stars_rect.centerx
    winnerName_rect.centery = bird_rect.bottom+settings.height/10

    quit_init = py.image.load("Media/quit.png")
    quit_init = py.transform.scale(quit_init, (settings.width/7.7,settings.height/10))
    quit_rect = quit_init.get_rect()


    while True:
        
        multiplier = 1

        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(event.pos):
                    sys.exit()

        
        screen.blit(bg, (0,0))
        screen.blit(confetti,confetti_rect)
        screen.blit(bird,bird_rect)
        screen.blit(crown,crown_rect)
        screen.blit(winnerName,winnerName_rect)
        screen.blit(stars,stars_rect)

        if quit_rect.collidepoint(py.mouse.get_pos()):
            multiplier = 1.2

        quit = py.transform.scale_by(quit_init, multiplier)
        quit_rect = quit.get_rect()
        quit_rect.center = (settings.width/1.1, settings.height/1.1)

        screen.blit(quit, quit_rect)

        py.display.flip()