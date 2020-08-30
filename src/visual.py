class Visual:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.standingOn = None # will be what the player is standing on

    def __repr__(self):
        return "v"

    def move(self, moveDirection):
        if moveDirection == "w":
            self.y -= 1
        elif moveDirection == "s":
            self.y += 1
        elif moveDirection == "a":
            self.x -= 1
        elif moveDirection == "d":
            self.x += 1


class Interact:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.standingOn = None # will be what the player is standing on

    def __repr__(self):
        return "i"

    def move(self, moveDirection):
        if moveDirection == "w":
            self.y -= 1
        elif moveDirection == "s":
            self.y += 1
        elif moveDirection == "a":
            self.x -= 1
        elif moveDirection == "d":
            self.x += 1

class Crosshair:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.symbol = "X"
        
        self.standingOn = None
        self.collide = False

    def __repr__(self):
        return self.symbol











