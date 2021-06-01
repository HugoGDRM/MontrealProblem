import osmnx as ox
import networkx as nx

def make_eulerian(city):
    if not nx.is_eulerian(city):
        return nx.eulerize(city)
    return city

def get_eulerian_circuit(graph):
    return nx.eulerian_circuit(graph, keys=True)

def init_graph():
    # Get the city graph (from OpenStreetMap), filter only the drive ways
    return ox.graph_from_place('Issou, France', network_type='drive')

city = init_graph()
# Display the graph
ox.plot_graph(city)
eulerian_city = make_eulerian(city.to_undirected())
ox.plot_graph(eulerian_city)

eulerian_circuit = get_eulerian_circuit(eulerian_city)
for e in eulerian_circuit:
    print(e)
