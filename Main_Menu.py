import pygame as py, numpy
import sys
import Modules.settings as settings
import time



maxAnimTime = 0.75

def returnScale(startTime):
    global maxAnimTime, minAnimTime
    timePassed = (py.time.get_ticks() - startTime)/1000
    if timePassed<=maxAnimTime:
        return timePassed*(1/maxAnimTime)
    else:
        return 1




def menu(screen):
    logo_init = py.image.load("Media/logo.png")

    sound_on = py.image.load("Media/Settings/volume_on_1.png")
    sound_on = py.transform.scale_by(sound_on, 0.2)
    sound_rect = sound_on.get_rect()
    sound_off = py.image.load("Media/Settings/volume_off_1.png")
    sound_off = py.transform.scale_by(sound_off, 0.2)
    currentSound = sound_on

    play_init = py.image.load("Media/play_1.png")
    play_init = py.transform.scale_by(play_init, 0.5)
    play_rect = play_init.get_rect()

    quit_init = py.image.load("Media/quit.png")
    quit_init = py.transform.scale_by(quit_init, 0.5)
    quit_rect = quit_init.get_rect()

    startTime = py.time.get_ticks()

    bg = py.image.load("Media/Menu_background.jpg")
    bg = py.transform.scale(bg, screen.get_size())
    
    py.mixer.music.load("Media/background_music.mp3")
    py.mixer.music.play(-1)
    py.mixer.music.set_volume(0.5)
    isMusicPaused = False

    

    while True:
        multiplier = [1,1,1]
        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                if sound_rect.collidepoint(event.pos):
                    if (currentSound==sound_on): 
                        currentSound=sound_off
                        settings.ifAudio = False
                    else: 
                        settings.ifAudio = True
                        currentSound=sound_on

                if play_rect.collidepoint(event.pos):
                    settings.state = "naming"
                    return
                
                if quit_rect.collidepoint(event.pos):
                    sys.exit()

        #Main logo
        logo = py.transform.scale_by(logo_init, returnScale(startTime))
        logo_rect = logo.get_rect()
        logo_rect.center = (settings.width/2, settings.height/2-250)

        if (currentSound==sound_off and isMusicPaused == False):
            py.mixer.music.pause()
            isMusicPaused = True

        if (currentSound==sound_on and isMusicPaused == True):
            py.mixer.music.unpause()
            isMusicPaused = False

        if sound_rect.collidepoint(py.mouse.get_pos()):
            multiplier[0] = 1.2

        if play_rect.collidepoint(py.mouse.get_pos()):
            multiplier[1] = 1.4

        if quit_rect.collidepoint(py.mouse.get_pos()):
            multiplier[2] = 1.4

        #Sound button
        sound = py.transform.scale_by(currentSound, multiplier[0]*returnScale(startTime))
        sound_rect = sound.get_rect()
        sound_rect.center = (1600, 800)

        #Play button
        play = py.transform.scale_by(play_init, multiplier[1]*returnScale(startTime))
        play_rect = play.get_rect()
        play_rect.center = (settings.width/2, 670)

        #Quit button
        quit = py.transform.scale_by(quit_init, multiplier[2]*returnScale(startTime))
        quit_rect = quit.get_rect()
        quit_rect.center = (settings.width/2, 870)

        screen.fill(settings.black)
        screen.blit(bg, (0,0))
        screen.blit(logo, logo_rect)
        screen.blit(sound, sound_rect)
        screen.blit(play, play_rect)
        screen.blit(quit, quit_rect)
        py.display.flip()


