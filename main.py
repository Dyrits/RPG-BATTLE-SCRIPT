from classes.spells import *
from classes.inventory import *
from classes.character import character
from classes.bcolors import bcolors
import random

#FUNCTIONS
# Situation overview:
def situation_overview():
    print()
    print(bcolors.CYELLOW2 + bcolors.CBOLD + f"TURN: {turn}" + bcolors.CEND)
    print()
    for player in players:
        player.situation_recap()
    for enemy in enemies:
        enemy.situation_recap(True)
    print("-" * 100)
    print()
    
# Active time battle:
def update_atb():
    for character in alive_characters:
        character.active_time_battle += character.speed
        if character.active_time_battle > 99:
            character.atb_ready = True
            character.active_time_battle -= 100
                                
# Defining the functions to select the target:
def choose_target():
    print(bcolors.CBLUE2 + "SELECT A TARGET:" + bcolors.CEND)
    print(bcolors.CVIOLET2 + "0" +
            bcolors.CEND + ".<<< Back")
    for index, enemy in enumerate(alive_enemies):
        print(" " * 5 + bcolors.CRED2 + str(index + 1) +
                bcolors.CEND + ": " + enemy.name.upper())
def select_target():
    try:
        index_target = int(input(
                            f"Which opponent do you want {player.name} to target? Input the corresponding number: "))
        if index_target < 0 or index_target > (len(alive_enemies)):
            print(bcolors.CITALIC + bcolors.CGREY +
                    "Did you select a valid target? It doesn't seem to work." + bcolors.CEND)
            index_target = None
    except:
        print(bcolors.CITALIC + bcolors.CGREY +
                "Did you select a valid target? It doesn't seem to work." + bcolors.CEND)
        index_target = None
    return index_target

# Defining the function to check the deaths among the enemies:
def check_deaths_enemies():
    for index, enemy in enumerate(alive_enemies):
        if enemy.vitality < 1:
            enemy.vitality = 0
            print()
            enemy.status = "[DEAD]"
            enemy.situation_recap()
            print()
            print(bcolors.CGREEN2 + f"{enemy.name} is dead." + bcolors.CEND)
            print()
            alive_enemies.pop(index)
            
# Defining the function to check the deaths among the enemies:
def check_deaths_players():
    for index, player in enumerate(alive_players):
        if player.vitality < 1:
            player.vitality = 0
            print()
            player.status = "[DEAD]"
            player.situation_recap()
            print()
            print(bcolors.CRED2 + f"{player.name} is dead." + bcolors.CEND)
            print()
            alive_players.pop(index)
            
# Defining the function to check if all the players are dead.
def lose():
    if len(alive_players) == 0:
        print(bcolors.CRED2 + "Everyone in the party is dead" + bcolors.CEND)
        print(bcolors.CRED2 + bcolors.CBOLD + "GAME OVER!" + bcolors.CEND)
        situation_overview()
        return True
    else:
        return False

# Defining the function to check if all the enemies are dead.
def win():
    if len(alive_enemies) == 0:
        print(bcolors.CGREEN2 + "Every opponent has been killed!" + bcolors.CEND)
        print(bcolors.CGREEN2 + bcolors.CBOLD + "VICTORY!" + bcolors.CEND)
        situation_overview()
        return True
    else:
        return False
    

# List of actions:
storyteller = ["Strike attack", "Spell", "Block & Focus", "Talk", "Items"]
thief = ["Strike attack", "Spell", "Block & Focus", "Steal", "Items"]
glasscanon = ["Strike attack", "Spell", "Items"]
barbaric = ["Strike attack", "Slicing claws", "Vodoo"]

# Starting variables:
turn = 0
game_over = False

# The characters are created:
dylan = character(True, "Dylan", 1000, 200, 15, 50, 250, storyteller, electricity, items)
oddin = character(True, "Oddin", 1500, 50, 40, 250, 100, thief, fire, items)
kevin = character(True, "Kevin", 500, 100, 10, 750, 750, glasscanon, controls, items)
krizkarsh = character(False, "Krizkarsh", 15000, 200, 25, 250, 100, barbaric, None, None)
ryorkush = character(False, "Ryorkush", 15000, 200, 5, 500, 100, barbaric, None, None)

players = [dylan, oddin, kevin]
alive_players = [dylan, oddin, kevin]
enemies = [krizkarsh, ryorkush]
alive_enemies = [krizkarsh, ryorkush]
alive_characters = alive_players + alive_enemies
atb_ready_characters = []

# START OF THE BATTLE:
print(bcolors.CITALIC + bcolors.CBOLD + f"There is a chest! But several opponents are on the way! Defeat them!" + bcolors.CEND)

# The fight is continuing until the game is over:
while game_over == False:
    
    # Updating the list of characters being ready:
    update_atb()
    turn += 1
    for character in alive_characters:
        if character.atb_ready:
            atb_ready_characters.append(character)
    if len(atb_ready_characters) == 0:
        situation_overview()
        print(bcolors.CITALIC + "No one is ready to attack this turn..." + bcolors.CEND)
        input("Press enter to continue: ")
        
    for character in atb_ready_characters:
        if not game_over:
            situation_overview()
        while character.atb_ready and game_over == False:
            
            #PLAYER TURN:
            if character.playable:
                player = character
                
            # Player's choice of action:
                player.situation_recap()
                print("-" * 100)
                player_action = None
                while player_action == None:
                    player.choose_action()
                    try:
                        player_action = int(input(f"What do you want {player.name} to do? Input the corresponding number: "))
                        if player_action < 1 or player_action > (len(player.actions)):
                            print(bcolors.CITALIC + bcolors.CGREY + "You didn't type a proper command. Select a number in the list." + bcolors.CEND)
                            player_action = None
                    except:
                        print(bcolors.CITALIC + bcolors.CGREY + "You didn't type a proper command. A simple number is required." + bcolors.CEND)
                        player_action = None
                    

                # STRIKE ATTACK:
                if player.actions[player_action - 1] == "Strike attack":
                    # Selecting the target:
                    index_target = None
                    while index_target == None:                  
                        choose_target()
                        index_target = select_target()
                    # An option is available for the player to go back to the previous menu:
                    if index_target == 0:
                        continue
                    # Outcome of the strike attack:
                    if "Spark" in player.spell_boon:
                        print(f"Spark's power is summoned to reinforce {player.name}'s attack.")
                    target = alive_enemies[index_target - 1]
                    player.strike_damage(target)
                
                    
                # SPELL :
                elif player.actions[player_action - 1] == "Spell":
                    player_spell = None
                    while player_spell == None:
                        player.choose_spell()
                        try:
                            player_spell = int(input(f"What spell do you want {player.name} to use? Input the corresponding number: "))
                            if player_spell != 0 and player.spells[player_spell - 1].cost > player.energy:
                                print(bcolors.CSELECTED +  f"{player.name} doesn't have enough energy for that. Try something else..." + bcolors.CEND)
                                player_spell = None
                                continue
                            if player_spell < 0 or player_spell > (len(player.spells)):
                                print(bcolors.CITALIC + bcolors.CGREY + "Did you select a valid spell? It doesn't seem to work." + bcolors.CEND)
                                player_spell = None
                        except:
                            print(bcolors.CITALIC + bcolors.CGREY + "Did you select a valid spell? It doesn't seem to work." + bcolors.CEND)
                            player_spell= None
                        
                        # Selecting the target:
                        if player_spell:
                            index_target = None
                            while index_target == None:
                                choose_target()
                                index_target = select_target()
                            if index_target == 0:
                                player_spell = None
                                continue
                            
                    # An option is available for the player to go back to the previous menu:
                    if player_spell == 0:
                        continue

                    # Player's spell outcomes :
                    player.energy -= player.spells[player_spell - 1].cost #We reduce the player energy according to the chosen spell's cost.
                    spell_damage = player.spell_damage(player_spell)
                    target = alive_enemies[index_target - 1]
                    target.take_damage(spell_damage)
                    print(f"{player.name} casts {player.spells[player_spell - 1].name}. {target.name} loses {spell_damage} health points.")
                    
                    # SPELL: SPECIAL EFFECTS:
                    if player.spells[player_spell - 1].name == "Lightning Leech":
                        # The player is healed for the same ammount of damaged done with Lightning Leech.
                        player.vitality += spell_damage
                        print(f"{player.name} recovers {spell_damage} health points.")
                        
                    if player.spells[player_spell - 1].name == "Blaze":
                        player.vitality //= 2
                        print(f"{player.name}'s health points are reduced by half.")
                        target.status = "Enraged"
                        
                    # Checking the deaths before resolving some special effects:
                    check_deaths_enemies()
                    game_over = win()
                    if game_over:
                        continue

                    if player.spells[player_spell - 1].name == "Zap":
                        zap_effect = int(target.precision() * 40 / 100)
                        # The precision will be restored at the end of the turn.
                        if "Zap" not in target.spell_hindrance:
                            target.extra_precision -= zap_effect
                            target.spell_hindrance.append("Zap")
                            print(f"{target.name}'s precision is reduced by {zap_effect} for one attack.")
                        else:
                            print(f"{target.name} was already affected by Zap.")

                    if player.spells[player_spell - 1].name == "Glow":
                        target.spell_hindrance.append(["Glow", 3])
                        glow_stack = sum(glow.count("Glow") for glow in target.spell_hindrance)
                        target.strenght = target.base_strenght - int(target.base_strenght * 5 / 100) * glow_stack
                        target.power = target.base_power - int(target.base_power * 5 / 100) * glow_stack
                        # The effect will be reduced at the end of the turn.
                        print(f"The strenght and power of {target.name} has been reduced.")
                        if target.strenght < 0:
                            target.strenght = 0
                        if target.power < 0:
                            target.strenght = 0
                            
                    if player.spells[player_spell - 1].name == "Spark":
                        player.spell_boon.append("Spark") #The boon is directly included in the function to calculate the strike attack damages.
                        print(f"{player.name}'s next strike attack will be twice as powerful.")
                    
                        
                # BLOCK AND FOCUS
                # Block & Focus has different effects. It removes the "Upset" status and remove any precision malus. It heals a little bit, and regenerates some energy:
                elif player.actions[player_action - 1] == "Block & Focus":
                    player.energy += int(player.max_energy * 5 / 100)
                    player.vitality += int(player.max_vitality * 5 / 100)
                    print(f"{player.name} focus and regenerates 5 percent of maximum energy and 5 percent of maximum health.\nThe next incoming damages will be reduced by 75 percent.")
                    if player.extra_precision < 0:
                        player.extra_precision = 0
                    player.block = True # Block also allows to reduce the next incoming damages by 75%.
                    if player.status == "Upset":
                        player.status = None
                        print(f"{player.name} is not upset anymore.")

                #TALK
                # This option will be reworked:
                elif player.actions[player_action - 1] == "Talk":
                    print()
                    print(f"{player.name}: I have nothing to say.")
                    print()
                    continue

                # STEAL:
                elif player.actions[player_action - 1] == "Steal":
                    stolen_item_index = random.randrange(len(player.items))
                    # If the stolen item is the dynamite or a hamburger/cheeseburgers, we are rerolling one time:
                    if player.items[stolen_item_index].name == "Dynamite" or player.items[stolen_item_index].name == "Hamburger" or player.items[stolen_item_index].name == "Cheeseburgers":
                        stolen_item_index = random.randrange(len(player.items)) 
                    player.items[stolen_item_index].quantity += 1
                    print(f"{player.name} gets closer and takes something from the chest. What is it? {player.items[stolen_item_index].name}!")
                    print(f"The party has now {player.items[stolen_item_index].quantity} of them!")

                # ITEMS:
                elif player.actions[player_action - 1] == "Items":
                    player_item = None
                    while player_item == None:
                        player.choose_item()
                        try:
                            player_item = int(input(f"What item do you want {player.name} to use? Input the corresponding number: "))
                            if player_item != 0 and player.items[player_item - 1].quantity < 1:
                                print(bcolors.CSELECTED + f"{player.name} doesn't have anymore of that item. Try something else..." + bcolors.CEND)
                                player_item = None
                                continue
                            if player_item < 0 or player_item > (len(player.items)):
                                print(bcolors.CITALIC + bcolors.CGREY + "Did you select a valid item? It doesn't seem to work. 1" + bcolors.CEND)
                                player_item = None
                        except:
                            print(bcolors.CITALIC + bcolors.CGREY + "Did you select a valid item? It doesn't seem to work." + bcolors.CEND)
                            player_item = None
                    # An option is available for the player to go back to the previous menu:
                    if player_item == 0:
                        continue

                    item = player.items[player_item - 1]
                    item.quantity -= 1
                    
                    # Player's item outcomes:
                    player.item_outcome(item)
                    if item.category == "Feast":
                        for player in alive_players:
                            player.vitality += 1000
                        print(f"{item.name} are delicious. Everyone recovers {item.value} health points.")
                    if item.category == "Explosive":
                        for enemy in alive_enemies:
                            enemy.vitality -= item.value
                        for player in alive_players:
                            player.vitality -= item.value // 10
                        print(f"{player.name} throw a {item.name} to the ennemies dealing {item.value} points of damage. {player.name} and his allies also receive {item.value // 10} points of damage from the explosion.")
                    
                check_deaths_enemies()
                check_deaths_players()
                
                # With the explosion, everyone could die at the same time:
                if len(alive_characters) == 0:
                    situation_overview()
                    print(bcolors.CRED2 + "Everyone died in the explosion. May they rest in peace." + bcolors.CEND)
                    game_over = True
                    continue
                
                # Checking if the game is over:
                game_over = win()
                if game_over:
                    continue
                game_over = lose()
                if game_over:
                    continue

                # In some situation, the character's health can be greater than its maximum ammount. In that case, the character's health is increased by 5% of the exceeding ammount:
                for player in alive_players:
                    if player.vitality > player.max_vitality:
                        print(f"{player.name} has an excedent of health points. The maximum ammount of health points is increased by {(player.vitality - player.max_vitality) // 20}.")
                        player.max_vitality += (player.vitality - player.max_vitality) // 20
                        player.vitality = player.max_vitality
                    
                # In some situation, the energy can be greater than it maximum ammounts. In that case, the character get damaged by this exceeding ammount:
                if player.energy > player.max_energy and player.vitality > 0:
                    player.vitality -= (player.energy - player.max_energy) * 2
                    if player.vitality < 0:
                        player.vitality = 0
                    print(f"{player.name} is holding too much energy. {player.name}'s body is struggling to handle it. {player.name} loses {(player.energy - player.max_energy) * 2} health points.")
                
                # The situation is checked again since the player canbe killed by the overcharged.
                check_deaths_players()
                game_over = lose()
                if game_over:
                    continue
                # The precision is adjusted every turn in order to have more chance of hit every time the enemy's strike attack misses a character:
                if player.extra_precision > 0:
                    player.extra_precision -= 5

                # The "Upset" status remove 5 points of precision every turn:
                if player.status == "Upset":
                    print(f"{player.name} is upset and lose some precision.")
                    player.extra_precision -= 5
                    if player.extra_precision < -65:
                        player.extra_precision = -70
                        print(f"{player.name} is very upset and unfocused. Strike attacks will always miss their target!")
                        
                # The "Brave" status increase the strenght and power by 5 every turn:
                if player.status == "Brave":
                    print(f"{player.name} ready to overcome any challenge with an increased strenght and power.")
                    player.strenght += 5
                    player.power += 5
                
                alive_characters = alive_players + alive_enemies
                    
                    
            # ENEMY TURN:
            elif character.playable == False:
                enemy = character
                
                print()
                input(f"{enemy.name} will attack. Press Enter to proceed: ")
                
                # Enemy choice of action:
                vodoo_energy_power = int(enemy.energy / random.uniform(1, 5))
                if enemy.vitality < enemy.max_vitality // 8:
                    enemy_action = "Vodoo"
                else:
                    enemy_action = random.choice(enemy.actions)
                    # Slicing claws and Vodoo have less chance to be used.
                    if enemy_action == "Slicing claws" or enemy_action == "Vodoo":
                        enemy_action = random.choice(enemy.actions)
                        
                # Vodoo can't be used if the energy is not enough.
                while enemy_action == "Vodoo" and enemy.energy < vodoo_energy_power :
                    enemy_action = random.choice(enemy.actions)
                    
                # Attacking only one character:
                if enemy_action == "Strike attack":
                    index_target = random.randrange(len(alive_players))
                    # The enemy attacks randomly an alive party member:
                    enemy.strike_damage(alive_players[index_target])

                # Attacking everyone: 
                if enemy_action == "Slicing claws":
                    print(f"{enemy.name} slice heavily multiple times with its claws attacking every party member.")
                    for player in alive_players:
                        enemy.strike_damage(player)
                        
                # Vodoo magic is strongly random:
                if enemy_action == "Vodoo":
                    enemy.energy -= vodoo_energy_power
                    print(f"{enemy.name} invokes some vodoo magic using {vodoo_energy_power} points of energy and not really knowing what is happening.")
                    for player in alive_players:
                        vodoo_damage = int(vodoo_energy_power * (random.uniform(0, 0.2)) * enemy.power)
                        player.vitality -= vodoo_damage
                        print(f"{player.name} receives {vodoo_damage} points of damage from the vodoo magic.")
                    vodoo_healing = int(vodoo_energy_power * random.uniform(-0.25, 0.25) * enemy.power)
                    enemy.vitality += vodoo_healing
                    if vodoo_healing < 0:
                        print(f"{enemy.name} gets hurt from handling vodoo magic. {enemy.name} loses {-(vodoo_healing)} health points.")
                    elif vodoo_healing > 0:
                        print(f"{enemy.name} recovers {vodoo_healing} health points.")
                    if enemy.vitality > enemy.max_vitality:
                        enemy.energy += enemy.vitality - enemy.max_vitality
                        print(f"{enemy.name} converts its excedent of health points ({enemy.vitality - enemy.max_vitality}) to energy.")
                        enemy.vitality = enemy.max_vitality
                        if enemy.energy > enemy.max_energy:
                            enemy.max_energy += (enemy.energy - enemy.max_energy) // 2
                            print(f"{enemy.name} holds too much energy. The maximum ammount of energy increases by {(enemy.energy - enemy.max_energy) // 2}.")
                            enemy.energy = enemy.max_energy
                            
                # Checking the outcome of the enemy actions:
                check_deaths_enemies()
                check_deaths_players()
                if len(alive_characters) == 0:
                    situation_overview()
                    print(bcolors.CRED2 + "Everyone died because of the vodoo magic. May they rest in peace." + bcolors.CEND)
                    game_over = True
                    continue
                
                # Checking if the game is over:
                game_over = win()
                if game_over:
                    continue
                game_over = lose()
                if game_over:
                    continue
                
                # The precision is adjusted in order to have only 5% more chance of hit every time a player's character's strike attack misses:
                if enemy.extra_precision > 0:
                    enemy.extra_precision -= 5

                # "Zap" must only last one turn:
                if "Zap" in enemy.spell_hindrance:
                    enemy.extra_precision += zap_effect
                    print("The effect of Zap is disappear.")
                    del enemy.spell_hindrance[enemy.spell_hindrance.index("Zap")]

                # The "Enraged" status increase or decrease the ennemy strenght randomly very turn.
                if enemy.status == "Enraged":
                    enemy.strenght += random.randint(-25, 50)

                # Every 5 turns, one stack of Glow is removed.
                glow_stack = sum(glow.count("Glow") for glow in enemy.spell_hindrance) 
                if glow_stack > 0:
                    for glow in enemy.spell_hindrance:
                        for glow_value in glow:
                            if str(glow_value).isdigit():
                                glow.remove(glow_value)
                                glow.append(glow_value - 1)
                                if not glow_value - 1:
                                    enemy.spell_hindrance.remove(glow)
                                    print(f"{enemy.name} recovers some strenght and power.")
                    new_glow_stack = sum(glow.count("Glow") for glow in enemy.spell_hindrance)
                    enemy.strenght += int(enemy.base_strenght * 5 / 100) * (glow_stack - new_glow_stack)
                    enemy.power += int(target.base_power * 5 / 100) * (glow_stack - new_glow_stack)
                    if enemy.strenght < 1:
                        enemy.strenght = 1;
                    if enemy.power < 1:
                        enemy.power = 1; 
                    if not glow_stack:
                        print("Glow is not effective anymore.")
                    
                        
            
            character.atb_ready = False
            
    atb_ready_characters = []
