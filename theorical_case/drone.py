import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.optimize import linear_sum_assignment

'''
    Convert the list of edges into an adjacency matrix

    edges: list of edges
    n: total number of vertex in the graph
'''
def edges_to_matrix(edges, n):
    matrix = np.zeros((n, n))
    for s, d, w in edges:
        matrix[s][d] = w
        matrix[d][s] = w
    return matrix

'''
    Find all odd vertices, in other words, find all vertices with an odd number
    of input and output edges

    edges: list of edges
    n: total number of vertex in the graph
'''
def find_odd_vertices(edges, n):
    parity = np.zeros(n)
    for s, d, _ in edges:
        parity[s] += 1
        parity[d] += 1

    result = []
    for i in range(n):
        if parity[i] % 2 != 0:
            result.append(i)
    return result

'''
    Get the path from the parent list gave by dijkstra

    prev: parent list
    x: source
    path: future path
'''
def get_path(prev, x, path):
    if prev[x] == -9999:
        path.append(x)
        return path
    get_path(prev , prev[x], path)
    path.append(x)

'''
    Find the pairing between all unbalanced vertices with the minimum weight

    M: adjacency matrix
    n: total number of vertex in the graph
    odd: list of odd vertices
'''
def find_minimum_pairing(graph, n, odd):
    dist_matrix = np.full((len(odd), len(odd)), np.inf)
    prevs = [[] for _ in range(n)]

    for s in range(len(odd)):
        dist, prev = dijkstra(csgraph=graph, directed=False, \
                indices=odd[s], return_predecessors=True)
        prevs[odd[s]] = prev
        for d in range(len(odd)):
            if s != d:
                dist_matrix[s][d] = dist[odd[d]]

    row_ind, col_ind = linear_sum_assignment(dist_matrix)

    set_pairs = set()
    for i in range(len(row_ind)):
        u, v = odd[row_ind[i]], odd[col_ind[i]]
        if (u > v):
            u, v = v, u
        set_pairs.add((u, v))

    result = []
    for s, d in set_pairs:
        path = []

        get_path(prevs[s], d, path)
        result.append((s, d, dist_matrix[odd.index(s)][odd.index(d)], path))

    return result

'''
    Add artificial edges to the graph in order to eulerize it

    edges: list of edges
    n: total number of vertex in the graph
'''
def make_graph_eulerian(edges, n):
    odd = find_odd_vertices(edges, n)
    if not odd:
        return []

    M = edges_to_matrix(edges, n)
    pairs = find_minimum_pairing(M, n, odd)
    for s, d, w, path in pairs:
        edges.append((s, d, int(w)))
    return pairs

'''
    Explicit name

    u: source
    v: destination
    w: weight
    pairs: list of pairs
'''
def find_corresponding_pair(u, v, w, pairs):
    if not len(pairs):
        return None

    for i in range(len(pairs)):
        if (u == pairs[i][0] and v == pairs[i][1]) \
                or (u == pairs[i][1] and v == pairs[i][0]) and w == pairs[i][2]:
            return (pairs[i], i)
    return None

'''
    Find one of the many eulerian cycles that contains this eulerian graph

    edges: list of edges
    pairs: list of pairs
    n: total number of vertex in the graph
'''
def find_eulerian_cycle(edges, pairs, n):
    cycle = [edges[0][0]]
    res = []
    while True:
        rest = []
        for u, v, w in edges:
            pair = find_corresponding_pair(u, v, w, pairs)
            if pair:
                path, i = pair[0][3], pair[1]
            if cycle[-1] == u:
                if pair and len(path) > 2:
                    cycle.pop()
                    pairs.pop(i)
                    for x in range(len(path)):
                        cycle.append(path[x])
                else:
                    cycle.append(v)
            elif cycle[-1] == v:
                if pair and len(path) > 2:
                    cycle.pop()
                    pairs.pop(i)
                    for x in range(len(path) - 1, -1, -1):
                        cycle.append(path[x])
                else:
                    cycle.append(u)
            else:
                rest.append((u,v,w))
        if not rest:
            return cycle
        edges = rest
        if cycle[0] == cycle[-1]:
            for u, v, _ in edges:
                if u in cycle:
                    idx = cycle.index(u)
                    cycle = cycle[idx:-1] + cycle[0:idx+1]
                    break

'''
    Solve the chinese postman problem (undirected) by returning an eulerian
    cycle

    edges: list of edges
    n: total number of vertex in the graph
'''
def chinese_postman_undirected_solver(edges, n):
    pairs = make_graph_eulerian(edges, n)
    return find_eulerian_cycle(edges, pairs, n)
