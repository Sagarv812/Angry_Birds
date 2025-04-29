import pygame as py
import Modules.settings as settings
import sys


#Mask to make the rectangular images have rounded edges
def returnRoundedSurface(img):
    surface = py.Surface(img.get_size(), py.SRCALPHA)
    surface.fill((0,0,0,0))
    mask = py.Surface(img.get_size(), py.SRCALPHA)
    mask.fill((0,0,0,0))
    py.draw.rect(mask, (255,255,255), (0,0,img.get_width(), img.get_height()), border_radius=30)
    surface.blit(img, (0,0))
    surface.blit(mask, (0,0), special_flags=py.BLEND_RGBA_MIN)
    return surface

def selectTheme(screen):
    py.mixer.stop()

    bg = py.transform.scale(settings.bg,screen.get_size())
    chooseText = settings.bigFont.render("CHOOSE YOUR THEME",True,settings.RED)
    chooseText_rect = chooseText.get_rect()
    chooseText_rect.center = (settings.width/2, settings.height/15)

    backButton_init = py.transform.scale(py.image.load("Media/back.png"),(settings.width/6,(settings.width/6)*(248/500)))
    backButtonRect = backButton_init.get_rect()
    backButtonRect.bottomleft = (settings.width/10,settings.height*9/10)

    #Initializing themes, theme songs and positions
    th1 = py.transform.scale(settings.bg1, (settings.width/3, settings.height/3))
    th2 = py.transform.scale(settings.bg2, (settings.width/3, settings.height/3))
    th3 = py.transform.scale(settings.bg3, (settings.width/3, settings.height/3))

    th1_rect = th1.get_rect()
    th2_rect = th2.get_rect()
    th3_rect = th3.get_rect()

    th1_rect.center = (settings.width/4, settings.height/3)
    th2_rect.center = (settings.width*3/4, settings.height/3)
    th3_rect.center = (settings.width/2, settings.height*3/4)

    th1_song = settings.bgm1
    th2_song = settings.bgm2
    th3_song = settings.bgm3

    channel1 = th1_song.play(-1)
    channel2 = th2_song.play(-1)
    channel3 = th3_song.play(-1)

    th1Hover = False
    th2Hover = False
    th3Hover = False

    backHover = False
    hoverSound = settings.buttonHoverSound
    hoverSound.set_volume(settings.sfxVolume)
    clickSound = settings.buttonClickSound
    clickSound.set_volume(settings.sfxVolume)
    


    while True:
        multiplier = [1,1,1]
        backMultiplier = 1
        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:

                #Checking if user clicked on any themes/back button
                if th1_rect.collidepoint(event.pos):
                    settings.currentBg = settings.bg1
                    settings.currentBgm = settings.bgm1
                    settings.state = "select"
                    settings.theme = "space"
                    return
                elif th2_rect.collidepoint(event.pos):
                    settings.currentBg = settings.bg2
                    settings.currentBgm = settings.bgm2
                    settings.state = "select"
                    settings.theme = "ghost"
                    return
                elif th3_rect.collidepoint(event.pos):
                    settings.currentBg = settings.bg3
                    settings.currentBgm = settings.bgm3
                    settings.state = "select"
                    settings.theme = "samurai"
                    return
                elif backButtonRect.collidepoint(event.pos):
                    settings.state = "naming"
                    clickSound.play()
                    return

        #If mouse hover, enlarge
        mouse_pos = py.mouse.get_pos()
        if th1_rect.collidepoint(mouse_pos):
            multiplier[0] = 1.2
        
        if th2_rect.collidepoint(mouse_pos):
            multiplier[1] = 1.2

        if th3_rect.collidepoint(mouse_pos):
            multiplier[2] = 1.2

        if backButtonRect.collidepoint(mouse_pos):
            backMultiplier = 1.2
            if not backHover:
                hoverSound.play()
                backHover = True
        else:
            backHover = False
                

        th1_final = py.transform.scale_by(th1, multiplier[0])
        th2_final = py.transform.scale_by(th2, multiplier[1])
        th3_final = py.transform.scale_by(th3, multiplier[2])
        th1_rect = th1_final.get_rect()
        th2_rect = th2_final.get_rect()
        th3_rect = th3_final.get_rect()
        th1_rect.center = (settings.width/4, settings.height/3)
        th2_rect.center = (settings.width*3/4, settings.height/3)
        th3_rect.center = (settings.width/2, settings.height*3/4)

        backButton = py.transform.scale_by(backButton_init,backMultiplier)
        backButtonRect = backButton.get_rect()
        backButtonRect.bottomleft = (settings.width/10,settings.height*9/10)

        #Displaying on screen
        screen.blit(bg, (0,0))
        screen.blit(chooseText, chooseText_rect)
        screen.blit(returnRoundedSurface(th1_final), th1_rect)
        screen.blit(returnRoundedSurface(th2_final), th2_rect)
        screen.blit(returnRoundedSurface(th3_final), th3_rect)
        screen.blit(backButton,backButtonRect)

        #Playing respective theme music when mouse hover
        if multiplier[0] == 1.2:
            py.draw.rect(screen, settings.ICE_BLUE, th1_rect, width=15, border_radius=30)
            if not th1Hover:
                channel1.unpause()
                channel1.set_volume(settings.musicVolume)
                th1Hover = True
        else:
            channel1.pause()
            th1Hover = False

        
        if multiplier[1] == 1.2:
            py.draw.rect(screen, settings.ICE_BLUE, th2_rect, width=15, border_radius=30)
            if not th2Hover:
                channel2.unpause()
                channel2.set_volume(settings.musicVolume)
                th2Hover = True
        else:
            channel2.pause()
            th2Hover = False

        if multiplier[2] == 1.2:
            py.draw.rect(screen, settings.ICE_BLUE, th3_rect, width=15, border_radius=30)
            if not th3Hover:
                channel3.unpause()
                channel3.set_volume(settings.musicVolume)
                th3Hover = True
        else:
            channel3.pause()
            th3Hover = False


        py.display.flip()

