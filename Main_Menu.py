import pygame as py, numpy
import sys
import Modules.settings as settings
import time



maxAnimTime = 0.75

def returnScale(startTime):
    global maxAnimTime
    timePassed = (py.time.get_ticks() - startTime)/1000
    if timePassed<=maxAnimTime:
        return timePassed*(1/maxAnimTime)
    else:
        return 1




def menu(screen):
    py.mixer.stop()
    print(settings.width)
    logo_init = py.image.load("Media/logo.png")
    logo_init = py.transform.scale(logo_init,(settings.width/2.15,settings.height/1.8))

    sound_on = py.image.load("Media/Settings/volume_on_1.png")
    sound_on = py.transform.scale(sound_on, (settings.width/9.4,settings.height/5.3))
    sound_rect = sound_on.get_rect()
    sound_off = py.image.load("Media/Settings/volume_off_1.png")
    sound_off = py.transform.scale(sound_off, (settings.width/9.4,settings.height/5.3))
    currentSound = sound_on

    play_init = py.image.load("Media/play_1.png")
    play_init = py.transform.scale(play_init, (settings.width/3.85,settings.height/5))
    play_rect = play_init.get_rect()

    quit_init = py.image.load("Media/quit.png")
    quit_init = py.transform.scale(quit_init, (settings.width/7.7,settings.height/10))
    quit_rect = quit_init.get_rect()

    startTime = py.time.get_ticks()

    bg = py.image.load("Media/Menu_background.jpg")
    bg = py.transform.scale(bg, screen.get_size())
    
    
    bgm = py.mixer.Sound("Media/background_music.mp3")
    channel = bgm.play(-1)
    bgm.set_volume(settings.musicVolume)
    
    isMusicPaused = False

    hoverSoundPlayed = False
    hoverPlayPlayed = False
    hoverQuitPlayed = False


    while True:
        multiplier = [1,1,1]

        settings.buttonHoverSound.set_volume(settings.sfxVolume)
        settings.buttonClickSound.set_volume(settings.sfxVolume)

        mouse_click = py.mouse.get_pressed()
        mouse_pos = py.mouse.get_pos()

        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                if sound_rect.collidepoint(event.pos):
                    if (currentSound==sound_on): 
                        currentSound=sound_off
                        settings.buttonClickSound.play()
                        settings.ifAudio = False
                    else: 
                        settings.ifAudio = True
                        currentSound=sound_on

                if play_rect.collidepoint(event.pos):
                    settings.state = "naming"
                    settings.buttonClickSound.play()
                    return
                
                if quit_rect.collidepoint(event.pos):
                    settings.buttonClickSound.play()
                    sys.exit()

        #Main logo
        logo = py.transform.scale_by(logo_init, returnScale(startTime))
        logo_rect = logo.get_rect()
        logo_rect.center = (settings.width/2, settings.height/3.75)

        if (currentSound==sound_off and isMusicPaused == False):
            channel.pause()
            isMusicPaused = True

        if (currentSound==sound_on and isMusicPaused == True):
            channel.unpause()
            isMusicPaused = False

        if sound_rect.collidepoint(py.mouse.get_pos()):
            multiplier[0] = 1.2
            if not hoverSoundPlayed:
                settings.buttonHoverSound.play()
                hoverSoundPlayed = True
        else:
            hoverSoundPlayed = False

        if play_rect.collidepoint(py.mouse.get_pos()):
            multiplier[1] = 1.4
            if not hoverPlayPlayed:
                settings.buttonHoverSound.play()
                hoverPlayPlayed = True
        else:
            hoverPlayPlayed = False

        if quit_rect.collidepoint(py.mouse.get_pos()):
            multiplier[2] = 1.4
            if not hoverQuitPlayed:
                settings.buttonHoverSound.play()
                hoverQuitPlayed = True
        else:
            hoverQuitPlayed = False

        #Sound button
        sound = py.transform.scale_by(currentSound, multiplier[0]*returnScale(startTime))
        sound_rect = sound.get_rect()
        sound_rect.center = (settings.width/1.2, settings.height/1.2)

        #Play button
        play = py.transform.scale_by(play_init, multiplier[1]*returnScale(startTime))
        play_rect = play.get_rect()
        play_rect.center = (settings.width/2, settings.height/1.6)

        #Quit button
        quit = py.transform.scale_by(quit_init, multiplier[2]*returnScale(startTime))
        quit_rect = quit.get_rect()
        quit_rect.center = (settings.width/2, settings.height/1.25)

        screen.fill(settings.black)
        screen.blit(bg, (0,0))
        screen.blit(logo, logo_rect)
        screen.blit(sound, sound_rect)
        screen.blit(play, play_rect)
        screen.blit(quit, quit_rect)
        py.display.flip()


