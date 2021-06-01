import osmnx as ox
import networkx as nx

def make_eulerian(city):
    if not nx.is_eulerian(city):
        #Do it by hand because weight with eulerize is false
        return nx.eulerize(city)
    return city

def get_eulerian_circuit(graph):
    return nx.eulerian_circuit(graph)

def init_graph():
    # Get the city graph (from OpenStreetMap), filter only the drive ways
    city = ox.graph_from_place('Issou, France', network_type='drive')
    for u, v in city.edges():
        city[u][v][0]["weight"] = city.get_edge_data(u, v)[0]["length"]
    return city

city = init_graph()
eulerian_city = make_eulerian(city.to_undirected())

for u, v in eulerian_city.edges():
    print(eulerian_city[u][v][0])

ox.plot_graph(eulerian_city)

eulerian_circuit = get_eulerian_circuit(eulerian_city)
for e in eulerian_circuit:
    print(e)
