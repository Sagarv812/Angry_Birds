import pygame as py, sys, time

birds = [
    ["Media/Birds/red1.png",None,10],
    ["Media/Birds/chuck1.png","wood",20],
    ["Media/Birds/bomb1.png","stone",5],
    ["Media/Birds/blue1.png","ice",15],
    ["Media/Birds/stella1.png",None,15]
]
#template = {image file,affinity,speed}

class Birds:

    def __init__(self, name, image, affinity, speed, baseDamage, damageMultiplier):
        self.name = name
        self.image = image
        self.affinity = affinity
        self.speed = speed
        self.baseDamage = baseDamage
        self.damageMultiplier = damageMultiplier

    def changeAffinity(self, newAffinity):
        self.affinity = newAffinity

    def clone(self):
        return Birds(self.name, self.image,self.affinity,self.speed,self.baseDamage,self.damageMultiplier)
    
    def getAffinity(self):
        return self.affinity
    
    def getImage(self):
        return self.image
    
    
    # g = 9.8 #acceleration due to gravity
    # scale = 50 #scale: 50 pixels is 1 meter

    #template(old pixel count, time b/w two frames in milliseconds, speed in pixels/s)
    def newPosition(time,speed):
        g = 9.8
        scale = 50
        speed[1] += g*time
        move = [speed[0]*time*scale,(speed[1]*time + 0.5*g*(time**2))*scale]
        return move

red = Birds("Red",py.transform.scale_by(py.image.load("Media/Birds/red1.png"), 0.11),None,10,20,1)
chuck = Birds("Chuck",py.transform.scale_by(py.image.load("Media/Birds/chuck1.png"), 0.3),"wood",20,15,1.5)
bomb = Birds("Bomb",py.transform.scale_by(py.image.load("Media/Birds/bomb1.png"), 0.35),"stone",5,25,1.5)
blue = Birds("Blue",py.transform.scale_by(py.image.load("Media/Birds/blue1.png"), 0.35),"ice",15,10,1.5)
stella = Birds("Stella",py.transform.scale_by(py.image.load("Media/Birds/stella1.png"), 0.42),None,15,20,2)

birds = [red,chuck,bomb,blue,stella]
