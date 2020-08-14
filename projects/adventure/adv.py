from room import Room
from player import Player
from world import World
from util import Queue, Stack
from graph import Graph
import random
from ast import literal_eval
import os

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = f"{os.getcwd()}/projects/adventure/maps/test_line.txt"
map_file = f"{os.getcwd()}/projects/adventure/maps/test_cross.txt"
# map_file = f"{os.getcwd()}/projects/adventure/maps/test_loop.txt"
# map_file = f"{os.getcwd()}/projects/adventure/maps/test_loop_fork.txt"
# map_file = f"{os.getcwd()}/projects/adventure/maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

#add current room properties as a vertex first
#as a player, move in to each room
# while in that room, add current room properties as another vertex
#connect current room to previous room and vice versa
# see if this room has more rooms
#if yes, repeat
#else backtrack?

#need to log direction with each move
# 

inverse_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}
traversal_path = []
visited = {}
prev_room = None

#we only need to visit each room once, so if len of visited == graph, we're done

def traverse(direction):
    print('traversing', direction)
    player.travel(direction)
    traversal_path.append(direction)

def bfs(start_room):
    q = Queue()
    cur_room = player.current_room
    q.enqueue([[cur_room, None]])
    path = []


    while q.size() > 0:
        cur_path_dir = q.dequeue()
        cur_room = cur_path_dir[-1][0]
        exits = cur_room.get_exits()

        if cur_room.id not in visited:
            #found a room we haven't visited
            #need to translate from vertexes into cardinal directions
            # new_path = cur_path.copy()
            # print('found a room we could visit')
            # print(cur_path)
            for room_dir in cur_path_dir[:-2]:
                path.append(room_dir[1])
            q.queue = []
            return path
                
        else:
            for direction in exits:
                new_q = cur_path_dir.copy()
                vert_in_dir = world.rooms[cur_room.id].get_room_in_direction(direction)
                new_q[-1][1] = direction
                new_q.append([vert_in_dir, direction])
                q.enqueue(new_q)




while len(visited) < len(world.rooms):
# if True:

    cur_room = player.current_room
    print('start of loop location', cur_room.id)
    exits = cur_room.get_exits()

    if cur_room.id not in visited:
        visited[cur_room.id] = {}
        if prev_room is not None:
            visited[prev_room.id][inverse_directions[traversal_path[-1]]] = cur_room.id

        for direction in exits:
            if direction not in visited[cur_room.id]:
                visited[cur_room.id][direction] = '?'
        
        for direction in visited[cur_room.id]:
            if visited[cur_room.id][direction] == '?':
                traverse(direction)
                print(direction)
                break
    elif cur_room.id in visited:
        for direction in exits:
            
    else:
        #if cur room id is in visited and no unvisited
        #go to the nearest node with unvisited exits
        paths = bfs(cur_room)
        for i in paths:
            print(player.current_room.id)
            traverse(i)


print(visited)
# You are provided with a pre-generated graph consisting of 500 rooms. You are responsible for filling `traversal_path` with directions that, when walked in order, will visit every room on the map at least once.

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
