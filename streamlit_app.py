import streamlit as st
from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx
from Scripts.data_preprocessing import preprocess_travel_time
from Scripts.random_forest_model import predict_travel_time
from Scripts.dijkstra_algorithm import create_graph, find_shortest_path
from city_details import find_all_paths


def load_flight_data():
    routes_data = pd.read_csv('D:/Flight Route Optimization/Data/routes.dat', header=None, names=[
        'Airline', 'AirlineID', 'SourceAirport', 'SourceAirportID', 
        'DestinationAirport', 'DestinationAirportID', 'Codeshare', 'Stops', 'Equipment'
    ])
    return routes_data


def load_airport_data():
    airports_data = pd.read_csv('D:/Flight Route Optimization/Data/airports.dat', header=None, names=[
        'AirportID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude', 'Longitude', 
        'Altitude', 'Timezone', 'DST', 'Tz', 'Type', 'Source'
    ])
    return airports_data


def get_connected_cities(route_data, airport_data, source_city):
    source_airport = airport_data[airport_data['City'] == source_city].iloc[0]
    source_iata = source_airport['IATA']
    connected_routes = route_data[route_data['SourceAirport'] == source_iata]
    connected_cities = airport_data[airport_data['IATA'].isin(connected_routes['DestinationAirport'])]
    top_9_cities = connected_cities['City'].head(9).tolist()
    top_10_cities = [source_city] + top_9_cities
    return top_10_cities


def filter_by_selected_cities(route_data, airport_data, selected_cities, destination_city):
    selected_airports = airport_data[airport_data['City'].isin(selected_cities)]
    destination_airports = airport_data[airport_data['City'] == destination_city]
    filtered_routes = route_data[
        route_data['SourceAirport'].isin(selected_airports['IATA']) &
        route_data['DestinationAirport'].isin(destination_airports['IATA'])
    ]
    return filtered_routes


def filter_by_country(airport_data, country):
    return airport_data[airport_data['Country'] == country]


st.title("Flight Route Optimization")

option = st.radio(
    "Choose the type of route you want to find:",
    ("City to City Routes", "Country Routes")
)

if option == "City to City Routes":
    source_city = st.text_input("Enter the source city:")
    destination_city = st.text_input("Enter the destination city:")

    if st.button("Find City Routes"):
        try:
            route_data = load_flight_data()
            airport_data = load_airport_data()

            selected_cities = get_connected_cities(route_data, airport_data, source_city)
            filtered_routes = filter_by_selected_cities(route_data, airport_data, selected_cities, destination_city)

            preprocessed_data = preprocess_travel_time(filtered_routes, airport_data)
            graph = create_graph(preprocessed_data)

            start_cities = airport_data[airport_data['City'].isin(selected_cities)]['IATA'].values
            end_city = airport_data[airport_data['City'] == destination_city]['IATA'].values[0]

            all_paths = []
            for start in start_cities:
                all_paths += find_all_paths(graph, start, end_city)

            shortest_path = None
            shortest_length = float('inf')
            for path in all_paths:
                total_length = len(path) - 1
                if total_length < shortest_length:
                    shortest_length = total_length
                    shortest_path = path

            st.subheader("Results:")
            st.write(f"Shortest Path: {shortest_path}")
            st.write(f"Total Stops: {shortest_length}")
            st.subheader("Flight Network Graph")
            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(graph)
            nx.draw(graph, pos, with_labels=True, node_size=50, node_color='blue', font_size=8, font_color='darkred')

            if shortest_path:
                edges_in_shortest_path = [(shortest_path[i], shortest_path[i + 1]) for i in range(len(shortest_path) - 1)]
                nx.draw_networkx_edges(graph, pos, edgelist=edges_in_shortest_path, edge_color='green', width=2)

            plt.title(f"Flight Network Graph from path {source_city} to {destination_city}")
            st.pyplot(plt)

        except Exception as e:
            st.error(f"An error occurred: {e}")

elif option == "Country Routes":
    country = st.text_input("Enter the country to filter routes:")

    if st.button("Find Country Routes"):
        try:
            route_data = load_flight_data()
            airport_data = load_airport_data()

            filtered_airports = filter_by_country(airport_data, country)
            filtered_routes = route_data[
                route_data['SourceAirport'].isin(filtered_airports['IATA']) |
                route_data['DestinationAirport'].isin(filtered_airports['IATA'])
            ]

            preprocessed_data = preprocess_travel_time(filtered_routes, airport_data)
            graph = create_graph(preprocessed_data)

            st.subheader("Filtered Routes for the Country:")
            st.write(filtered_routes.head())

            st.subheader("Flight Network Graph")
            plt.figure(figsize=(12, 8))
            nx.draw(graph, with_labels=True, node_size=50, node_color='blue', font_size=8, font_color='darkred')
            plt.title(f"Flight Network Graph for {country}")
            st.pyplot(plt)

        except Exception as e:
            st.error(f"An error occurred: {e}")

            
# #streamlit run streamlit_app.py
