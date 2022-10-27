from classes import *
from game_objects import *




# First instance: two rooms, 1 with nothing, 1 with a goblin

armory_description = "An armory. There should be some weapon around..."
chest01 = Chest("Chest 01", [laser_gun])
armory = Room('Armory', armory_description, [],[chest01],None)

hall_description = "A dusty old hall with nothin' much in it!"
hall = Room('Hall', hall_description, None, None, None)

final_room_description = "This room smells like a boss fight..."
final_room = Room('Final Room', final_room_description, [goblin], None, None)

rooms = [hall, final_room, armory]

adjacency_matrix = [[0,1,1],[1,0,0],[1,0,0]]

game_map = Map(rooms, adjacency_matrix, hall)
