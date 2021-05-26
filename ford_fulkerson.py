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

#------------------------------------------------------------------------------
# Utilities
n = 7
pMark = np.zeros(n)
mMark = np.zeros(n)
order = [] # queue
#------------------------------------------------------------------------------
# (source, destination, capacity)
graph = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2,
5, 5), (5, 6, 9), (4, 6, 12), (3, 6, 7)]
M = list_to_adj_list(graph, n)
#------------------------------------------------------------------------------
# M : matrix representing the graph
# n : number of nodes
def find_chain(M):
    pMark[0] = 1

    end = False
    while not end:

        # front marking
        next = True
        while next:
            next = False
            for i in range(n):
                for j in range(n):
                    if M[i][j] is not None:
                        if is_saturated(M[i][j]) == 0 \
                            and pMark[i] == 1 and pMark[j] == 0:
                            pMark[j] = 1
                            order.append(j)
                            next = True

        if pMark[n - 1] or mMark[n - 1]:
            end = True

    return 0

def bfs(M):
    pMark[0] = 1
    visited = [False] * n
    queue = []
    queue.append(0)

    while not queue:

        if pMark[n - 1] or mMark[n - 1]:
            end = True

        curr = queue.pop()
        for adj in range(n):
            if M[curr][adj] is not None and not visited[adj]:
                queue.append(adj)
                visited[adj] = True
                if is_saturated(M[curr][adj]) == 0 \
                    and pMark[curr] == 1 and pMark[adj] == 0:
                    pMark[adj] = 1
                    order.append(adj)

    return 0


# marking : tuple of marking list
def update_flot():
    # find alpha
    alpha = order[0]
    for i in range(len(order) - 1):
        u, v = order[i], order[i + 1]
        residual_capacity = M[u][v][0] - M[u][v][1]
        if residual_capacity < alpha:
            alpha = residual_capacity

    for i in range(order - 1):
        M[i][i + 1][1] += alpha


#find_chain(M)
bfs(M)
print(pMark)
print(mMark)
print(order)
#print(bfs(M))
