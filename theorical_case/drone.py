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
    result = []
    for u in range(len(odd)):
        min = np.inf
        min_index = 0
        min_dist = []
        for v in range(len(odd)):
            if (u != v):
                dist = find_shortest_path(M, odd[u])
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

def find_eulerian_cycle(edges, n):
    cycle = [edges[0][0]]
    res = []
    while True:
        rest = []
        for u, v, w in edges:
            if cycle[-1] == u:
                cycle.append(v)
                res.append((u,v,w))
            elif cycle[-1] == v:
                cycle.append(u)
                res.append((v,u,w))
            else:
                rest.append((u,v,w))
        if not rest:
            return res
        edges = rest
        if cycle[0] == cycle[-1]:
            for u, v, _ in edges:
                if u in cycle:
                    idx = cycle.index(u)
                    cycle = cycle[idx:-1] + cycle[0:idx+1]
                    break
