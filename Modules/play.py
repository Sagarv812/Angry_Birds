import pygame as py, time, sys
import Modules.birds as Birds
import Modules.players as Players

def playGame():

    while True:

        for event in py.event.get():
            if event.type == py.QUIT: sys.exit()

    