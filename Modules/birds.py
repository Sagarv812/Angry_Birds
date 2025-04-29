import pygame as py, sys, time

birds = [
    ["Media/Birds/red1.png",None,10],
    ["Media/Birds/chuck1.png","wood",20],
    ["Media/Birds/bomb1.png","stone",5],
    ["Media/Birds/blue1.png","ice",15],
    ["Media/Birds/stella1.png",None,15]
]
#template = {image file,affinity,speed}

def transformX(x, playerNo, width):
    return x if playerNo==1 else width-x

def rotateImg(self,playerNo):
    return py.transform.scale()

def scaler(img):
    return py.transform.scale(img, (300,280))

def scalerEagle(img):
    return py.transform.scale(img, (200,200))

class Birds:

    def __init__(self, name, image, affinity, speed, baseDamage, damageMultiplier, damageDivider, avatarImg, scaleFactor):
        self.name = name
        self.image = image
        self.initImage = image
        self.affinity = affinity
        self.speed = speed
        self.baseDamage = baseDamage
        self.damageMultiplier = damageMultiplier
        self.avatarImg = avatarImg
        self.ifLaunched = False
        self.ifCollided = False
        self.ifDragging = False
        self.velocity = py.Vector2(0,0)
        self.startTime = 0
        self.bounceTime = 0
        self.collideTime = 0
        self.ifBounced = False
        self.ifCollideTop = False
        self.damageDivider = damageDivider
        self.launchSound = None
        self.scaleFactor = scaleFactor

    def changeAffinity(self, newAffinity):
        self.affinity = newAffinity

    def clone(self):
        bird = Birds(self.name, self.image,self.affinity,self.speed,self.baseDamage,self.damageMultiplier,self.damageDivider,self.avatarImg,self.scaleFactor)
        bird.addLaunchSound(self.launchSound)
        return bird
    
    def getAffinity(self):
        return self.affinity
    
    def getImage(self):
        return self.image
    
    def getAvatarImage(self):
        return self.avatarImg
    
    def updateRect(self):
        self.rect = self.image.get_rect()
        if not(self.ifDragging or self.ifLaunched):
            self.initRect = self.rect
    # def updatePos(self):
    # g = 9.8 #acceleration due to gravity
    # scale = 50 #scale: 50 pixels is 1 meter

    # def drawLine(self,screen):
    #     py.draw.line(screen, (193,107,30),self.initRect.center,self.rect.center,3)

    # def drawTrajectory(self, point1, start, screen):
    #     g = 9.8
    #     dot_radius = 4
    #     powerFactor = 5
    #     scale = 50 #1m is 50 pixels
    #     velocity = self.speed*(point1-start)*0.5

    #     for t in range(50):
    #         dt = t*0.1
    #         x = start.x + (velocity.x*dt)*scale
    #         y = start.y + (velocity.y*dt + 0.5*g*(dt**2))*scale
    #         py.draw.circle(screen, (255,255,255), (int(x),int(y)), dot_radius)

        
    def initVelocity(self,width):
        slingCenter = py.Vector2(self.initRect.center)
        birdCenter = py.Vector2(self.rect.center)
        self.velocity = (slingCenter-birdCenter)*0.2*(self.speed**0.2)*((width/1920)**0.1)
        self.changeVelocity = self.velocity.copy()
        self.initRect = self.rect   

    #template(old pixel count, time b/w two frames in milliseconds, speed in pixels/s)
    def updatePos(self, birdNo, playerNo, sling_rect, bottom, width, height):
        g = 20*height/1080
        # sling_rect_trans = copy.copy(sling_rect)
        # sling_rect_trans.x = transformX(sling_rect.x,playerNo)
        if birdNo==3:
            if self.ifDragging:
                point1 = py.math.Vector2(self.initRect.center)
                point2 = py.math.Vector2(py.mouse.get_pos())
                if (point1.distance_to(point2)<200*width/1920):
                    self.rect.center = py.mouse.get_pos()
                else:
                    direction = point2 - point1
                    unit_direction = direction.normalize()
                    self.rect.center = point1+200*unit_direction*width/1920
                    point2 = py.Vector2(self.rect.center)

                # self.drawTrajectory(point1, point2, screen)
            elif self.ifLaunched or self.ifCollided:
                scale = 20
                t = (py.time.get_ticks()-self.startTime)/1000
                # print("before if: ",self.rect)
                self.changeVelocity[1] += g/60
                self.rect.centerx = self.initRect.centerx + self.velocity[0]*(t-self.collideTime)*scale
                self.rect.centery = self.initRect.centery + (self.velocity[1]*(t-self.bounceTime) + 0.5*g*((t-self.bounceTime)**2))*scale
                # print(self.rect)
                # print("y velocity = ", self.velocity[1])
                if (self.rect.bottom >= bottom and not self.ifBounced and t>=0.2) or self.ifCollideTop:
                    self.velocity[1] = -(self.velocity[1]+g*(t-self.bounceTime))*0.5
                    self.changeVelocity[1] = -(self.velocity[1]+g*(t-self.bounceTime))*0.5
                    self.bounceTime = (py.time.get_ticks()-self.startTime)/1000
                    self.initRect.centery = self.rect.centery
                    self.ifBounced = True
                    self.ifCollideTop = False
                    
                    # print(self.velTracker)
                    # print(self.velocity)
                    # print()
                else:
                    self.ifBounced = False
                
                
                
            else:
                self.rect.centerx = transformX(sling_rect.centerx+width/128-self.image.get_width()/2,playerNo,width)
                self.rect.bottom = sling_rect.centery-height/36
        else:
            self.rect.centerx = transformX((birdNo+1)*100*width/1920+width/38.4-self.image.get_width()/2,playerNo,width)
            self.rect.bottom = bottom


    # def newPosition(time,speed):
    #     g = 9.8
    #     scale = 50
    #     speed[1] += g*time
    #     move = [speed[0]*time*scale,(speed[1]*time + 0.5*g*(time**2))*scale]
    #     return move
    
    def printInfo(self):
        print("Name = ",self.name)
        print("ifLaunched = ", self.ifLaunched)
        print("ifCollided = ", self.ifCollided)

    def addLaunchSound(self,sound):
        self.launchSound = sound

red = Birds("Red",py.transform.scale_by(py.image.load("Media/Birds/red1.png"), 0.11),None,2,20,1,1,scaler(py.image.load("Media/Birds/red_avatar.png")),(33.1,19.3))
chuck = Birds("Chuck",py.transform.scale_by(py.image.load("Media/Birds/chuck1.png"), 0.3),"wood",4,15,1.5,0.75,scaler(py.image.load("Media/Birds/chuck_avatar.png")),(31.5,19.3))
bomb = Birds("Bomb",py.transform.scale_by(py.image.load("Media/Birds/bomb1.png"), 0.35),"stone",1.5,25,1.5,0.75,scaler(py.image.load("Media/Birds/bomb_avatar.png")),(34.9,15.2))
blue = Birds("Blue",py.transform.scale_by(py.image.load("Media/Birds/blue1.png"), 0.35),"ice",3,10,1.5,0.75,scaler(py.image.load("Media/Birds/blue_avatar.png")),(32.5,18.3))
stella = Birds("Stella",py.transform.scale_by(py.image.load("Media/Birds/stella1.png"), 0.42),None,2,20,2,0.5,scaler(py.image.load("Media/Birds/stella_avatar.png")),(26.3,18.9))

birdNames = ["red","chuck","bomb","blue","stella"]
birds = [red,chuck,bomb,blue,stella]

birdNos = {"Red":0,"Chuck":1,"Bomb":2,"Blue":3,"Stella":4}

spaceBirds = []
for i in range(5):
    spaceBirds.append(scaler(py.image.load(f"Media/Birds/{birdNames[i]}_space.png")))

ghostBirds = []
for i in range(5):
    ghostBirds.append(scaler(py.image.load(f"Media/Birds/{birdNames[i]}_ghost.png")))

samuraiBirds = []
for i in range(5):
    samuraiBirds.append(scaler(py.image.load(f"Media/Birds/{birdNames[i]}_samurai.png")))

for i in range(5):
    birds[i].addLaunchSound(f"Media/audio/{birdNames[i]}_launch.mp3")

eagle1 = scalerEagle(py.image.load("Media/Birds/eagle_ghost.png"))
eagle2 = scalerEagle(py.image.load("Media/Birds/eagle_space.png"))
eagle3 = scalerEagle(py.image.load("Media/Birds/eagle_samurai.png"))



