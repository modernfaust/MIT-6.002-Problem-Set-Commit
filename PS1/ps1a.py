###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1

class WeightError(Exception):
    pass
    

with open('ps1_cow_data.txt') as list_1:
    cow_list = list_1.read()

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cow_dict = {}
    lines = filename.splitlines()
    for l in lines:
        split = (l.split(','))
        cow_dict[split[0]] = int(split[1])
    return cow_dict

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    list_of_lists = []
    temp_dict = cows
    highest_val = 0
    highest = ""
    empty = False
    while not empty:
        weight = 0
        trip=[]
        while weight+highest_val <= limit and len(temp_dict) !=0:
            highest = max(temp_dict, key=temp_dict.get)
            highest_val = temp_dict.pop(highest)
#            print("Dict has left:",temp_dict,"and length is:",len(temp_dict))
            weight += highest_val
#            print("Highest",highest,"and to store",highest_val)
            trip.append(highest)
        if len(temp_dict) == 0:
            empty = True
        list_of_lists.append(trip)
    return list_of_lists
    
# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    total = 0
    partition_list = [] #a list of a list of lists
    temp_dict = {}
    for partition in get_partitions(cows):
        partition_list.append(partition)
    for plan in partition_list:
        excess = False
        for trip in plan:
            for c in trip:
                total+=cows[c]
            if total > limit:
                excess = True
            total = 0
        if excess == False:
            temp_dict[len(plan)]=plan
    return temp_dict[min(temp_dict)]

# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    #BRUTE FORCE
    start_time = time.time()
    result = brute_force_cow_transport(load_cows(cow_list),limit=10)
    length = len(result)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Brute Force took: {total_time} seconds, with {length} trips.")
    #GREEDY
    start_time = time.time()
    result = greedy_cow_transport(load_cows(cow_list),limit=10)
    length = len(result)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Greedy took: {total_time} seconds, with {length} trips.")
    

    pass
#print(brute_force_cow_transport(load_cows(cow_list),limit=10))
#print(greedy_cow_transport(load_cows(cow_list),limit=10))
compare_cow_transport_algorithms()
