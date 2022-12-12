
from game import location
from game import config
from game.display import announce 
from game.events import *
from game.items import Cutlass
from game.items import Flintlock
from game.items import BowAndArrow
from game import Wordle


class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'I'
        self.visitable = True
        self.starting_location = Beach_with_ship(self)
        self.locations = {}
        self.locations["beach"] = self.starting_location
        self.locations["trees"] = Trees(self)
        self.locations["room1"] = room1(self)
        self.locations["room2"] = room2(self)
        self.locations["room3"] = room3(self)
        self.locations["room4"] = room4(self)
        self.locations["room5"] = room5(self)


    def enter (self, ship):
        print ("You arrived at an island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
#        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        announce ("You arrive at the beach. Your ship is at anchor in a small bay to the south.")
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["trees"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["room1"]
        elif (verb == "west"):
            announce ("You walk all the way around the island on the beach. It's not very interesting.")


class Trees (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "trees"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

        # Include a couple of items and the ability to pick them up, for demo purposes
        self.verbs['take'] = self
        self.item_in_tree = Cutlass()
        self.item_in_clothes = Flintlock()
        self.item_in_ground = BowAndArrow()

        self.event_chance = 50
        self.events.append(man_eating_monkeys.ManEatingMonkeys())
#        self.events.append(drowned_pirates.DrownedPirates())

    def enter (self):
        edibles = False
        for e in self.events:
            if isinstance(e, man_eating_monkeys.ManEatingMonkeys):
                edibles = True
        #The description has a base description, followed by variable components.
        description = "You walk into the small forest on the island."
        if edibles == False:
             description = description + " Nothing around here looks very edible."
        
        #Add a couple items as a demo. This is kinda awkward but students might want to complicated things.
        if self.item_in_tree != None:
            description = description + " You see a " + self.item_in_tree.name + " stuck in a tree."
        if self.item_in_clothes != None:
            description = description + " You see a " + self.item_in_clothes.name + " in a pile of shredded clothes on the forest floor."
        if self.item_in_ground != None:
            description = description + " You see a " + self.item_in_ground.name + "stuck in mud in the ground."
        announce (description)
    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        #Handle taking items. Demo both "take cutlass" and "take all"
        if verb == "take":
            if self.item_in_tree == None and self.item_in_clothes == None and self.item_in_ground == None:
                announce ("You don't see anything to take.")
            elif len(cmd_list) > 1:
                at_least_one = False #Track if you pick up an item, print message if not.
                item = self.item_in_tree
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You take the "+item.name+" from the tree.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_tree = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_clothes
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce ("You pick up the "+item.name+" out of the pile of clothes. ...It looks like someone was eaten here.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_clothes = None
                    config.the_player.go = True
                    at_least_one = True
                item = self.item_in_ground
                if item != None and (cmd_list[1] == item.name or cmd_list[1] == "all"):
                    announce("You pick up the "+item.name+" out of the mud. You clean it off and look at what you have found.")
                    config.the_player.add_to_inventory([item])
                    self.item_in_ground = None
                    config.the_player.go = True
                    at_least_one = True
                if at_least_one == False:
                    announce ("You don't see one of those around.")
class room1(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "room1"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        
    def enter(self):
        announce ("You have entered a room.")
        
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            announce ("You find the entrance is locked. The only way for you to go is forward, which, by looking at your compass is North.")
        if (verb == "north"):
            announce ("You walk up to a door. The door is locked, but there is a riddle on the door. The riddle states, 'What can fly, but has no wings?'")
            guessedCorrectly = False
            while guessedCorrectly != True:
                userGuess = input()
                answer = 'Time'
                if userGuess == answer:
                    announce ("You have answered correctly. The door opens and you walk through")
                    guessedCorrectly = True
                elif userGuess != answer:
                    announce ("You must guess again. The door did not open")
                    guessedCorrectly = False
            if guessedCorrectly == True:
                config.the_player.next_loc = self.main_location.locations["room2"]
        if (verb == "west"):
            announce ("You look around. It appears the only place to go is north")
        if (verb == "south"):
            announce ("You look around. It appears the only place to go is north")


class room2(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "room2"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
    def enter(self):
        announce("You have entered the second room. Now to see what's inside")
    def process_verb(self, verb,cmd_list, nouns):
        if (verb == "east"):
            announce("You walk forward. There appears to be a shimmering white light. You walk into the light. A screen appears in front of you. You must play a game of Wordle to advance.")
            #play wordle code
            gameOver = False
            while gameOver != True:
                game = Wordle.Wordle()
                game.playGame()
                if game.gameWon == True:
                    gameOver = True
                elif game.gameLost == True:
                    gameOver = False
                    game.playGame()
            if gameOver == True:
                config.the_player.next_loc = self.main_location.locations["room3"]
                
class room3(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "room3"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
    def enter(self):
        announce("You have entered the third room.")
    def process_verb(self, verb,cmd_list, nouns):
        if (verb == "north"):
            SkeletonAttack.SkeletonAttack()
            config.the_player.next_loc = self.main_location.locations["room4"]

class room4(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "room4"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
    def enter(self):
        announce("You have entered the fourth room.")
    def process_verb(self, verb,cmd_list, nouns):
        if (verb == "west"):
            announce ("You walk forwards")

class room5(location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "room5"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
    def enter(self):
        announce("You have entered the fifth room.")
    def process_verb(self, verb,cmd_list, nouns):
        if (verb == "west"):
            announce ("You walk forwards")

                    

