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

    def addBird(self, bird):
        self.birds.append(bird)

    def changeName(self, name):
        self.name = name

    def getName(self):
        return self.name

Player1 = Player("Player 1")
Player2 = Player("Player 2")