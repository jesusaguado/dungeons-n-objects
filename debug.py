from sys import argv
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
player = bobby

print(argv[1])

# game_map is loaded from the module gamemap.py
if int(argv[1]) == 1:
    print("miau")
    current_room = game_map.initial_room
    while True:
        current_room = current_room.enter_room(player, game_map)
    

