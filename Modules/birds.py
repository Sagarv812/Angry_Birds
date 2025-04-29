import pygame as py


def transformX(x, playerNo, width):
    return x if playerNo==1 else width-x

#Scale bird images
def scaler(img):
    return py.transform.scale(img, (300,280))

#Scale Mighty Eagle
def scalerEagle(img):
    return py.transform.scale(img, (200,200))

#Bird class which contains all info about birds
class Birds:

    def __init__(self, name, image, affinity, speed, baseDamage, damageMultiplier, damageDivider, scaleFactor):
        self.name = name
        self.image = image
        self.initImage = image
        self.affinity = affinity
        self.speed = speed
        self.baseDamage = baseDamage
        self.damageMultiplier = damageMultiplier
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
    
    #Makes a clone of the object (to avoid pass by reference errors)
    def clone(self):
        bird = Birds(self.name, self.image,self.affinity,self.speed,self.baseDamage,self.damageMultiplier,self.damageDivider,self.scaleFactor)
        bird.addLaunchSound(self.launchSound)
        return bird
    
    def getAffinity(self):
        return self.affinity
    
    def getImage(self):
        return self.image

    
    def updateRect(self):
        self.rect = self.image.get_rect()
        if not(self.ifDragging or self.ifLaunched):
            self.initRect = self.rect

    #Initialize velocity
    def initVelocity(self,width):
        slingCenter = py.Vector2(self.initRect.center)
        birdCenter = py.Vector2(self.rect.center)
        self.velocity = (slingCenter-birdCenter)*0.2*(self.speed**0.2)*((width/1920)**0.1)
        self.changeVelocity = self.velocity.copy()
        self.initRect = self.rect   

    #Update the position of bird as game goes on
    def updatePos(self, birdNo, playerNo, sling_rect, bottom, width, height):
        g = 20*height/1080

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

            elif self.ifLaunched or self.ifCollided:
                scale = 20
                t = (py.time.get_ticks()-self.startTime)/1000

                self.changeVelocity[1] += g/60
                self.rect.centerx = self.initRect.centerx + self.velocity[0]*(t-self.collideTime)*scale
                self.rect.centery = self.initRect.centery + (self.velocity[1]*(t-self.bounceTime) + 0.5*g*((t-self.bounceTime)**2))*scale

                #Bouncing mechanism
                if (self.rect.bottom >= bottom and not self.ifBounced and t>=0.2) or self.ifCollideTop:
                    self.velocity[1] = -(self.velocity[1]+g*(t-self.bounceTime))*0.5
                    self.changeVelocity[1] = -(self.velocity[1]+g*(t-self.bounceTime))*0.5
                    self.bounceTime = (py.time.get_ticks()-self.startTime)/1000
                    self.initRect.centery = self.rect.centery
                    self.ifBounced = True
                    self.ifCollideTop = False
                    
                else:
                    self.ifBounced = False
                
                
                
            else:
                self.rect.centerx = transformX(sling_rect.centerx+width/128-self.image.get_width()/2,playerNo,width)
                self.rect.bottom = sling_rect.centery-height/36
        else:
            self.rect.centerx = transformX((birdNo+1)*100*width/1920+width/38.4-self.image.get_width()/2,playerNo,width)
            self.rect.bottom = bottom


    def addLaunchSound(self,sound):
        self.launchSound = sound

#Birds object creation with necessary arguments
red = Birds("Red",py.transform.scale_by(py.image.load("Media/Birds/red1.png"), 0.11),None,2,20,1,1,(33.1,19.3))
chuck = Birds("Chuck",py.transform.scale_by(py.image.load("Media/Birds/chuck1.png"), 0.3),"wood",4,15,1.5,0.75,(31.5,19.3))
bomb = Birds("Bomb",py.transform.scale_by(py.image.load("Media/Birds/bomb1.png"), 0.35),"stone",1.5,25,1.5,0.75,(34.9,15.2))
blue = Birds("Blue",py.transform.scale_by(py.image.load("Media/Birds/blue1.png"), 0.35),"ice",3,10,1.5,0.75,(32.5,18.3))
stella = Birds("Stella",py.transform.scale_by(py.image.load("Media/Birds/stella1.png"), 0.42),None,2,20,2,0.5,(26.3,18.9))

birdNames = ["red","chuck","bomb","blue","stella"]
birds = [red,chuck,bomb,blue,stella]

birdNos = {"Red":0,"Chuck":1,"Bomb":2,"Blue":3,"Stella":4}

#Initializing bird avatars
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


#Initializing Mighty Eagle forms
eagle1 = scalerEagle(py.image.load("Media/Birds/eagle_ghost.png"))
eagle2 = scalerEagle(py.image.load("Media/Birds/eagle_space.png"))
eagle3 = scalerEagle(py.image.load("Media/Birds/eagle_samurai.png"))



