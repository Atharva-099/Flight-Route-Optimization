import pandas as pd
import numpy as np
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c 

def preprocess_travel_time(route_data, airport_data):
    airport_data.columns = ['AirportID', 'Name', 'City', 'Country', 'IATA', 'ICAO', 
                            'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz', 'Type', 'Source']

    route_data.columns = ['Airline', 'AirlineID', 'SourceAirport', 'SourceAirportID', 
                          'DestinationAirport', 'DestinationAirportID', 'Codeshare', 'Stops', 'Equipment']

    route_data = route_data.merge(airport_data[['IATA', 'Latitude', 'Longitude']], 
                                  left_on='SourceAirport', right_on='IATA', how='left').rename(
        columns={'Latitude': 'SourceLat', 'Longitude': 'SourceLon'}
    )
    route_data = route_data.merge(airport_data[['IATA', 'Latitude', 'Longitude']], 
                                  left_on='DestinationAirport', right_on='IATA', how='left').rename(
        columns={'Latitude': 'DestLat', 'Longitude': 'DestLon'}
    )

    route_data['Distance'] = route_data.apply(lambda row: haversine(
        row['SourceLat'], row['SourceLon'], row['DestLat'], row['DestLon']
    ), axis=1)

    route_data['Speed'] = 900

    route_data['TravelTime'] = route_data['Distance'] / route_data['Speed']

    model_data = route_data[['SourceAirport', 'DestinationAirport', 'Distance', 'TravelTime']].dropna()

    print("Preprocessed data:\n", model_data.head())
    return model_data

if __name__ == "__main__":
    route_data = pd.read_csv('D:/Flight Route Optimization/Data/routes.dat', header=None)
    airport_data = pd.read_csv('D:/Flight Route Optimization/Data/airports.dat', header=None)

    preprocessed_data = preprocess_travel_time(route_data, airport_data)

    preprocessed_data.to_csv('D:/Flight Route Optimization/Data/preprocessed_data.csv', index=False)
