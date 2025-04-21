import pygame as py, time, sys
import Modules.birds as Birds
import Modules.players as Players
import Modules.settings as settings
import Modules.blocks as Blocks
import random
import copy
import math
import numpy as np



def drawTrajectory(screen, bird, slingCenter, start):
    g = 20
    dot_radius = 4
    powerFactor = 5
    scale = 20 #1m is 50 pixels
    velocity = (bird.speed**0.2)*(slingCenter-start)*0.2

    for t in range(40):
        dt = t*0.1
        x = start.x + (velocity.x*dt)*scale
        y = start.y + (velocity.y*dt + 0.5*g*(dt**2))*scale
        # if t%2==0:
        py.draw.circle(screen, settings.RED, (int(x),int(y)), dot_radius)

def drawLine(screen, bird, sling_rect):
    if bird.ifDragging:
        py.draw.line(screen, settings.ROPE_BROWN, bird.rect.center,(sling_rect.centerx-25,sling_rect.centery-55),width=15)
        py.draw.line(screen, settings.ROPE_BROWN, bird.rect.center,(sling_rect.centerx+5,sling_rect.centery-50),width=15)
        # py.draw.line(screen, settings.ROPE_BROWN, bird.rect.center,bird.initRect.center,width=10)
        

def displayAvatar(screen, birdNos1, birds1, birdNos2, birds2, active=None):
    if any(x != -1 for x in birdNos1):  
        avatar1 = birds1[birdNos1[3]].getAvatarImage()
    else:
        avatar1 = py.image.load("Media/avatar1.png")
        avatar1 = py.transform.scale_by(avatar1, 0.5)

    if any(x != -1 for x in birdNos2):
        avatar2 = py.transform.flip(birds2[birdNos2[3]].getAvatarImage(),True,False)
    else:
        avatar2 = py.image.load("Media/avatar2.png")
        avatar2 = py.transform.scale_by(avatar2, 0.5)

    avatar1_rect = avatar1.get_rect()
    avatar2_rect = avatar2.get_rect()
    avatar1_rect.topleft = (0,0)
    avatar2_rect.topright = (settings.width,0)


    py.draw.circle(screen, settings.DARK_GRAY, (120,100),250)
    if active==1:
        py.draw.circle(screen, settings.YELLOW, (120,100),250,20)
    else:
        py.draw.circle(screen,settings.GRAY,(120,100),250,20)

    py.draw.circle(screen,settings.DARK_GRAY, (settings.width-120,100),250)

    if active==2:
        py.draw.circle(screen, settings.RED, (settings.width-120,100),250,20)
    else:
        py.draw.circle(screen, settings.GRAY, (settings.width-120,100),250,20)

    screen.blit(avatar1, avatar1_rect)
    screen.blit(avatar2, avatar2_rect)

def displayScore(screen, score1, score2, turn=None):
    multiplier = [1,1]
    if turn is not None:
        multiplier[turn-1] = 1.3
    score1 = py.transform.scale_by(score1, multiplier[0])
    score2 = py.transform.scale_by(score2, multiplier[1])
    sep = settings.bigFont.render("i",True,settings.black)
    sep = py.transform.scale_by(sep, 2)
    score1_rect = score1.get_rect()
    score2_rect = score2.get_rect()
    score1_rect.topright = (settings.width/2-100,50)
    score2_rect.topleft = (settings.width/2+100,50)
    sep_rect = sep.get_rect(center=((score1_rect.right+score2_rect.left)/2,100))
    screen.blit(sep, sep_rect)
    screen.blit(score1, score1_rect)
    screen.blit(score2, score2_rect)

def transformX(x, playerNo):
    return x if playerNo==1 else settings.width-x

def rotateImg(img, playerNo):
    return img if playerNo==1 else py.transform.flip(img, True, False)

def rotateBirds(birdNos, birdsPlay):
    for i in range(3,0,-1):
        birdNos[i] = birdNos[i-1]
        birdsPlay[i] = birdsPlay[i-1]

    birdNos[0] = -1
    birdsPlay[0] = None

    print("Rotation")
    for i in range(4):
        if birdNos[i]==-1: continue
        else:
            print(birdsPlay[i].affinity)
        
def displayBirds(screen, playerNo, birdNos, sling_rect, birdsPlay):
    print("player no = ",playerNo)
    sling_rect_trans = copy.deepcopy(sling_rect)
    sling_rect_trans.centerx = transformX(sling_rect.centerx, playerNo)
    print("sling 1 rect",sling_rect)
    print("sling 2 rect ", sling_rect_trans)

    sling2 = rotateImg(py.transform.scale_by(py.image.load("Media/sling(2).png"),0.8),playerNo)
    sling2_rect = sling2.get_rect()
    sling2_rect.bottom = sling_rect.bottom
    sling2_rect.centerx = transformX(sling_rect.right-20-sling2.get_width()/2, playerNo)
    
    screen.blit(sling2, sling2_rect)


    for i in range(4):
        if birdNos[i]==-1: continue

        bird = birdsPlay[i]
        # if isDragged:
        #     return
        # elif isFly:
        #     return
        # else:
        #     bird.image = rotateImg(py.transform.scale_by(bird.initImage, 0.2),playerNo)
        #     bird.updateRect()

        #     if i==3:
        #         bird.rect.centerx = transformX(sling_rect.centerx+15-bird.image.get_width()/2,playerNo)
        #         bird.rect.bottom = sling_rect.centery-30
            
        #     else:
        #         bird.rect.centerx = transformX((i+1)*100+50-bird.image.get_width()/2,playerNo)
        #         bird.rect.bottom = 930
        bird.image = rotateImg(py.transform.scale_by(bird.initImage, 0.2),playerNo)
        bird.updateRect()    
        bird.updatePos(i,playerNo,sling_rect, screen)
        drawLine(screen, bird, sling_rect_trans)
        if bird.ifDragging:
            drawTrajectory(screen, bird, py.Vector2(bird.initRect.center), py.Vector2(bird.rect.center))
        screen.blit(bird.image, bird.rect)

    del sling_rect_trans
    sling1 = py.image.load("Media/sling(1).png")
    sling1 = rotateImg(py.transform.scale_by(sling1, 0.8),playerNo)
    sling1_rect = sling1.get_rect()
    sling1_rect.topleft = sling_rect.topleft
    sling1_rect.centerx = transformX(sling1_rect.left+sling1.get_width()/2,playerNo)
    if playerNo==1: sling1_rect.left -=5
    else: sling1_rect.left+=5
    screen.blit(sling1, sling1_rect)


def displayBlocks(screen, blocks, playerNo):
    for i in range(4):
        for j in range(2):
            if blocks[i][j] is not None:
                block = blocks[i][j].returnImg()
                if block is not None and blocks[i][j] is not None:
                    block_rect = blocks[i][j].rect
                    block_rect.centerx = transformX(350+90*j,playerNo)
                    block_rect.centery = int(930-block.get_width()/2-90*i)
                    screen.blit(block,block_rect)

    

def playGame(screen):

    startTime = py.time.get_ticks()
    state = "static"
    prevState = "static"

    fightImg = py.image.load("Media/fight.png")
    fightInitSize = fightImg.get_size()

    start_scale = 7
    end_scale = 1

    
    # start_size = 3000
    # end_size = 200
    duration = 1

    py.mixer.music.stop()
    # py.mixer.music.load("Media/audio/battle_music.mp3")
    # py.mixer.music.play(-1)
    # py.mixer.music.set_volume(0.2)

    #Player 1
    birdNos1 = [random.randint(0,Players.Player1.getBirdsNo()-1) for _ in range(4)] #Initializing birds
    birds1 = Players.Player1.getBirds()
    birdsPlay1 = [birds1[x].clone() for x in birdNos1]

    #Sling
    sling = py.image.load("Media/sling.png")
    sling = py.transform.scale_by(sling,0.8)
    sling_rect = sling.get_rect()
    sling_rect.bottom = 930
    sling_rect.left = 400   

    #Player 2
    birdNos2 = [random.randint(0,Players.Player2.getBirdsNo()-1) for _ in range(4)]
    birds2 = Players.Player2.getBirds()
    birdsPlay2 = [birds2[x].clone() for x in birdNos2]

    #Blocks
    blockKeys = np.random.randint(0, 3, size=(4,2))
    blockKeys = np.array([[2,2],[2,2],[2,2],[2,2],[2,2]])
    blocks1 = np.empty_like(blockKeys, dtype=object)
    blocks2 = np.empty_like(blockKeys, dtype=object)
    for i in range(4):
        for j in range(2):
           blocks1[i,j] = Blocks.blocks[blockKeys[i,j]].clone() 
           blocks2[i,j] = Blocks.blocks[blockKeys[i,j]].clone()

    for i in range(4):
        for j in range(2):
           print(blocks2[i,j].name, end='')

        print()
        

   
    while True:

        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()
            elif event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    if state != "pause":
                        prevState = state
                        state = "pause"
                    else:
                        state = prevState

            if state=="player1":
                if event.type == py.MOUSEBUTTONDOWN:
                    if birdsPlay1[3].rect.collidepoint(event.pos) and birdsPlay1[3].ifLaunched == False:
                        birdsPlay1[3].ifDragging = True

                elif event.type == py.MOUSEBUTTONUP:
                    if birdsPlay1[3].ifDragging:
                        birdsPlay1[3].ifDragging = False
                        birdsPlay1[3].ifLaunched = True

                        birdsPlay1[3].initVelocity()    
                        birdsPlay1[3].startTime = py.time.get_ticks()

            elif state=="player2":
                if event.type == py.MOUSEBUTTONDOWN:
                    if birdsPlay2[3].rect.collidepoint(event.pos) and birdsPlay2[3].ifLaunched == False:
                        birdsPlay2[3].ifDragging = True

                elif event.type == py.MOUSEBUTTONUP:
                    if birdsPlay2[3].ifDragging:
                        birdsPlay2[3].ifDragging = False
                        birdsPlay2[3].ifLaunched = True

                        birdsPlay2[3].initVelocity()
                        birdsPlay2[3].startTime = py.time.get_ticks()


        score1 = settings.bigFont.render(str(Players.Player1.getScore()),True,settings.YELLOW)
        score2 = settings.bigFont.render(str(Players.Player2.getScore()),True,settings.RED)
        screen.blit(py.transform.scale(settings.bg1,screen.get_size()),(0,0))


        if state=="static":
            displayScore(screen, score1, score2)

            displayBirds(screen,1,birdNos1,sling_rect,birdsPlay1)

            displayBirds(screen,2,birdNos2,sling_rect,birdsPlay2)

            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2)

            dim_surface = py.Surface(screen.get_size(), py.SRCALPHA)
            dim_surface.fill((0, 0, 0, 180))
            screen.blit(dim_surface,(0,0))

            elapsed = (py.time.get_ticks()-startTime)/1000
            t = min(elapsed/duration,1)

            ease = 1- (1-t)**3
            # font_size = start_size+(end_size-start_size)*ease
            # font = py.font.Font("Media/angrybirds-regular.ttf", int(font_size))
            # fight = font.render("FIGHT",True,settings.RED)
            # fight_rect = fight.get_rect()
            # fight_rect.center = (settings.width/2, settings.height/2)
            # screen.blit(fight, fight_rect)
            scale = start_scale + (end_scale-start_scale)*ease
            newFightSize = (int(fightInitSize[0]*scale),int(fightInitSize[1]*scale))
            fight = py.transform.smoothscale(fightImg, newFightSize)
            fight_rect = fight.get_rect(center=(settings.width/2,settings.height/2))
            screen.blit(fight,fight_rect)
            if (py.time.get_ticks()-startTime)/1000>2:
                state = "player1"

        elif state == "player1":
            displayBirds(screen,1,birdNos1,sling_rect,birdsPlay1)

            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2,1)

            displayScore(screen, score1, score2,1)

            displayBlocks(screen, blocks1, 2)


            if birdsPlay1[3].ifLaunched:
                for i in range(4):
                    if birdsPlay1[3].ifCollided:
                        break
                    for j in range(2):
                        if blocks1[i][j] is not None:
                            if birdsPlay1[3].rect.colliderect(blocks1[i][j].rect):
                                py.draw.rect(screen,settings.black,blocks1[i][j].rect,width=20)
                                time.sleep(1)
                                birdsPlay1[3].ifCollided = True
                                if birdsPlay1[3].affinity == blocks1[i][j].name:
                                    blocks1[i][j].health -= birdsPlay1[3].damageMultiplier*20
                                    Players.Player1.score += int(birdsPlay1[3].damageMultiplier*20)
                                else:
                                    blocks1[i][j].health -= 20/birdsPlay1[3].damageMultiplier
                                    Players.Player1.score += int(20/birdsPlay1[3].damageMultiplier)

                                if blocks1[i][j].health<=0:
                                    if i<=2 and blocks1[i+1][j] is not None:
                                        for k in range(i+1,4):
                                            if blocks1[k][j] is None:
                                                blocks1[k-1][j] = None
                                            else:
                                                blocks1[k-1][j] = blocks1[k][j].clone()
                                        blocks1[3][j] = None
                                    else:
                                        blocks1[i][j] = None


                                break

                if birdsPlay1[3].ifCollided:
                    print("1 calling rot")
                    print("Before rotation:")
                    for i in range(4):
                        print("Bird",i)
                        if birdsPlay1[i] is None: continue
                        else:
                            birdsPlay1[i].printInfo()
                    rotateBirds(birdNos1,birdsPlay1)
                    print("After rotation:")
                    for i in range(4):
                        print("Bird",i)
                        if birdsPlay1[i] is None: continue
                        else:
                            birdsPlay1[i].printInfo()

                    if Players.Player1.score >= 480:
                        settings.state = "winner"
                        settings.winner = "player1"
                    state = "player2"


        elif state == "player2":
            displayBirds(screen,2,birdNos2,sling_rect,birdsPlay2)

            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2,2)

            displayScore(screen, score1, score2, 2)

            
            displayBlocks(screen, blocks2,1)

            if birdsPlay2[3].ifLaunched:
                print("launched ig")
                for i in range(4):
                    if birdsPlay2[3].ifCollided:
                        break
                    for j in range(2):
                        if blocks2[i][j] is not None:
                            if birdsPlay2[3].rect.colliderect(blocks2[i][j].rect):
                                py.draw.rect(screen,settings.black,blocks2[i][j].rect)
                                time.sleep(1)
                                birdsPlay2[3].ifCollided = True
                                if birdsPlay2[3].affinity == blocks2[i][j].name:
                                    blocks2[i][j].health -= birdsPlay2[3].damageMultiplier*20
                                    Players.Player2.score += int(birdsPlay2[3].damageMultiplier*20)
                                else:
                                    blocks2[i][j].health -= 20/birdsPlay2[3].damageMultiplier
                                    Players.Player2.score += int(20/birdsPlay2[3].damageMultiplier)

                                if blocks2[i][j].health<=0:
                                    if i<=2 and blocks2[i+1][j] is not None:
                                        for k in range(i+1,4):
                                            if blocks2[k][j] is None:
                                                blocks2[k-1][j] = None
                                            else:
                                                blocks2[k-1][j] = blocks2[k][j].clone()
                                        blocks2[3][j] = None
                                    else:
                                        blocks2[i][j] = None

                                break

                if birdsPlay2[3].ifCollided:     
                    if any(x != -1 for x in birdNos1):
                        print("2 calling rot")
                        print("Before rotation:")
                        for i in range(4):
                            print("Bird",i)
                            if birdsPlay2[i] is None: continue
                            else:
                                birdsPlay2[i].printInfo()
                        rotateBirds(birdNos2,birdsPlay2)
                        for i in range(4):
                            print("Bird",i)
                            if birdsPlay2[i] is None: continue
                            else:
                                birdsPlay2[i].printInfo()
                        state = "player1"
                    else:
                        birdNos1 = [random.randint(0,Players.Player1.getBirdsNo()-1) for _ in range(4)] #Initializing birds
                        birdsPlay1 = [birds1[x].clone() for x in birdNos1]

                        birdNos2 = [random.randint(0,Players.Player2.getBirdsNo()-1) for _ in range(4)]
                        birdsPlay2 = [birds2[x].clone() for x in birdNos2]

                        state = "player1"



        elif state == "pause":
            displayScore(screen, score1, score2)
            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2)
            dim_surface = py.Surface(screen.get_size(), py.SRCALPHA)
            dim_surface.fill((0, 0, 0, 180))
            screen.blit(dim_surface,(0,0))

        
        py.display.flip()
        

    