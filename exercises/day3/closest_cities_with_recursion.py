# author: Selina Ernst
# date: 11.11.2021

from collections import Counter
import csv
import matplotlib.pyplot as plt
import math
import geopy.distance
import numpy as np
import random
import json

# ----------------------------------------------------------------
# DEPENDENCIES OF FUNCTIONS in this program (not in order):

# ! - create_heapified_tree(map_data_file, point)
# !     - create_tree_from_list(dict_list, i)
#               - get_values_of_key(key, list_dict)
# !     - heapify_tree()
#               - order_root_after_distance_to_point(dict_tree, tuple_point)
# ! - order_root_after_distance_to_point(dict_tree, tuple_point)
#       - distance(lat1,long1,lat2,long2)
#       - swap_children(binary_tree)
#       - swap_right_child_with_parent(binary_tree)
#       - swap_left_child_with_parent(binary_tree)
# ! - find_closest_cities(heapified_tree)
#       - dive_k(tree, k)

#   - main()
# ----------------------------------------------------------------

# --------------------------------
# Defining minor function
#   - get_values_of_key(key, list_dict)
#   - create_tree_from_list(dict_list, i)
#   - dive_k(tree, k)
#   - distance(lat1,long1,lat2,long2)
# --------------------------------

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

def create_tree_from_list(dict_list, i):
    """creates binary tree
    Node of tree is element of dict_list at index i.
    Right child is element of list with index 2i + 2.
    Left child is element of list with index 2i + 1.
    Args:
        dict_list (list): list of dictionaries 
        i (integer): index (i < len(dict_list))
    Returns:
        dict: complete binary tree
    """

    if i >= len(dict_list):
        return None

    else:
        tree = dict_list[i]
        tree.update({
                    "child_right": create_tree_from_list(dict_list, 2*i + 2), 
                    "child_left" : create_tree_from_list(dict_list, 2*i + 1)
                    })
        return tree

def dive_k(tree, k):
    """ diving in k levels and return city names of nodes
    Args:
        tree (dict): binary tree with keys (city, ...)
        k (int): describes how many levels to dive
    Returns:
        [string]: all city names for given levels
    """
    roots = "{0}".format(tree["city"])

    if k == 1:
        return roots
    else:
        
        tree_right = tree["child_right"]
        tree_left = tree["child_left"]
        roots_right = dive_k(tree_right, k-1)
        roots_left = dive_k(tree_left, k-1)
        roots += ", " + roots_right + ", " + roots_left
        
        return roots

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

def swap_children(binary_tree):

    move_child_1 = binary_tree["child_left"]
    move_child_2 = binary_tree["child_right"]
    binary_tree["child_right"] = move_child_1
    binary_tree["child_left"] = move_child_2

def swap_right_child_with_parent(binary_tree):

    move_parent = {key: binary_tree[key] for key in ["city", "lat", "lng", "distance"]}
    move_child = {key: binary_tree["child_right"][key] for key in ["city", "lat", "lng", "distance"]}

    binary_tree.update(move_child)
    binary_tree["child_right"].update(move_parent)

def swap_left_child_with_parent(binary_tree):

    move_parent = {key: binary_tree[key] for key in ["city", "lat", "lng", "distance"]}
    move_child = {key: binary_tree["child_left"][key] for key in ["city", "lat", "lng", "distance"]}

    binary_tree.update(move_child)
    binary_tree["child_left"].update(move_parent)

def order_root_after_distance_to_point(dict_tree, tuple_point): 
    """order parent and children after their distance to certain point
    Args:
        dict_tree (dict): tree (nested dictionary)
        tuple_point (tuple): (latitude, longitude) of point
    Returns:
        [type]: [description]
    """

    d_parent = distance(tuple_point[0], tuple_point[1], dict_tree["lat"], dict_tree["lng"])
    d_child_left = distance(tuple_point[0], tuple_point[1], dict_tree["child_left"]["lat"], dict_tree["child_left"]["lng"])
    d_child_right = distance(tuple_point[0], tuple_point[1], dict_tree["child_right"]["lat"], dict_tree["child_right"]["lng"])
    
    dict_tree.update({"distance" : d_parent}) 
    dict_tree["child_right"].update({"distance" : d_child_right}) 
    dict_tree["child_left"].update({"distance" : d_child_left}) 

    if d_parent < d_child_left and d_parent < d_child_right and d_child_right < d_child_left:
        #  small
        #   /  \
        # big  middle
        pass
    elif d_parent < d_child_left and d_parent < d_child_right and d_child_right > d_child_left:
        #  small
        #   /  \
        # middle  big
        swap_children(dict_tree)
        #  small
        #   /  \
        # big  middle
    elif d_parent < d_child_left and d_parent > d_child_right and d_child_right > d_child_left:
        #  middle
        #   /  \
        # big  small
        swap_right_child_with_parent(dict_tree)
        #  small
        #   /  \
        # big  middle
    elif d_parent > d_child_left and d_parent < d_child_right and d_child_right > d_child_left:
        #  middle
        #   /  \
        # small  big
        swap_children(dict_tree)                
        #  middle
        #   /  \
        # big  small
        swap_right_child_with_parent(dict_tree)
        #  small
        #   /  \
        # big  middle
    elif d_parent > d_child_left and d_parent > d_child_right and d_child_right < d_child_left:
        #      big
        #      /  \
        # middle  small
        swap_left_child_with_parent(dict_tree)
        #  middle
        #   /  \
        # big  small
        swap_right_child_with_parent(dict_tree)
        #  small
        #   /  \
        # big  middle
    elif d_parent > d_child_left and d_parent > d_child_right and d_child_right > d_child_left:
        #   big
        #   /  \
        # small  middle
        swap_children(dict_tree)   
        #    big
        #    /  \
        # middle  small
        swap_left_child_with_parent(dict_tree)
        #   middle
        #   /  \
        # big  small
        swap_right_child_with_parent(dict_tree)
        #  small
        #   /  \
        # big  middle
    return dict_tree


def heapify_tree(point, tree):

    """order tree so that the smallest distances are at the root
    Args:
        point (tuple of floats): latitude and longitude
        tree (dict): each node is one city 
    Returns:
        tree (dict): each node is one city
    """

    if tree["child_left"] == None or tree["child_left"] == None:
        return tree
    
    else:
        tree.update({
        "child_right": heapify_tree(point, tree["child_right"]), 
        "child_left" : heapify_tree(point, tree["child_left"])
        })

        order_root_after_distance_to_point(tree, point)

        return tree

def create_heapified_tree(map_data_file, point):
    """Create a data structure from a map_data_file that allows rapid quering positions on the map
    Args:
        map_data_file (Path) csv file with the following columns:
            city,lat,lng,country,iso3,local_name,population,continent
    Returns
        dict: complete binary tree
            - keys of each Node: city, lat, lng, chil_right, child_left
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

    dict_tree = create_tree_from_list(locations, 0)  
    closeest_tree = heapify_tree(point, dict_tree)

    with open("cities_in_tree.json","w") as f:
        json.dump(dict_tree,f)
    with open("close_cities.json","w") as f:
        json.dump(closeest_tree,f)

    return dict_tree

def find_closest_cities(heapified_tree, levels_of_tree = 3):
    """Find ten close cities to the given point on the world given the data structure
    Args:    
        heapified_tree (dict): each node is one city (at root are cities with smalles distance)
    Returns:
         (string): of cities at level 1 - 3
    """
    return dive_k(heapified_tree, levels_of_tree)

def main():

    point_latitude = float(input("latitude:"))
    point_longitude = float(input("longitude:"))
    point = tuple([point_latitude, point_longitude])
    # (50.998401, 10.993570)

    tree = create_heapified_tree("cities.csv", point)
    print(find_closest_cities(tree, 4))

main()