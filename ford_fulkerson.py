import numpy as np

# L : list of edges
# n : number of nodes
def list_to_adj_list(L, n):
    M = np.empty((n, n), dtype=tuple)
    for s, d, c in L:
        M[s][d] = (c, 0) # (capacity, flux)
    return M

# T : (capacity, flux)
def is_saturated(T):
    return T[0] == T[1]

# M : matrix representing the graph
def find_chain(M, n):
    pMark = np.zeros(n)
    mMark = np.zeros(n)

    pmark[0] = 1

    next = True
    while next:
        next = False




# (source, destination, capacity)
graph = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2,
5, 5), (5, 6, 9), (4, 6, 12), (3, 6, 7)]

print(list_to_adj_list(graph, 7))
