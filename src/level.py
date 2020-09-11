import tiles as TILES
import visual as VISUAL
import character as CHARACTER

import pathfinding

from copy import copy
from time import time, sleep

class Level:
    def __init__(self, fileName, entities, levelName=None):
        if levelName == None:
            self.levelName = self.randomName()
        else:
            self.levelName = levelName

        self.turn = True
        self.cont = False
            
        self.boundY = 0
        self.boundX = 0
        self.layout = self.loadLevel(fileName)
        
        self.instructions = True

        self.entities = entities
        self.player = None

        self.textBox = ["","","",""]
        self.alterTextBox("You enter " + self.levelName)

        self.characterMenu = False
        self.selectedItem = 0

        self.search = False
        self.searchContainer = None

        self.visualActive = False
        self.visual = None

        self.interactiveActive = False
        self.interact = None

        self.attackActive = False
        self.valid = None

        self.infoBar = None
        self.alterInfoBar(self.player)

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

        boundary = False
        go = False
        for levelY, row in enumerate(levelFile.readlines()):
            line = []
            if boundary and not go:
                self.boundY = int(row.strip())
                go = True
                continue
            elif boundary and go:
                self.boundX = int(row.strip())
                break
            if row == "\n":
                boundary = True
                continue
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
        #for single in entities.values():
        for index, single in enumerate(entities.values(), 1):
            #if not isinstance(single, CHARACTER.Player):
            if single.isRandom:
                single = copy(single)
                single.name = single.randomName()
                single.stats = single.randomStats()
                while True:
                    single.y = single.randomPosY(self.boundY)
                    single.x = single.randomPosX(self.boundX)
                    if not self.layout[single.y][single.x].collide:
                        single.standingOn = self.layout[single.y][single.x]
                        self.layout[single.y][single.x] = single
                        break
                entities[index] = single
            else:
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
            total3 = total - (len("Health: " + str(self.player.stats["HP"])) + len("Action Points: " + str(self.player.stats["AP"])))
            string_list.append("Health: " + str(self.player.stats["HP"]) + " " * total3 + "Action Points: " + str(self.player.stats["AP"]))
            string_list.append("-" * total)
            
            total1 = total - (len(entity.name) + len(entity.klass))
            string_list.append(entity.name.title() + " " * total1 + entity.klass.title())
            """
            total2 = total - (len("Health: " + str(entity.stats["HP"])) + len("Action Points: " + str(entity.stats["AP"])))
            string_list.append("Health: " + str(entity.stats["HP"]) + " " * total2 + "Action Points: " + str(entity.stats["AP"]))
            """

        elif isinstance(entity, TILES.Tile):
            total3 = total - (len("Health: " + str(self.player.stats["HP"])) + len("Action Points: " + str(self.player.stats["AP"])))
            string_list.append("Health: " + str(self.player.stats["HP"]) + " " * total3 + "Action Points: " + str(self.player.stats["AP"]))
            string_list.append("-" * total)
            if isinstance(entity, TILES.Container) or isinstance(entity, TILES.Door):
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

        string_list.append("-" * total)
        if self.valid and self.attackActive:
            string_list.append("Clear Shot")
        elif not self.valid and self.attackActive:
            string_list.append("Shot Blocked")

        self.infoBar = string_list


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
            return self.player.characterMenu(self.selectedItem)

        elif self.search:
            return self.searchContainer.searchMenu(self.selectedItem, self.player)
        
        else:

            total = len(self.layout[len(self.layout) - 1])
            spacer = (self.player.visRangeX * 2) + 1
            spacer = " " * ((total - spacer) // 2)
            lis = []
            lis.append("-"*total)

            for line in self.textBox:
                total -= (len(line) + 6)
                lis.append("|  " + line + " " * total + "  |")
                total = len(self.layout[len(self.layout) - 1])

            lis.append("-"*total)
            lis.append("\n")

            counter = 0
            for layer in range(len(self.layout)):
                raw = spacer

                topY = self.player.y - self.player.visRangeY
                if topY < 0:
                    topY = 0

                botY = self.player.y + self.player.visRangeY
                if botY > len(self.layout) - 1:
                    botY = len(self.layout) - 1

                rightX = self.player.x + self.player.visRangeX
                if rightX > len(self.layout[layer]) - 1:
                    rightX = len(self.layout[layer]) - 1

                leftX = self.player.x - self.player.visRangeX
                if leftX < 0:
                    leftX = 0

                if layer >= topY and layer <= botY:
                    for item in range(len(self.layout[layer])):
                        if item <= rightX and item >= leftX:
                            raw += str(self.layout[layer][item])
                    lis.append(raw)
                else:
                    counter += 1
              

            for i in range(counter - 2):
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
        if entity.stats["AP"][0] <= 0:
            self.cont = False
            return

        # opening and closing menues
        if self.instructions:
            self.instructions = False
            return
        if key == 61 and not self.instructions: # =
            self.instructions = True
            return

        if key == 101 and self.search: #q
            self.fullDeactivation()
            self.search = False
            self.selectedItem = 0
            return

        if key == 101 and not self.characterMenu: # e
            self.characterMenu = True
            return
        elif key == 101 and self.characterMenu:
            self.selectedItem = 0
            self.characterMenu = False
            return

        
        # go into this if the character menu is currently open
        if self.characterMenu:
            if key == 119:
                if self.selectedItem - 1 >= 0:
                    self.selectedItem -= 1
                    return
            elif key == 115:
                if self.selectedItem + 1 <= len(self.player.inventory) - 1 + 2:
                    self.selectedItem += 1
                    return
            elif key == 32:
                self.player.useItem(self.selectedItem)
                self.alterInfoBar(self.player)
            return

        if self.search:
            if key == 119:
                if self.selectedItem - 1 >=0:
                    self.selectedItem -= 1
                    return
            elif key == 115:
                if self.selectedItem + 1 <= (len(self.player.inventory)) + (len(self.searchContainer.inventory) - 1) + 2:
                    self.selectedItem += 1
                    return
            elif key == 32:
                self.player.loot(self.searchContainer, self.selectedItem)
            return

            
        #checks for current active state and changes entity based on it
        if self.visualActive:
            entity = self.visual
        elif self.interactiveActive:
            entity = self.interact
        elif self.attackActive:
            entity = self.attack
            if key == 32:
                if self.valid and entity.standingOn.canAttack:
                    if self.player.caluculateHit(entity.standingOn):
                        self.player.attack(self.attack.standingOn)
                        self.alterInfoBar(self.attack.standingOn)
                        self.alterTextBox("You hit " + str(self.attack.standingOn.name) + " with " + str(self.player.calculateDMG()) + " damage")
                    else:
                        self.player.stats["AP"][0] -= self.player.calculateWeaponAPCost()
                        self.alterInfoBar(self.attack.standingOn)
                        self.alterTextBox("You attacked " + str(self.attack.standingOn.name) + ", but missed!")

                elif self.valid and not entity.standingOn.canAttack:
                    if self.player.caluculateHit(entity.standingOn):
                        self.alterInfoBar(self.attack.standingOn)
                        self.alterTextBox("You hit the " + str(entity.standingOn.name) + "... It did nothing...")
                    else:
                        self.player.stats["AP"][0] -= self.player.calculateWeaponAPCost()
                        self.alterInfoBar(self.attack.standingOn)
                        self.alterTextBox("You attacked " + str(entity.standingOn.name) + ", but missed!")
                return

        elif entity != self.player:
            sleep(0.15)
            self.cont = True
            if entity.stats["AP"][0] <= 0:
                self.cont = False
                return
            if entity.isHostile:
                if entity.caluculateHit(self.player):
                    entity.attack(self.player)
                    self.alterTextBox(str(entity.name) + " attacked " + str(self.player.name) + " with a " + str(entity.weapon.name))
                else:
                    path = pathfinding.movementPath(self.layout, entity, self.player, entity.x, entity.y) 
                    x = entity.x
                    y = entity.y
                    if self.layout[y][x + 1] == path[0]:
                        self.charRight(entity)
                    elif self.layout[y][x - 1] == path[0]:
                        self.charLeft(entity)
                    elif self.layout[y + 1][x] == path[0]:
                        self.charDown(entity)
                    elif self.layout[y - 1][x] == path[0]:
                        self.charUp(entity)
            self.resetAttackLayout()
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
        if key == 32 and self.interactiveActive:
            tile = self.interact.standingOn

            if isinstance(tile, TILES.Container):
                if tile.status == "LOCKED":
                    self.player.stats["AP"][0] -= 1
                    tile.status = "UNLOCKED"
                    self.alterTextBox("You manage to unlock the container")
                else:
                    self.alterTextBox("You search the container")
                    if not tile.searched:
                        tile.inventory = tile.initContainer()
                        tile.searched = True
                    self.searchContainer = tile
                    self.search = True

            elif isinstance(tile, TILES.Door):
                if tile.status == "LOCKED":
                    self.player.stats["AP"][0] -= 1
                    tile.status = "UNLOCKED"
                    self.alterTextBox("You manage to unlock the door")
                elif tile.status == "UNLOCKED":
                    tile.open = not tile.open
                    if tile.open:
                        self.player.stats["AP"][0] -= 1
                        tile.symbol = "/"
                        tile.collide = False
                        self.alterTextBox("You open the door")
                    elif not tile.open:
                        self.player.stats["AP"][0] -= 1
                        tile.symbol = "|"
                        tile.collide = True
                        self.alterTextBox("You close the door")
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
            self.alterInfoBar(self.player)

                            
    def charUp(self, entity):
        if isinstance(entity, VISUAL.Visual) and self.visual.y - 1 >= 0:
            if self.visual.y - 1 >= (self.player.y - self.player.visRangeY):
                self.layout[entity.y][entity.x] = entity.standingOn
                entity.move("w")
                entity.standingOn = self.layout[entity.y][entity.x]
                self.layout[entity.y][entity.x] = entity
                self.alterInfoBar(self.visual.standingOn)

        elif isinstance(entity, VISUAL.Crosshair) and self.attack.y - 1 >= 0:
            if self.attack.y - 1 >= (self.player.y - self.player.visRangeY):
                self.layout[entity.y][entity.x] = entity.standingOn
                entity.move("w")
                entity.standingOn = self.layout[entity.y][entity.x]
                self.layout[entity.y][entity.x] = entity

                self.valid = pathfinding.validPath(self.layout, self.player.standingOn, self.attack.standingOn, self.player.x, self.player.y)
                self.resetAttackLayout()

                self.alterInfoBar(self.attack.standingOn)

        elif isinstance(entity, VISUAL.Interact) and self.interact.y - 1 >= self.player.y - 1:
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
            if self.visual.y + 1 <= (self.player.y + self.player.visRangeY):
                self.layout[entity.y][entity.x] = entity.standingOn
                entity.move("s")
                entity.standingOn = self.layout[entity.y][entity.x]
                self.layout[entity.y][entity.x] = entity
                self.alterInfoBar(self.visual.standingOn)

        elif isinstance(entity, VISUAL.Crosshair) and self.attack.y + 1 <= len(self.layout) - 1:
            if self.attack.y + 1 <= (self.player.y + self.player.visRangeY):
                self.layout[entity.y][entity.x] = entity.standingOn
                entity.move("s")
                entity.standingOn = self.layout[entity.y][entity.x]
                self.layout[entity.y][entity.x] = entity

                self.valid = pathfinding.validPath(self.layout, self.player.standingOn, self.attack.standingOn, self.player.x, self.player.y)
                self.resetAttackLayout()

                self.alterInfoBar(self.attack.standingOn)

        elif isinstance(entity, VISUAL.Interact) and self.interact.y + 1 <= self.player.y + 1:
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
            if self.visual.x - 1 >= (self.player.x - self.player.visRangeX):
                self.layout[entity.y][entity.x] = entity.standingOn
                entity.move("a")
                entity.standingOn = self.layout[entity.y][entity.x]
                self.layout[entity.y][entity.x] = entity
                self.alterInfoBar(self.visual.standingOn)

        elif isinstance(entity, VISUAL.Crosshair) and self.attack.x - 1 >= 0:
            if self.attack.x - 1 >= (self.player.x - self.player.visRangeX):
                self.layout[entity.y][entity.x] = entity.standingOn
                entity.move("a")
                entity.standingOn = self.layout[entity.y][entity.x]
                self.layout[entity.y][entity.x] = entity

                self.valid = pathfinding.validPath(self.layout, self.player.standingOn, self.attack.standingOn, self.player.x, self.player.y)
                self.resetAttackLayout()

                self.alterInfoBar(self.attack.standingOn)

        elif isinstance(entity, VISUAL.Interact) and self.interact.x - 1 >= self.player.x - 1:
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
            if self.visual.x + 1 <= (self.player.x + self.player.visRangeX):
                self.layout[entity.y][entity.x] = entity.standingOn
                entity.move("d")
                entity.standingOn = self.layout[entity.y][entity.x]
                self.layout[entity.y][entity.x] = entity
                self.alterInfoBar(self.visual.standingOn)

        elif isinstance(entity, VISUAL.Crosshair) and entity.x + 1 <= len(self.layout[entity.y]) - 1:
            if self.attack.x + 1 <= (self.player.x + self.player.visRangeX):
                self.layout[entity.y][entity.x] = entity.standingOn
                entity.move("d")
                entity.standingOn = self.layout[entity.y][entity.x]
                self.layout[entity.y][entity.x] = entity

                self.valid = pathfinding.validPath(self.layout, self.player.standingOn, self.attack.standingOn, self.player.x, self.player.y)
                self.resetAttackLayout()

                self.alterInfoBar(self.attack.standingOn)

        elif isinstance(entity, VISUAL.Interact) and self.interact.x + 1 <= self.player.x + 1:
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
        self.visual = VISUAL.Visual(self.player.x, self.player.y)
        self.visual.standingOn = self.layout[self.visual.y][self.visual.x]
        self.layout[self.visual.y][self.visual.x] = self.visual

    def deactivateVisualMode(self):
        self.layout[self.visual.y][self.visual.x] = self.visual.standingOn
        self.visualActive = False
        self.visual = None
        self.alterInfoBar(self.player)

    def interactMode(self):
        self.interactiveActive = True
        self.interact = VISUAL.Interact(self.player.x, self.player.y)
        self.interact.standingOn = self.layout[self.interact.y][self.interact.x]
        self.layout[self.interact.y][self.interact.x] = self.interact

    def deactivateInteractMode(self):
        self.layout[self.interact.y][self.interact.x] = self.interact.standingOn
        self.interactiveActive = False
        self.interact = None
        self.alterInfoBar(self.player)

    def attackMode(self):

        self.attackActive = True
        self.attack = VISUAL.Crosshair(self.player.x, self.player.y)
        self.attack.standingOn = self.layout[self.attack.y][self.attack.x]
        self.layout[self.attack.y][self.attack.x] = self.attack

        self.valid = pathfinding.validPath(self.layout, self.player.standingOn, self.attack.standingOn, self.player.x, self.player.y)
        self.resetAttackLayout()

        self.alterInfoBar(self.player)


    def deactivateAttackMode(self):
        self.layout[self.attack.y][self.attack.x] = self.attack.standingOn
        self.attackActive = False
        self.alterInfoBar(self.player)

    def resetAttackLayout(self):
        for i in self.layout:
            for item in i:
                item.visited = False
                item.previous = None
                if item.standingOn != None:
                    item.standingOn.visited = False
                    item.standingOn.previous = None


    def alterTextBox(self, text):
        if len(self.textBox) >= 4:
            self.textBox.pop(0)
            self.textBox.append(text)
        else:
            self.textBox.append(text)
        return




all_levels = {"level_1":Level("level_1.txt", {1:CHARACTER.all_NPCs["bandit"], 
                                              2:CHARACTER.all_NPCs["bandit"]})
             }

