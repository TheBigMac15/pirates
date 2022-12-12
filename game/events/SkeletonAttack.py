from game import event
import random
from game.combat import Combat
from game.combat import Skeleton
from game.display import announce

class SkeletonAttack (event.Event):

    def __init__ (self):
        self.name = " skeleton attack"

    def process (self, world):
        result = {}
        result["message"] = "the skeletons are defeated!"
        monsters = []
        min = 2
        uplim = 6
        if random.randrange(2) == 0:
            min = 1
            uplim = 5
            monsters.append(Skeleton("Skeleton Boss"))
            monsters[0].speed = 1.2*monsters[0].speed
            monsters[0].health = 2*monsters[0].health
        n_appearing = random.randrange(min, uplim)
        n = 1
        while n <= n_appearing:
            monsters.append(Skeleton("Skeleton "+str(n)))
            n += 1
        announce ("You are attacked by a mob of skeletons!")
        Combat(monsters).combat()
        result["newevents"] = [ self ]
        return result

