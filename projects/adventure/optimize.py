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
# map_file = f"{os.getcwd()}/projects/adventure/maps/test_loop_fork.txt"
map_file = f"{os.getcwd()}/projects/adventure/maps/main_maze.txt"

# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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



a = [0,1,2,3,4,5]
print(a[:-2])

#we only need to visit each room once, so if len of visited == graph, we're done

def traverse(direction):
    global prev_room
    prev_room = player.current_room
    print('traversing', direction)
    player.travel(direction)
    traversal_path.append(direction)

def bfs(start_room):
    q = Queue()
    cur_room = player.current_room
    last_move = traversal_path[-1]
    print(f'bfs invoked in room {cur_room.id}')
    #enqueue the current room object, and the path taken to get to that room from player's current room
    q.enqueue([cur_room, None])



    while q.size() > 0:
        cur_path_dir = q.dequeue()
        cur_room = cur_path_dir[0]
        cur_path = cur_path_dir[1]
        exits = cur_room.get_exits()

        print(cur_path)
        print(f'current length of visited: {len(visited)}')

        if cur_room.id not in visited:
            #found a room we haven't visited
            print(f'cur path dir: {cur_path_dir}')
            # path = []
            # for room_dir in cur_path_dir[:-1]:
            #     if room_dir[1] is not None:
            #         path.append(room_dir[1])
            print(f'{cur_room.id} not in visited, need to go there. we are at {player.current_room.id}')
            print(f'return path {cur_path}')
            return cur_path
                
        else:
            for direction in exits:
                #this part is fucked
                vert_in_dir = world.rooms[cur_room.id].get_room_in_direction(direction)
                new_path = None
                if cur_path is None:
                    new_path = []
                else:
                    new_path = cur_path.copy()

                new_path.append(direction)

                new_q = [vert_in_dir, new_path]
                q.enqueue(new_q)

def dfs(start_room):
    s = Stack()
    cur_room = start_room
    last_move = traversal_path[-1]
    print(f'dfs invoked in room {cur_room.id}')
    #enqueue the current room object, and the path taken to get to that room from player's current room
    s.push([cur_room, None])

    #need to stop dfs from going back to the room it just came from and repeating [n, s, n, s, n, s, etc]

    while s.size() > 0:
        cur_path_dir = s.pop()
        cur_room = cur_path_dir[0]
        cur_path = cur_path_dir[1]
        exits = cur_room.get_exits()

        print(cur_path)
        print(f'current length of visited: {len(visited)}')

        if cur_room.id not in visited:
            #found a room we haven't visited
            print(f'cur path dir: {cur_path_dir}')
            # path = []
            # for room_dir in cur_path_dir[:-1]:
            #     if room_dir[1] is not None:
            #         path.append(room_dir[1])
            print(f'{cur_room.id} not in visited, need to go there. we are at {player.current_room.id}')
            print(f'return path {cur_path}')
            return cur_path
                
        else:
            for direction in exits:
                #this part is fucked
                if len(exits) > 1:
                #if direction NOT where we just came from
                    if direction != cur_path[-1]:
                        vert_in_dir = world.rooms[cur_room.id].get_room_in_direction(direction)
                        new_path = None
                        if cur_path is None:
                            new_path = []
                        else:
                            new_path = cur_path.copy()

                        new_path.append(direction)

                        new_s = [vert_in_dir, new_path]
                        s.push(new_s)
                else:
                    #we hit a 1 room dead end, go back one
                    return dfs(cur_room)




# while len(visited) > len(world.rooms):
while len(visited) < len(world.rooms):
# if True:
    
    cur_room = player.current_room
    print(f'start of loop at location {cur_room.id}---------------------------------------------------------')
    print(f'current length of visited: {len(visited)}')
    exits = cur_room.get_exits()
    has_unvisited = []
    # print(exits)


    if cur_room.id not in visited:
        print(f'room {cur_room.id} not in visited')
        print(f'room has exits to: {exits}')
        #if current room not in visited,
        #connect this room to previous room
        #for exits in this room, if not already in visited[cur room], add them as '?'
        #travel to the first exit with a '?'
        #go to next loop
        visited[cur_room.id] = {}
        print(f'prev room is {prev_room}')
        if prev_room is not None:
            print(f'linked this room to prev room')
            visited[cur_room.id][inverse_directions[traversal_path[-1]]] = prev_room.id
            visited[prev_room.id][traversal_path[-1]] = cur_room.id

            

        for direction in exits:
            if direction not in visited[cur_room.id]:
                visited[cur_room.id][direction] = '?'
        print(f'data in visited dict at this room: {visited[cur_room.id]}')
        
        for direction in visited[cur_room.id]:
            if visited[cur_room.id][direction] == '?':
                traverse(direction)
                break
        
        continue
    elif cur_room.id in visited:
        print(f'{cur_room.id} is already in visited')
        # print(f'prev room: {prev_room.id}')
        # print(visited[cur_room.id])
        #if we've been here before
        #make sure we link prev room
        #are there any unexplored exits?
        #if yes, go check it out
        if prev_room is not None:
            # print('setting prev room')
            visited[prev_room.id][traversal_path[-1]] = cur_room.id
            visited[cur_room.id][inverse_directions[traversal_path[-1]]] = prev_room.id


        for direction in exits:
            if visited[cur_room.id][direction] == '?':
                has_unvisited.append(direction)

        if len(has_unvisited) > 0:
            print(f'traversing to unvisited direction {has_unvisited[0]}')
            traverse(has_unvisited[0])
        elif len(has_unvisited) == 0 and len(visited) < 300:
            print(f'invoking bfs')
            #we've been here and there are no unvisited paths
            paths = bfs(cur_room)
            for i in paths:
                print(player.current_room.id)
                traverse(i)
        elif len(has_unvisited) == 0 and len(visited) >= 300:
            print(f'invoking dfs')
            paths = dfs(cur_room)
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
