import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.sparse.csgraph import floyd_warshall
from scipy.optimize import linear_sum_assignment

def edges_to_matrix(edges, n):
    matrix = np.zeros((n, n))
    for s, d, w in edges:
        matrix[s][d] = w
    return matrix

def find_unbalanced_vertices(edges, n):
    parity = np.zeros(n)
    for s, d, _ in edges:
        parity[s] += 1
        parity[d] -= 1

    out_co, in_co = [], []
    for i in range(n):
        if parity[i] > 0:
            in_co.append((i, int(abs(parity[i]))))
        elif parity[i] < 0:
            out_co.append((i, int(abs(parity[i]))))
    return (out_co, in_co)

def get_path(prev, x, path):
    if prev[x] == -9999:
        path.append(x)
        return path
    get_path(prev , prev[x], path)
    path.append(x)

def find_minimum_pairing(graph, n, out_u, in_u):
    OUT = []
    for o, oN in out_u:
        for x in range(oN):
            OUT.append(o)
    IN = []
    for i, iN in in_u:
        for x in range(iN):
            IN.append(i)

    dist_matrix = np.full((len(OUT), len(IN)), np.inf)
    prevs = [[] for _ in range(n)]

    for s in range(len(OUT)):
        dist, prev = dijkstra(csgraph=graph, directed=True,\
                indices=OUT[s], return_predecessors=True)
        prevs[OUT[s]] = prev
        for d in range(len(IN)):
            dist_matrix[s][d] = dist[IN[d]]

    row_ind, col_ind = linear_sum_assignment(dist_matrix)

    result = []
    for i in range(len(row_ind)):
        u, v = OUT[row_ind[i]], IN[col_ind[i]]
        path = []
        get_path(prevs[u], v, path)
        result.append((u, v, dist_matrix[OUT.index(u)][IN.index(v)], path))

    return result

def make_graph_eulerian(edges, n):
    out_u, in_u = find_unbalanced_vertices(edges, n)
    if not out_u and not in_u:
        return

    M = edges_to_matrix(edges, n)
    pairs = find_minimum_pairing(M, n, out_u, in_u)
    for s, d, w, _ in pairs:
        edges.append((s, d, w))

    return pairs

def find_corresponding_pair(u, v, w, pairs):
    for i in range(len(pairs)):
        if u == pairs[i][0] and v == pairs[i][1] and w == pairs[i][2]:
            return (pairs[i], i)
    return None

def find_eulerian_cycle(edges, pairs, n):
    cycle = [edges[0][0]]
    while True:
        rest = []
        for u, v, w in edges:
            pair = find_corresponding_pair(u, v, w, pairs)
            if pair:
                path, i = pair[0][3], pair[1]
            if cycle[-1] == u:
                if pair:
                    pairs.pop(i)
                    cycle.pop()
                    for x in path:
                        cycle.append(x)
                else:
                    cycle.append(v)
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
