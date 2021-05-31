import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

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

def edges_to_matrix(edges, n):
    matrix = np.zeros((n, n))
    for s, d, w in edges:
        matrix[s][d] = w
        matrix[d][s] = w
    return matrix

def get_path(prev, x, path):
    if prev[x] == -9999:
        path.append(x)
        return path
    get_path(prev , prev[x], path)
    path.append(x)

def find_minimum_pairing(graph, n, odd):
    result = []
    for u in range(len(odd)):
        min = np.inf
        min_index = 0
        min_dist = []
        min_path = []
        for v in range(len(odd)):
            if (u != v):
                dist, prev = dijkstra(csgraph=graph, directed=False, \
                        indices=odd[u], return_predecessors=True)
                paths = []
                for d in range(n):
                    path = []
                    get_path(prev, d, path)
                    paths.append(path)

                if dist[odd[v]] < min:
                    min = dist[odd[v]]
                    min_path = paths[odd[v]]
                    min_index = v
                    min_dist = dist
        result.append((odd[u], odd[min_index], min_dist[odd[min_index]], min_path))

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

def make_graph_eulerian(edges, n):
    odd = find_odd_vertices(edges, n)
    if not odd:
        return

    M = edges_to_matrix(edges, n)
    pairs = find_minimum_pairing(M, n, odd)
    for s, d, w, path in pairs:
        edges.append((s, d, int(w)))
    return pairs

def find_corresponding_pair(u, v, w, pairs):
    for i in range(len(pairs)):
        if (u == pairs[i][0] and v == pairs[i][1]) \
                or (u == pairs[i][1] and v == pairs[i][0]) and w == pairs[i][2]:
            return pairs.pop(i)
    return None

def find_eulerian_cycle(edges, pairs, n):
    cycle = [edges[0][0]]
    res = []
    while True:
        rest = []
        for u, v, w in edges:
            path = find_corresponding_pair(u, v, w, pairs)
            if path:
                path = path[3]
            if cycle[-1] == u:
                if path and len(path) > 2:
                    cycle.pop()
                    for x in path:
                        cycle.append(x)
                else:
                    cycle.append(v)
            elif cycle[-1] == v:
                if path and len(path) > 2:
                    cycle.pop()
                    for x in path:
                        cycle.append(x)
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

edges = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2, 5, 5),\
(5, 6, 7), (6, 4, 12), (3, 6, 9), (2, 1, 3), (4, 0, 4), (4, 3, 2), (1, 5, 6)]
n = 7
pairs = make_graph_eulerian(edges, n)
res = find_eulerian_cycle(edges, pairs, n)
print(res)
