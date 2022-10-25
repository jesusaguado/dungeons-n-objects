from classes import *
from events import *
from objects import *
from script import *
from sys import exit
import random

##################################################
# PARAMETERS
##################################################

INTRO = False
FAST_START = False

##################################################
# ROOMS
##################################################

chest01 = Chest("Chest 01", [laser_gun], None, None)
start_room = Room("Start room", None, [chest01], None, None)



##################################################
# MONSTERS 
##################################################

goblin = Character("Goblin", 3, 1, 1, 1, None)

cthulhu = Character("Cthulhu Lord of Darkness", 40, 15, 10, 1, None)
cthulhu.attach_event(event_end_game)

sheep = Character("Sheep", 20, 2, 2, 1, None)

monsters = [goblin, cthulhu, sheep]
#monster = random.choice(monsters)
monster = goblin

#give_frame(bobby)

##################################################
# INITIALIZE GAME
##################################################
bobby = Character("Bobby", 10, 3, 2, 1, None)
#bobby.give_item(laser_gun)
monster.give_item(laser_gun)


print("Fast start? (y/n)")
choice = input("> ")
if choice == 0:
    exit()
elif choice in yeses:
    FAST_START = True
    INTRO = False
else:
    FAST_START = False
    INTRO = False

if INTRO:
    intro()

if FAST_START:
    player = bobby
else:
    player = start_game()
    gpause()
    slow_type(welcome.format(player.name))
    gpause()

b=initiate_combat(player, monster)
post_combat(player, monster, b)

slow_type("{} may have defeated the {}, but can {} defeat {}?".format(player.name, monster.name, player.name, cthulhu.name))
npause()

a=initiate_combat(player, cthulhu)
post_combat(player, cthulhu, a)

