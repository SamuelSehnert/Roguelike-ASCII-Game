import tiles as TILES
import visual as VISUAL
import character as CHARACTER

import pathfinding

from copy import copy

class Level:
    def __init__(self, fileName, entities, levelName=None):
        if levelName == None:
            self.levelName = self.randomName()
        else:
            self.levelName = levelName
        self.layout = self.loadLevel(fileName)

        self.instructions = True

        self.entities = entities

        self.infoBar = None
        self.alterInfoBar(self.entities["player"])

        self.textBox = ["","","",""]

        self.initEntities(self.entities)

        self.characterMenu = False
        self.selectedItem = 0

        self.search = False

        self.visualActive = False
        self.visual = None

        self.interactiveActive = False
        self.interact = None

        self.attackActive = False
        self.target = None
        self.currentTarget = 0
        self.attackList = []
        self.valid = None

    def randomName(self):
        """
        Generats a random name for the level
        from a list of from a text file

        NEED TO IMPLEMENT
        """
        return "Ancient Ruins"

    def loadLevel(self, fileName):
        """
        Loads the layout of the level from
        a prefabricated text file
        """
        levelFile = open("../art/" + fileName, "r")
        levelList = []

        for levelY, row in enumerate(levelFile.readlines()):
            line = []
            for levelX, item in enumerate(row.strip()):
                tile = copy(TILES.all_tiles[item])
                tile.x = levelX
                tile.y = levelY
                line.append(tile)
            levelList.append(line)

        levelFile.close()
        return levelList
    
    def initEntities(self, entities):
        """
        Distributes the entities accoring
        to their x and y positions

        TODO:
        [ ] while loop to see if generated
            coordinates are on a valid tile
        """
        for single in entities.values():
            single.standingOn = self.layout[single.y][single.x]
            self.layout[single.y][single.x] = single


    def alterInfoBar(self, entity):
        """
        Changes the info bar below the map
        depending on current character action
        """
        string_list = []
        total = len(self.layout[len(self.layout) - 1])
        if isinstance(entity, CHARACTER.Player):
            string_list.append(entity.name)
            total2 = total - (len("Health: " + str(entity.stats["HP"])) + len("Action Points: " + str(entity.stats["AP"])))
            string_list.append("Health: " + str(entity.stats["HP"]) + " " * total2 + "Action Points: " + str(entity.stats["AP"]))

        elif isinstance(entity, CHARACTER.NPC):
            total3 = total - (len("Health: " + str(self.entities["player"].stats["HP"])) + len("Action Points: " + str(self.entities["player"].stats["AP"])))
            string_list.append("Health: " + str(self.entities["player"].stats["HP"]) + " " * total3 + "Action Points: " + str(self.entities["player"].stats["AP"]))
            string_list.append("-" * total)
            
            total1 = total - (len(entity.name) + len(entity.klass))
            string_list.append(entity.name.title() + " " * total1 + entity.klass.title())

            total2 = total - (len("Health: " + str(entity.stats["HP"])) + len("Action Points: " + str(entity.stats["AP"])))
            string_list.append("Health: " + str(entity.stats["HP"]) + " " * total2 + "Action Points: " + str(entity.stats["AP"]))

            if self.valid:
                string_list.append("YUP")
            else:
                string_list.append("NO")

        elif isinstance(entity, TILES.Tile):
            total3 = total - (len("Health: " + str(self.entities["player"].stats["HP"])) + len("Action Points: " + str(self.entities["player"].stats["AP"])))
            string_list.append("Health: " + str(self.entities["player"].stats["HP"]) + " " * total3 + "Action Points: " + str(self.entities["player"].stats["AP"]))
            string_list.append("-" * total)
            if entity.interact == "CONTAINER" or entity.interact == "DOOR":
                if entity.status == "LOCKED":
                    total = total - (len("Status: ") + len(entity.status) + len("Lock Level: ") + len(str(entity.lockLevel)))
                    string_list.append(str(entity.name))
                    string_list.append("Status: " +  str(entity.status) + " " * total + "Lock Level: " + str(entity.lockLevel))
                elif entity.status == "UNLOCKED":
                    if entity.open:
                        total -= (len("Status: ") + len(str(entity.status)) + len("OPEN"))
                        string_list.append(str(entity.name))
                        string_list.append("Status: " +  str(entity.status) + " " * total + "OPEN")
                    elif not entity.open:
                        total -= (len("Status: ") + len(str(entity.status)) + len("CLOSED"))
                        string_list.append(str(entity.name))
                        string_list.append("Status: " +  str(entity.status) + " " * total + "CLOSED")

            else:
                string_list.append(str(entity.name))

        self.infoBar = string_list
        #self.infoBar = []


    def refreshLayout(self):
        """
        Returns a list of strings to be printed
        to the screen
        """
        if self.instructions:
            lis = []
            lis.append("-" * 20)
            lis.append("|   " + "INSTRUCTIONS" + "   |")
            lis.append("-" * 20)

            lis.append("WASD: player movement")
            lis.append("v: enter visual mode, use WASD to move and gather information about surroundings")
            lis.append("i: enter interactive mode, use WASD to interact with nearby objects. Spacebar to activate object")
            lis.append("x: enter attack mode, cycle between NPC's with A and D. Spacebar to attack")
            lis.append("e: enter inventory. Use W and S to cycle between items. Spacebar to use/equip item")
            lis.append("r: reload currently equip wepon if able")
            lis.append("=: return to INSTRUCTIONS")
            lis.append("ESC: quit game")
            lis.append("\n" + (" " * 50) + "[press any key(not esc...) to return to main game]")

            return lis

        elif self.characterMenu:
            return self.entities["player"].characterMenu(self.selectedItem)


        lis = []

        lis.append("-"*50)

        for line in self.textBox:
            lis.append(" | " + line + " | ")

        lis.append("-"*50)
        lis.append("\n")

        lis.append("-" * (len(self.levelName) + 2))
        lis.append("|" + self.levelName + "|")
        lis.append("-" * (len(self.levelName) + 2))
        for layer in self.layout:
            raw = ""
            for item in layer:
                raw += str(item)
            lis.append(raw)
        lis.append("\n")

        for line in self.infoBar:
            lis.append(line)

        return lis


    def distributeInput(self, entity, key):
        """
        v: visual mode to see what objects are
        i: interact mode to interact with objects and characters around you
        x: attack mode to attack NPC's on the map
        r: reload weapon if applicable
        e: bring up player inventory menu
        =: bring up the instructions and explanation of keybinding
        """

        # opening and closing menues
        if self.instructions:
            self.instructions = False
            return
        if key == 61 and not self.instructions: # =
            self.instructions = True
            return

        if key == 101 and not self.characterMenu: # e
            self.characterMenu = True
            return
        elif key == 101 and self.characterMenu:
            self.selectedItem = 0
            self.characterMenu = False
            return
            
        #checks for current active state and changes entity based on it
        if self.visualActive:
            entity = self.visual
        elif self.interactiveActive:
            entity = self.interact

        elif self.attackActive:
            entity = self.target
            if key == 97:
                self.targetLeft(entity)
                self.valid = pathfinding.validPath(self.layout, self.entities["player"].standingOn, self.attackList[self.currentTarget], self.entities["player"].x, self.entities["player"].y)
                self.alterInfoBar(self.attackList[self.currentTarget])

                self.resetAttackLayout()
                
                return
            elif key == 100:
                self.targetRight(entity)
                self.valid = pathfinding.validPath(self.layout, self.entities["player"].standingOn, self.attackList[self.currentTarget], self.entities["player"].x, self.entities["player"].y)
                self.alterInfoBar(self.attackList[self.currentTarget])

                self.resetAttackLayout()

                return
            elif key == 32:
                if self.valid:
                    self.entities["player"].stats["AP"][0] -= self.entities["player"].calculateWeaponAPCost()
                    self.entities["player"].attack(self.attackList[self.currentTarget])
                    self.alterInfoBar(self.attackList[self.currentTarget])
                return


        # go into this if the character menu is currently open
        if self.characterMenu:
            if key == 119:
                if self.selectedItem - 1 >= 0:
                    self.selectedItem -= 1
                    return
            elif key == 115:
                if self.selectedItem + 1 <= len(self.entities["player"].inventory) - 1 + 2:
                    self.selectedItem += 1
                    return
            elif key == 32:
                self.entities["player"].useItem(self.selectedItem)
            return

        #default movement for any entity
        if key == 119:
            self.charUp(entity)
        elif key == 115:
            self.charDown(entity)
        elif key == 97:
            self.charLeft(entity)
        elif key == 100:
            self.charRight(entity)
        elif key == 114: #r: to be deleted. only for debugging purposes
            self.nextTurn()

        #interact with tile/NPC that "i" is currently on
        elif key == 32 and self.interactiveActive:
            if self.interact.standingOn.interact:
                tile = self.interact.standingOn
                if tile.interact == "CONTAINER":
                    if tile.status == "LOCKED":
                        self.entities["player"].stats["AP"][0] -= 1
                        tile.status = "UNLOCKED"
                    else:
                        search = True
                elif tile.interact == "DOOR":
                    if tile.status == "LOCKED":
                        self.entities["player"].stats["AP"][0] -= 1
                        tile.status = "UNLOCKED"
                    elif tile.status == "UNLOCKED":
                        tile.open = not tile.open
                        if tile.open:
                            self.entities["player"].stats["AP"][0] -= 1
                            tile.symbol = "/"
                            tile.collide = False
                        elif not tile.open:
                            self.entities["player"].stats["AP"][0] -= 1
                            tile.symbol = "|"
                            tile.collide = True
                self.alterInfoBar(self.interact.standingOn)




        #activate and deactivate visual mode
        elif key == 118 and not self.visualActive: #v
            self.fullDeactivation()
            self.visualMode()
        elif key == 118 and self.visualActive:
            self.fullDeactivation()


        #activate and deactivate interact mode
        elif key == 105 and not self.interactiveActive: #i
            self.fullDeactivation()
            self.interactMode()
        elif key == 105 and self.interactiveActive:
            self.fullDeactivation()


        #activate and deactivate attack mode
        elif key == 120 and not self.attackActive: #x
            self.fullDeactivation()
            self.attackMode()
        elif key == 120 and self.attackActive:
            self.fullDeactivation()


        #reverts the info bar back to the player when no mode is active
        if not self.visualActive and not self.interactiveActive and not self.attackActive:
            self.alterInfoBar(self.entities["player"])

                            
    def charUp(self, entity):
        if isinstance(entity, VISUAL.Visual) and self.visual.y - 1 >= 0:
            self.layout[entity.y][entity.x] = entity.standingOn
            entity.move("w")
            entity.standingOn = self.layout[entity.y][entity.x]
            self.layout[entity.y][entity.x] = entity
            self.alterInfoBar(self.visual.standingOn)

        elif isinstance(entity, VISUAL.Interact) and self.interact.y - 1 >= self.entities["player"].y - 1:
            self.layout[entity.y][entity.x] = entity.standingOn
            entity.move("w")
            entity.standingOn = self.layout[entity.y][entity.x]
            self.layout[entity.y][entity.x] = entity
            self.alterInfoBar(self.interact.standingOn)

        elif isinstance(entity, CHARACTER.NPC) or isinstance(entity, CHARACTER.Player):
            if self.layout[entity.y - 1][entity.x].collide:
                return False
            else:
                if entity.stats["AP"][0] > 0:
                    self.layout[entity.y][entity.x] = entity.standingOn
                    entity.move("w")
                    entity.stats["AP"][0] -= 1
                    entity.standingOn = self.layout[entity.y][entity.x]
                    self.layout[entity.y][entity.x] = entity
                else:
                    return False
        else:
            return False

    def charDown(self, entity):
        if isinstance(entity, VISUAL.Visual) and self.visual.y + 1 <= len(self.layout) - 1:
            self.layout[entity.y][entity.x] = entity.standingOn
            entity.move("s")
            entity.standingOn = self.layout[entity.y][entity.x]
            self.layout[entity.y][entity.x] = entity
            self.alterInfoBar(self.visual.standingOn)

        elif isinstance(entity, VISUAL.Interact) and self.interact.y + 1 <= self.entities["player"].y + 1:
            self.layout[entity.y][entity.x] = entity.standingOn
            entity.move("s")
            entity.standingOn = self.layout[entity.y][entity.x]
            self.layout[entity.y][entity.x] = entity
            self.alterInfoBar(self.interact.standingOn)

        elif isinstance(entity, CHARACTER.NPC) or isinstance(entity, CHARACTER.Player):
            if self.layout[entity.y + 1][entity.x].collide:
                return False
            else:
                if entity.stats["AP"][0] > 0:
                    self.layout[entity.y][entity.x] = entity.standingOn
                    entity.move("s")
                    entity.stats["AP"][0] -= 1
                    entity.standingOn = self.layout[entity.y][entity.x]
                    self.layout[entity.y][entity.x] = entity
                else:
                    return False
        else:
            return False
    
    def charLeft(self, entity):
        if isinstance(entity, VISUAL.Visual) and self.visual.x - 1 >= 0:
            self.layout[entity.y][entity.x] = entity.standingOn
            entity.move("a")
            entity.standingOn = self.layout[entity.y][entity.x]
            self.layout[entity.y][entity.x] = entity
            self.alterInfoBar(self.visual.standingOn)

        elif isinstance(entity, VISUAL.Interact) and self.interact.x - 1 >= self.entities["player"].x - 1:
            self.layout[entity.y][entity.x] = entity.standingOn
            entity.move("a")
            entity.standingOn = self.layout[entity.y][entity.x]
            self.layout[entity.y][entity.x] = entity
            self.alterInfoBar(self.interact.standingOn)

        elif isinstance(entity, CHARACTER.NPC) or isinstance(entity, CHARACTER.Player):
            if self.layout[entity.y][entity.x - 1].collide:
                return False
            else:
                if entity.stats["AP"][0] > 0:
                    self.layout[entity.y][entity.x] = entity.standingOn
                    entity.move("a")
                    entity.stats["AP"][0] -= 1
                    entity.standingOn = self.layout[entity.y][entity.x]
                    self.layout[entity.y][entity.x] = entity
                else:
                    return False
        else:
            return False

    def charRight(self, entity):
        if isinstance(entity, VISUAL.Visual) and entity.x + 1 <= len(self.layout[entity.y]) - 1:
            self.layout[entity.y][entity.x] = entity.standingOn
            entity.move("d")
            entity.standingOn = self.layout[entity.y][entity.x]
            self.layout[entity.y][entity.x] = entity
            self.alterInfoBar(self.visual.standingOn)

        elif isinstance(entity, VISUAL.Interact) and self.interact.x + 1 <= self.entities["player"].x + 1:
            self.layout[entity.y][entity.x] = entity.standingOn
            entity.move("d")
            entity.standingOn = self.layout[entity.y][entity.x]
            self.layout[entity.y][entity.x] = entity
            self.alterInfoBar(self.interact.standingOn)

        elif isinstance(entity, CHARACTER.NPC) or isinstance(entity, CHARACTER.Player):
            if self.layout[entity.y][entity.x + 1].collide:
                return False
            else:
                if entity.stats["AP"][0] > 0:
                    self.layout[entity.y][entity.x] = entity.standingOn
                    entity.move("d")
                    entity.stats["AP"][0] -= 1
                    entity.standingOn = self.layout[entity.y][entity.x]
                    self.layout[entity.y][entity.x] = entity
                else:
                    return False
        else:
            return False

    def targetLeft(self, entity):
        self.currentTarget -= 1
        if self.currentTarget < 0:
            self.currentTarget = len(self.attackList) - 1

        self.layout[entity.y][entity.x] = entity.standingOn

        self.target.x = self.attackList[self.currentTarget].x
        self.target.y = self.attackList[self.currentTarget].y

        entity.standingOn = self.layout[entity.y][entity.x]
        self.layout[entity.y][entity.x] = entity

        self.alterInfoBar(entity.standingOn)

    def targetRight(self, entity):
        self.currentTarget += 1
        if self.currentTarget > len(self.attackList) - 1:
            self.currentTarget = 0

        self.layout[entity.y][entity.x] = entity.standingOn

        self.target.x = self.attackList[self.currentTarget].x
        self.target.y = self.attackList[self.currentTarget].y

        entity.standingOn = self.layout[entity.y][entity.x]
        self.layout[entity.y][entity.x] = entity

        self.alterInfoBar(entity.standingOn)


    def nextTurn(self):
        for char in self.entities.values():
            char.stats["AP"][0] = char.stats["AP"][1]

    def fullDeactivation(self):
        if self.visualActive:
            self.deactivateVisualMode()
        if self.interactiveActive:
            self.deactivateInteractMode()
        if self.attackActive:
            self.deactivateAttackMode()


    def visualMode(self):
        self.visualActive = True
        self.visual = VISUAL.Visual(self.entities["player"].x, self.entities["player"].y)
        self.visual.standingOn = self.layout[self.visual.y][self.visual.x]
        self.layout[self.visual.y][self.visual.x] = self.visual

    def deactivateVisualMode(self):
        self.layout[self.visual.y][self.visual.x] = self.visual.standingOn
        self.visualActive = False
        self.visual = None
        self.alterInfoBar(self.entities["player"])

    def interactMode(self):
        self.interactiveActive = True
        self.interact = VISUAL.Interact(self.entities["player"].x, self.entities["player"].y)
        self.interact.standingOn = self.layout[self.interact.y][self.interact.x]
        self.layout[self.interact.y][self.interact.x] = self.interact

    def deactivateInteractMode(self):
        self.layout[self.interact.y][self.interact.x] = self.interact.standingOn
        self.interactiveActive = False
        self.interact = None
        self.alterInfoBar(self.entities["player"])

    def attackMode(self):
        self.attackActive = True
        nonPlayerNPC = self.entities.copy()
        del nonPlayerNPC["player"]

        for single in nonPlayerNPC.values():
            self.attackList.append(single)

        self.target = VISUAL.Crosshair(self.attackList[self.currentTarget].x, self.attackList[self.currentTarget].y)
        self.target.standingOn = self.layout[self.target.y][self.target.x]
        self.layout[self.target.y][self.target.x] = self.target

        self.valid = pathfinding.validPath(self.layout, self.entities["player"].standingOn, self.attackList[self.currentTarget], self.entities["player"].x, self.entities["player"].y)
        self.resetAttackLayout()

        self.alterInfoBar(self.target.standingOn)

    def deactivateAttackMode(self):
        self.layout[self.target.y][self.target.x] = self.target.standingOn
        self.attackActive = False
        self.target = None
        self.alterInfoBar(self.entities["player"])

    def resetAttackLayout(self):
        for i in self.layout:
            for item in i:
                item.visited = False
                item.previous = None
                if item.standingOn != None:
                    item.standingOn.visited = False
                    item.standingOn.previous = None




