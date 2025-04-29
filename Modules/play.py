import pygame as py, time, sys
import Modules.birds as Birds
import Modules.players as Players
import Modules.settings as settings
import Modules.blocks as Blocks
import random
import math
import numpy as np


#Check if bird went out of bounds
def checkBounds(birdRect):
    if birdRect.centerx > settings.width or birdRect.centerx<0 or birdRect.centery<-100:
        return True
    else:
        return False

#Scale down collision detection rectangle of birds
def scaleRect(rect):
    newRect = rect.copy()
    center = rect.center
    newRect.width = int(rect.width*0.9)
    newRect.height = int(rect.height*0.9)
    newRect.center = center
    return newRect

#Draw guide dots when launching
def drawTrajectory(screen, bird, slingCenter, start):
    g = settings.height/54
    dot_radius = 4
    scale = 20*((settings.width/1920)**0.2) #1m is 50 pixels
    velocity = (bird.speed**0.2)*(slingCenter-start)*0.2*((settings.width/1920)**0.1)

    #Different colour dots for different birds
    if bird.name == "Red":
        colour = settings.RED
    elif bird.name == "Chuck":
        colour = settings.YELLOW
    elif bird.name == "Bomb":
        colour = settings.GRAY
    elif bird.name == "Blue":
        colour = settings.ICE_BLUE
    else:
        colour = settings.PINK

    for t in range(8):
        dt = t*0.1
        x = start.x + (velocity.x*dt)*scale
        y = start.y + (velocity.y*dt + 0.5*g*(dt**2))*scale
        py.draw.circle(screen, colour, (int(x),int(y)), dot_radius)

#Draw slingshot rope lines when launching
def drawLine(screen, bird, sling_rect, playerNo):
    if bird.ifDragging:
        py.draw.line(screen, settings.ROPE_BROWN, bird.rect.center,(sling_rect.centerx-(3-2*playerNo)*settings.width/76.8,sling_rect.centery-settings.height/19.6),width=15)
        py.draw.line(screen, settings.ROPE_BROWN, bird.rect.center,(sling_rect.centerx+(3-2*playerNo)*settings.width/384,sling_rect.centery-settings.height/21.6),width=15)
        
#Display avatars of Players on top left and top right of screen. Shows current bird-if empty, shows fixed
def displayAvatar(screen, birdNos1, birds1, birdNos2, birds2, active=None):
    #Shows birds according to theme
    if settings.theme == "space":
        avatars = Birds.spaceBirds
    elif settings.theme == "ghost":
        avatars = Birds.ghostBirds
    elif settings.theme == "samurai":
        avatars = Birds.samuraiBirds

    
    if any(x != -1 for x in birdNos1):  
        avatar1 = avatars[Birds.birdNos[birds1[birdNos1[3]].name]]
    else:
        avatar1 = avatars[0]

    if any(x != -1 for x in birdNos2):
        avatar2 = py.transform.flip(avatars[Birds.birdNos[birds2[birdNos2[3]].name]],True,False)
    else:
        avatar2 = py.transform.flip(avatars[1],True,False)

    avatar1 = py.transform.scale_by(avatar1, settings.width/1920)
    avatar2 = py.transform.scale_by(avatar2, settings.width/1920)
    avatar1_rect = avatar1.get_rect()
    avatar2_rect = avatar2.get_rect()
    avatar1_rect.topleft = (0,0)
    avatar2_rect.topright = (settings.width,0)

    radius = settings.width/7.7
    thickness = int(settings.width/96)
    
    #If P1 is active, Yellow circle around its Avatar
    py.draw.circle(screen, settings.DARK_GRAY, (settings.width/16,settings.height/10.8),radius)
    if active==1:
        py.draw.circle(screen, settings.YELLOW, (settings.width/16,settings.height/10.8),radius,thickness)
    else:
        py.draw.circle(screen,settings.GRAY,(settings.width/16,settings.height/10.8),radius,thickness)

    py.draw.circle(screen,settings.DARK_GRAY, (settings.width*15/16,settings.height/10.8),radius)
    #If P2 is active, Red circle aruond its avatar
    if active==2:
        py.draw.circle(screen, settings.RED, (settings.width*15/16,settings.height/10.8),radius,thickness)
    else:
        py.draw.circle(screen, settings.GRAY, (settings.width*15/16,settings.height/10.8),radius,thickness)

    screen.blit(avatar1, avatar1_rect)
    screen.blit(avatar2, avatar2_rect)

#Displays score on top middle of screen
def displayScore(screen, score1, score2, turn=None, ifAdding=False):
    multiplier = [1,1]
    if turn is not None:
        multiplier[turn-1] = 1.3
    score1 = py.transform.scale_by(score1, multiplier[0])
    score2 = py.transform.scale_by(score2, multiplier[1])
    sep = settings.bigFont.render("i",True,settings.black)
    sep = py.transform.scale(sep, (settings.width/38.4,settings.height/3.5))
    score1_rect = score1.get_rect()
    score2_rect = score2.get_rect()
    score1_rect.topright = (settings.width/2-settings.width/19.2,settings.height/21.6)
    score2_rect.topleft = (settings.width/2+settings.width/19.2,settings.height/21.6)
    sep_rect = sep.get_rect(center=((score1_rect.right+score2_rect.left)/2,settings.height/10.8))
    screen.blit(sep, sep_rect)
    if(not ifAdding):
        screen.blit(score1, score1_rect)
        screen.blit(score2, score2_rect)

def transformX(x, playerNo):
    return x if playerNo==1 else settings.width-x

def rotateImg(img, playerNo):
    return img if playerNo==1 else py.transform.flip(img, True, False)

#Cycles through the birds as they're used
def rotateBirds(birdNos, birdsPlay):
    for i in range(3,0,-1):
        birdNos[i] = birdNos[i-1]
        birdsPlay[i] = birdsPlay[i-1]

    birdNos[0] = -1
    birdsPlay[0] = None


#Displaying the birds on screen      
def displayBirds(screen, playerNo, birdNos, sling_rect, birdsPlay):
    sling_rect_trans = sling_rect.copy()
    sling_rect_trans.centerx = transformX(sling_rect.centerx, playerNo)

    sling2 = rotateImg(py.transform.scale(py.image.load("Media/sling(2).png"),(settings.width/49.2,settings.height/6.7)),playerNo)
    sling2_rect = sling2.get_rect()
    sling2_rect.bottom = sling_rect.bottom
    sling2_rect.centerx = transformX(sling_rect.right-settings.width/96-sling2.get_width()/2, playerNo)
    
    screen.blit(sling2, sling2_rect)


    for i in range(4):
        if birdNos[i]==-1: continue

        bird = birdsPlay[i]
        bird.image = rotateImg(py.transform.scale(bird.initImage, (settings.width/bird.scaleFactor[0],settings.height/bird.scaleFactor[1])),playerNo)
        bird.updateRect()    
        bird.updatePos(i,playerNo,sling_rect, settings.bottom, settings.width, settings.height)
        drawLine(screen, bird, sling_rect_trans, playerNo)
        if bird.ifDragging:
            drawTrajectory(screen, bird, py.Vector2(bird.initRect.center), py.Vector2(bird.rect.center))
        screen.blit(bird.image, bird.rect)

    del sling_rect_trans
    sling1 = py.image.load("Media/sling(1).png")
    sling1 = rotateImg(py.transform.scale(sling1, (settings.width/42.7,settings.height/10.4)),playerNo)
    sling1_rect = sling1.get_rect()
    sling1_rect.topleft = sling_rect.topleft
    sling1_rect.centerx = transformX(sling1_rect.left+sling1.get_width()/2,playerNo)
    if playerNo==1: sling1_rect.left -= settings.width/384
    else: sling1_rect.left+= settings.width/384
    screen.blit(sling1, sling1_rect)

#Displaying the blocks on screen
def displayBlocks(screen, blocks, playerNo):
    for i in range(4):
        for j in range(2):
            if blocks[i][j] is not None:
                block = blocks[i][j].returnImg()
                if block is not None and blocks[i][j] is not None:
                    block_rect = blocks[i][j].rect
                    block_rect.centerx = transformX(settings.width/5.5+(settings.width/21.3)*j,playerNo)
                    block_rect.centery = int(settings.bottom-block.get_width()/2-block.get_height()*i)
                    screen.blit(block,block_rect)

#Making the blocks fall down if no block below it (i.e., gravity for blocks)
def rotateBlocks(screen, blocks, blocksNo):
    for i in range(4):
        for j in range(2):
            if blocks[i][j] is not None and blocks[i][j].health<=0:
                if i<=2 and blocks[i+1][j] is not None:
                    for k in range(i+1,4):
                        if blocks[k][j] is None:
                            blocks[k-1][j] = None
                        else:
                            blocks[k-1][j] = blocks[k][j].clone()
                    blocks[3][j] = None
                else:
                    blocks[i][j] = None

                displayBlocks(screen, blocks, blocksNo)


#Main playing game function (called from main)
def playGame(screen):
    py.mixer.stop()

    clock = py.time.Clock()

    startTime = py.time.get_ticks()
    state = "static"
    prevState = "static"

    fightImg = py.image.load("Media/fight.png")
    fightInitSize = fightImg.get_size()

    start_scale = 7
    end_scale = 1

    #Defining theme specific settings
    if settings.theme == "ghost":
        settings.bottom = settings.height/1.2
        r,g,b = settings.GRAY
        eagle = py.transform.scale_by(Birds.eagle1,settings.width/1920)
    elif settings.theme == "space":
        settings.bottom = settings.height/1.14
        r,g,b = settings.ICE_BLUE
        eagle = py.transform.scale_by(Birds.eagle2,settings.width/1920)
    elif settings.theme == "samurai":
        settings.bottom = settings.height/1.18
        r,g,b = settings.YELLOW
        eagle = py.transform.scale_by(Birds.eagle3,settings.width/1920)
    eagle_rect = eagle.get_rect()

    p1Eagle = False
    p2Eagle = False

    #Parameters for special ability
    maxFreq = 10
    vibrationAmplitude = 5
    vibrationDuration = 3.5
    ballMaxRadius = int(30*settings.width/1920)
    lineWidth = int(20*settings.width/1920)


    duration = 1
    scoreTime = 0
    score = 0

    bgm = settings.currentBgm
    bgm.play(-1)
    bgm.set_volume(settings.musicVolume/3)
    

    #Player 1
    birdNos1 = [random.randint(0,Players.Player1.getBirdsNo()-1) for _ in range(4)] #Initializing birds
    birds1 = Players.Player1.getBirds()
    birdsPlay1 = [birds1[x].clone() for x in birdNos1]

    #Sling
    sling = py.image.load("Media/sling.png")
    sling = py.transform.scale(sling,(settings.width/24,settings.height/6.4))
    sling_rect = sling.get_rect()
    sling_rect.bottom = settings.bottom
    sling_rect.left = settings.width/4.8

    #Player 2
    birdNos2 = [random.randint(0,Players.Player2.getBirdsNo()-1) for _ in range(4)]
    birds2 = Players.Player2.getBirds()
    birdsPlay2 = [birds2[x].clone() for x in birdNos2]

    #Blocks
    blockKeys = np.random.randint(0, 3, size=(4,2))
    blocks1 = np.empty_like(blockKeys, dtype=object)
    blocks2 = np.empty_like(blockKeys, dtype=object)
    for i in range(4):
        for j in range(2):
           blocks1[i,j] = Blocks.blocks[blockKeys[i,j]].clone() 
           blocks2[i,j] = Blocks.blocks[blockKeys[i,j]].clone()

    
    #Initializing of volume sliders
    slider_width = settings.width/5
    slider_height = settings.height/20
    handler_x = settings.width/2 - slider_width/2 + settings.width/12
    slider_y = 0
    slider_x = handler_x
    dragging = False

    slider_width2 = settings.width/5
    slider_height2 = settings.height/20
    handler_x2 = settings.width/2 - slider_width2/2 + settings.width/12
    slider_y2 = 0
    slider_x2 = handler_x2
    dragging2 = False
    
    #Initializing images
    musicImg = py.image.load("Media/music.png")
    musicImg = py.transform.scale(musicImg, (slider_height*(775/322),slider_height))
    musicImg_rect = musicImg.get_rect()
    sfxImg = py.image.load("Media/sfx.png")
    sfxImg = py.transform.scale(sfxImg, (slider_height*(642/389), slider_height))   
    sfxImg_rect = sfxImg.get_rect() 

    quitImg = py.image.load("Media/quit.png")
    quitImg = py.transform.scale(quitImg, (settings.width/12, settings.width/12*(214/499)))
    quitImg_rect = quitImg.get_rect()

    backImg = py.image.load("Media/back.png")
    backImg = py.transform.scale(backImg, quitImg.get_size())
    backImg_rect = backImg.get_rect()
    

    while True:

        bgm.set_volume(settings.musicVolume/3)

        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()
            elif event.type == py.KEYDOWN:

                #Checking if pause menu triggered
                if event.key == py.K_ESCAPE:
                    if state != "pause":
                        prevState = state
                        state = "pause"
                    else:
                        state = prevState

            if state=="player1":
                if event.type == py.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #Checking if launching bird
                        if birdsPlay1[3].rect.collidepoint(event.pos) and birdsPlay1[3].ifLaunched == False:
                            birdsPlay1[3].ifDragging = True
                            py.mixer.music.load("Media/audio/sling_pull-2.mp3")
                            py.mixer.music.play(loops=0)
                            py.mixer.music.set_volume(settings.sfxVolume)
                    elif event.button == 3:
                        #Checking if special ability
                        if birdsPlay1[3].ifLaunched == True and birdsPlay1[3].ifCollided == False and not p1Eagle:
                            p1Eagle = True
                            py.mixer.stop()
                            currentCenter = py.Vector2(*birdsPlay1[3].rect.center)
                            angle = math.degrees(math.atan2(-birdsPlay1[3].changeVelocity.y, birdsPlay1[3].changeVelocity.x))
                            direction = birdsPlay1[3].changeVelocity.normalize()
                            eagleStart = py.time.get_ticks()/1000
                            birdsPlay1[3] = None
                            birdNos1[3] = -1
                            state = "p1ability"
                            py.mixer.music.load("Media/audio/laser_charge.mp3")
                            py.mixer.music.set_volume(settings.sfxVolume)
                            py.mixer.music.play()

                #Second part of launching bird
                elif event.type == py.MOUSEBUTTONUP:
                    if birdsPlay1[3].ifDragging:
                        birdsPlay1[3].ifDragging = False
                        birdsPlay1[3].ifLaunched = True

                        birdsPlay1[3].initVelocity(settings.width)    
                        birdsPlay1[3].startTime = py.time.get_ticks()
                        py.mixer.music.load(birdsPlay1[3].launchSound)
                        py.mixer.music.play(loops=0)
                        py.mixer.music.set_volume(settings.sfxVolume)
                        

            elif state=="player2":
                if event.type == py.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if birdsPlay2[3].rect.collidepoint(event.pos) and birdsPlay2[3].ifLaunched == False and not p2Eagle:
                            birdsPlay2[3].ifDragging = True
                            py.mixer.music.load("Media/audio/sling_pull-2.mp3")
                            py.mixer.music.play(loops=0)
                            py.mixer.music.set_volume(settings.sfxVolume)

                    elif event.button == 3:
                        if birdsPlay2[3].ifLaunched == True and birdsPlay2[3].ifCollided == False:
                            py.mixer.stop()
                            currentCenter = py.Vector2(*birdsPlay2[3].rect.center)
                            angle = math.degrees(math.atan2(-birdsPlay2[3].changeVelocity.y, birdsPlay2[3].changeVelocity.x))
                            direction = birdsPlay2[3].changeVelocity.normalize()
                            eagleStart = py.time.get_ticks()/1000
                            birdsPlay2[3] = None
                            birdNos2[3] = -1
                            state = "p2ability"
                            py.mixer.music.load("Media/audio/laser_charge.mp3")
                            py.mixer.music.set_volume(settings.sfxVolume)
                            py.mixer.music.play()

                elif event.type == py.MOUSEBUTTONUP:
                    if birdsPlay2[3].ifDragging:
                        birdsPlay2[3].ifDragging = False
                        birdsPlay2[3].ifLaunched = True

                        birdsPlay2[3].initVelocity(settings.width)
                        birdsPlay2[3].startTime = py.time.get_ticks()
                        py.mixer.music.load(birdsPlay2[3].launchSound)
                        py.mixer.music.play(loops=0)
                        py.mixer.music.set_volume(settings.sfxVolume)

            elif state=="pause":
                if event.type == py.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if (slider_x <= mx <= slider_x + slider_width) and (slider_y <= my <= slider_y + slider_height):
                        dragging = True
                        handler_x = max(slider_x, min(slider_x + slider_width, event.pos[0]))
                        volume = (mx - slider_x) / slider_width
                        settings.sfxVolume = volume
                    elif (slider_x2 <= mx <= slider_x2+slider_width2) and (slider_y2 <= my <= slider_y2 + slider_height2):
                        dragging2 = True
                        handler_x2 = max(slider_x2, min(slider_x2+slider_width2,event.pos[0]))
                        settings.musicVolume = (mx - slider_x2)/slider_width
                    elif backImg_rect.collidepoint(event.pos):
                        settings.state = "select"
                        Players.Player1.birds = []
                        Players.Player2.birds = []
                        Players.Player1.score = 0
                        Players.Player2.score = 0
                        bgm.stop()
                        return
                    elif quitImg_rect.collidepoint(event.pos):
                        sys.exit()
                    
                elif event.type == py.MOUSEBUTTONUP:
                    dragging = False
                    dragging2 = False
                elif event.type == py.MOUSEMOTION and dragging:
                    mx, my = event.pos
                    volume = (mx - slider_x) / slider_width
                    volume = max(0.0, min(1.0, volume))  # clamp between 0.0 and 1.0
                    handler_x = max(slider_x, min(slider_x + slider_width, event.pos[0]))
                    settings.sfxVolume = volume
                elif event.type == py.MOUSEMOTION and dragging2:
                    mx, my = event.pos
                    volume = (mx - slider_x2) / slider_width2
                    volume = max(0.0, min(1.0, volume))  # clamp between 0.0 and 1.0
                    handler_x2 = max(slider_x2, min(slider_x2 + slider_width2, event.pos[0]))
                    settings.musicVolume = volume

        #Getting score from Player Classes
        score1 = settings.bigFont.render(str(Players.Player1.getScore()),True,settings.YELLOW)
        score1 = py.transform.scale_by(score1, settings.width/1920)
        score2 = settings.bigFont.render(str(Players.Player2.getScore()),True,settings.RED)
        score2 = py.transform.scale_by(score2, settings.width/1920)

        screen.blit(py.transform.scale(settings.currentBg,screen.get_size()),(0,0))

        #When nothing is happening, i.e., no player's turn
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
            
            scale = start_scale + (end_scale-start_scale)*ease
            newFightSize = (int(fightInitSize[0]*scale),int(fightInitSize[1]*scale))
            fight = py.transform.smoothscale(fightImg, newFightSize)
            fight_rect = fight.get_rect(center=(settings.width/2,settings.height/2))

            screen.blit(fight,fight_rect)

            if (py.time.get_ticks()-startTime)/1000>2:
                state = "player1"

        #When it is Player 1's turn
        elif state == "player1":
            #Check for winner
            if Players.Player2.score >= 480:
                settings.state = "winner"
                settings.winner = Players.Player2.name
                return
            
            displayBirds(screen,1,birdNos1,sling_rect,birdsPlay1)

            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2,1)

            displayScore(screen, score1, score2,1)

            displayBlocks(screen, blocks1, 2)


            if birdsPlay1[3].ifLaunched:

                #Check if bird slowed down a lot/stopped or went out of bounds
                if checkBounds(birdsPlay1[3].rect) or (birdsPlay1[3].changeVelocity.magnitude()<(20*settings.width/1920) and birdsPlay1[3].rect.bottom>settings.bottom):
                    score = 0
                    state = "p1score"
                    scoreTime = py.time.get_ticks()/1000
                    continue

                #Check for collision
                for i in range(4):
                    if birdsPlay1[3].ifCollided:
                        break
                    for j in range(2):
                        if blocks1[i][j] is not None:
                            if (scaleRect(birdsPlay1[3].rect)).colliderect(blocks1[i][j].rect):

                                #Playing collision sfx
                                py.mixer.music.load("Media/audio/collision.wav")
                                py.mixer.music.play()
                                py.mixer.music.set_volume(settings.sfxVolume)

                                #Collision bounce mechanism
                                if birdsPlay1[3].rect.centerx<=(blocks1[i][j].rect.left):
                                    birdsPlay1[3].collideTime = (py.time.get_ticks()-birdsPlay1[3].startTime)/1000
                                    birdsPlay1[3].velocity[0] = -birdsPlay1[3].velocity[0]*0.5
                                    birdsPlay1[3].initRect.centerx = birdsPlay1[3].rect.centerx
                                elif birdsPlay1[3].rect.centery<=(blocks1[i][j].rect.top):
                                    birdsPlay1[3].ifCollideTop = True
                                    birdsPlay1[3].updatePos(3,1,sling_rect,settings.bottom, settings.width, settings.height)

                                py.draw.rect(screen,settings.WHITE,blocks1[i][j].rect,width=20)

                                birdsPlay1[3].ifCollided = True

                                #Score calculation
                                if birdsPlay1[3].affinity == blocks1[i][j].name:
                                    score = int(birdsPlay1[3].damageMultiplier*20)
                                else:
                                    score = int(20*birdsPlay1[3].damageDivider)
                                
                                score = min(score,blocks1[i][j].health)

                                blocks1[i][j].health -= score
                                Players.Player1.score += score
                                
                                state = "p1score"
                                
                                scoreTime = py.time.get_ticks()/1000

                                #Rotate blocks downwards (gravity)
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

        #When it is Player 2's turn
        elif state == "player2":

            #Checking for winner
            if Players.Player1.score >= 480:
                settings.state = "winner"
                settings.winner = Players.Player1.name
                return
            

            displayBirds(screen,2,birdNos2,sling_rect,birdsPlay2)

            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2,2)

            displayScore(screen, score1, score2, 2)

            
            displayBlocks(screen, blocks2,1)

            if birdsPlay2[3].ifLaunched:

                #Checking if bird went out or slowed down a lot/stopped
                if checkBounds(birdsPlay2[3].rect) or (birdsPlay2[3].changeVelocity.magnitude()<(20*settings.width/1920) and birdsPlay2[3].rect.bottom>(settings.bottom-10)):
                    score = 0
                    state = "p2score"
                    scoreTime = py.time.get_ticks()/1000
                    continue

                #Checking for collision
                for i in range(4):
                    if birdsPlay2[3].ifCollided:
                        break
                    for j in range(2):
                        if blocks2[i][j] is not None:
                            if scaleRect(birdsPlay2[3].rect).colliderect(blocks2[i][j].rect):

                                #Playing collision sfx
                                py.mixer.music.load("Media/audio/collision.wav")
                                py.mixer.music.play()
                                py.mixer.music.set_volume(settings.sfxVolume)

                                #Collision bounce mechanism
                                if birdsPlay2[3].rect.centerx>=(blocks2[i][j].rect.right):
                                    birdsPlay2[3].collideTime = (py.time.get_ticks()-birdsPlay2[3].startTime)/1000
                                    birdsPlay2[3].velocity[0] = -birdsPlay2[3].velocity[0]*0.5
                                    birdsPlay2[3].initRect.centerx = birdsPlay2[3].rect.centerx
                                elif birdsPlay2[3].rect.centery<=(blocks2[i][j].rect.top):
                                    birdsPlay2[3].ifCollideTop = True
                                    birdsPlay2[3].updatePos(3,1,sling_rect,settings.bottom, settings.width, settings.height)

                                py.draw.rect(screen,settings.WHITE,blocks2[i][j].rect)
                                birdsPlay2[3].ifCollided = True

                                #Score calculation
                                if birdsPlay2[3].affinity == blocks2[i][j].name:
                                    score = int(birdsPlay2[3].damageMultiplier*20)
                                else:
                                    score = int(20*birdsPlay2[3].damageDivider)

                                score = min(score, blocks2[i][j].health)

                                blocks2[i][j].health -= score
                                Players.Player2.score += score

                                #Blocks gravity
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
                    
                    state = "p2score"
                    scoreTime = py.time.get_ticks()/1000

        #When Player 1 uses ability
        elif state == "p1ability":

            displayBirds(screen, 1, birdNos1, sling_rect, birdsPlay1)
            
            displayBlocks(screen, blocks1, 2)
            
            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2,1)

            displayScore(screen, score1, score2,1)
            
            eagle_rotated = py.transform.rotate(eagle,angle)

            t = py.time.get_ticks()/1000 - eagleStart
            
            #Displaying beam
            origin = currentCenter + direction*eagle_rotated.get_width()/2
            laser_surf = py.Surface(screen.get_size(), py.SRCALPHA)
            beam_length = (py.time.get_ticks()/1000 - eagleStart - vibrationDuration - 1)*400*settings.width/1920
            end_pos = origin + direction*beam_length
            glow_width = random.randint(lineWidth+5,lineWidth+int(15*settings.width/1920))

            if t<vibrationDuration:
                t1 = t/vibrationDuration
                freq = t1**3 * maxFreq
                theta = math.sin(t * freq * 2 * math.pi)*vibrationAmplitude
                radius = t1**3 * ballMaxRadius
            elif t-vibrationDuration<=0.1:
                time.sleep(1)
            else:
                theta = 0
                
                radius = ballMaxRadius

                py.draw.line(laser_surf, (r,g,b,128), origin, end_pos, glow_width)
                
                py.draw.line(screen, (r,g,b), origin, end_pos, lineWidth)
            
            eagle_final = py.transform.rotate(eagle_rotated,theta)
            glow_radius = random.randint(int(radius),int(radius)+10)
            py.draw.circle(screen, (r,g,b), (int(origin.x),int(origin.y)),int(radius))
            py.draw.circle(laser_surf, (r,g,b,128), (int(origin.x),int(origin.y)),glow_radius)
            eagle_rect = eagle_final.get_rect(center=currentCenter)
            screen.blit(eagle_final,eagle_rect)
            screen.blit(laser_surf, (0,0))

            #Particle effects
            for _ in range(10):
                angle1 = random.uniform(-30, 30)
                spark_dir = direction.rotate(angle1) * random.uniform(2, 4)
                spark_pos = origin + spark_dir * random.uniform(2, 10)
                py.draw.circle(screen, (r,g,b), spark_pos, 2)

            #Beam collision with blocks
            for i in range(4):
                for j in range(2):
                    if blocks1[i][j] is not None:
                        if (blocks1[i][j].rect.collidepoint(end_pos)):
                            py.draw.rect(screen,settings.WHITE,blocks1[i][j].rect,width=20)
                            score += blocks1[i][j].health
                            Players.Player1.score += blocks1[i][j].health
                            blocks1[i][j].health = 0
                            displayBlocks(screen, blocks1, 2)

            if t>8:
                for i in range(3):
                    rotateBlocks(screen, blocks1, 2)
                scoreTime = py.time.get_ticks()/1000
                state = "p1score"

        #When Player 2 uses ability
        elif state == "p2ability":
            displayBirds(screen, 2, birdNos2, sling_rect, birdsPlay2)
            
            displayBlocks(screen, blocks2, 1)
            
            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2,1)

            displayScore(screen, score1, score2, 2)

            eagle_rotated = py.transform.flip(py.transform.rotate(py.transform.flip(eagle,True,False),angle),True,True)

            t = py.time.get_ticks()/1000 - eagleStart
            
            #Initializing and displaying beam
            origin = currentCenter + direction*eagle_rotated.get_width()/2
            laser_surf = py.Surface(screen.get_size(), py.SRCALPHA)
            beam_length = (py.time.get_ticks()/1000 - eagleStart - vibrationDuration - 1)*400*settings.width/1920
            end_pos = origin + direction*beam_length
            glow_width = random.randint(lineWidth+5,lineWidth+int(15*settings.width/1920))

            if t<vibrationDuration:
                t1 = t/vibrationDuration
                freq = t1**3 * maxFreq
                theta = math.sin(t * freq * 2 * math.pi)*vibrationAmplitude
                radius = t1**3 * ballMaxRadius
            elif t-vibrationDuration<=0.1:
                time.sleep(1)
            else:
                theta = 0
                
                radius = ballMaxRadius

                py.draw.line(laser_surf, (r,g,b,128), origin, end_pos, glow_width)
                
                py.draw.line(screen, (r,g,b), origin, end_pos, lineWidth)
            
            eagle_final = py.transform.rotate(eagle_rotated,theta)
            glow_radius = random.randint(int(radius),int(radius)+10)
            py.draw.circle(screen, (r,g,b), (int(origin.x),int(origin.y)),int(radius))
            py.draw.circle(laser_surf, (r,g,b,128), (int(origin.x),int(origin.y)),glow_radius)
            eagle_rect = eagle_final.get_rect(center=currentCenter)
            screen.blit(eagle_final,eagle_rect)
            screen.blit(laser_surf, (0,0))

            #Particle effects
            for _ in range(10):
                angle1 = random.uniform(-30, 30)
                spark_dir = direction.rotate(angle1) * random.uniform(2, 4)
                spark_pos = origin + spark_dir * random.uniform(2, 10)
                py.draw.circle(screen, (r,g,b), spark_pos, 2)


            for i in range(4):
                for j in range(2):
                    if blocks2[i][j] is not None:
                        if (blocks2[i][j].rect.collidepoint(end_pos)):
                            py.draw.rect(screen,settings.WHITE,blocks2[i][j].rect,width=20)
                            score += blocks2[i][j].health
                            Players.Player2.score += blocks2[i][j].health
                            blocks2[i][j].health = 0
                            displayBlocks(screen, blocks2, 1)

            if t>8:
                for i in range(3):
                    rotateBlocks(screen, blocks2, 1)
                scoreTime = py.time.get_ticks()/1000
                state = "p2score"

        #When displaying Player 1's score animation
        elif state == "p1score":

            if not py.mixer.get_busy():
                bgm.play(-1)

            t = py.time.get_ticks()/1000-scoreTime

            if t >= 1:
                rotateBirds(birdNos1,birdsPlay1)
                state = "player2"
                score = 0

            displayScore(screen, score1, score2, ifAdding=True)
            displayAvatar(screen, birdNos1, birds1, birdNos2,birds2)
            displayBlocks(screen, blocks1, 2)
            displayBirds(screen, 1, birdNos1, sling_rect, birdsPlay1)

            #Dim background
            dim_surface = py.Surface(screen.get_size(), py.SRCALPHA)
            dim_surface.fill((0, 0, 0, 200))
            screen.blit(dim_surface,(0,0))

            #Display score animation
            scoreDisplay = settings.bigFont.render("+"+str(score),True,settings.YELLOW)
            scoreDisplay = py.transform.scale_by(scoreDisplay,max(2-t**2,1))
            scoreDisplayRect = scoreDisplay.get_rect(center=(settings.width/2+(settings.width/2.4-settings.width/2)*(t**2),(settings.height/2+(settings.height/10-settings.height/2)*(t**2))))
            screen.blit(scoreDisplay,scoreDisplayRect)
            
        #When displaying Player 2's score animation
        elif state == "p2score":
            if not py.mixer.get_busy():
                bgm.play(-1)
            t = py.time.get_ticks()/1000-scoreTime
            if t >= 1:

                if any(x != -1 for x in birdNos1): 
                    rotateBirds(birdNos2,birdsPlay2)
                else:
                    birdNos1 = [random.randint(0,Players.Player1.getBirdsNo()-1) for _ in range(4)] #Initializing birds
                    birdsPlay1 = [birds1[x].clone() for x in birdNos1]

                    birdNos2 = [random.randint(0,Players.Player2.getBirdsNo()-1) for _ in range(4)]
                    birdsPlay2 = [birds2[x].clone() for x in birdNos2]

                score = 0
                state = "player1"

            displayScore(screen, score1, score2, ifAdding=True)
            displayAvatar(screen, birdNos1, birds1, birdNos2,birds2)
            displayBlocks(screen, blocks2, 1)
            displayBirds(screen, 2, birdNos2, sling_rect, birdsPlay2)

            dim_surface = py.Surface(screen.get_size(), py.SRCALPHA)
            dim_surface.fill((0, 0, 0, 200))
            screen.blit(dim_surface,(0,0))

            scoreDisplay = settings.bigFont.render("+"+str(score),True,settings.RED)
            scoreDisplay = py.transform.scale_by(scoreDisplay,max(2-t**2,1))
            scoreDisplayRect = scoreDisplay.get_rect(center=(settings.width/2+(settings.width/1.8-settings.width/2)*(t**2),settings.height/2+(settings.height/10-settings.height/2)*(t**2)))
            screen.blit(scoreDisplay,scoreDisplayRect)
            
        #When displaying pause popup
        elif state == "pause":
            displayScore(screen, score1, score2)
            displayAvatar(screen, birdNos1, birds1, birdNos2, birds2)

            #Dim background
            dim_surface = py.Surface(screen.get_size(), py.SRCALPHA)
            dim_surface.fill((0, 0, 0, 180))
            screen.blit(dim_surface,(0,0))

            #Pause menu rectangle and texts
            pauseMenu = py.Rect(10,10,settings.width/3,settings.height/3)
            pauseMenu.center = (settings.width/2,settings.height/2)
            
            py.draw.rect(screen, settings.RED, pauseMenu, border_radius=int(20*settings.width/1920))
            py.draw.rect(screen, settings.black, pauseMenu, width=int(10*settings.width/1920))

            pauseText = settings.bigFont.render("PAUSE",True,settings.black)
            pauseText = py.transform.scale(pauseText, (settings.width*0.8/8,settings.height*0.8/10))
            pauseText_rect = pauseText.get_rect()
            pauseText_rect.center = (pauseMenu.centerx,pauseMenu.top + settings.height/17)
            screen.blit(pauseText,pauseText_rect)

            #Volume sliders
            slider_x = pauseText_rect.centerx-slider_width/2+settings.width/30
            slider_y = pauseText_rect.bottom + settings.height/60
            py.draw.rect(screen, settings.GRAY, (slider_x, slider_y, slider_width, slider_height))

            fill_width = handler_x-slider_x
            if fill_width>0:
                py.draw.rect(screen, settings.YELLOW, (slider_x, slider_y, fill_width, slider_height))

            slider_x2 = slider_x
            slider_y2 = slider_y + slider_height + settings.height/40
            py.draw.rect(screen, settings.GRAY, (slider_x2, slider_y2, slider_width2, slider_height2))

            fill_width2 = handler_x2-slider_x2
            if fill_width2>0:
                py.draw.rect(screen, settings.YELLOW, (slider_x2, slider_y2, fill_width2, slider_height2))

            #Displaying images
            musicImg_rect.centery = slider_y2+slider_height2/2
            musicImg_rect.centerx = (slider_x+settings.width/3)/2
            screen.blit(musicImg, musicImg_rect)

            sfxImg_rect.centery = slider_y+slider_height/2
            sfxImg_rect.centerx = (slider_x+settings.width/3)/2
            screen.blit(sfxImg, sfxImg_rect)

            quitImg_rect.bottom = pauseMenu.bottom-settings.height/80
            quitImg_rect.centerx = (settings.width/2+pauseMenu.right)/2
            screen.blit(quitImg, quitImg_rect)

            backImg_rect.bottom = quitImg_rect.bottom
            backImg_rect.centerx = (pauseMenu.left+settings.width/2)/2
            screen.blit(backImg, backImg_rect)

        clock.tick_busy_loop(60) #Set FPS to 60
        py.display.flip()
        

    