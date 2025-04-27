import pygame as py, sys
import Modules.settings as settings
import Modules.birds as Birds
import Modules.players as Players

def chooseBird(screen, pNo):
    py.mixer.music.stop()
    if settings.ifAudio:
        py.mixer.music.load("Media/background_music.mp3")
        py.mixer.music.play(-1)
        py.mixer.music.set_volume(settings.musicVolume)

    if pNo==1:
        playerName = settings.bigFont.render(f'{Players.Player1.getName()}, SELECT BIRDS', True, settings.RED)
    else:
        playerName = settings.bigFont.render(f"{Players.Player2.getName()}, SELECT BIRDS", True, settings.RED)

    # playerName = py.transform.scale_by(playerName, 1.5)
    font = py.font.SysFont("ubuntu",60)
    playerName_rect = playerName.get_rect()
    playerName_rect.center = (settings.width/2, 100)
    instructions1 = settings.bigFont.render("CHOOSE UPTO 3 BIRDS", True, settings.RED)
    instructions1 = py.transform.scale_by(instructions1, 0.5)
    instructions1_rect = instructions1.get_rect()
    instructions1_rect.center = (settings.width/2, 200)

    red_init = py.transform.scale_by(settings.red, 0.11)
    red_rect = red_init.get_rect()
    chuck_init = py.transform.scale_by(settings.chuck, 0.3)
    chuck_rect = chuck_init.get_rect()
    bomb_init = py.transform.scale_by(settings.bomb, 0.35)
    bomb_rect = bomb_init.get_rect()
    blue_init = py.transform.scale_by(settings.blue, 0.35)
    blue_rect = blue_init.get_rect()
    stella_init = py.transform.scale_by(settings.stella, 0.42)
    stella_rect = stella_init.get_rect()
    birdRects = [red_rect, chuck_rect, bomb_rect, blue_rect, stella_rect]

    red_center = (300+red_init.get_width()/2,300+red_init.get_height()/2)
    chuck_center = (800+chuck_init.get_width()/2, 300+chuck_init.get_height()/2)
    bomb_center = (1350+bomb_init.get_width()/2, 250+bomb_init.get_height()/2)
    blue_center = (550+blue_init.get_width()/2, 650+blue_init.get_height()/2)
    stella_center = (1000+stella_init.get_width()/2, 650+stella_init.get_height()/2)

    box = py.Rect(80, 80, playerName.get_width()+40, instructions1_rect.bottom-playerName_rect.top+40)
    box.centerx = settings.width/2
    box.top = playerName_rect.top - 20

    backButtonInit = py.image.load("Media/back.png")
    backButtonInit = py.transform.scale_by(backButtonInit, 0.5)
    backButtonRect = backButtonInit.get_rect()
    backButtonRect.topleft = (50,50)

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
    tick = py.transform.scale_by(tick, 0.3)
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
    wood_text = py.transform.scale_by(wood_text, 0.35)
    wood_text_rect = wood_text.get_rect()
    ice_text = settings.bigFont.render("ICE", True, settings.ICE_BLUE)
    ice_text = py.transform.scale_by(ice_text, 0.35)
    ice_text_rect = ice_text.get_rect()
    stone_text = settings.bigFont.render("STONE", True, settings.STONE_GRAY)
    stone_text = py.transform.scale_by(stone_text, 0.35)
    stone_text_rect = stone_text.get_rect()

    next_init = py.image.load("Media/next.png")
    next_init = py.transform.scale_by(next_init, 0.4)
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
                    settings.state = "naming"
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
        backButtonRect.topleft = (100,50)

        

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
        screen.blit(py.transform.scale(settings.bg, screen.get_size()), (0,0))
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
                birdName = py.transform.scale_by(birdName, 0.4)
                birdName_rect = birdName.get_rect()
                birdText = settings.bigFont.render(birdsInfo[i][1], True, settings.WHITE)
                birdText = py.transform.scale_by(birdText, 0.3)
                birdText_rect = birdText.get_rect()
                infoBox = py.Rect(10,10,max(birdName.get_width(),birdText.get_width())+20, 100)
                if i==0 or i==1:
                    infoBox.topleft = (py.mouse.get_pos()[0]+10,py.mouse.get_pos()[1])
                elif i==2:
                    infoBox.topright = (py.mouse.get_pos()[0]-10,py.mouse.get_pos()[1])
                elif i==3:
                    infoBox.bottomleft = (py.mouse.get_pos()[0]+10,py.mouse.get_pos()[1])
                else:
                    infoBox.bottomright = (py.mouse.get_pos()[0]-10,py.mouse.get_pos()[1])

                birdName_rect.center = (infoBox.centerx, infoBox.centery-20)
                birdText_rect.center = (infoBox.centerx, birdName_rect.centery+40)

                py.draw.rect(screen, settings.black, infoBox, border_radius=15)
                screen.blit(birdName, birdName_rect)
                screen.blit(birdText, birdText_rect)

        if stellaSelect:
            screen.blit(dim_surface, (0,0))
            screen.blit(stella, stella_rect)
            wood_rect.center = (stella_rect.right+50, stella_rect.top+50)
            ice_rect.center = (wood_rect.centerx, wood_rect.centery+100)
            stone_rect.center = (wood_rect.centerx, ice_rect.centery+100)
            wood_text_rect.centery = wood_rect.centery
            wood_text_rect.left = wood_rect.right+20
            ice_text_rect.centery = ice_rect.centery
            ice_text_rect.left = ice_rect.right+20
            stone_text_rect.centery = stone_rect.centery
            stone_text_rect.left = stone_rect.right+20
            screen.blit(wood, wood_rect)
            screen.blit(ice, ice_rect)
            screen.blit(stone, stone_rect)
            screen.blit(wood_text, wood_text_rect)
            screen.blit(ice_text, ice_text_rect)
            screen.blit(stone_text, stone_text_rect)

        if sum(selectBirds)>0:
            next = py.transform.scale_by(next_init, nextMultipler)
            next_rect = next.get_rect()
            next_rect.center = (settings.width - backButtonRect.centerx-50,settings.height-backButtonRect.centery-50)
            screen.blit(next, next_rect)


        py.display.flip()

        # settings.clock.tick_busy_loop(30)