#Player class containing info about Players
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