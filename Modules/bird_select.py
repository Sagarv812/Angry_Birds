import pygame as py, sys
import Modules.settings as settings
import Modules.birds as Birds
import Modules.players as Players

def chooseBird(screen, pNo):
    py.mixer.stop()
    w, h = screen.get_size()
    if settings.ifAudio:
        settings.currentBgm.play(-1)
        settings.currentBgm.set_volume(settings.musicVolume)

    if pNo==1:
        playerName = settings.bigFont.render(f'{Players.Player1.getName()}, SELECT BIRDS', True, settings.RED)
    else:
        playerName = settings.bigFont.render(f"{Players.Player2.getName()}, SELECT BIRDS", True, settings.RED)

    playerName = py.transform.scale_by(playerName, w/1920)
    font = py.font.SysFont("ubuntu",int(settings.width/32))
    playerName_rect = playerName.get_rect()
    playerName_rect.center = (settings.width/2, settings.height/10.8)
    instructions1 = settings.bigFont.render("CHOOSE UPTO 3 BIRDS", True, settings.RED)
    instructions1 = py.transform.scale(instructions1, (settings.width/2.2, settings.height/9.3))
    instructions1 = py.transform.scale(instructions1, (settings.width/4.32, settings.height/18))
    instructions1_rect = instructions1.get_rect()
    instructions1_rect.center = (settings.width/2, settings.height/5.4)

    red_init = py.transform.scale(settings.red, (settings.width/6.5, settings.height/3.8))
    red_rect = red_init.get_rect()
    chuck_init = py.transform.scale(settings.chuck, (settings.width/6.3, settings.height/3.8))
    chuck_rect = chuck_init.get_rect()
    bomb_init = py.transform.scale(settings.bomb, (settings.width/7, settings.height/3))
    bomb_rect = bomb_init.get_rect()
    blue_init = py.transform.scale(settings.blue, (settings.width/6.5, settings.height/4))
    blue_rect = blue_init.get_rect()
    stella_init = py.transform.scale(settings.stella, (settings.width/5.2, settings.height/3.8))
    stella_rect = stella_init.get_rect()
    birdRects = [red_rect, chuck_rect, bomb_rect, blue_rect, stella_rect]

    red_center = (w/4.3,h/2.4)
    chuck_center = (w/2, h/2.4)
    bomb_center = (w/1.3, h/2.5)
    blue_center = (w/2.75, h/1.35)
    stella_center = (w/1.6, h/1.4)

    box = py.Rect(80, 80, max(w/2,playerName.width), h/4.7)
    box.centerx = settings.width/2
    box.top = playerName_rect.top - h/54

    backButtonInit = py.image.load("Media/back.png")
    backButtonInit = py.transform.scale(backButtonInit, (w/7.7,h/8.7))
    backButtonRect = backButtonInit.get_rect()
    backButtonRect.topleft = (w/38.4,h/21.6)

    birdsInfo = [
        ("RED","does equal damage to all blocks"),
        ("CHUCK","does more damage to wood blocks and less to others"),
        ("BOMB","does more damage to stone blocks and less to others"),
        ("BLUE","does more damage to ice blocks and less to others"),
        ("STELLA","does way more damage to any block of your choice but way less to others")
    ]

    colours = [
        settings.RED,
        settings.YELLOW,
        settings.GRAY,
        settings.ICE_BLUE,
        settings.PINK
    ]

    selectBirds = [False,False,False,False,False]
    tick = py.image.load("Media/tick1.png")
    tick = py.transform.scale(tick, (w/12,h/7.7))
    tick_rect = tick.get_rect()
    stellaSelect = False

    dim_surface = py.Surface(screen.get_size(), py.SRCALPHA)
    dim_surface.fill((0, 0, 0, 180))

    wood = py.transform.scale(settings.WOOD[0], (settings.width/30,settings.width/30))
    wood_rect= wood.get_rect()
    stone = py.transform.scale(settings.STONE[0], (settings.width/30,settings.width/30))
    stone_rect = stone.get_rect()
    ice = py.transform.scale(settings.ICE[0], (settings.width/30,settings.width/30))
    ice_rect = ice.get_rect()

    blocks = {}
    blocks["wood"] = wood
    blocks["ice"] = ice
    blocks["stone"] = stone


    wood_text = settings.bigFont.render("WOOD", True, settings.WOOD_BROWN)
    wood_text = py.transform.scale_by(wood_text, w/5485.7)
    wood_text_rect = wood_text.get_rect()
    ice_text = settings.bigFont.render("ICE", True, settings.ICE_BLUE)
    ice_text = py.transform.scale_by(ice_text, w/5485.7)
    ice_text_rect = ice_text.get_rect()
    stone_text = settings.bigFont.render("STONE", True, settings.STONE_GRAY)
    stone_text = py.transform.scale_by(stone_text, w/5485.7)
    stone_text_rect = stone_text.get_rect()

    next_init = py.image.load("Media/next.png")
    next_init = py.transform.scale(next_init, (w/6.7,h/7.7))
    next_rect = next_init.get_rect()
    next_rect.center = (settings.width - backButtonRect.centerx,settings.height-backButtonRect.centery)
    Birds.stella.changeAffinity(None)

    while True:
        backMultiplier = 1
        nextMultipler = 1

        birdsMultiplier = [1,1,1,1,1]
        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()
            
            elif event.type == py.MOUSEBUTTONDOWN:
                if backButtonRect.collidepoint(event.pos):
                    settings.state = "theme"
                    return
                elif next_rect.collidepoint(event.pos):
                    settings.state = "play"
                    for i in range(5):
                        if selectBirds[i]:
                            if pNo==1:
                                Players.Player1.addBird(Birds.birds[i].clone())
                            else:
                                Players.Player2.addBird(Birds.birds[i].clone())

                    return

                else:

                    if stellaSelect:
                        if wood_rect.collidepoint(event.pos):
                            Birds.stella.changeAffinity("wood")
                            selectBirds[4] = True

                        elif ice_rect.collidepoint(event.pos):
                            Birds.stella.changeAffinity("ice")
                            selectBirds[4] = True

                        elif stone_rect.collidepoint(event.pos):
                            Birds.stella.changeAffinity("stone")
                            selectBirds[4] = True

                        stellaSelect = False

                    else:
                        for i in range(5):
                            if birdRects[i].collidepoint(event.pos):
                                if selectBirds[i]:
                                    selectBirds[i] = False
                                    if i==4: 
                                        Birds.stella.changeAffinity(None)
                                        stellaSelect = False
                                else:
                                    if sum(selectBirds)<3:
                                        if i==4: stellaSelect = True
                                        else: selectBirds[i] = True

        
        if backButtonRect.collidepoint(py.mouse.get_pos()):
            backMultiplier = 1.2

        if next_rect.collidepoint(py.mouse.get_pos()):
            nextMultipler = 1.2

        backButton = py.transform.scale_by(backButtonInit, backMultiplier)
        backButtonRect = backButton.get_rect()
        backButtonRect.topleft = (w/19.2,h/21.6)

        

        for i in range(5):
            if birdRects[i].collidepoint(py.mouse.get_pos()):
                if stellaSelect and i==4:
                    birdsMultiplier[i] = 1
                else:
                    birdsMultiplier[i] = 1.2

        red = py.transform.scale_by(red_init, birdsMultiplier[0])
        red_rect = red_init.get_rect()
        chuck = py.transform.scale_by(chuck_init, birdsMultiplier[1])
        chuck_rect = chuck_init.get_rect()
        bomb = py.transform.scale_by(bomb_init, birdsMultiplier[2])
        bomb_rect = bomb_init.get_rect()
        blue = py.transform.scale_by(blue_init, birdsMultiplier[3])
        blue_rect = blue_init.get_rect()
        stella = py.transform.scale_by(stella_init, birdsMultiplier[4])
        stella_rect = stella_init.get_rect()

        red_rect.center = red_center
        chuck_rect.center = chuck_center
        bomb_rect.center = bomb_center
        blue_rect.center = blue_center
        stella_rect.center = stella_center

        birdRects = [red_rect, chuck_rect, bomb_rect, blue_rect, stella_rect]

        screen.fill(settings.black)
        screen.blit(py.transform.scale(settings.currentBg, screen.get_size()), (0,0))
        py.draw.rect(screen, settings.YELLOW, box, border_radius=15)
        screen.blit(playerName, playerName_rect)
        screen.blit(instructions1, instructions1_rect)
        screen.blit(backButton, backButtonRect)
        screen.blit(red, red_rect)
        screen.blit(chuck, chuck_rect)
        screen.blit(bomb, bomb_rect)
        screen.blit(blue, blue_rect)
        screen.blit(stella, stella_rect)

        for i in range(5):
            if selectBirds[i]:
                tick_rect.topleft = birdRects[i].topleft
                screen.blit(tick, tick_rect)

        for i in range(5):
            if birdsMultiplier[i] == 1.2:
                birdName = settings.bigFont.render(birdsInfo[i][0], True, colours[i])
                birdName = py.transform.scale_by(birdName, w/4800)
                birdName_rect = birdName.get_rect()
                birdText = settings.bigFont.render(birdsInfo[i][1], True, settings.WHITE)
                birdText = py.transform.scale_by(birdText, w/6400)
                birdText_rect = birdText.get_rect()
                infoBox = py.Rect(10,10,max(birdName.get_width(),birdText.get_width())+w/96, h/10.8)
                if i==0 or i==1:
                    infoBox.topleft = (py.mouse.get_pos()[0]+w/192,py.mouse.get_pos()[1])
                elif i==2:
                    infoBox.topright = (py.mouse.get_pos()[0]-w/192,py.mouse.get_pos()[1])
                elif i==3:
                    infoBox.bottomleft = (py.mouse.get_pos()[0]+w/192,py.mouse.get_pos()[1])
                else:
                    infoBox.bottomright = (py.mouse.get_pos()[0]-w/192,py.mouse.get_pos()[1])

                birdName_rect.center = (infoBox.centerx, infoBox.centery-h/54)
                birdText_rect.center = (infoBox.centerx, birdName_rect.centery+h/27)

                py.draw.rect(screen, settings.black, infoBox, border_radius=15)
                screen.blit(birdName, birdName_rect)
                screen.blit(birdText, birdText_rect)

        if stellaSelect:
            screen.blit(dim_surface, (0,0))
            screen.blit(stella, stella_rect)
            wood_rect.center = (stella_rect.right+w/38.4, stella_rect.top+h/21.6)
            ice_rect.center = (wood_rect.centerx, wood_rect.centery+h/10.8)
            stone_rect.center = (wood_rect.centerx, ice_rect.centery+h/10.8)
            wood_text_rect.centery = wood_rect.centery
            wood_text_rect.left = wood_rect.right+w/96
            ice_text_rect.centery = ice_rect.centery
            ice_text_rect.left = ice_rect.right+w/96
            stone_text_rect.centery = stone_rect.centery
            stone_text_rect.left = stone_rect.right+w/96
            screen.blit(wood, wood_rect)
            screen.blit(ice, ice_rect)
            screen.blit(stone, stone_rect)
            screen.blit(wood_text, wood_text_rect)
            screen.blit(ice_text, ice_text_rect)
            screen.blit(stone_text, stone_text_rect)

        if sum(selectBirds)>0:
            next = py.transform.scale_by(next_init, nextMultipler)
            next_rect = next.get_rect()
            next_rect.center = (settings.width - backButtonRect.centerx-w/38.4,settings.height-backButtonRect.centery-h/21.6)
            screen.blit(next, next_rect)


        py.display.flip()

        # settings.clock.tick_busy_loop(30)