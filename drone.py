import numpy as np

# L : list of edges
# n : number of nodes
def list_to_adj_matrix(L, n):
    M = np.full((n,n), 0)
    for s, d, w in L:
        M[s][d] = w # (capacity, flux)
        M[d][s] = w # (capacity, flux)
    return M

#------------------------------------------------------------------------------
# (source, destination, weight)
graph = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2,
5, 5), (5, 6, 9), (4, 6, 12), (3, 6, 7), (2, 1, 3), (4, 0, 4), (4, 3, 2)]
n = 7
M = list_to_adj_matrix(graph, n)

def find_odd_vertices(M, n):
    parity = np.full(n, 0)
    for u in range(n):
        for v in range(n):
            if u >= v:
                continue
            if M[u][v] > 0:
                parity[u] += 1
                parity[v] += 1

    result = []
    for i in range(n):
        if parity[i] % 2 != 0:
            result.append(i)

    return result

def min_distance(M, meet, dist):
    min, min_index = np.inf, 0

    for i in range(len(dist)):
        if dist[i] < min and meet[i] is False:
            min = dist[i]
            min_index = i

    return min_index

def dijkstra(M, s, d):
    dist = np.full(n, np.inf)
    dist[s] = 0
    meet = np.full(n, False)

    for curr in range(n):
        u = min_distance(M, meet, dist)
        meet[u] = True

        for v in range(n):
            if u != v and meet[v] is False and dist[v] > dist[u] + M[u][v]:
                dist[v] = dist[u] + M[u][v]

    print(dist)

    return dist[d]

def find_minimum_pairing(odd):
    result = []
    for u in range(len(odd)):
        min = np.inf
        for v in range(len(odd)):
            d = dijkstra(M, odd[u], odd[v])
            if d < min:
                min = d
        result.append((odd[u], odd[v]))

    return result

odd = find_odd_vertices(M, n)
print(odd)
print(find_minimum_pairing(odd))
