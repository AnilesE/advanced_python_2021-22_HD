# author: Selina Ernst
# date: 11.11.2021

from collections import Counter
import csv
import matplotlib.pyplot as plt
import math
import geopy.distance
import numpy as np
import random

def distance(lat1,long1,lat2,long2):
    """compute distance (in km) between two points
    Args:
        lat1 ([type]): latidue point 1
        long1 ([type]): longitude point 2
        lat2 ([type]): longitude point 2
        long2 ([type]): longitude point 2
    Returns:
        [int]: distance in km
    """
    coords_1 = (lat1, long1)
    coords_2 = (lat2, long2)

    d = geopy.distance.geodesic(coords_1, coords_2).km      
    return d

def distance_to_point(point_tuple, list_lat, list_long):
    d = [distance(point_tuple[0], point_tuple[1], list_lat[x], list_long[x]) for x in range(len(list_lat))]
    return d

def get_values_of_key(key, list_dict):
    """lists values of different dict with same key
    Args:
        key (string): key of dictionary 
        list_dict (list): list of dictionaries with equal keys but different values
    Returns:
        [list]: list of values from that key
    """
    key_values = []
    for i in range(len(list_dict)):
        if key in list_dict[i]:
            key_values.append(list_dict[i][key])
    return key_values

def create_list_dict(map_data_file):
    """read file and create list of dictionaries
    Args:
        map_data_file (string): filename of .csv file with cities
    Returns:
        [list]: list of dictionaries (each dictionary is one city)
    """
    with open(map_data_file, encoding="utf8") as f:
        f_reader = csv.DictReader(f, delimiter=",") 
        list_dict = []
        
        for line_dict in f_reader:
            list_dict.append(line_dict)
        
    return list_dict

def close(point, list_dict, k = 10):
    """create list of k city names that are closest to point 
    Args:
        point (tule)
        list_dict (list): list of ALL cities
        k (int, optional): Defaults to 10.
    Returns:
        [list]: list of strings (cities ordered after distance to point)
    """
    city = get_values_of_key("city", list_dict)
    lat = get_values_of_key("lat", list_dict)
    long = get_values_of_key("lng", list_dict)

    d_to_point = distance_to_point(point, lat, long)

    # sort city values after d_to_point (only first 10)
    idx = sorted(range(len(d_to_point)), key = lambda sub: d_to_point[sub])[:k]
    closest_cities = [city[x] for x in idx]
    
    return closest_cities
    
def main():
    
    # point_latitude = float(input("latitude:"))
    # point_longitude = float(input("longitude:"))
    # point = tuple([point_latitude, point_longitude])
    point = (50.998401, 10.993570)
    cities_list = create_list_dict("cities.csv")

    city_value = get_values_of_key("city", cities_list)
    lat_value = get_values_of_key("lat", cities_list)
    long_value = get_values_of_key("lng", cities_list)

    lat_value = [float(x) for x in lat_value]
    long_value = [float(x) for x in long_value]
    
    # list of 10 closest cities
    cities_close = close(point, cities_list, 10) 
    
    # id = [city_value.index(x) for x in cities_close]
    # cities_sub_list = [cities_list[x] for x in id]

    # filename = "cities_close_to_point{0}.csv".format(point)
    # with open(filename, "w", newline = "") as output:
    #     writer = csv.DictWriter(output, fieldnames=["city", "lat", "lng", "country"], extrasaction='ignore')
    #     for dict in cities_sub_list:
    #         writer.writerow(dict)
    
    print(cities_close)

    

main()
