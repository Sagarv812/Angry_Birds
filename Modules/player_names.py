import pygame as py, sys
import Modules.settings as settings
import Modules.players as Players

def naming(screen):

    #Rendering text
    p1 = settings.bigFont.render("PLAYER 1", True, (0,0,0))
    p2 = settings.bigFont.render("PLAYER 2", True, (0,0,0))
    p1 = py.transform.scale(p1, (settings.width/3.5,settings.height/6.2))
    p2 = py.transform.scale(p2, (settings.width/3.5,settings.height/6.2))


    #Rendering Images
    vs = py.image.load("Media/versus1.png")
    vs = py.transform.scale(vs, (settings.width/5.12,settings.height/2.9))
    vs_rect = vs.get_rect()
    vs_rect.center = (settings.width/2, settings.height/2)
    
    backButtonInit = py.image.load("Media/back.png")
    backButtonInit = py.transform.scale(backButtonInit, (settings.width/7.7,settings.height/8.7))
    backButtonRect = backButtonInit.get_rect()
    backButtonRect.center = (settings.width/5.13, settings.height/1.2)
    

    font = py.font.SysFont("latinmodernmono", int(settings.width/23))
    fontSmaller = py.font.Font("Media/angrybirds-regular.ttf", int(settings.width/32))

    bg = py.image.load("Media/Menu_background.jpg")
    bg = py.transform.scale(bg, screen.get_size())

    box_width = settings.width/3.85
    box_height = settings.height/11

    #Rendering input box
    input_box1 = py.Rect(10, 10, box_width, box_height)
    input_box1.center = (settings.width/5.13, settings.height/3.17)
    input_box2 = py.Rect(10, 10, box_width, box_height)
    input_box2.center = (settings.width/1.25, settings.height/1.45)
    color1 = settings.GRAY
    color2 = settings.GRAY
    text1 = ""
    text2 = ""
    active1 = False
    active2 = False
    done = [False, False]

    #Dims background to highlight the foreground
    dim_surface = py.Surface((screen.get_size()), py.SRCALPHA)
    dim_surface.fill((0, 0, 0, 180))

    popup = py.Rect(10, 10, settings.width/2.4, settings.height/2.7)
    popup.center = (settings.width/2, settings.height/2)

    next = py.Rect(10, 10, settings.width/6.4, settings.height/10.8)
    next.topleft = (popup.x+settings.width/38.5, popup.y+settings.height/4.15)
    back = py.Rect(10, 10, next.width, next.height)
    back.right = popup.right-settings.width/38.5
    back.top = next.top
    
    hoverPlay = False

    while True:
        
        multiplier = 1

        for event in py.event.get():

            if event.type == py.QUIT: sys.exit()

            elif event.type == py.MOUSEBUTTONDOWN:

                #Checks if names are entered and then does further action accordingly
                if done != [True, True]:
                    if input_box1.collidepoint(event.pos):
                        settings.buttonClickSound.set_volume(settings.sfxVolume)
                        settings.buttonClickSound.play()
                        active1 = True
                        active2 = False
                    elif input_box2.collidepoint(event.pos):
                        settings.buttonClickSound.set_volume(settings.sfxVolume)
                        settings.buttonClickSound.play()
                        active2 = True
                        active1 = False
                    elif backButtonRect.collidepoint(event.pos):
                        settings.buttonClickSound.set_volume(settings.sfxVolume)
                        settings.buttonClickSound.play()
                        Players.Player1.changeName("Player 1")
                        Players.Player2.changeName("Player 2")
                        settings.state = "menu"
                        return
                    else:
                        active1 = active2 = False
                
                else:
                    if next.collidepoint(event.pos):
                        settings.state = "theme"
                        return
                    elif back.collidepoint(event.pos):
                        done = [False, False]

            #Takes the name input and stores it in Player name
            elif event.type == py.KEYDOWN:
                if active1:
                    if event.key == py.K_RETURN:
                        active1 = False
                        Players.Player1.changeName(text1.strip().upper())
                        if (text1 != ""):
                            done[0] = True
                    elif event.key == py.K_BACKSPACE:
                        text1 = text1[:-1]
                    elif event.key == py.K_ESCAPE:
                        active1 = False
                    elif event.key == py.K_TAB:
                        active1 = False
                        active2 = True
                        Players.Player1.changeName(text1.strip().upper())
                        if (text1 != ""):
                            done[0] = True
                    else:
                        text1 += event.unicode

                elif active2:
                    if event.key == py.K_RETURN:
                        active2 = False
                        Players.Player2.changeName(text2.strip().upper())
                        if (text2 != ""):
                            done[1] = True
                    elif event.key == py.K_BACKSPACE:
                        text2 = text2[:-1]
                    elif event.key == py.K_ESCAPE:
                        active2 = False
                    else:
                        text2 += event.unicode

            color1 = (251,204,22) if active1 else settings.GRAY
            color2 = (185,15,18) if active2 else settings.GRAY

        
        if backButtonRect.collidepoint(py.mouse.get_pos()):
            multiplier = 1.2
            if not hoverPlay:
                settings.buttonHoverSound.set_volume(settings.sfxVolume)
                settings.buttonHoverSound.play()
                hoverPlay = True
        else:
            hoverPlay = False


        #Displaying objects on screen
        screen.fill(settings.black)
        screen.blit(bg, (0,0))
        screen.blit(p1, (settings.width/19.2, settings.height/10.8))
        screen.blit(p2, (settings.width/1.5, settings.height/1.35))
        
        p1_textSurface = font.render(text1, True, color1)
        p2_textSurface = font.render(text2, True, color2)
        width1 = max(p1_textSurface.get_width()+10, box_width)
        input_box1.w = width1
        width2 = max(p2_textSurface.get_width()+10, box_width)
        input_box2.w = width2

        screen.blit(vs, vs_rect)
        
        py.draw.rect(screen, settings.WHITE, input_box1, border_radius=15)
        py.draw.rect(screen, color1, input_box1, 5, border_radius=15)
        screen.blit(p1_textSurface, (input_box1.x+10, input_box1.y+5))

        py.draw.rect(screen, settings.WHITE, input_box2, border_radius=15)
        py.draw.rect(screen, color2, input_box2, 5, border_radius=15)
        screen.blit(p2_textSurface, (input_box2.x+10, input_box2.y+8))
        backButton = py.transform.scale_by(backButtonInit, multiplier)
        backButtonRect = backButton.get_rect()
        backButtonRect.center = (settings.width/5, settings.height/1.2)
        screen.blit(backButton, backButtonRect)

        #Popup confirmation box
        if (done == [True, True]):
            screen.blit(dim_surface, (0, 0))
            py.draw.rect(screen, settings.YELLOW, popup, border_radius=20)
            popup_heading = settings.bigFont.render("CONFIRM PLAYER NAMES", True, (0,0,0))
            popup_heading = py.transform.scale(popup_heading, (settings.width/2.8, settings.height/13.5))
            popup_heading_rect = popup_heading.get_rect()
            popup_heading_rect.center = (settings.width/2, popup.y+settings.height/21.5)
            name1 = fontSmaller.render(f"Player 1: {text1}", True, settings.RED)
            name2 = fontSmaller.render(f"Player 2: {text2}", True, settings.RED)
            name1_rect = name1.get_rect()
            name2_rect = name2.get_rect()

            name1_rect.x = name2_rect.x = popup.x + settings.width/48
            name1_rect.y = popup.y + settings.height/10.8
            name2_rect.y = name1_rect.y + settings.height/13.5

            

            nextText = settings.bigFont.render("CONTINUE", True, (0,0,0))
            nextText = py.transform.scale(nextText, (settings.width/9.6,settings.height/18))
            nextText_rect = nextText.get_rect()
            nextText_rect.center = (next.x+settings.width/12.8, next.y+settings.height/21.6)

            backText = settings.bigFont.render("BACK", True, (0,0,0))
            backText = py.transform.scale(backText, (settings.width/17.8,settings.height/18))
            backText_rect = backText.get_rect()
            backText_rect.center = (back.x+settings.width/12.8, back.y+settings.height/21.6)

            screen.blit(popup_heading, popup_heading_rect)
            screen.blit(name1, name1_rect)
            screen.blit(name2, name2_rect)
            py.draw.rect(screen, settings.GREEN, next, border_radius=15)
            py.draw.rect(screen, settings.RED, back, border_radius=15)
            screen.blit(nextText, nextText_rect)
            screen.blit(backText, backText_rect)


        py.display.flip()
