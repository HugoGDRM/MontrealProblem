import numpy as np

# L : list of edges
# n : number of nodes
def list_to_adj_matrix(L, n):
    M = np.empty((n,n), dtype=tuple)
    for s, d, w in L:
        M[s][d] = (w, 1)
        M[d][s] = (w, 1)
    return M

#------------------------------------------------------------------------------
# (source, destination, weight)
graph = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2, 5, 5),\
(5, 6, 7), (4, 6, 12), (3, 6, 9), (2, 1, 3), (4, 0, 4), (4, 3, 2), (1,5, 6)]
#graph = [(0,1,10),(0, 5, 4), (0,2,2), (2, 6, 8), (0,3,8),(0,4,1),(1,2,4)\
#,(3,1,10),(4,1,3),(3,2,6),(2,4,5),(4,3,2)]

n = 7
M = list_to_adj_matrix(graph, n)
#------------------------------------------------------------------------------

def find_odd_vertices(M, n):
    parity = [0] * n
    for u in range(n):
        for v in range(n):
            if u >= v:
                continue
            if M[u][v] is not None and M[u][v][0] > 0:
                parity[u] += 1
                parity[v] += 1

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

def get_path(prev, x, path):
    if prev[x] == -1:
        path.append(x)
        return path
    get_path(prev , prev[x], path)
    path.append(x)

def dijkstra(M, s):
    dist = [float('inf')] * n
    meet = [False] * n
    prev = [-1] * n

    dist[s] = 0

    for curr in range(n):
        u = min_distance(M, meet, dist)
        meet[u] = True
        for v in range(n):
            if M[u][v] is not None and  M[u][v][0] > 0 \
                    and meet[v] is False and dist[v] > dist[u] + M[u][v][0]:
                dist[v] = dist[u] + M[u][v][0]
                prev[v] = u

    paths = []
    for d in range(n):
        path = []
        get_path(prev, d, path)
        paths.append(path)

    return dist, paths

def find_minimum_pairing(odd):
    result = []
    for u in range(len(odd)):
        min = np.inf
        min_index = 0
        for v in range(len(odd)):
            if (u != v):
                dist, paths = dijkstra(M, odd[u])
                print("Paths from " + str(u))
                print(paths)
                if dist[odd[v]] < min:
                    min = dist[odd[v]]
                    min_index = v
        result.append((odd[u], odd[min_index]))


    item1 = 0
    while item1 < len(result):
            diff = True
            item2 = item1 + 1
            while item2 < len(result):
                if result[item1][0] == result[item2][1] \
                        and result[item1][1] == result[item2][0]:
                    result.pop(item2)
                    result.pop(item1)
                    break
                item2 += 1
            item1 += 1
    return result

print("---Matrix---")
print(M)
odd = find_odd_vertices(M, n)
print("---Odd-Vertices---")
print(odd)
print(find_minimum_pairing(odd))
