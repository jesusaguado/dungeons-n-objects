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
    # clear screen, works cross platforms
    os.system('cls' if os.name=='nt' else 'clear')

def fast_type(t):
    # types sequentially with set speed, 1 character at a time
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/FAST_SPEED)
    print('')

def slow_type(t):
    # types sequentially with set speed, 1 character at a time
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/TYPING_SPEED)
    print('')


def npause():
    # n- for nihil, gives a text output pause, waiting the user to "PRESS ENTER"
    # to continue playing
    input()
    
def Npause():
    # n- for nihil, gives a text output pause, waiting the user to "PRESS ENTER"
    # to continue playing. This one also clears the screen
    input()
    cls()


##############################################################
# CHARACTERS
##############################################################

class Event(object):

    def __init__(self, name, event_type, event_function, event_items = None):
        """
        Event constructor. Besides the obvious, an event must be of some
        numeric type:
            -2: event to be triggered post combat, with priority
            -1: event to be triggered post combat
             0: to be triggered while in a room
        """

        self.name = name
        self.event_type = event_type
        self.event_function = event_function

        if event_items == None:
            event_items = []

    def attach_items(self, item):
        """
        To endow an event with some item related to it. 
        """
        self.event_items.append(item)

# The basic class for NPC's and the player

class Character(object):

    def __init__(self, name, hp, atk, df, status, items = None, events = None):
        """
        Basic constructor for a character. Only interesting thing is
        .status attribute, 0 for DEAD and 1 for ALIVE
        """

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

    def check_dead(self):
        """
        Checks if character is alive. Used to check if combat has finished.
        """
        if not self.status:
            slow_type("{} died!".format(self.name))
        return not self.status

    def delete_item(self, item):
        """
        This function gets called for example when you need to delete an
        item from the inventory after using it.
        """
        items = self.items
        new_items = []
        for cycle_item in items:
            if cycle_item != item:
                new_items.append(cycle_item)
        self.items = new_items


    def print_status(self):
        """
        Basic status prompt to tell the user in-game.
        """
         
        print(bars)
        print(f"Name: {self.name}")
        print(f"HP: {self.hp} / {self.max_hp}")
        print(f"ATK: {self.atk}")
        print(f"DF: {self.df}")
        print(bars)

    def modify_hp(self,delta):
        """
        Basic HP modifier. Status alteration is done OUTSIDE of this, if
        the Character ends up DEAD.
        """
        final_health = self.hp + delta
        if final_health <= 0:
            self.status = 0
        self.hp = final_health

    def give_item(self, item, silent = False):
        """
        Pass the True optional argument to not print when some Character
        acquires an item.
        """
        self.items.append(item)
        if not silent:
            print("(!) {} obtains {}".format(self.name, item.name))

    def attach_event(self, event):
        self.events.append(event)

    def trigger_post_event(self):
        """
        Function called in post_combat function to trigger post combat
        events in order. So far events are stored forever.
        """
        for event in self.events:
            if event.event_type == -2:
                event.event_function()
            if event.event_type == -1:
                event.event_function()

class Item(object):

    def __init__(self, name, function, usage, uses, description = ""):
        """
        An item has to have 
            - name, 
            - function that CAN depend on USER and TARGET Characters
            - usage = "combat", "map", "anywhere" to determine where/when it can be used
                    Note a "map" or "anywhere" item function should only depend on USER
            - uses: an integer for how many uses remaining. Set -1 to infinity.
            - description
        """

        self.name = name
        self.function = function
        self.description = description
        self.uses = uses
        self.usage = usage

    def combat_use(self, player, foe):
        """
        Uses item in combat. Item function MUST depend on the foe.
        BUG: this prevents the use of potions in combat! Fix POTION item
        """

        if self.usage not in ["combat","anywhere"]:
            slow_type("{} cannot be used in combat!".self.name)
            return -1
        else:
            slow_type(self.name+': '+self.description)
            slow_type("{} used {}!".format(player.name, self.name))
            self.function(player,foe)
            self.check_uses_and_use(player)

    def check_uses_and_use(self, player):
        """
        This checks if item has infinite durability or finite one. If finite,
        decreases it by 1.

        This is used when using any item.
        """
        if self.uses >= 1:
            self.uses -= 1

        if self.uses == 0:
            slow_type("{} was used up...".format(self.name))
            player.delete_item(self)
        elif self.uses >=0:
            slow_type("{Can still use {} {} more time(s)".format(self.name, self.uses))


    def map_use(self, player):
        """
        Uses item in map. Item function CANNOT depend on a foe.
        """

        if self.usage not in ["map", "anywhere"]:
            slow_type("{} cannot be used here".self.name)
            return -1

        else:
            slow_type("{} used {}!".format(player.name, self.name))
            self.function(player)
            self.check_uses_and_use(player)

##############################################################
# CHESTS
##############################################################

class Chest(object):

    def __init__(self, name, content, trigger_event = None):
        """
        A chest can have:
            - content: a list of items
            - trigger_event, only 1
        """
        self.name = name
        if content == None:
            self.content = []
        else:
            self.content = content
        self.trigger_event = trigger_event

    def open_chest(self, player):
        """
        This method opens a chest and puts everything in the player's inventory.
        """
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
        """
        A map requires:
            - non-empty list of rooms
            - adjacency matrix for the graph of the rooms
            - an initial room to start the game
        """

        self.rooms = list_of_rooms
        self.adjacency_matrix = adjacency_matrix
        self.initial_room = initial_room

class Room(object):

    def __init__(self, name, description, monsters, chests, events):
        """
        A room requires:
            - name
            - description (will be printed everytime player enters room)
            - list of monsters, can be empty
            - list of chests, can be empty
            - list of events, can be empty
        """

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
        """
        Outputs a list of rooms objects adjacent to self, from Map info
        Used for selecting rooms in basic game interaction.
        """

        i=Map.rooms.index(self)
        adjacents = []
        edges = Map.adjacency_matrix[i]
        for j in range(0,len(edges)):
            if edges[j] != 0:
                adjacents.append(Map.rooms[j])
        return adjacents

    def room_header(self):
        print(bars)
        print(spaces+"{}".format(self.name.upper()))
        print(bars)

    def enter_room(self,player, gamemap):
        """
        Very important function. Enters the room selected and gives
        the main loop of the game. Takes as input a room to enter, the
        actual map, and the actual player. It scripts the game as follows:

            1. If there are monsters, combat against a random one is initiated.
                1.1 If won, monster will be deleted.
                1.2 If fled, monster will be waiting for immediate combat again.
            2. If there are no monsters, give a room overlook.
            3. Print, if any loot, a hint towards its existence.
            4. Execute the give_room_options function which gives the
                player basic interaction dialog (check status, items, move).
                The output of the give_room_options IS an adjacent room to
                move to. Give that room as output!
        
        This function will be called iteratively:
            2nd_room = 1st_room.enter()
            3rd_room = 2nd_room.enter()...

        """
        cls()
        self.room_header()
        monsters = self.monsters
        random.shuffle(monsters)

        while monsters != []:

            monster = monsters.pop()
            slow_type("{} is suddenly attacked!".format(player.name))
            npause()
            result_last_combat = initiate_combat(player, monster)
            post_combat(player, monster, result_last_combat)
            cls()

            if result_last_combat == 1:
                self.monsters = monsters
            else:
                self.monsters = monsters.append(monster)

            self.room_header()

        slow_type(self.description)
        npause()
        
        if self.chests != []:
            slow_type("(!) There might be some loot around.")
            npause()

        exited = give_room_options(player, self, gamemap)

        return exited


    
       
################################################# #
# GENERAL FUNCTIONS
################################################# #

def selector(objects, message_if_empty, prompt_confirm = True):
    """
    Abstract funtion that gives a selector dialogue.

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

        # if selected cancelling output -1
        if choice == N+1:
            print("Cancelling selection")
            npause()
            return -1

        # if selected a good possibility give confirmation, IF DESIRED, and
        # output that object

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

        # otherwise, keep looping cause selection was not okay
        else:
            slow_type('You seem to be somewhat confused... Try again!')
            npause()
            continue

def header(string):
    print(bars)
    print(spaces+"{}".format(string.upper()))
    print(bars)


def loot_corpse(winner, loser):
    """
    This gets called in post_combat function. If non-empty, will move
    all of the defeated loser's inventory to the winner.
    Funnily, it can be done to the player.
    """
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
    Npause()
    
    fast_type(title)
    fast_type(middle)
    fast_type(tittle2)
    Npause()


def start_game():
    """
    Basic function to construct player and set it.
    It returns the player as output.
    """

    cls()
    name = ""

    # user input should be sanitized even if that means more while loops...
    while len(name) == 0:
        slow_type("Insert name:")
        name = str(input("> "))
        if len(name) == 0:
            slow_type("Enter a non-empty name!")
            cls()
    creating = True


    # user input should be sanitized even if that means more while loops...
    while creating:
        slow_type("You can distribute up to {} points in HP (health points), ATK (attack) and DF (defense).".format(TOTAL_POINTS))
        slow_type("How many points in HP?")
        hp = input("> ")
        slow_type("How many points in ATK?")
        atk = input("> ")
        slow_type("How many points in DF?")
        df = input("> ")

        # check inputs are digits
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
    """
    Function used in end of game event.
    """
    cls()
    print(end)
    npause()
    # Not yet implemented
    #slow_type(spaces+"Play again? (y/n)")
    #choice = input("> ")
    #if choice in yeses:
    #    start_game()
    #else:
    #    exit()
    exit()

def game_over():
    """
    Function used when defeated in combat.
    """
    cls()
    print(gameovertext)
    choice = "no"
    if choice in yeses:
        start_game()
    else:
        exit()

def give_room_options(player, room, gamemap):
    """
    This is an infinite while loop as long as the player is in
    the room! It exits with the exit room.

    It is a very important function.
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
                if item.usage in ["anywhere", "map"]:
                    slow_type("Want to use {}? (y/n)".format(item.name))
                    choice = input("> ")
                    if choice in yeses:
                        result = item.map_use(player)
                npause()

        elif choice in ['room', 'ROOM']:
            slow_type(room.description)
            npause()

        elif choice in ['move','MOVE','door','DOOR','travel','TRAVEL']:
            slow_type("You consider where to go from here...")
            adjacents = room.give_adjacent_rooms(gamemap)
            exit_room = selector(adjacents, "You cannot go anywhere from here!", False)
            if exit_room not in [0,-1]:
                exiting_room = True
                slow_type("Moving towards {}...".format(exit_room.name.format()))
                npause()

        elif choice in ['loot','LOOT','chest','CHEST','chests','CHESTS']:
            slow_type("You look around for anything of value...")
            chest = selector(room.chests, "There is nothing to be found...", False) 
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
    """
    Basic combat function that outputs the damage done upon attack.
    It's somewhat random.
    """
    atk = attackant.atk 
    df = defendant.df
    atk_plus = int(round(atk*1.5))
    atk_minus = int(round(atk*0.5))
    rng = random.randint(atk_minus, atk_plus)
    return max(rng - df,0)


##############################################################
# COMBAT
##############################################################

def combat_header(player, foe):
    print("")
    print("     COMBAT AGAINST {}!".format(foe.name.upper()))
    print("________________________________________________________________________")
    print("{} HP: {}         vs   {} HP: {}".format(player.name.upper(), player.hp, foe.name.upper(), foe.hp))
    print("________________________________________________________________________")

def attack(attackant, defendant):
    """
    Simple wrapper around calculate_damage and .modify_hp to execute
    an attack.
    """
    damage = calculate_damage(attackant, defendant)
    defendant.modify_hp(-damage)
    slow_type("{} attacks {} and deals {} points of damage!".format(attackant.name, defendant.name, damage))

def use_item(user, target, item):
    #if item == 0:
    #    # no items
    #elif item == -1:
    #    # cancelled item selection
    if True:
        item.function(user, target)
        print("{} used {} on {}.".format(user.name, item.name, target.name))
        
def initiate_combat(player, foe):
    """
    Basic combat loop function. Outputs the result of the combat:
        - 2: for easter egg exit of combat
        - 1: for succesful defeat of foe

        If the player dies in combat the game_over event will take over
        and finish the game.

    """

    # Introduce the combat
    slow_type("{} battles {}!".format(player.name, foe.name))
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
                #use_item(player, foe, item)
                item.combat_use(player, foe)
                if foe.check_dead():
                    slow_type("{} wins!".format(player.name))
                    Npause()
                    return 1

        elif choice == "attack":
            attack(player, foe)
            if foe.check_dead():
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
            npause()
            return 1

        # not valid user input for combat option
        else:
            slow_type("This is not a valid option.")
            npause()
            continue
        
        # pause before foe's turn begins
        npause()

        # the foe attacks and the combat proceed
        attack(foe, player)

        if player.status == 0:
            print("{} has been defeated by {}.".format(player.name, foe.name))
            npause()
            game_over()

        both_alive = foe.status and player.status

        # clean pause and clear screen
        Npause()

def post_combat(player, foe, result):
    """
    Loot the corpse of a defeated foe and trigger any post-death events it
    may carry.
    """
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
