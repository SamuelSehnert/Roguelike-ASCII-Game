
class Tile:
    def __init__(self, name, symbol, collide, interact=None):
        self.name = name
        self.symbol = symbol
        self.collide = collide
        self.interact = interact

        if interact == "CONTAINER": #container
            self.open = False
            self.status = "LOCKED"
            if self.status == "LOCKED":
                self.lockLevel = 10
            self.inventory = self.initContainer()

        elif interact == "DOOR":
            self.open = False
            self.status = "LOCKED"
            if self.status == "LOCKED":
                self.lockLevel = 10

    def __eq__(self, other):
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
        return {}





all_tiles = {" ": Tile("Air", " ", True),
             ".": Tile("Floor", ".", False),
             "#": Tile("Wall", "#", True),
             "|": Tile("Closed Door", "|", True, interact="DOOR"),
             "C": Tile("Chest", "C", True, interact="CONTAINER"),
             }
