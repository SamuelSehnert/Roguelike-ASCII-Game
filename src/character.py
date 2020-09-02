from random import randint
import items as ITEMS

import level as LEVEL


class Player:
    def __init__(self, name, health, AP,  collide=True):
        self.name = name

        self.weapon = ITEMS.all_weapons["fists"]
        self.armor = ITEMS.all_armor["underwear"]

        self.stats = {"HP":[health, health], "AP":[AP,AP], "DF":self.calculateDF(),"DMG":self.calculateDMG()}

        self.visRangeY = 3
        self.visRangeX = self.visRangeY * 2

        self.x = 5
        self.y = 7

        self.standingOn = None
        self.collide = collide

        self.canAttack = True

        self.interact = False

        #{common name:[object pointer, quantity]}
        self.inventory = {"rusty pistol": [ITEMS.all_items["rusty pistol"], 1],
                          "common clothes": [ITEMS.all_items["common clothes"], 1],
                          } 

    def __repr__(self):
        return "@"


    def move(self, moveDirection):
        if moveDirection == "w":
            self.y -= 1
        elif moveDirection == "s":
            self.y += 1
        elif moveDirection == "a":
            self.x -= 1
        elif moveDirection == "d":
            self.x += 1

    def attack(self, other):
        damage = self.calculateDMG()
        other.stats["HP"][0] -= damage

    def calculateDF(self):
        return self.armor.raw_defence

    def calculateDMG(self):
        return self.weapon.raw_damage

    def calculateWeaponAPCost(self):
        return self.weapon.APCost


    def loot(self, container, selected):
        if selected <= (len(self.inventory) - 1) + 2:
            container.cap += 1
            for x, item in enumerate(self.inventory, 2):
                if x == selected:
                    if item in container.inventory:
                        container.inventory[item][1] += 1
                        self.inventory[item][1] -= 1
                        if self.inventory[item][1] <= 0:
                            del self.inventory[item]
                        return
                    else:
                        container.inventory[item] = [self.inventory[item][0], 1]
                        self.inventory[item][1] -= 1
                        if self.inventory[item][1] <= 0:
                            del self.inventory[item]
                        return



        elif selected > (len(self.inventory) - 1) + 2:
            container.cap -= 1
            for x, item in enumerate(container.inventory, (len(self.inventory) - 1) + 3):
                if x == selected:
                    if item in self.inventory:
                        self.inventory[item][1] += 1
                        container.inventory[item][1] -= 1
                        if container.inventory[item][1] <= 0:
                            del container.inventory[item]
                        return
                    else:
                        self.inventory[item] = [container.inventory[item][0], 1]
                        container.inventory[item][1] -= 1
                        if container.inventory[item][1] <= 0:
                            del container.inventory[item]
                        return


    def useItem(self, selected):
        # if player selecting current weapon to unequip
        if selected == 0:
            if self.weapon.name.lower() != "fists":
                self.equipWeapon("fists") 
                self.weapon = ITEMS.all_weapons["fists"]
                self.stats["DMG"] = self.calculateDMG()
                self.stats["AP"][0] -= 1

        # if player selecting current armor to unequip
        elif selected == 1:
            if self.armor.name.lower() != "underwear":
                self.equipArmor("underwear")
                self.armor = ITEMS.all_armor["underwear"]
                self.stats["DF"] = self.calculateDF()
                self.stats["AP"][0] -= 1
        # if player is selecting item in inventory
        else:
            for x, item in enumerate(self.inventory, 2):
                if x == selected:
                    if item in ITEMS.all_weapons:
                        self.equipWeapon(item)
                        self.stats["DMG"] = self.calculateDMG()

                    elif item in ITEMS.all_armor:
                        self.equipArmor(item)
                        self.stats["DF"] = self.calculateDF()
                    self.stats["AP"][0] -= 1
                    return

    def equipWeapon(self, item):
        # if the current weapon is in the inventory, will then add one to item quantity
        if self.weapon.name.lower() in self.inventory:
            self.inventory[self.weapon.name.lower()][1] += 1
        # if the current weapon is NOT in the inventory
        else:
            if self.weapon.name.lower() != "fists":
                self.inventory[self.weapon.name.lower()] = [ITEMS.all_weapons[self.weapon.name.lower()], 1]
        
        if item != "fists":
            self.weapon = self.inventory[item][0]
            self.inventory[item][1] -= 1
            if self.inventory[item][1] == 0:
                del self.inventory[item]


    def equipArmor(self, item):
        # if the current armor is in the inventory, will then add one to item quantity
        if self.armor.name.lower() in self.inventory:
            self.inventory[self.armor.name.lower()][1] += 1
        # if the current armor is NOT in the inventory
        else:
            if self.armor.name.lower() != "underwear":
                self.inventory[self.armor.name.lower()] = [ITEMS.all_armor[self.armor.name.lower()], 1]
        
        if item != "underwear":
            self.armor = self.inventory[item][0]
            self.inventory[item][1] -= 1
            if self.inventory[item][1] == 0:
                del self.inventory[item]


    def characterMenu(self, selected):
        def display(health, ap, df, dmg, inventory, selected):
            total = []
            health_ap_string = "Health: {0}/{1}     |     Action Points {2}/{3}     |     Defence: {4}     |     Damage: {5}"
            total.append("-"*len(health_ap_string))
            
            total.append(health_ap_string.format(health[0], health[1], ap[0], ap[1], df, dmg))
            total.append("-"*len(health_ap_string))


            head = "   0"
            if selected == 0:
                chest = " _/|\_" + (" " * 3) + "--> " +  "Weapon: " + str(self.weapon)
            else:
                chest = " _/|\_" + (" " * 3) + "Weapon: " + str(self.weapon.name.title())
            if selected == 1:
                torso = "   |" + (" " * 5) + "--> " +  "Armor: " + str(self.armor)
            else:
                torso = "   |" + (" " * 5) + "Armor: " + str(self.armor.name.title())

            thigh = "  / \ "
            legs = "_/   \_"
            all_parts = [head, chest, torso, thigh, legs]
            for part in all_parts:
                total.append(part)
            total.append("-"*20)

            total.append("INVENTORY")

            for x, item in enumerate(inventory, 2):
                if x == selected:
                    if isinstance(self.inventory[item][0], ITEMS.Weapon):
                        total.append("-->  | " + str(inventory[item][0].name) + " x " + str(inventory[item][1]) + "|  " + str(ITEMS.all_weapons[item]))
                    if isinstance(self.inventory[item][0], ITEMS.Armor):
                        total.append("-->  | " + str(inventory[item][0].name) + " x " + str(inventory[item][1]) + "|  " + str(ITEMS.all_armor[item]))
                    if isinstance(self.inventory[item][0], ITEMS.General):
                        total.append("-->  | " + str(self.inventory[item][0].name) + " x " + str(self.inventory[item][1]) + "|  " + str(ITEMS.all_general[item]))

                else:
                    total.append("| " + str(inventory[item][0].name) + " x " + str(inventory[item][1]) + "|")
            total.append("-"*20)

            return total
        return display(self.stats["HP"], self.stats["AP"], self.stats["DF"], self.stats["DMG"], self.inventory, selected)


class NPC:
    def __init__(self, name, klass, health, AP, isHostile, collide=True):
        self.name = name
        self.stats = {"HP":[health, health], "AP":[AP,AP]}

        self.isHostile = isHostile
        self.canAttack = True

        self.klass = klass

        self.x = 0
        self.y = 0

        self.standingOn = None
        self.collide = collide

        self.visited = False

        self.interact = True

        #{common name:[object pointer, quantity]}
        self.inventory = {}

        self.weapon = ITEMS.all_weapons["fists"]
        self.armor = ITEMS.all_armor["underwear"]

    def __repr__(self):
        if self.klass == "bandit":
            return "B"

    def randomPosX(self):
        return randint(0, 45)

    def randomPosY(self):
        return randint(0, 7)

