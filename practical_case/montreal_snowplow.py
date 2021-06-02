import osmnx as ox
import networkx as nx
import time

def init_graph(place):
    city = ox.graph_from_place(place, network_type='drive')
    city = ox.add_edge_speeds(city)
    city = ox.speed.add_edge_travel_times(city)

    for u, v in city.edges():
        city[u][v][0]["weight"] = city.get_edge_data(u, v)[0]["length"]
    return city

city = init_graph("Neuville-sur-Oise, France")
ox.plot_graph(city)
