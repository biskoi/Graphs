import random
from util import Queue

class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name, self.last_id)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(i)

        # Create friendships

        possible = []

        #add combinations to possible list
        for user in self.users:
            for i in range(user + 1, self.last_id + 1):
                if user == i:
                    continue

                possible.append([user, i])

        n = avg_friendships * self.last_id # for each user, plan to give them this many friends
        random.shuffle(possible) # randomizes so it's no longer in order, otherwise the first users would get all the friends
        # print(possible)
        for i in range(0, n // 2): # each op will make two people friends with each other, so halve the number
            self.add_friendship(possible[i][0], possible[i][1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        #bfs
        q = Queue()
        q.enqueue([user_id]) #enqueue starting node

        while q.size() > 0:
            curr_path = q.dequeue()
            node = curr_path[-1]

            if len(curr_path) > 1:
                
                if node in visited or node == user_id:
                    continue
                elif node not in visited:
                    visited[node] = curr_path
                elif len(visited[node]) > len(curr_path):
                    visited[node] = curr_path
            
            # print(self.users[node].id)

            for item in self.friendships[node]:
                path_copy = curr_path.copy()
                path_copy.append(item)
                q.enqueue(path_copy)

        avg_separation = 0

        for node in visited:
            avg_separation += len(visited[node])

        pop_percent = len(visited) / self.last_id
        
        return [pop_percent, avg_separation // len(visited), visited]


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    # print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
