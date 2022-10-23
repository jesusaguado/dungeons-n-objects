from classes import *
from objects import *
from script import *
from sys import exit
import random


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

#cls()
#initiate_combat(bobby, cthulhu)
#
#exit

cls()
fast_type(ea)
slow_type("                    PRESENTS")
gpause()

fast_type(title)
fast_type(middle)
fast_type(tittle2)
gpause()

player = start_game()
gpause()
slow_type(welcome.format(player.name))
gpause()
initiate_combat(player, monster)

slow_type("{} may have defeated the {}, but can {} defeat {}?".format(player.name, monster.name, player.name, cthulhu.name))
gpause()

initiate_combat(player, cthulhu)
