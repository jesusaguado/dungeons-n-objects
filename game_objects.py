from classes import *
from game_events import *

##################################################
# MONSTERS 
##################################################
bobby = Character("Bobby", 10, 3, 2, 1, None)


goblin = Character("Goblin", 3, 1, 1, 1, None)
goblin.attach_event(event_end_game)

cthulhu = Character("Cthulhu Lord of Darkness", 40, 15, 10, 1, None)
cthulhu.attach_event(event_end_game)

sheep = Character("Sheep", 20, 2, 2, 1, None)

##################################################
# ITEMS
##################################################

def laser_gun_fun(user, target):
        hp = target.hp
        target.modify_hp(-hp)

laser_gun = Item("Laser Gun", laser_gun_fun, "A laser gun that instantly kills anything!")

#bobby.give_item(laser_gun, True)
