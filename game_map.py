from classes import *
from game_objects import *
import random


# First instance: two rooms, 1 with nothing, 1 with a goblin

armory_description = "An armory. There should be some weapon around..."
chest01 = Chest("Chest 01", [potions.pop()])
armory = Room('Armory', armory_description, [knight],[chest01],None)

hall_description = "A dusty old hall with nothin' much in it!"
hall = Room('Hall', hall_description, None, None, None)

living_room_description = "This living room is covered in spider web and dust, and ... chocolate chips?"
living_room = Room("Living Room", living_room_description, [sheep], None, None)


final_room_description = "This room smells like a boss fight..."
final_room = Room('Final Room', final_room_description, [golem], None, None)

rooms = [hall, armory, living_room, final_room]

for room in rooms:
    if room != final_room:
        n = random.randint(1,3)
        for i in range(1,n):
            room.monsters.append(goblins.pop())

 
adjacency_matrix = [[0,1,1,0],[1,0,0,0],[1,0,0,1],[0,0,1,1]]

game_map = Map(rooms, adjacency_matrix, hall)
