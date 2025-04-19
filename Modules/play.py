import pygame as py, time, sys
import Modules.birds as Birds
import Modules.players as Players
import Modules.settings as settings
import Modules.blocks as Blocks
import random
import numpy as np


def displayAvatar(screen, birdNos1, birds1, birdNos2, birds2, active=None):
    if any(x != -1 for x in birdNos1):  
        avatar1 = birds1[birdNos1[3]].getImage()
    else:
        avatar1 = py.image.load("Media/avatar1.png")
        avatar1 = py.transform.scale_by(avatar1, 0.5)

    if any(x != -1 for x in birdNos2):
        avatar2 = py.transform.flip(birds2[birdNos2[3]].getImage(),True,False)
    else:
        avatar2 = py.image.load("Media/avatar2.png")
        avatar2 = py.transform.scale_by(avatar2, 0.5)

    avatar1_rect = avatar1.get_rect()
    avatar2_rect = avatar2.get_rect()
    avatar1_rect.topleft = (0,0)
    avatar2_rect.topright = (settings.width,0)

    py.draw.circle(screen, settings.DARK_GRAY, (120,100),250)
    if active==0:
        py.draw.circle(screen, settings.YELLOW, (120,100),250,20)
    else:
        py.draw.circle(screen,settings.GRAY,(120,100),250,20)

    py.draw.circle(screen,settings.DARK_GRAY, (settings.width-120,100),250)

    if active==1:
        py.draw.circle(screen, settings.RED, (settings.width-120,100),250,20)
    else:
        py.draw.circle(screen, settings.GRAY, (settings.width-120,100),250,20)

    screen.blit(avatar1, avatar1_rect)
    screen.blit(avatar2, avatar2_rect)

def displayScore(screen, score1, score2, turn=None):
    multiplier = [1,1]
    if turn is not None:
        multiplier[turn] = 1.3
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

def rotateBirds(birdNos):
    birdNos[0] = -1
    for i in range(3,0,-1):
        birdNos[i] = birdNos[i-1]
        
def displayBirds(screen, playerNo, birdNos, birds, sling_rect):

    sling2 = rotateImg(py.transform.scale_by(py.image.load("Media/sling(2).png"),0.8),playerNo)
    sling2_rect = sling2.get_rect()
    sling2_rect.bottom = sling_rect.bottom
    sling2_rect.centerx = transformX(sling_rect.right-20-sling2.get_width()/2, playerNo)
    screen.blit(sling2, sling2_rect)

    

    for i in range(4):
        if birdNos[i]==-1: continue

        bird_block = birds[birdNos[i]].getImage()
        bird_block = rotateImg(py.transform.scale_by(bird_block, 0.2),playerNo)
        bird_block_rect = bird_block.get_rect()

        if i==3:
            bird_block_rect.centerx = transformX(sling_rect.centerx+15-bird_block.get_width()/2,playerNo)
            bird_block_rect.bottom = sling_rect.centery-30
        
        else:
            bird_block_rect.centerx = transformX((i+1)*100+50-bird_block.get_width()/2,playerNo)
            bird_block_rect.bottom = 930    
        screen.blit(bird_block, bird_block_rect)

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
            block = blocks[i][j].returnImg()
            block_rect = block.get_rect()
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

    #Sling
    sling = py.image.load("Media/sling.png")
    sling = py.transform.scale_by(sling,0.8)
    sling_rect = sling.get_rect()
    sling_rect.bottom = 930
    sling_rect.left = 400   

    #Player 2
    birdNos2 = [random.randint(0,Players.Player2.getBirdsNo()-1) for _ in range(4)]
    birds2 = Players.Player2.getBirds()

    #Blocks
    blockKeys = np.random.randint(0, 3, size=(4,2))
    blocks = np.array(Blocks.blocks)[blockKeys]
    # for i in range(4):
    #     for j in range(2):
    #         print(blocks[i][j].getName(),end='')

    #     print()

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


        score1 = settings.bigFont.render(str(Players.Player1.getScore()),True,settings.YELLOW)
        score2 = settings.bigFont.render(str(Players.Player2.getScore()),True,settings.RED)
        screen.blit(py.transform.scale(settings.bg1,screen.get_size()),(0,0))


        if state=="static":
            displayScore(screen, score1, score2)

            displayBirds(screen,1,birdNos1,birds1,sling_rect)

            displayBirds(screen,2,birdNos2,birds2,sling_rect)

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
            displayBirds(screen,1,birdNos1,birds1,sling_rect)

            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2,0)

            displayScore(screen, score1, score2,0)

            displayBlocks(screen, blocks, 2)


        elif state == "pause":
            displayScore(screen, score1, score2)
            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2)
            dim_surface = py.Surface(screen.get_size(), py.SRCALPHA)
            dim_surface.fill((0, 0, 0, 180))
            screen.blit(dim_surface,(0,0))

        
        py.display.flip()
        

    