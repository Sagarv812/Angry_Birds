import numpy
import pygame as py
import Modules.settings as settings

def scaler(block):
    return py.transform.scale(block,(settings.width/21.3,settings.width/21.3))

class Block:

    def __init__(self, name, health, img1, img2, img3, img4, img5):
        self.name = name
        self.health = health
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3
        self.img4 = img4
        self.img5 = img5
    
    def returnImg(self):
        if self.health>48:
            self.rect = scaler(self.img1).get_rect()
            return scaler(self.img1)
        elif self.health>36:
            self.rect = scaler(self.img2).get_rect()
            return scaler(self.img2)
        elif self.health>24:
            self.rect = scaler(self.img3).get_rect()
            return scaler(self.img3)
        elif self.health>12:
            self.rect = scaler(self.img4).get_rect()
            return scaler(self.img4)
        elif self.health>0:
            self.rect = scaler(self.img5).get_rect()
            return scaler(self.img5)
        else:
            return None
        
    def getName(self):
        return self.name
    
    def clone(self):
        return Block(self.name, self.health,self.img1,self.img2,self.img3,self.img4,self.img5)
    
        
wood = Block("wood",60,scaler(settings.WOOD[0]),scaler(settings.WOOD[1]),scaler(settings.WOOD[2]),scaler(settings.WOOD[3]),scaler(settings.WOOD[4]))
ice = Block("ice",60,scaler(settings.ICE[0]),scaler(settings.ICE[1]),scaler(settings.ICE[2]),scaler(settings.ICE[3]),scaler(settings.ICE[4]))
stone = Block("stone",60,scaler(settings.STONE[0]),scaler(settings.STONE[1]),scaler(settings.STONE[2]),scaler(settings.STONE[3]),scaler(settings.STONE[4]))

blocks = [wood,ice,stone]