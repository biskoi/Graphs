from graph import Graph
from util import Stack

def earliest_ancestor(ancestors, starting_node):
    g = Graph()
    verts = g.vertices
    for (parent, child) in ancestors:
        # all_ids.add(parent)
        # all_ids.add(child)
        if parent not in verts:
            g.add_vertex(parent)

        if child not in verts:
            g.add_vertex(child)

        g.add_edge(child, parent)

    #dft for path lists, compare length, use longest one
    s = Stack()
    s.push([starting_node])
    paths = []
    visited = set()

    while s.size() > 0:
        curr_path = s.pop()
        # print(curr_path)
        curr = curr_path[-1]

        neighbors = g.get_neighbors(curr)
        # print(neighbors)
        if neighbors == set():
            paths.append(curr_path)
        else:
            for each in neighbors:
                visited.add(each)
                path_copy = curr_path.copy()
                path_copy.append(each)
                s.push(path_copy)

    print('paths', paths)

    longest = 0
    item = None
    for items in paths:
        length = len(items)
        if length > longest:
            item = items
            longest = length
        elif length == longest and items[-1] < item[0]:
            item = items

    if len(item) == 1:
        return -1

    return item[-1]



# print(earliest_ancestor([(1, 3), (1, 2)], 1))

# need to swap child and parent