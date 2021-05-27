import numpy as np

# L : list of edges
# n : number of nodes
def list_to_adj_matrix(L, n):
    M = np.empty((n, n), dtype=tuple)
    for s, d, c in L:
        M[s][d] = (c, 0) # (capacity, flux)
    return M

# T : (capacity, flux)
def is_saturated(T):
    return T[0] == T[1]

#------------------------------------------------------------------------------
# Utilities
# (source, destination, capacity)
graph = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2,
5, 5), (5, 6, 9), (4, 6, 12), (3, 6, 7)]
n = 7
M = list_to_adj_list(graph, n)
#------------------------------------------------------------------------------
def bfs(M, s, t, P):
    P[s] = -1
    queue = []
    queue.append(s)
    visited = [False for _ in range(n)]

    while queue:
        curr = queue.pop(0)
        for adj in range(n):
            if M[curr][adj] is not None and not visited[adj] \
                not is_saturated(M[curr][adj]):
                P[adj] = curr
                if adj == t:
                    return True
                queue.append(adj)
                visited[adj] = True

    return False


# marking : tuple of marking list
def ford_fulkerson(M, s, t):
    rM = M.copy() # residual graph
    P = [0 for _ in range(n)]
    flux = 0

    while bfs(rM, s, t, P):
        # find alpha
        alpha = float('inf')
        v = t
        while v != s:
            u = P[v]
            if M[u][v][1] < alpha:
                alpha = M[u][v][1]
            v = u

        # update flux
        v = t
        while v != s:
            u = P[v]
            if M[u][v] is not None:
                M[u][v] = (M[u][v][0], M[u][v][1] - alpha)
            if M[v][u] is not None:
                M[v][u] = (M[v][u][0], M[v][u][1] + alpha)
            v = u

        flux += alpha

    return flux

print(M)
print(ford_fulkerson(M, 0, 6))
print(M)
