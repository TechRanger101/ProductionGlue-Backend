import googlemaps
from geopy.distance import geodesic
from datetime import datetime
from config import *


gmaps = googlemaps.Client(key=GOOGLE_MAP_API_KEY)

def get_geospatial_distance(location1, location2):
    return geodesic(location1, location2).kilometers

def get_lat_lng_for_zip(zip_code):
    result = gmaps.geocode(zip_code)
    location = result[0]['geometry']['location']
    return [location['lat'], location['lng']]

def get_gmap_distance(origin, destination, mode='driving'):

    now = datetime.now()
    distance_result = gmaps.distance_matrix(origin, destination,
                                            mode=mode,
                                            departure_time=now)

    if distance_result['status'] == 'OK':
        element = distance_result['rows'][0]['elements'][0]
        if element['status'] == 'OK':
            distance_text = element['distance']['text']
            distance_value = element['distance']['value'] / 1000  # Distance in meters
            duration_text = element['duration']['text']
            # print(f"Distance between {origin} and {destination} is: {distance_text}")
            # print(f"It will take approximately {duration_text} by {mode}")
            return [distance_value, duration_text]
        else:
            # print(f"Distance Matrix API returned error for elements: {element['status']}")
            return [None, None]
    else:
        print(f"Distance Matrix API returned overall error: {distance_result['status']}")
        return [None, None]
    
def check_gmap_distance(distance_dict, location):
    return distance_dict.get(str(location), None)

def search_place_in_radius(origin, radius, places, serviceType=None):
    right_places = []
    distance_dict = {}
    try:
        origin_location = get_lat_lng_for_zip(origin)
        for place in places:
            geo_distance = get_geospatial_distance(origin_location, [place['lat'], place['lng']])
            if geo_distance < radius:
                checking = check_gmap_distance(distance_dict, [place['lat'], place['lng']])
                if checking is None:
                    map_distance, duration = get_gmap_distance([origin_location], [(place['lat'], place['lng'])])
                    distance_dict[str([place['lat'], place['lng']])] = [map_distance, duration]
                else:
                    map_distance, duration = checking[0], checking[1]

                if map_distance is not None and map_distance <= radius:
                    place['distance_from_search_location'] = f"Distance between this place and search position({origin}) is {map_distance} km. It will take approximately {duration} by driving."
                    right_places.append(place)
        if len(right_places) == 0:
            return [{"search_result": f"No Result in {radius} km from {origin}"}]
    except:
        return [{"search_result": f"No Result in {radius} km from {origin}"}]
    return right_places