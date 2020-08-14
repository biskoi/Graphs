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
# map_file = f"{os.getcwd()}/projects/adventure/maps/test_cross.txt"
# map_file = f"{os.getcwd()}/projects/adventure/maps/test_loop.txt"
map_file = f"{os.getcwd()}/projects/adventure/maps/test_loop_fork.txt"
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
s = Stack()

def backtrack(path):
    print('backtrack called while in room', player.current_room.id)
    print(path)
    if len(path) == 0:
        return 'END'
    direction = path[-1]
    player.travel(inverse_directions[direction])
    traversal_path.append(inverse_directions[direction])
    path.pop(-1)

    unvisited = False

    for direction in visited[player.current_room.id]:
        # print(visited[player.current_room.id][direction], direction)
        if visited[player.current_room.id][direction] == '?':
            unvisited = True
    # print(unvisited)
    if unvisited == True:
        print('out of backtrack in room', player.current_room.id)
        return
    elif len(visited) == len(world.rooms):
        return
    # elif len(visited) == len(world.rooms):
    #     return
    else:
        backtrack(path)
    # # backtrack(last_move)

def bfs(path):
    print('bfs called')
    q = Queue()
    room_id = player.current_room.id
    back_path = path.copy()
    back_path = back_path[::-1]
    for i in range(len(back_path)):
        back_path[i] = inverse_directions[back_path[i]]
    q.enqueue([back_path.pop(0)])

    while q.size() > 0:
        cur_path = q.dequeue()
        cur = cur_path[-1]
        cur_room = room_id
        # inc = -1
        for direction in back_path:
            # if inc <= len(cur_path):
            nextRoom = world.rooms[cur_room].get_room_in_direction(direction)
            if nextRoom is not None:
                cur_room = nextRoom.id
                # inc += 1

        neighbors = {}
        cardinals = ['n', 's', 'w', 'e']
        for cardinal in cardinals:
            neighbor = world.rooms[cur_room].get_room_in_direction(cardinal)
            if neighbor is not None:
                neighbors[cardinal] = neighbor.id

        for key in neighbors:
            next_room = neighbors[key]
            if visited[cur_room][key] != next_room:
                # for i in range(1, abs(inc)):
                # print(back_path)
                if player.current_room.id == cur_room:
                    break
                print(neighbors)
                print(cur_room)
                print('cur path',cur_path)
                print('stack:',s.stack)
                # print(visited[cur_room], next_room)
                # print(player.current_room.id, key)
                # print(cur_path)
                for direction in back_path:
                    print(direction)
                    player.travel(direction)
                    traversal_path.append(direction)
                    q.queue = []
                return
            elif len(cur_path) == 1:
                print('asdasdasdadasd')
                return
            else:
                # might need to instantiate a counter so we can rewind through traversal path with each enqueue?
                #enqueue path where we go back twice from traversal path
                # inc -= 1
                print('new enqueue')
                new_path = cur_path.copy()
                new_path.append(cur_path[0])
                q.enqueue(new_path)

#start
visited[player.current_room.id] = {} #puts room id into visited dict as key, value is a dict of direction: room it connects to
exits = player.current_room.get_exits() # array of cardinal directions
for direction in exits:
    visited[player.current_room.id][direction] = '?'
    s.push(direction)

#stack is now [n, s, w, e]
# [n, s, w, ]

while s.size() > 0:
    # print(player.current_room.id, 'prev room id')
    # print('-------------------------')
    # print(s.stack)
    # print(visited[player.current_room.id])
    # print(traversal_path)
    direction = s.pop()
    prev_room_id = player.current_room.id
    player.travel(direction)
    traversal_path.append(direction)
    visited[prev_room_id][direction] = player.current_room.id
    # print(player.current_room.id, 'curr room id')

    if player.current_room.id not in visited:
        visited[player.current_room.id] = {inverse_directions[direction]: prev_room_id}


    exits = player.current_room.get_exits() # array of cardinal directions
    # print('exits:', exits)
    unvisited = 0

    if len(exits) > 1:
        
        for direction in exits:
            if direction not in visited[player.current_room.id]:
                visited[player.current_room.id][direction] = '?'
                unvisited += 1
                s.push(direction)
            elif visited[player.current_room.id][direction] == '?':
                unvisited += 1
                s.push(direction)

        if unvisited == 0:
            #bfs to find next unvisited node?
            traversal_path_copy = traversal_path.copy()
            # backtrack(traversal_path_copy)

            print('loc before bfs', player.current_room.id)
            bfs(traversal_path_copy)
            print('loc after bfs', player.current_room.id)
    else:
        traversal_path_copy = traversal_path.copy()
        backtrack(traversal_path_copy) #until we find a node with a ?

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
