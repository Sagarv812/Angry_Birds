import numpy
import pygame as py
import Modules.settings as settings

def scaler(block):
    return py.transform.scale(block,(90,90))

class Block:

    def __init__(self, name, health, img1, img2, img3):
        self.name = name
        self.health = health
        self.img1 = img1
        self.img2 = img2
        self.img3 = img3
    
    def returnImg(self):
        if self.health>40:
            return self.img1
        elif self.health>20:
            return self.img2
        elif self.health>0:
            return self.img3
        
    def getName(self):
        return self.name
        
wood = Block("wood",60,scaler(settings.WOOD[0]),scaler(settings.WOOD[1]),scaler(settings.WOOD[2]))
ice = Block("ice",60,scaler(settings.ICE[0]),scaler(settings.ICE[1]),scaler(settings.ICE[2]))
stone = Block("stone",60,scaler(settings.STONE[0]),scaler(settings.STONE[1]),scaler(settings.STONE[2]))

blocks = [wood,ice,stone]