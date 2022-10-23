from sys import exit
import random

class Item:
    def __init__(self, name, function):
        self.name = name
        self.function = function

class Room(object):

    def __init__(self, name, monsters, loots, events):
        self.name = name
        if monsters == None:
            self.monsters = []
        if chests == None:
            self.chests = []
        if events == None:
            self.events = []


class Character:

    def __init__(self, name, hp, atk, df, status, items = None):

        self.name = name
        self.hp = hp
        self.atk = atk
        self.df = df
        self.status = status

        if items == None:
            self.items = []

    def modify_hp(self,delta):
        final_health = self.hp + delta
        if final_health <= 0:
            self.status = 0
        self.hp = final_health
    def give_item(self, item):
        self.items.append(item)


def game_over():
    print("You lost. Want to play again? (y/n)")
    print("ERROR: not yet implemented :(")

def give_frame(player):
    print("Select option:")
    print("s: check status")
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
        print("Starting combat...")
    

def calculate_damage(attackant, defendant):
    atk = attackant.atk
    df = defendant.df
    rng = random.randint(1,max(1,atk))
    return max(rng - df,0)

def choose_item(player):
    items = player.items
    confirmed = False
    while not confirmed:
        print("{} has these items".format(player.name))
        N = len(player.items)
        for j in range(0, N):
            print(j+1,')',items[j].name)
        print("Which item to use? (Enter number)")
        try:
            choice = int(input("> "))
        except:
            print("Enter a number!")
            continue
        print("Use {}? (y/n)".format(items[choice-1].name))
        confirmation = input("> ")
        if confirmation in ["yes", "YES", "y", "Y"]:
            confirmed = True
            return items[choice-1]
        else:
            continue

def check_dead(character):
    if not character.status:
        print("{} died!".format(character.name))
    return not character.status



def initiate_combat(player, foe):
    print("{} encounters a {}".format(player.name, foe.name))
    both_alive = player.status and foe.status
    if not both_alive:
        print("ERROR: some of the combatants is already DEAD!")
        exit
    while both_alive:
        print("What should {} do? (attack/item/run)".format(player.name))
        choice = input("> ")
        if choice == "item":
            item = choose_item(player)
            item.function(player, foe)
            if check_dead(foe):
                print("{} wins!".format(player.name))
                break

        elif choice == "attack":
            damage = calculate_damage(player, monster)
            foe.modify_hp(-damage)
            print("{} attacks {} and deals {} points of damage!".format(player.name, foe.name, damage))
            if check_dead(foe):
                print("{} wins!".format(player.name))
                break
        elif choice == "run":
            print("{} played chicken and fleed from combat!".format(player.name))
            break
        else:
            print("This is not a valid option.")
            continue
        # the foe attacks if it is alive and the combat proceed
        damage = calculate_damage(foe, player)
        print("{} attacks {} and deals {} points of damage!".format(foe.name, player.name, damage))
        player.modify_hp(-damage)
        if player.status == 0:
            print("{} has been defeated by {}".format(player.name, foe.name))
            game_over()
            break
        else:
            both_alive = foe.status and player.status


##################################################
def laser_gun_fun(user, target):
    hp = target.hp
    target.modify_hp(-hp)

laser_gun = Item("Laser Gun", laser_gun_fun)

bobby = Character("Bobby", 10, 3, 2, 1, None)
bobby.give_item(laser_gun)

deep = Character("Deep", 3, 1, 1, 1, None)
cthulhu = Character("Cthulhu Lord of Darkness", 100, 10, 10, 1, None)
sheep = Character("Sheep", 20, 2, 2, 1, None)

monsters = [deep, cthulhu, sheep]
monster = random.choice(monsters)

give_frame(bobby)


initiate_combat(bobby, monster)
