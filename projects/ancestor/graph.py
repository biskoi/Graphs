"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy

# ```python
# {
#     '0': {'1', '3'},
#     '1': {'0'},
#     '2': set(),
#     '3': {'0'}
# }
# ```

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()
        # pass  # TODO

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        # pass  # TODO

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        # pass  # TODO
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # pass  # TODO

        # create an empty queue, put starting vertex in queue

        bft_queue = Queue()
        bft_queue.enqueue(starting_vertex)

        #create a set to store the visited vertices

        visited = set()
        
        #while queue is not empty
        while bft_queue.size() > 0:
            curr = bft_queue.dequeue()
            #dequeue vertex 1
            print(curr)

            #if vertex has not been visited
            if curr not in visited:
                visited.add(curr)
                #mark as visited
                #print for debug

                #add all of its neighbors to the queue
                for neighbor in self.get_neighbors(curr):
                    if neighbor not in visited:
                        bft_queue.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        dft_stack = Stack()
        dft_stack.push(starting_vertex)

        #create a set to store the visited vertices

        visited = set()
        
        #while queue is not empty
        while dft_stack.size() > 0:
            curr = dft_stack.pop()
            #dequeue vertex 1

            #if vertex has not been visited
            if curr not in visited:
                visited.add(curr)
                print(curr)
                #mark as visited
                #print for debug

                #add all of its neighbors to the queue
                for neighbor in self.get_neighbors(curr):
                    if neighbor not in visited:
                        dft_stack.push(neighbor)
        # pass  # TODO

    def dft_recursive(self, starting_vertex, visited = None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """

        if visited is None:
            visited = set()

        visited.add(starting_vertex)
        print(starting_vertex)
        
        neighbors = self.get_neighbors(starting_vertex)
        if len(neighbors) == 0:
            return
        for item in neighbors:
            if item not in visited:
                self.dft_recursive(item, visited)



    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breadth-first order.
        """

        #create empty queue and enqeueue PATH to the starting vertex ID
        q = Queue()
        q.enqueue([starting_vertex])
        #create a set to store visited
        visited = set()

        #while queue isnt empty:
        while q.size() > 0:
            #dequeue the first path
            path = q.dequeue()
            #get last vertex in that path (list[-1:])
            curr = path[-1]
            
            #if not visited:
            if curr not in visited:
                #check if it's the target
                if curr == destination_vertex:
                    #if yes, return the path to this vertex
                    return path

                #mark as visited
                visited.add(curr)

                #add paths to its neighbors to the back of the queue
                # for a vert with 2 neighbors, two paths/lists will be added
                for neighbors in self.get_neighbors(curr):
                    path_copy = path.copy()
                    path_copy.append(neighbors)
                    q.enqueue(path_copy)

                #make a copy of the path
                # append the neighbor to the back of the path
                # enqueue out new path

        return None


    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        s.push([starting_vertex])

        visited = set()

        while s.size() > 0:
            path = s.pop()
            curr = path[-1]

            if curr not in visited:
                if curr == destination_vertex:
                    return path

                visited.add(curr)

                for neighbors in self.get_neighbors(curr):
                    path_copy = path.copy()
                    path_copy.append(neighbors)
                    s.push(path_copy)
                
        return None

        # pass  # TODO

    def dfs_recursive(self, starting_vertex, destination_vertex, visited = None, path = None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if visited is None and path is None:
            visited = set()
            path = [starting_vertex]

        curr = path[-1]

        if curr == destination_vertex:
            # print(path)
            return path

        if curr not in visited:
            
            visited.add(curr)

            neighbors = self.get_neighbors(curr)
            # if len(neighbors) == 0:
            #     return

            for item in neighbors:
                path_copy = path.copy()
                path_copy.append(item)
                self.dfs_recursive(item, destination_vertex, visited, path_copy)

        return path
        


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    # print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    # graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    # graph.dft(1)
    # graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    # print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    # print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
