import numpy as np

# L : list of edges
# n : number of nodes
def list_to_adj_matrix(L, n):
    M = np.zeros((n, n))
    for s, d, w in L:
        M[s][d] = w # (capacity, flux)
        M[d][s] = w # (capacity, flux)
    return M

#------------------------------------------------------------------------------
# (source, destination, capacity)
graph = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2,
5, 5), (5, 6, 9), (4, 6, 12), (3, 6, 7)]
n = 7
M = list_to_adj_matrix(graph, n)

def find_odd_vertices(M, n):
    parity = [0 for _ in range(n)]
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

print(M)
print(find_odd_vertices(M, n))
