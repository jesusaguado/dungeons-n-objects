from sys import exit
import random

from classes import *
from game_events import *
from game_text import *
from game_objects import *
from game_map import *

##################################################
# PARAMETERS
##################################################

INTRO = False
FAST_START = False


##################################################
# INITIALIZE GAME
##################################################

print("Fast start? (y/n)")
choice = input("> ")

if choice == 0:
    exit()
elif choice in yeses:
    FAST_START = True
    INTRO = False
else:
    FAST_START = False
    INTRO = True

if INTRO:
    intro()

if FAST_START:
    player = bobby
else:
    player = start_game()
    slow_type(welcome.format(player.name))
    Npause()

# game_map is loaded from the module gamemap.py
current_room = game_map.initial_room
while True:
    current_room = current_room.enter_room(player, game_map)
    

