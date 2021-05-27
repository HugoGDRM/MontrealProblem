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
5, 5), (5, 6, 7), (4, 6, 12), (3, 6, 9), (2, 1, 3), (4, 0, 4), (4, 3, 2), (1,
5, 6)]
n = 7
M = list_to_adj_matrix(graph, n)

def find_odd_vertices(M, n):
    parity = [0] * n
    for u in range(n):
        for v in range(n):
            if u >= v:
                continue
            if M[u][v] > 0:
                parity[u] += 1
                parity[v] += 1

    print(parity)

    result = []
    for i in range(n):
        if parity[i] % 2 != 0:
            result.append(i)

    return result

def min_distance(M, meet, dist):
    min, min_index = np.inf, 0

    for i in range(n):
        if dist[i] < min and meet[i] is False:
            min = dist[i]
            min_index = i

    return min_index

def dijkstra(M, s, d):
    dist = [float('inf')] * n
    dist[s] = 0
    meet = [False] * n

    for curr in range(n):
        u = min_distance(M, meet, dist)
        meet[u] = True

        for v in range(n):
            #print(v)
            #print(meet)
            #print(M[u][v] > 0)
            #print(meet[v] is False)
            #print(dist[v] > dist[u] + M[u][v])
            if M[u][v] > 0 and meet[v] is False and dist[v] > dist[u] + M[u][v]:
                dist[v] = dist[u] + M[u][v]
    print("{0}: source {1}, destination {2}".format(dist[d], s, d))
    return dist[d]

def find_minimum_pairing(odd):
    result = []
    for u in range(len(odd)):
        min = np.inf
        min_index = 0
        for v in range(len(odd)):
            if (u != v):
                d = dijkstra(M, odd[u], odd[v])
                if d < min:
                    min = d
                    min_index = v
        result.append((odd[u], odd[min_index]))
    return result

print("---Matrix---")
print(M)
odd = find_odd_vertices(M, n)
print("---Odd-Vertices---")
print(odd)
print(find_minimum_pairing(odd))
