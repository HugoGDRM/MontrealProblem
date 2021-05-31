import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from scipy.sparse.csgraph import floyd_warshall

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

    in_co, out_co = [], []
    for i in range(n):
        if parity[i] > 0:
            out_co.append((i, int(abs(parity[i]))))
        elif parity[i] < 0:
            in_co.append((i, int(abs(parity[i]))))
    return (in_co, out_co)

def find_minimum_pairing(graph, n, in_u, out_u):
    dist, pred = floyd_warshall(csgraph=graph, directed=True, return_predecessors=True)
    dic_dist = {}
    for s, _ in in_u:
        tmp = []
        for d, _ in out_u:
            if dist[s][d] > 0:
                tmp.append((d, dist[s][d]))
        dic_dist[s] = tmp
    #FIXME
    pass

def make_graph_eulerian(edges, n):
    in_u, out_u = find_unbalanced_vertices(edges, n)
    if not in_u and not out_u:
        return

    M = edges_to_matrix(edges, n)
    pairs = find_minimum_pairing(M, n, in_u, out_u)
    for s, d, w, path in pairs:
        edges.append((s, d, int(w)))
    return pairs

def find_corresponding_pair(u, v, w, pairs):
    for i in range(len(pairs)):
        if u == pairs[i][0] and v == pairs[i][1] and w == pairs[i][2]:
            return pairs.pop(i)
    return None

def find_eulerian_cycle(edges, pairs, n):
    cycle = [edges[0][0]]
    while True:
        rest = []
        for u, v, w in edges:
            pair = find_corresponding_pair(u, v, w, pairs)
            if cycle[-1] == u:
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

##############################################################################

edges = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2, 5, 5),\
(5, 6, 7), (6, 4, 12), (3, 6, 9), (2, 1, 3), (4, 0, 4), (4, 3, 2), (1,5, 6)]#,\
#(3, 2, 35), (3, 2, 35), (5, 0, 23), (6, 1, 26)]
n = 7

in_odd, out_odd = find_unbalanced_vertices(edges, n)
print((in_odd, out_odd))
M = edges_to_matrix(edges, n)
find_minimum_pairing(M, n, in_odd, out_odd)
#print(pairs)

#res = find_eulerian_cycle(edges, [], n)
#print(res)
