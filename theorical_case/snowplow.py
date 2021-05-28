import numpy as np

def list_to_adj_matrix(L, n):
    M = np.full((n, n), 0)
    for s, d, w in L:
        M[s][d] = w
    return M

def find_odd_vertices(M, n):
    parity = [0] * n
    for s in range(n):
        for d in range(n):
            if M[s][d] > 0:
                parity[s] += 1
                parity[d] -= 1

    in_co, out_co = [], []
    for i in range(n):
        if parity[i] > 0:
            out_co.append(i)
        elif parity[i] < 0:
            in_co.append(i)
    return (in_co, out_co)

def find_min_distance(M, n, meet, dist):
    min, min_index = np.inf, 0

    for i in range(n):
        if dist[i] < min and meet[i] is False:
            min = dist[i]
            min_index = i

    return min_index

#dijkstra
def find_shortest_path(M, s):
    n = len(M)
    dist = [float('inf')] * n
    meet = [False] * n

    dist[s] = 0
    for curr in range(n):
        u = find_min_distance(M, n, meet, dist)
        meet[u] = True
        for v in range(n):
            if M[u][v] > 0 \
                    and meet[v] is False and dist[v] > dist[u] + M[u][v]:
                dist[v] = dist[u] + M[u][v]
    return dist

def find_minimum_pairing(M, odd):
