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
    res = []
    meet = set()
    for s, sp in out_u:
        dist, prev = dijkstra(csgraph=graph, directed=True, indices=s,\
            return_predecessors=True)

        for d, dp in in_u:
            path = []
            get_path(prev, d, path)

            if sp == dp and str(s) not in meet and str(d) not in meet:
                for i in range(sp):
                    res.append((s, d, int(dist[d]), path))
                    new_meeting = {str(s):'', str(d):''}
                    meet.update(new_meeting)

    return res

def make_graph_eulerian(edges, n):
    out_u, int_u = find_unbalanced_vertices(edges, n)
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

##############################################################################
#
#edges = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2, 5, 5),\
#(5, 6, 7), (6, 4, 12), (3, 6, 9), (2, 1, 3), (4, 0, 4), (4, 3, 2), (1, 5, 6)]
#n = 7
#
#out_u, in_u = find_unbalanced_vertices(edges, n)
#M = edges_to_matrix(edges, n)
#print("OUT", out_u)
#print("IN", in_u)
#pairs = make_graph_eulerian(edges, n)
#res = find_eulerian_cycle(edges, pairs, n)
#print(res)
