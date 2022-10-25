from classes import *
from sys import exit
import random


def laser_gun_fun(user, target):
    hp = target.hp
    target.modify_hp(-hp)

laser_gun = Item("Laser Gun", laser_gun_fun)
