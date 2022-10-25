from sys import exit
import random
import sys,time,random
import os
from script import *

##############################################################
# GAME SETTINGS
##############################################################

TOTAL_POINTS = 20 # total points to invets in hp+atk+df
TYPING_SPEED = 300 # writing speed
FAST_SPEED = 2000
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

def pinput():
    return input("\n> ")

def slow_type(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/TYPING_SPEED)
    print('')

# deprecated bc it's ugly to have the prompt everywhere
def gpause():
    input("> ")
    cls()

def spause():
    input(">")

def npause():
    input()
    
def Npause():
    input()
    cls()


##############################################################
# OBJECTS AND CLASSES
##############################################################
class Event:
    def __init__(self, name, event_type, event_function, event_items = None):
        self.name = name
        self.event_type = event_type
        # types: -1: after combat, 0: in room
        self.event_function = event_function
        if event_items == None:
            event_items = []

    def attach_items(self, item):
        self.event_items.append(item)

    def trigger(self):
        self.event_function()
        


class Character:

    def __init__(self, name, hp, atk, df, status, items = None, events = None):

        self.name = name
        self.hp = hp
        self.atk = atk
        self.df = df
        self.status = status

        if events == None:
            self.events = []
        if items == None:
            self.items = []

    def modify_hp(self,delta):
        final_health = self.hp + delta
        if final_health <= 0:
            self.status = 0
        self.hp = final_health

    def give_item(self, item):
        self.items.append(item)

    def attach_event(self, event):
        self.events.append(event)

    def trigger_post_event(self):
        for event in self.events:
            if event.event_type == -2:
                event.trigger()
            if event.event_type == -1:
                event.trigger()

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

def loot_corpse(winner, loser):
    if loser.items != []:
        for item in loser.items:
            slow_type("(!) {} obtains {} from {}!".format(winner.name, item.name, loser.name))
            winner.give_item(item)
            npause()
        loser.items = []


##############################################################
# GAME STRUCTURE FUNCTION
##############################################################
def intro():
    cls()
    fast_type(ea)
    slow_type(spaces+"PRESENTS")
    gpause()
    
    fast_type(title)
    fast_type(middle)
    fast_type(tittle2)
    gpause()


def start_game():
    cls()
    global player
    name = ""
    while len(name) == 0:
        slow_type("Insert name:")
        name = str(input("> "))
        if len(name) == 0:
            slow_type("Enter a non-empty name!")
            cls()
    creating = True
    while creating:
        slow_type("You can distribute up to {} points in HP (health points), ATK (attack) and DF (defense).".format(TOTAL_POINTS))
        slow_type("How many points in HP?")
        hp = input("> ")
        slow_type("How many points in ATK?")
        atk = input("> ")
        slow_type("How many points in DF?")
        df = input("> ")
        if hp.isdigit() and atk.isdigit() and df.isdigit():
            hp, atk, df = int(hp), int(atk), int(df)
        else:
            slow_type("Enter only positive integers! Try again...")
            Npause()
            continue
        if hp >=1 and atk >= 1 and df >= 1 and hp+atk+df <= TOTAL_POINTS:
            creating = False
            player = Character(name, hp, atk, df, 1, None)
            print("Created {}!".format(player.name))
            break
        else:
            slow_type("This is not a valid distribution. Put at least 1 point in each characteristic and do not exceed {} in total.".format(TOTAL_POINTS))
            Npause()
    return player


def end_game():
    cls()
    print(end)
    slow_type(spaces+"Play again? (y/n)")
    choice = input("> ")
    if choice in yeses:
        start_game()
    else:
        exit()

def game_over():
    cls()
    print(gameovertext)
    slow_type(spaces + "Play again? (y/n)")
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
    """
    In combat, let player select or choose items from a list.

    Outputs:
        0: if there are no items
        -1: if item selection is cancelled
    """
    items = player.items
    confirmed = False
    if items == []:
        # if there are no items, cancel
        print("{} has no items!".format(player.name))
        npause()
        return 0
        exit
        
    while not confirmed:
        slow_type("Enter number to select.")
        N = len(player.items)
        for j in range(0, N):
            print(j+1,')',items[j].name)
        print(N+1,') Cancel')
        try:
            choice = int(input("> "))
        except:
            slow_type("Enter a number!")
            continue
        if choice <= N and choice >= 1:
            slow_type("Use {}? (y/n)".format(items[choice-1].name))
            confirmation = input("> ")
            if confirmation in ["yes", "YES", "y", "Y"]:
                confirmed = True
                return items[choice-1]
            else:
                print("Cancelling item selection")
                choice = N+1
                npause()
                return -1
        elif choice == N+1:
            print("Cancelled item selection...")
            npause()
            return -1
        else:
            continue

def check_dead(character):
    if not character.status:
        slow_type("{} died!".format(character.name))
    return not character.status

##############################################################
# COMBAT
##############################################################

def combat_header(player, foe):
    print("")
    print("     COMBAT AGAINST {}!".format(foe.name.upper()))
    print("________________________________________________________________________")
    print("{} HP: {}         vs   {} HP: {}".format(player.name.upper(), player.hp, foe.name.upper(), foe.hp))
    print("________________________________________________________________________")

def attack(player, foe):
    damage = calculate_damage(player, foe)
    foe.modify_hp(-damage)
    slow_type("{} attacks {} and deals {} points of damage!".format(player.name, foe.name, damage))

def use_item(player, foe, item):
    #if item == 0:
    #    # no items
    #elif item == -1:
    #    # cancelled item selection
    if True:
        item.function(player, foe)
        print("{} used {} on {}.".format(player.name, item.name, foe.name))
        
def initiate_combat(player, foe):
    # Introduce the combat
    slow_type("{} encounters a {}!".format(player.name, foe.name))
    npause()

    both_alive = player.status and foe.status
    if not both_alive:
        slow_type("ERROR: some of the combatants is already DEAD!")
        exit()
    # main combat loop
    while both_alive:
        # clean screen and give the combat header
        cls()
        combat_header(player, foe)
        # Give the combat options
        slow_type("What should {} do? (attack/item/run)".format(player.name))
        choice = input("> ")

        # execute combat options
        if choice == "item":
            item = choose_item(player)
            if item == 0: # there are no items!
                continue
            elif item == -1: # item selection was cancelled...
                continue
            else:
                use_item(player, foe, item)
                if check_dead(foe):
                    slow_type("{} wins!".format(player.name))
                    Npause()
                    return 1

        elif choice == "attack":
            attack(player, foe)
            if check_dead(foe):
                slow_type("{} wins!".format(player.name))
                Npause()
                return 1

        elif choice == "run":
            slow_type("{} played chicken and fleed from combat!".format(player.name))
            print("DEBUG: implement fleeing consequences!")
            return 2

        # easter egg
        elif "sing" in choice:
            slow_type("{} sings {} the song of his people!".format(player.name, foe.name))
            slow_type("{} is now friends with {}. No need to combat anymore!".format(player.name, foe.name))
            spause()
            return 2

        # not valid user input for combat option
        else:
            slow_type("This is not a valid option.")
            spause()
            continue
        # pause before foe's turn begins
        npause()
        # the foe attacks if it is alive and the combat proceed
        attack(foe, player)
        if player.status == 0:
            print("{} has been defeated by {}.".format(player.name, foe.name))
            spause()
            game_over()

        both_alive = foe.status and player.status
        # clean pause and clear screen
        Npause()
        # down here we should implement exit procedure!

def post_combat(player, foe, result):
    if result == 1:
        loot_corpse(player, foe)
        if foe.events != []:
            foe.trigger_post_event() 
