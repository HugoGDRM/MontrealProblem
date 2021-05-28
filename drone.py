import numpy as np

def list_to_adj_matrix(L, n):
    M = np.full((n,n), 0)
    for s, d, w in L:
        M[s][d] = w
        M[d][s] = w
    return M

def find_odd_vertices(M, n):
    parity = [0] * n
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

def find_min_distance(M, meet, dist):
    min, min_index = np.inf, 0

    for i in range(n):
        if dist[i] < min and meet[i] is False:
            min = dist[i]
            min_index = i

    return min_index

#dijkstra
def find_shortest_path(M, s):
    dist = [float('inf')] * n
    meet = [False] * n

    dist[s] = 0

    for curr in range(n):
        u = find_min_distance(M, meet, dist)
        meet[u] = True
        for v in range(n):
            if M[u][v] > 0 \
                    and meet[v] is False and dist[v] > dist[u] + M[u][v]:
                dist[v] = dist[u] + M[u][v]

    return dist

def find_minimum_pairing(M, odd):
    result = []
    for u in range(len(odd)):
        min = np.inf
        min_index = 0
        min_dist = []
        for v in range(len(odd)):
            if (u != v):
                dist = find_shortest_path(M, odd[u])
                print(odd[u])
                print(odd[v])
                print(dist)
                if dist[odd[v]] < min:
                    min = dist[odd[v]]
                    min_index = v
                    min_dist = dist
        result.append((odd[u], odd[min_index], min_dist[odd[min_index]]))

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

def make_graph_eulerian(graph, n):
    M = list_to_adj_matrix(graph, n)
    odd = find_odd_vertices(M, n)
    if not odd:
        return

    pairs = find_minimum_pairing(M, odd)
    return graph + pairs



# L : list of edges
# n : number of nodes
#------------------------------------------------------------------------------
# (source, destination, weight)
graph = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2, 5, 5),\
(5, 6, 7), (4, 6, 12), (3, 6, 9), (2, 1, 3), (4, 0, 4), (4, 3, 2), (1,5, 6)]
#graph = [(0,1,10),(0, 5, 4), (0,2,2), (2, 6, 8), (0,3,8),(0,4,1),(1,2,4)\
#,(3,1,10),(4,1,3),(3,2,6),(2,4,5),(4,3,2)]
n = 7
#------------------------------------------------------------------------------

print("---Eulerian-graph---")
print(make_graph_eulerian(graph, n))

