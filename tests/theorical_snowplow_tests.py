import os,sys,inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import theorical_case.snowplow as snowplow

def test_function(name, edges, n, exp):
    pairs = snowplow.make_graph_eulerian(edges, n)
    #print("PAIRS", pairs)
    res = snowplow.find_eulerian_cycle(edges, pairs, n)
    #print("RES", res)
    if res == exp:
        print("OK --", name)
    else:
        print("KO --", name)

#TEST_1 OK
edges = [(0, 1, 10), (0, 2, 10), (1, 3, 7), (1, 4, 4), (2, 3, 5), (2, 5, 5),\
        (5, 6, 7), (4, 6, 12), (3, 6, 9), (2, 1, 3), (4, 0, 4), (4, 3, 2)\
        ,(1,5, 6), (6, 1, 4)]
n = 7
exp = [0, 1, 3, 6, 1, 4, 6, 1, 4, 0, 2, 3, 6, 1, 4, 0, 2, 5, 6, 1, 4, 3, 6, 1,\
        4, 0, 2, 1, 5, 6, 1, 4, 0]

test_function("TEST_1", edges, n, exp)

#TEST_2 KO
edges = [(0,1,10),(0, 5, 4), (0,2,2), (2, 6, 8), (0,3,8),(0,4,1),(1,2,4)\
        ,(3,1,10),(4,1,3),(3,2,6),(2,4,5),(4,3,2), (6, 0, 4), (5, 4, 8)]
exp = []
n = 7

#test_function("TEST_2", edges, n, exp)

#TEST_4 KO
edges = [(0, 1, 2), (1, 2, 1), (2, 3, 7), (3, 7, 9), (7, 5, 4), (5, 6, 10)\
        ,(5, 4, 9), (4, 0, 8), (0, 5, 6), (2, 8, 5), (2, 4, 15), (8, 6, 12),\
        (6, 7, 5)]
exp = []
n = 9

#test_function("TEST_4", edges, n, exp)

#TEST_5 OK
edges = [(0, 1, 2), (1, 2, 1), (2, 3, 7), (3, 7, 9), (7, 5, 4), (5, 6, 10)\
        ,(5, 4, 9), (4, 0, 8), (0, 5, 6), (2, 8, 5), (2, 4, 15), (8, 6, 12)\
        ,(5, 9, 5), (9, 6, 5), (6, 7, 5)]

exp = [0, 1, 2, 3, 7, 5, 6, 7, 5, 4, 0, 5, 9, 6, 7, 5, 4, 0, 1, 2, 8, 6, 7, 5,\
        4, 0, 1, 2, 4, 0]
n = 10

test_function("TEST_5", edges, n, exp)

#TEST_6 KO
edges = [(0, 1, 2), (1, 2, 1), (2, 3, 7), (3, 7, 9), (7, 5, 4), (5, 6, 10)\
        ,(5, 4, 9), (4, 0, 8), (0, 5, 6), (2, 8, 5), (2, 4, 15), (8, 6, 12)\
        ,(5, 9, 5), (9, 6, 5), (10, 1, 3), (0, 10, 2), (6, 7, 5)]

exp = []

n = 11

#test_function("TEST_6", edges, n, exp)

#TEST_7 KO
edges = [(0, 1, 6), (1, 7, 11), (7, 5, 9), (5, 6, 12), (6, 4, 6), (4, 2, 4)\
        ,(2, 0, 7), (1, 3, 8), (3, 2, 3), (3, 4, 5), (3, 6, 7), (3, 5, 14)]

exp = []

n = 8

#test_function("TEST_7", edges, n, exp)
