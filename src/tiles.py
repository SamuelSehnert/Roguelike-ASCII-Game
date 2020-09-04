import items as ITEMS
from random import choice, randint

class Tile:
    def __init__(self, name, symbol, collide, interact=None, canAttack=False):
        self.name = name
        self.symbol = symbol
        self.collide = collide
        self.interact = interact

        self.canAttack = canAttack

        self.standingOn = None

        self.previous = None #used for BFS backtracking
        self.visited = False
        self.x = 0
        self.y = 0

        if interact == "CONTAINER": #container
            self.cap = 4
            self.open = False
            self.searched = False
            self.status = "LOCKED"
            if self.status == "LOCKED":
                self.lockLevel = 10
                self.level = self.lockLevel // 10
            self.inventory = {}

        elif interact == "DOOR": #door
            self.open = False
            self.status = "LOCKED"
            if self.status == "LOCKED":
                self.lockLevel = 10

    def __eq__(self, other):
        if other == None or self == None:
            return False

        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __repr__(self):
        return self.symbol

    def openDoor(self):
        self.open = not self.open
        if self.open:
            self.symbol = "/"
            self.collide = False
        elif not self.open:
            self.symbol = "|"
            self.collide = True

    def initContainer(self):
        contains = {}
        i = 0
        while i < self.cap:
            addition = choice(list(ITEMS.all_items))
            if addition == "underwear" or addition == "fists":
                continue
            if addition in contains:
                contains[addition][1] += 1
            else:
                contains[addition] = [ITEMS.all_items[addition], 1]
            i += 1
        return contains

    def searchMenu(self, selected, player):
        limit = (len(player.inventory) - 1) + 3
        display = player.characterMenu(selected)

        for i in range(2):
            display.append("\n")

        display.append("-"*(4+len(self.name)))
        display.append("| "+self.name+" |")
        display.append("-"*(4+len(self.name)))

        for x, item in enumerate(self.inventory, limit):
            if x == selected:
                if isinstance(self.inventory[item][0], ITEMS.Weapon):
                    display.append("-->  | " + str(self.inventory[item][0].name) + " x " + str(self.inventory[item][1]) + "|  " + str(ITEMS.all_weapons[item]))
                if isinstance(self.inventory[item][0], ITEMS.Armor):
                    display.append("-->  | " + str(self.inventory[item][0].name) + " x " + str(self.inventory[item][1]) + "|  " + str(ITEMS.all_armor[item]))
                if isinstance(self.inventory[item][0], ITEMS.General):
                    display.append("-->  | " + str(self.inventory[item][0].name) + " x " + str(self.inventory[item][1]) + "|  " + str(ITEMS.all_general[item]))
            else:
                display.append("| " + str(self.inventory[item][0].name) + " x " + str(self.inventory[item][1]) + "|")
        display.append("-"*20)

        return display
            
all_tiles = {" ": Tile("Air", " ", True),
             ".": Tile("Floor", ".", False),
             "#": Tile("Wall", "#", True),
             "|": Tile("Door", "|", True, interact="DOOR"),
             "C": Tile("Chest", "C", True, interact="CONTAINER"),
             }
