import pandas as pd
import networkx as nx

def load_routes_data(file_path):
    """
    Load the routes data from a CSV file with no headers.
    
    Parameters:
        file_path (str): Path to the routes data file.
    
    Returns:
        pd.DataFrame: Loaded routes data.
    """
    columns = ['Airline', 'AirlineID', 'SourceAirport', 'SourceAirportID', 
               'DestinationAirport', 'DestinationAirportID', 'Codeshare', 
               'Stops', 'Equipment']
    
    routes_data = pd.read_csv(file_path, header=None, names=columns)
    print("Routes data loaded successfully.")
    return routes_data

def create_graph(routes_data):
    """
    Create a graph using the routes data where each airport is a node and
    each route between airports is an edge.
    
    Parameters:
        routes_data (pd.DataFrame): The routes data.
    
    Returns:
        networkx.Graph: The constructed graph.
    """
    graph = nx.Graph()
    
    for index, row in routes_data.iterrows():
        source = row['SourceAirport']
        destination = row['DestinationAirport']
        

        graph.add_node(source)
        graph.add_node(destination)


        graph.add_edge(source, destination)
    
    print("Graph constructed with", len(graph.nodes), "nodes and", len(graph.edges), "edges.")
    return graph


def find_shortest_path(graph, source, destination):
    """
    Find the shortest path between source and destination using Dijkstra's algorithm.
    
    Parameters:
        graph (networkx.Graph): The graph object with nodes and edges.
        source (str): The source airport code.
        destination (str): The destination airport code.
    
    Returns:
        list: The list of airports in the shortest path from source to destination.
    """
    try:
        
        path = nx.shortest_path(graph, source=source, target=destination)
        return path
    except nx.NetworkXNoPath:
        print(f"No path found between {source} and {destination}.")
        return None

routes_file_path = "D:/Flight Route Optimization/Data/routes.dat"
routes_data = load_routes_data(routes_file_path)

graph = create_graph(routes_data)
