import sys
sys.path.append("../theorical_case/")

import drone

edges1 = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2, 5, 5),\
(5, 6, 7), (4, 6, 12), (3, 6, 9), (2, 1, 3), (4, 0, 4), (4, 3, 2), (1,5, 6)]

edge2 = [(0,1,10),(0, 5, 4), (0,2,2), (2, 6, 8), (0,3,8),(0,4,1),(1,2,4)\
,(3,1,10),(4,1,3),(3,2,6),(2,4,5),(4,3,2)]

#--------------------------------------------------------------------------------
L = [edge1, edge2]

def create_cycle(cycle):
    path = []
    for i in range(len(cycle) - 1):
        path.append((cycle[i], cycle[i + 1]))
    return path

def same(a, b):
    return a == b or (a[0] == b[1] and a[1] == b[0])

def is_eulerian_cycle(edges, cycle):
    if not len(cycle):
        return len(edges) == 0

    copy = edges.copy()
    path = create_cycle(cycle)
    last = (cycle[0], cycle[-1])

    for x in path:
        for y in copy:
            if same(x, y):
                copy.remove(y)

    return len(copy) == 1 and same(copy[0], last)

def test_suite():
    for edges in L:
        print(is_eulerian_cycle(drone.find_eulerian_cycle(drone.make_graph_eulerian(edges,7))))
