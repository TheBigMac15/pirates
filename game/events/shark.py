from game import event
import random
import game.config as config
from game.player import Player

class Shark (event.Event):
    def __init__(self):
        self.name = " crew member has been eaten by a shark!"
        self.sharkDamage = 100
        
    def process (self, world):
        # a random shark will eat one of the crew members. There is nothing you can do to prevent this, nothing you can do after. It simply happens.
        s = random.choice(config.the_player.get_pirates())
#         msg = s.get_name() + "has been eaten by a shark"
        s.inflict_damage(self.sharkDamage,"has been eaten by a shark")
        result = {}
        result["message"] = msg
        result["newevents"] = [ self ]
        return result
        