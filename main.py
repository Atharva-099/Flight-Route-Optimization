from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx
from Scripts.data_preprocessing import preprocess_travel_time
from Scripts.random_forest_model import predict_travel_time
from Scripts.dijkstra_algorithm import create_graph, find_shortest_path

# Step 1: Load Flight Data
def load_flight_data():
    routes_data = pd.read_csv('D:/Flight Route Optimization/Data/routes.dat', header=None, names=[
        'Airline', 'AirlineID', 'SourceAirport', 'SourceAirportID', 
        'DestinationAirport', 'DestinationAirportID', 'Codeshare', 'Stops', 'Equipment'
    ])
    print("Routes Data Loaded:\n", routes_data.head())
    return routes_data

# Step 2: Load Airport Data
def load_airport_data():
    airports_data = pd.read_csv('D:/Flight Route Optimization/Data/airports.dat', header=None, names=[
        'AirportID', 'Name', 'City', 'Country','IATA', 'ICAO', 'Latitude', 'Longitude', 
        'Altitude', 'Timezone', 'DST', 'Tz','Type', 'Source'
    ])
    print("Airports Data Loaded:\n", airports_data.head())
    return airports_data

# Step 3: Filter airports by country
def filter_by_country(airport_data, country):
    # Filter airports by the given country
    filtered_airports = airport_data[airport_data['Country'] == country]
    return filtered_airports

# Step 4: Main Execution
if __name__ == "__main__":
    # Load data
    route_data = load_flight_data()
    airport_data = load_airport_data()

    # Ask user for country to filter by
    country = input("Enter the country to filter the routes: ")

    # Filter airport data by country
    filtered_airports = filter_by_country(airport_data, country)

    # Filter route data based on the filtered airports
    filtered_routes = route_data[
        route_data['SourceAirport'].isin(filtered_airports['IATA']) |
        route_data['DestinationAirport'].isin(filtered_airports['IATA'])
    ]
    
    print(f"Filtered Routes for {country}:\n", filtered_routes.head())

    # Ensure proper data types for merging
    route_data['SourceAirport'] = route_data['SourceAirport'].astype(str)
    route_data['DestinationAirport'] = route_data['DestinationAirport'].astype(str)
    airport_data['AirportID'] = airport_data['AirportID'].astype(str)

    # Preprocess data
    preprocessed_data = preprocess_travel_time(filtered_routes, airport_data)

    # Construct graph
    graph = create_graph(preprocessed_data)

    # Output for visualization
    print(f"Graph constructed with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges.")

    # Visualize the graph
    plt.figure(figsize=(12, 8))
    nx.draw(graph, with_labels=True, node_size=50, node_color='blue', font_size=8, font_color='darkred')
    plt.title(f"Flight Network Graph for {country}")
    plt.show()
