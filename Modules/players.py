import pygame as py, sys
import Modules.settings as settings

# Player1 = {}
# Player1["birds"] = []
# Player1["name"] = "Player 1"

# Player2 = {}
# Player2["birds"] = []
# Player2["name"] = "Player 2"

class Player:

    def __init__(self,name="Player"):
        self.name = name
        self.birds = []
        self.score = 0

    def addBird(self, bird):
        self.birds.append(bird)

    def changeName(self, name):
        self.name = name

    def getName(self):
        return self.name
    
    def getBirdsNo(self):
        return len(self.birds)
    
    def getBirds(self):
        return self.birds
    
    def updateScore(self,addScore):
        self.score += addScore

    def getScore(self):
        return self.score

Player1 = Player("Player 1")
Player2 = Player("Player 2")