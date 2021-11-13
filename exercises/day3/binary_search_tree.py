from collections import Counter
import csv
import matplotlib.pyplot as plt
import math
import geopy.distance
import numpy as np
import random
import json

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
    # latidue and longitude coordinates
    coords_1 = (lat1, long1)
    coords_2 = (lat2, long2)

    # distance in km:
    d = geopy.distance.geodesic(coords_1, coords_2).km      
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
        
    city_value = get_values_of_key("city", list_dict)
    lat_value = get_values_of_key("lat", list_dict)
    long_value = get_values_of_key("lng", list_dict)

    lat_value = [float(x) for x in lat_value]
    long_value = [float(x) for x in long_value]

    locations = [{"city": city_value[x], "lat" : lat_value[x], "lng" : long_value[x]} for x in range(len(list_dict))]       
    return locations

def key_exists(dict, key):
    if key in dict.keys():
        return True
    else: return False

def insert(value, tuple_point, dict_tree = None):
    if dict_tree == None:
        value.update({"distance": distance(tuple_point[0], tuple_point[1], value["lat"], value["lng"])})
        return value
    else:
        node_distance = distance(tuple_point[0], tuple_point[1], dict_tree["lat"], dict_tree["lng"])
        new_distance = distance(tuple_point[0], tuple_point[1], value["lat"], value["lng"])
        if new_distance == node_distance:
            dict_tree.update(value)
            return dict_tree
        if key_exists(dict_tree, "child_left") == True and new_distance < node_distance:
            dict_tree.update({"child_left": insert(value, tuple_point, dict_tree["child_left"])})
            return dict_tree
        elif key_exists(dict_tree, "child_left") == False and new_distance < node_distance:
            value.update({"distance": new_distance})
            dict_tree.update({"child_left": value})
            return dict_tree
        elif key_exists(dict_tree, "child_right") == True and new_distance > node_distance:
            dict_tree.update({"child_right":insert(value, tuple_point, dict_tree["child_right"])})
            return dict_tree
        elif key_exists(dict_tree, "child_right") == False:
            value.update({"distance": new_distance})
            dict_tree.update({"child_right": value})
            return dict_tree

def get_min(BST_tree):
    if key_exists(BST_tree, "child_left") == True:
        return get_min(BST_tree["child_left"])
    else: return BST_tree["city"]

def inorder(BST_tree):
    if key_exists(BST_tree, "child_left") == True:
        close = inorder(BST_tree["child_left"]) + [BST_tree["city"]] 
    else: close = [BST_tree["city"]]
    if key_exists(BST_tree, "child_right") == True:
        close = close + inorder(BST_tree["child_right"])
    return close

cities = create_list_dict("cities.csv")
point = (50.998401, 10.993570)

# # CREATING tree takes about 30 min 
# tree = insert(cities[0], point)

# for i in range(1, len(cities)):
#     tree = insert(cities[i], point, tree)
# with open("BSTtree.json","w") as f:
#     json.dump(t,f)

tree = json.load(open("BSTtree.json"))
print(inorder(tree)[0:10])
