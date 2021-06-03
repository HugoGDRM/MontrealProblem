from montreal_drone import get_best_route
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, LineString

import matplotlib.pyplot as plt
import plotly_express as px

import networkx as nx
import osmnx as ox

G, route, length, travel_time = get_best_route("Issou, France")
# impute missing edge speeds and add travel times
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)
node_start = []
node_end = []
X_to = []
Y_to = []
X_from = []
Y_from = []

start = (48.987813, 1.794107)
end = (48.987813, 1.794107)
start_node = ox.get_nearest_node(G.to_undirected(), start)
end_node = ox.get_nearest_node(G.to_undirected(), end)
ox.plot_graph_route(G.to_undirected(), route)
for u, v in zip(route[:-1], route[1:]):
    node_start.append(u)
    node_end.append(v)
    X_from.append(G.nodes[u]['x'])
    Y_from.append(G.nodes[u]['y'])
    X_to.append(G.nodes[v]['x'])
    Y_to.append(G.nodes[v]['y'])

df = pd.DataFrame(list(zip(node_start, node_end, X_from, Y_from,  X_to, Y_to)),
               columns =["node_start", "node_end", "X_from", "Y_from",  "X_to", "Y_to"])
df.head()

df.reset_index(inplace=True)
df.head()

def create_line_gdf(df):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.X_from, df.Y_from))
    gdf["geometry_to"] = [Point(xy) for xy in zip(gdf.X_to, gdf.Y_to)]
    gdf['line'] = gdf.apply(lambda row: LineString([row['geometry_to'], row['geometry']]), axis=1)
    line_gdf = gdf[["node_start","node_end","line"]].set_geometry('line')
    return line_gdf

line_gdf = create_line_gdf(df)

line_gdf.plot()


start = df[df["node_start"] == start_node]
end = df[df["node_end"] == end_node]
px.set_mapbox_access_token("pk.eyJ1IjoiamV4ZnJlZG8iLCJhIjoiY2twZW1nbm82MXluYjJubmx6endsN25tdyJ9.AR5KtIhw-_kDoe3NUahpHg")
px.scatter_mapbox(df, lon= "X_from", lat="Y_from", zoom=12)
fig = px.scatter_mapbox(df, lon= "X_from", lat="Y_from", width=800, height=400, zoom=12)
fig.add_trace(px.line_mapbox(df, lon= "X_from", lat="Y_from").data[0])
fig.data[1].marker = dict(size = 15, color="red")
fig.add_trace(px.scatter_mapbox(end, lon= "X_from", lat="Y_from").data[0])
fig.data[2].marker = dict(size = 15, color="green")
fig.add_trace(px.line_mapbox(df, lon= "X_from", lat="Y_from").data[0])
fig.show()
