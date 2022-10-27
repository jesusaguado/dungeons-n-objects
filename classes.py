from sys import exit
import random
from resources import *
import sys,time,random
import os

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
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.df = df
        self.status = status

        if events == None:
            self.events = []
        if items == None:
            self.items = []

    def print_status(self):
         
        print(bars)
        print(f"Name: {self.name}")
        print(f"HP: {self.hp} / {self.max_hp}")
        print(f"ATK: {self.atk}")
        print(f"DF: {self.df}")
        print(bars)

    def modify_hp(self,delta):
        final_health = self.hp + delta
        if final_health <= 0:
            self.status = 0
        self.hp = final_health

    def give_item(self, item, silent = False):
        self.items.append(item)
        if not silent:
            print("(!) {} obtains {}".format(self.name, item.name))

    def attach_event(self, event):
        self.events.append(event)

    def trigger_post_event(self):
        for event in self.events:
            if event.event_type == -2:
                event.trigger()
            if event.event_type == -1:
                event.trigger()

class Item:
    def __init__(self, name, function, description = ""):
        self.name = name
        self.function = function
        self.description = description
    




class Chest(object):
    def __init__(self, name, content, trigger_event = None):
        self.name = name
        if content == None:
            self.content = []
        else:
            self.content = content
        self.trigger_event = trigger_event

    def open_chest(self,player):
        contents = self.content
        if contents == []:
            slow_type("Chest is empty...")
            npause()
        else:
            for item in contents:
                slow_type("There is something in here!")
                player.give_item(item, False)
                npause()
        self.content = []
################################################# #
# NAVIGATION
################################################# #
class Map(object):

    def __init__(self, list_of_rooms, adjacency_matrix, initial_room):
        self.rooms = list_of_rooms
        self.adjacency_matrix = adjacency_matrix
        self.initial_room = initial_room

class Room(object):

    def __init__(self, name, description, monsters, chests, events):
        self.name = name
        self.description = description
        if monsters == None:
            self.monsters = []
        else:
            self.monsters = monsters
        if chests == None:
            self.chests = []
        else:
            self.chests = chests
        if events == None:
            self.events = []
        else:
            self.events = events

    def give_adjacent_rooms(self, Map):
        i=Map.rooms.index(self)
        adjacents = []
        edges = Map.adjacency_matrix[i]
        for j in range(0,len(edges)):
            if edges[j] != 0:
                adjacents.append(Map.rooms[j])
        return adjacents

    def enter_room(self,player, gamemap):
        cls()
        #slow_type("{} is in {}".format(player.name, self.name))
        self.room_header()
        monsters = self.monsters
        random.shuffle(monsters)
        while monsters != []:
            monster = monsters.pop()
            slow_type("{} is suddenly attack!".format(player.name))
            result_last_combat = initiate_combat(player, monster)
            post_combat(player, monster, result_last_combat)
            self.monsters = monsters
        slow_type(self.description)
        npause()
        exited = give_room_options(player, self, gamemap)
        



        return exited


    def room_header(self):
        print(bars)
        print(spaces+"{}".format(self.name.upper()))
        print(bars)
    
def header(string):
    print(bars)
    print(spaces+"{}".format(string.upper()))
    print(bars)
       
################################################# #
################################################# #



def loot_corpse(winner, loser):
    if loser.items != []:
        for item in loser.items:
            slow_type("(!) {} obtains some items from {}!".format(winner.name, loser.name))
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
            slow_type("Created {}!".format(player.name))
            Npause()
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
    #slow_type(spaces + "Play again? (y/n)")
    #choice = input("> ")
    choice = "no"
    if choice in yeses:
        start_game()
    else:
        exit()

def give_room_options(player, room, gamemap):
    """
    This is an infinite while loop as long as the player is in
    the room! It exits with the exit room.
    """
    options = ["check STATUS", "check ITEMS", "check ROOM", "MOVE", "LOOT", "HELP"]


    exiting_room = False

    while not exiting_room:
        cls()
        room.room_header()
        for option in options:
            print('-',option)
        print("")
        choice = input("> ")

        if choice in ['status','STATUS']:
            cls()
            player.print_status()
            npause()
            
        elif choice in ['item','items','ITEMS', 'ITEM']:
            slow_type("Checking your backpack...")
            npause()
            cls()
            header("items")
            item = selector(player.items, "{} has no items!".format(player.name), False)
            if item not in [0,-1]:
                slow_type(item.name+': '+item.description)
                npause()

        elif choice in ['room', 'ROOM']:
            slow_type(room.description)
            npause()

        elif choice in ['move','MOVE','door','DOOR','travel','TRAVEL']:
            slow_type("You consider where to go from here...")
            adjacents = room.give_adjacent_rooms(gamemap)
            exit_room = selector(adjacents, "You cannot go anywhere from here!", False)
            slow_type("Moving towards {}...".format(exit_room.name.format()))
            npause()
            if exit_room not in [0,-1]:
                exiting_room = True

        elif choice in ['loot','LOOT','chest','CHEST','chests','CHESTS']:
            slow_type("You look around for anything of value...")
            chest = selector(room.chests, "There is nothing to be found...") 
            if chest not in [0,-1]:
                chest.open_chest(player)

        elif choice in ['help','HELP']:
            slow_type('Help is yet to be implemented hehe')
            npause()

        else:
            slow_type('You seem to be somewhat confused... Try again!')
            npause()

    return exit_room
         
    

def calculate_damage(attackant, defendant): 
    atk = attackant.atk 
    df = defendant.df
    atk_plus = int(round(atk*1.5))
    atk_minus = int(round(atk*0.5))
    rng = random.randint(atk_minus, atk_plus)
    return max(rng - df,0)



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
            item = selector(player.items, "{} has no items!".format(player.name))
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
            npause()
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

#####################################################################


def selector(objects, message_if_empty, prompt_confirm = True):
    """
    Print out a select dialog and output the desired object selected.
    Objects are required to have .name attribute

    Outputs:
        object: the object chosen
        0: if there are no objects to select
        -1: if object selection is cancelled
    """
    confirmed = False
    if objects == []:
        # if there are no objects, cancel and print out message
        slow_type(message_if_empty)
        npause()
        return 0
        exit
        
    while not confirmed:
        slow_type("Enter number to select.")
        N = len(objects)
        for j in range(0, N):
            print(j+1,')',objects[j].name)
        print(N+1,') Cancel')
        try:
            choice = int(input("> "))
        except:
            slow_type("Enter a number!")
            continue
        if choice == N+1:
            print("Cancelling selection")
            npause()
            return -1
        elif choice <= N and choice >= 1:
            if prompt_confirm:
                slow_type("Select {}? (y/n)".format(objects[choice-1].name))
                confirmation = input("> ")
                if confirmation in ["yes", "YES", "y", "Y"]:
                    confirmed = True
                    return objects[choice-1]
            else:
                confirmed = True
                return objects[choice-1]
        else:
            continue
