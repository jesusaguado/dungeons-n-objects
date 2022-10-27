from classes import *
from game_events import *
import random

##################################################
# MONSTERS 
##################################################
bobby = Character("Bobby", 10, 3, 2, 1, None)

knight = Character("Forgotten Knight", 2, 4, 1, 1, None)

cthulhu = Character("Cthulhu Lord of Darkness", 40, 15, 10, 1, None)
cthulhu.attach_event(event_end_game)

sheep = Character("Sheep", 20, 2, 2, 1, None)

golem = Character("Golem", 20, 3, 5, 1, None)
golem.attach_event(event_end_game)

##################################################
# ITEMS
##################################################

def potion_fun(power):
    def concrete_potion(user):
        hp = user.hp
        max_hp = user.max_hp
        delta = max_hp - hp
        healing = min(delta, power)
        user.modify_hp(healing)
        slow_type("{} healed {} HP!".format(user.name, healing))
    return concrete_potion

potions = []
for i in range(0,100):
    potions.append(Item("Health Potion", potion_fun(3), "anywhere", 1, "A potion that heals 3 HP."))

def laser_gun_fun(user, target):
    hp = target.hp
    target.modify_hp(-hp)

def sword_fun(user, target):
    atk = user.atk
    user.atk = atk + 5
    attack(user, target)
    user.atk = atk

sword = Item("Sword", sword_fun, "combat", -1, "A sword that deals +5 atk in combat.")

laser_gun = Item("Laser Gun", laser_gun_fun, "combat", -1, "A laser gun that instantly kills anything!")

#bobby.give_item(laser_gun, True)
#bobby.give_item(potion, True)
knight.give_item(sword, True)
bobby.give_item(potions.pop(), True)

goblins = []
for i in range(0,30):
    hp_goblin = random.randint(2,8)
    atk_goblin = random.randint(1,4)
    goblin = Character("Goblin", hp_goblin, atk_goblin, 1, 1, None)
    if atk_goblin % 3 == 0:
        goblin.give_item(potions.pop(), True)
    goblins.append(goblin)
