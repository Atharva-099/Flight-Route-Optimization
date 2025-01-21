import requests

# AviationStack API details
AVIATIONSTACK_API_KEY = '7c924ebefbe8fca10ef86c54cc38f1c2'  # AviationStack API key for traffic and delay data
AVIATIONSTACK_BASE_URL = 'http://api.aviationstack.com/v1'

# Fetch Traffic Data
def get_traffic_data(airport_code):
    """
    Fetches traffic data for the given airport code using AviationStack API.
    
    Args:
        airport_code (str): IATA code of the airport.
    
    Returns:
        dict: Traffic data for the airport, or None if the API call fails.
    """
    params = {'access_key': AVIATIONSTACK_API_KEY, 'airport': airport_code}
    response = requests.get(f'{AVIATIONSTACK_BASE_URL}/traffic', params=params)
    if response.status_code == 200:
        traffic_data = response.json()
        return traffic_data
    else:
        return None  # Return None if API call fails

# Fetch Delay Data
def get_delay_data(airport_code):
    """
    Fetches delay data for the given airport code using AviationStack API.
    
    Args:
        airport_code (str): IATA code of the airport.
    
    Returns:
        dict: Delay data for the airport, or None if the API call fails.
    """
    params = {'access_key': AVIATIONSTACK_API_KEY, 'airport': airport_code}
    response = requests.get(f'{AVIATIONSTACK_BASE_URL}/delays', params=params)
    if response.status_code == 200:
        delay_data = response.json()
        return delay_data
    else:
        return None  # Return None if API call fails
