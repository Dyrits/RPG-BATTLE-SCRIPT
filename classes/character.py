from classes.bcolors import bcolors
import random


# Class used to create a character.
class character:
    base_precision = 70 # Fixed chances of hitting: 70%. Equivalent to 20% of chance of landing a critical hit and 0% of chance of landing a perfect hit.
    extra_precision = 0 # Bonus/Malus of critical chances. If this value is more than 5, every 1% more is giving 1% more chance of landing a perfect hit. 
    active_time_battle = 0 # Counter to know when a character is ready to take action.
    atb_ready = False # Variable set to "True" when the ATB reachs 100.
    talk = 0 # Number of time the character has talked.
    status = None # Specific status obtained by talking.
    block = False  # The next attack will block (or not) 75% points of damage.
    def __init__(self, playable, name, vitality, energy, speed, strenght, power, actions, spells, items):
        self.playable = playable # Allows to differentiate NPC and PC.
        self.name = name # Name of the character.
        self.max_vitality = vitality # Maximum ammount of health points. It can be increased by overhealing.
        self.vitality = vitality # Current ammount of health points. Once it reachs 0, the character is dead.
        self.max_energy = energy # Maximum ammount of energy points. Having more energy than this value will cause damage.
        self.energy = energy # Current ammount of energy points. It is used to cast spells.
        self.speed = speed # Speed between 2 actions.
        self.base_strenght = strenght # Fixed physical strenght 
        self.strenght = strenght # Variable physical strenght. It can be increased with the "Brave" status.
        self.base_power = power # Fixed magic power.
        self.power = power # Variable magic power. It can be increases with the "Brave" status.
        self.spells = spells # Set of spells.
        self.actions = actions # Possible actions.
        self.items = items
        self.spell_hindrance = []  # Hindrance granted by a spell.
        self.spell_boon = [] # Boon granted by a spell. Currently, it is only used with spark.

    #Function used to calculate the actual precision:
    def precision(self):
        return self.base_precision + self.extra_precision

    # Function used to display a situation overview:
    def situation_recap(self, is_npc=False):
        print("-" * 100)
        if self.atb_ready == False:
            print(f"{str(self.active_time_battle) + '% (+' + str(self.speed) + ')':<10}", end="")
        else:
            print(f"{'Ready'.upper():<10}", end="")
        print(f"{self.name.upper():<15}", end="") # Name
        print("{:>15}".format(f"{self.vitality}/{self.max_vitality} "), end="") # Vitality numeric display
        # Vitality visual display: 
        if is_npc == True:
            print("{:<30}".format(bcolors.CRED2 + "█" * (25 * self.vitality // self.max_vitality) + bcolors.CBLACK + "█" * (25 - (25 * self.vitality // self.max_vitality)) + bcolors.CEND), end="")
        else:
            print("{:<30}".format(bcolors.CGREEN + "█" * (25 * self.vitality // self.max_vitality) + bcolors.CBLACK + "█" * (25 - (25 * self.vitality // self.max_vitality)) + bcolors.CEND), end="")
        print("{:>15}".format(f"{self.energy}/{self.max_energy} "), end="") # Energy numeric display
        # Energy visual display:
        if self.energy > self.max_energy:
            print(bcolors.CYELLOW + bcolors.CBLINK2 + "█" * 15 + bcolors.CBOLD + "+" + "█" * (15 * (self.energy - self.max_energy) // self.max_energy) + bcolors.CEND + " OVERCHARGED!")
        else: 
            print(bcolors.CYELLOW + "█" * (15 * self.energy // self.max_energy) + bcolors.CBLACK + "█" * (15 - (15 * self.energy // self.max_energy)) + bcolors.CEND)
        if self.status:
            print(bcolors.CITALIC +  f"{self.status}" + bcolors.CEND)
        if self.strenght > self.base_strenght:
            print(f"Strenght +{self.strenght - self.base_strenght}")
        elif self.strenght < self.base_strenght:
            print(f"Strenght {self.strenght - self.base_strenght}")
        if self.power > self.base_power:
            print(f"Power {self.power - self.base_power}")
        elif self.power < self.base_power:
            print(f"Power {self.power - self.base_power}")
        if self.precision() > self.base_precision:
            print(f"Precision +{self.precision() - self.base_precision}")
        elif self.precision() != self.base_precision:
            print(f"Precision {self.precision() - self.base_precision}")

    # Function used to calculate the outcome of a strike attack based on the character's strenght and precision.
    def strike_damage(self, target):
        strike_attack = int(self.strenght * random.uniform(0.8, 1.2))
        if "Spark" in self.spell_boon:
            strike_attack *= 2
            self.spell_boon.remove("Spark")
        if target.block == True:
            strike_attack //= 4
        critical_chance = self.precision() + random.randint(0, 100)
        if critical_chance > 175:
            strike_attack *= 2
            print(f"{self.name} lands a perfect hit  to {target.name} for {strike_attack} points of damage.")
            target.take_damage(strike_attack)
        elif critical_chance > 150:
            strike_attack = int(strike_attack * 1.5)
            print(f"{self.name} lands a critical hit to {target.name} for {strike_attack} points of damage.")
            target.take_damage(strike_attack)
        elif critical_chance > 100:
            print(f"{self.name} attacks {target.name} for {strike_attack} points of damage.")
            target.take_damage(strike_attack)
        else:
            print(f"{self.name} attacks {target.name} but misses. {target.name} sees an opportunity to hit more precisely.")
            target.extra_precision += 5
        target.block = False

    # Function used for the character to receive the damaged.
    def take_damage(self, damage):
        self.vitality -= damage
        if self.vitality < 1:
            self.vitality = 0
        return self.vitality

    # Function used to print the menu of actions:
    def choose_action(self):
        print(bcolors.CBLUE + "SELECT AN ACTION:" + bcolors.CEND)
        for index, action in enumerate(self.actions):
            print(bcolors.CVIOLET + str(index + 1) + bcolors.CEND + ": " + action.upper())
            
    # Function used to print the menu of spells:
    def choose_spell(self):
        print(bcolors.CBLUE2 + "SELECT A SPELL:" + bcolors.CEND)
        print(bcolors.CVIOLET2 + "0" + bcolors.CEND + ".<<< Back")
        for index, spell in enumerate(self.spells):
            print(" " * 5 + bcolors.CVIOLET2 + str(index + 1) + bcolors.CEND + ": " + spell.name.upper() + f"(Energy cost: {spell.cost})" + "\n" + " " * 5 + "# " + spell.description)

    # Function used to calculate the damage of a spell based on the character's power:
    def spell_damage(self, index):
        return int(self.spells[index - 1].damage * self.power * random.uniform(0.04, 0.06))

    # Function used to print the menu of items:
    def choose_item(self):
        print(bcolors.CBLUE2 + "SELECT AN ITEM:" + bcolors.CEND)
        print(bcolors.CVIOLET2 + "0" + bcolors.CEND + ".<<< Back")
        index = 1
        for index, item in enumerate(self.items):
            print(" " * 5 + bcolors.CVIOLET2 + str(index + 1) + bcolors.CEND + ": " + item.name.upper() + f"(Quantity: {item.quantity})" + "\n" + " " * 5 + "# " + item.description)

    # Fucntion used to define the outcome of an item being used:
    def item_outcome(self, item):
        if item.category == "Food":
            self.vitality += item.value
            print(f"{self.name} eats. {item.name}! It is yummy. {self.name} heals {item.value} health points.")
        if item.category == "Beverage":
            self.energy += item.value
            print(f"{self.name} drinks a {item.name}! It gives {self.name} wings! {item.value} energy points recovered.")
