class Weapon:
    def __init__(self, name, klass, raw_damage, raw_range, ammoCap, APCost, weight, value):
        self.name = name
        self.klass = klass

        self.raw_damage = raw_damage
        self.raw_range = raw_range
        self.ammoCap = ammoCap
        if self.ammoCap != None:
            self.currentAmmo = [self.ammoCap, self.ammoCap]

        self.APCost = APCost

        self.weight = weight
        self.value = value

    def __repr__(self):
        if self.klass == "MELEE":
            string = (self.name + " | " + self.klass + " | Damage: " + str(self.raw_damage) +
                    " | Range: " + str(self.raw_range) + " | AP Cost: " + str(self.APCost) + " | Weight: " + str(self.weight) + 
                      " | Value: " + str(self.value))
        elif self.klass == "EXPLOSIVE":
            string = ""
        else:
            string = (self.name + " | " + self.klass + " | Damage: " + str(self.raw_damage) +
                      " | Range: " + str(self.raw_range) + " | Ammo: " + str(self.currentAmmo) + " | AP Cost: " + str(self.APCost) +
                      " | Weight: " + str(self.weight) + " | Value: " + str(self.value))
        return string

class Armor:
    def __init__(self, name, klass, raw_defence, weight, value):
        self.name = name
        self.klass = klass
        self.raw_defence = raw_defence
        self.weight = weight
        self.value = value

    def __repr__(self):
        string = (self.name + " | " + self.klass + " | Defence: " +
                  str(self.raw_defence) + " | Weight: " + str(self.weight) + 
                  " | Value: " + str(self.value))
        return string

class General:
    def __init__(self, name, klass):
        self.name = name
        self.klass = klass

        if self.klass == "HEAL":
            self.healAmount = 1
            self.turnDuration = 3





all_weapons = {"fists": Weapon(name="Fists", klass="MELEE", raw_damage=1, raw_range=1, ammoCap=None, APCost=1, weight=0, value=0),
               "rusty pistol": Weapon(name="Rusty Pistol", klass="PISTOL", raw_damage=2, raw_range=5, ammoCap=6, APCost=2, weight=4, value=5),
              }

all_armor = {"underwear": Armor(name="Underwear", klass = "LIGHT", raw_defence=0, weight=0, value=0),
             "common clothes": Armor(name="Common Clothes", klass="LIGHT", raw_defence=2, weight=1, value=2),
            }

all_items = {**all_weapons, **all_armor}


