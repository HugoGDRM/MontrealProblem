import osmnx as ox
import networkx as nx

###REWRITE nx.eulerize()
from itertools import combinations

def get_weight(G, P):
    weight = 0
    for i in range(1, len(P)):
        weight += G[P[i-1]][P[i]][0]["weight"]
    return weight

def eulerize(G):
    if G.order() == 0:
        raise nx.NetworkXPointlessConcept("Cannot Eulerize null graph")
    if not nx.is_connected(G):
        raise nx.NetworkXError("G is not connected")
    odd_degree_nodes = [n for n, d in G.degree() if d % 2 == 1]
    G = nx.MultiGraph(G)
    if len(odd_degree_nodes) == 0:
        return G

    odd_deg_pairs_paths = [(m,
                            {n: nx.shortest_path(G, source=m, target=n)}
                            )
                           for m, n in combinations(odd_degree_nodes, 2)]

    Gp = nx.Graph()
    for n, Ps in odd_deg_pairs_paths:
        for m, P in Ps.items():
            if n != m:
                Gp.add_edge(m, n, weight=get_weight(G, P), path=P)

    best_matching = nx.Graph(list(nx.max_weight_matching(Gp)))

    for m, n in best_matching.edges():
        path = Gp[m][n]["path"]
        G.add_edges_from(nx.utils.pairwise(path))
    return G
##END_REWRITE

def make_eulerian(city):
    if not nx.is_eulerian(city):
        #Do it by hand because weight with eulerize is false
        return eulerize(city)
    return city

def get_eulerian_circuit(graph):
    return nx.eulerian_circuit(graph)

def init_graph():
    # Get the city graph (from OpenStreetMap), filter only the drive ways
    city = ox.graph_from_place('Issou, France', network_type='drive')
    city = ox.add_edge_speeds(city)
    city = ox.speed.add_edge_travel_times(city)
    for u, v in city.edges():
        city[u][v][0]["weight"] = city.get_edge_data(u, v)[0]["length"]
    return city

city = init_graph()
eulerian_city = make_eulerian(city.to_undirected())

#ox.plot_graph(eulerian_city)

eulerian_circuit = get_eulerian_circuit(eulerian_city)

length = 0
travel_time = 0
for u, v in eulerian_circuit:
    travel_time += eulerian_city[u][v][0]['travel_time']
    length += eulerian_city[u][v][0]['weight']

print("Distance:", round(length), "meters | Travel time:", round(travel_time/60), "minutes")

m = ox.plot_graph_folium(city, popup_attribute='name', tiles='openstreetmap')
m.save("test.html")

