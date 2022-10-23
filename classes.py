from sys import exit
import random
import sys,time,random
import os

##############################################################
# GAME SETTINGS
##############################################################

TOTAL_POINTS = 20 # total points to invets in hp+atk+df
TYPING_SPEED = 300 # writing speed
FAST_SPEED = 1000
yeses = ["yes", "YES", "Y", "y", "ok"]
noes = ["no", "NO", "n", "N"]

##############################################################
# Printing styles...
##############################################################

def cls():
    #input("> ")
    os.system('cls' if os.name=='nt' else 'clear')

def fast_type(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/FAST_SPEED)
    print('')

def slow_type(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/TYPING_SPEED)
    print('')

def gpause():
    input("> ")
    cls()

def spause():
    input(">")
    


##############################################################
# OBJECTS AND CLASSES
##############################################################

class Character:

    def __init__(self, name, hp, atk, df, status, items = None):

        self.name = name
        self.hp = hp
        self.atk = atk
        self.df = df
        self.status = status

        if items == None:
            self.items = []

    def modify_hp(self,delta):
        final_health = self.hp + delta
        if final_health <= 0:
            self.status = 0
        self.hp = final_health
    def give_item(self, item):
        self.items.append(item)

class Item:
    def __init__(self, name, function):
        self.name = name
        self.function = function

class Room(object):

    def __init__(self, name, monsters, chests, events, doors):
        self.name = name
        if monsters == None:
            self.monsters = []
        if chests == None:
            self.chests = []
        if events == None:
            self.events = []
        self.doors = doors

class Chest(object):
    def __init__(self, name, content, trigger_event, lock):
        self.name = name
        if content == None:
            self.content = []
        self.trigger_event = trigger_event
        self.lock = lock

##############################################################
# GAME STRUCTURE FUNCTION
##############################################################

def start_game():
    cls()
    global player
    slow_type("Insert name:")
    name = str(input("> "))
    creating = True
    while creating:
        slow_type("You can distribute up to {} points in HP (health points), ATK (attack) and DF (defense).".format(TOTAL_POINTS))
        slow_type("How many points in HP?")
        hp = int(input("> "))
        slow_type("How many points in ATK?")
        atk = int(input("> "))
        slow_type("How many points in DF?")
        df = int(input("> "))
        if hp >=1 and atk >= 1 and df >= 1 and hp+atk+df <= TOTAL_POINTS:
            creating = False
            player = Character(name, hp, atk, df, 1, None)
            print("Created {}!".format(player.name))
            break
        else:
            slow_type("This is not a valid distribution. Put at least 1 point in each characteristic and do not exceed {} in total.".format(TOTAL_POINTS))
    return player



def game_over():
    slow_type("You lost. Want to play again? (y/n)")
    choice = input("> ")
    if choice in yeses:
        start_game()
    else:
        exit()

def give_frame(player):
    slow_type("Select option:")
    slow_type("s: check status")
    print("c: combat random oponent")
    choice = input("> ")

    if choice == "s":
        print("==    STATUS   =====")
        print(f"Name: {player.name}")
        print(f"HP: {player.hp}")
        print(f"ATK: {player.atk}")
        print(f"DF: {player.df}")
        print("====================")
        give_frame(player)
    elif choice == "c":
        slow_type("Starting combat...")
    

def calculate_damage(attackant, defendant): 
    atk = attackant.atk 
    df = defendant.df
    atk_plus = int(round(atk*1.5))
    atk_minus = int(round(atk*0.5))
    rng = random.randint(atk_minus, atk_plus)
    return max(rng - df,0)

def choose_item(player):
    items = player.items
    confirmed = False
    while not confirmed:
        slow_type("{} has these items".format(player.name))
        N = len(player.items)
        for j in range(0, N):
            print(j+1,')',items[j].name)
        slow_type("Which item to use? (Enter number)")
        try:
            choice = int(input("> "))
        except:
            slow_type("Enter a number!")
            continue
        slow_type("Use {}? (y/n)".format(items[choice-1].name))
        confirmation = input("> ")
        if confirmation in ["yes", "YES", "y", "Y"]:
            confirmed = True
            return items[choice-1]
        else:
            continue

def check_dead(character):
    if not character.status:
        slow_type("{} died!".format(character.name))
    return not character.status

##############################################################
# COMBAT
##############################################################


def initiate_combat(player, foe):
    slow_type("{} encounters a {}".format(player.name, foe.name))
    spause()
    both_alive = player.status and foe.status
    if not both_alive:
        slow_type("ERROR: some of the combatants is already DEAD!")
        exit()
    while both_alive:
        cls()
        print("")
        print("     COMBAT AGAINST {}!".format(foe.name.upper()))
        print("________________________________________________________________________")
        print("{} HP: {}         vs   {} HP: {}".format(player.name.upper(), player.hp, foe.name.upper(), foe.hp))
        print("________________________________________________________________________")
        slow_type("What should {} do? (attack/item/run)".format(player.name))
        choice = input("> ")
        if choice == "item":
            item = choose_item(player)
            item.function(player, foe)
            if check_dead(foe):
                slow_type("{} wins!".format(player.name))
                gpause()
                break

        elif choice == "attack":
            damage = calculate_damage(player, foe)
            foe.modify_hp(-damage)
            slow_type("{} attacks {} and deals {} points of damage!".format(player.name, foe.name, damage))
            if check_dead(foe):
                slow_type("{} wins!".format(player.name))
                gpause()
                break
        elif choice == "run":
            slow_type("{} played chicken and fleed from combat!".format(player.name))
            print("DEBUG: implement fleeing consequences!")
            break
        elif "sing" in choice:
            slow_type("{} sings {} the song of his people!".format(player.name, foe.name))
            slow_type("{} is now friends with {}. No need to combat anymore!".format(player.name, foe.name))
            spause()
            break
        else:
            slow_type("This is not a valid option.")
            continue
        spause()
        # the foe attacks if it is alive and the combat proceed
        damage = calculate_damage(foe, player)
        slow_type("{} attacks {} and deals {} points of damage!".format(foe.name, player.name, damage))
        player.modify_hp(-damage)
        if player.status == 0:
            print("{} has been defeated by {}.".format(player.name, foe.name))
            spause()
            game_over()
        both_alive = foe.status and player.status
        gpause()
        # down here we should implement exit procedure!


