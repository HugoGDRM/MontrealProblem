import osmnx as ox
import networkx as nx
import numpy as np
from scipy.sparse.csgraph import dijkstra
from scipy.optimize import linear_sum_assignment
import time

def find_unbalanced_vertices(edges, n, cor_table):
    parity = np.zeros(n)
    for s, d, _ in edges:
        parity[cor_table.index(s)] += 1
        parity[cor_table.index(d)] -= 1

    out_co, in_co = [], []
    for i in range(n):
        if parity[i] > 0:
            in_co.append((cor_table[i], int(abs(parity[i]))))
        elif parity[i] < 0:
            out_co.append((cor_table[i], int(abs(parity[i]))))
    return (out_co, in_co)

def edges_to_matrix(edges, n, cor_table):
    matrix = np.zeros((n, n))
    for s, d, w in edges:
        matrix[cor_table.index(s)][cor_table.index(d)] = w
    return matrix

def find_minimum_pairing(M, n, out_u, in_u, cor_table):
    OUT = []
    for o, oN in out_u:
        for _ in range(oN):
            OUT.append(cor_table.index(o))
    IN = []
    for i, iN in in_u:
        for _ in range(iN):
            IN.append(cor_table.index(i))

    dist_matrix = np.full((len(OUT), len(IN)), np.inf)

    for s in range(len(OUT)):
        dist = dijkstra(csgraph=M, directed=True,\
                indices=OUT[s], return_predecessors=False)
        for d in range(len(IN)):
            dist_matrix[s][d] = dist[IN[d]]

    row_ind, col_ind = linear_sum_assignment(dist_matrix)

    result = []
    for i in range(len(row_ind)):
        u, v = OUT[row_ind[i]], IN[col_ind[i]]
        result.append((u, v))

    return result

def get_datas(G, s, d):
    path = nx.shortest_path(G, source=s, target=d, weight='weight')
    travel_time = 0
    weight = 0
    for i in range(1, len(path)):
        travel_time += G[path[i-1]][path[i]][0]['travel_time']
        weight += G[path[i-1]][path[i]][0]['weight']
    return {"weight": weight, "travel_time": travel_time}

def eulerize(G):
    edges = []
    cor_table = []
    for u, v in G.edges():
        if not u in cor_table:
            cor_table.append(u)
        if not v in cor_table:
            cor_table.append(v)
        edges.append((u, v, G[u][v][0]["weight"]))

    n = len(cor_table)
    out_u, in_u = find_unbalanced_vertices(edges, n, cor_table)

    if not out_u and not in_u:
        return []

    M = edges_to_matrix(edges, n, cor_table)
    pairs = find_minimum_pairing(M, n, out_u, in_u, cor_table)
    tmp = []
    for u, v in pairs:
        s, d = cor_table[u], cor_table[v]
        #Cannot add s, d if it exists multiple nodes between
        tmp.append((s, d, get_datas(G, s, d)))

    G.add_edges_from(tmp)

def init_graph(place):
    city = ox.graph_from_place(place, network_type='drive')
    city = ox.add_edge_speeds(city)
    city = ox.speed.add_edge_travel_times(city)
    connected = max(nx.strongly_connected_components(city), key=len)

    to_remove = set()
    for u, v in city.edges():
        if u not in connected:
            to_remove.add(u)
        if v not in connected:
            to_remove.add(v)
        city[u][v][0]["weight"] = city.get_edge_data(u, v)[0]["length"]
    city.remove_nodes_from(to_remove)
    return city

def convert_graph(graph):
    tmp = []

    for u, v in graph.edges():
        data = graph.get_edge_data(u, v)[0]
        tmp.append((u, v, {"weight": data["weight"], "travel_time": data["travel_time"]}))
        if data['oneway'] == False:
            tmp.append((v, u, {"weight": data["weight"], "travel_time": data["travel_time"]}))

    new_graph = nx.MultiDiGraph()
    new_graph.add_edges_from(tmp)
    return new_graph

def make_eulerian(city):
    if not nx.is_eulerian(city):
        eulerize(city)
    return city

def get_eulerian_circuit(graph):
    return nx.eulerian_circuit(graph)

def get_best_route(place):
    print("Loading map from OpenStreetMap ...")
    city = init_graph(place)
    print("Convert graph to fully directed graph ...")
    converted_graph = convert_graph(city)
    print("Apply treatment to the map ...")
    eulerian_city = make_eulerian(converted_graph)
    print("Find a path to visit all the city ...")
    eulerian_circuit = get_eulerian_circuit(eulerian_city)

    print("Generate results ...")
    length, travel_time = 0, 0
    route = []
    for u, v in eulerian_circuit:
        travel_time += eulerian_city[u][v][0]["travel_time"]
        length += eulerian_city[u][v][0]["weight"]
        route.append(u)

    return city, route, length, travel_time

city, route, length, travel_time = get_best_route("Neuville-sur-Oise, France")
ox.plot_graph_route(city, route)
