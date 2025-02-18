# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 23:11:14 2022

@author: ADMINISTRATOR

"""

import os
import numpy as np
import pandas as pd
import math
from scipy.optimize import minimize, rosen, rosen_der


def distanceGPS(lat1, lon1 ,lat2, lon2):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    # lat1, lon1 = origin
    # lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def distancelatlon(origin ,destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def rssiToDistance(rssi):
   A= -29

   if rssi > -60:
       n=2
   elif rssi > -72:
       n = 2.4
   elif rssi > -81:
       n =3
   else: n = 3.4
   return pow(10, (A-rssi) / (10 * n))/1000

def euclidean_distance(x1, y1, x2, y2):
    p1 = np.array((x1 ,y1))
    p2 = np.array((x2, y2))
    return np.linalg.norm(p1-p2)

# Mean Square Error
# locations: [ (lat1, long1), ... ]
# distances: [ distance1, ... ]
def mse(x, locations, distances):
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = distanceGPS(x[0], x[1], location[0], location[1])
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(distances)
#********************************************************************************************#
#********************************************************************************************#

# relays locations
locations =[ (43.615459, 7.072282),(43.614775, 7.073123),(43.614198, 7.072174)] #3.8.6

# end device real location
gps_location = (43.615046, 7.072142)

# distance by RSSI
l1 =rssiToDistance(-78)
l2=rssiToDistance(-94)
l3=rssiToDistance(-93)
distances =[l1,l2,l3] 

# Initial point: the point with the closest distance
# min_distance     = float('inf')
# closest_location = None
# for member in data:
#     # A new closest point!
#     if member['distance'] < min_distance:
#         min_distance = member['distance']
#         closest_location = member['location']
# initial_location = closest_location
initial_location =  (43.0, 7.0)
# initial_location: (lat, long)
# locations: [ (lat1, long1), ... ]
# distances: [ distance1,     ... ] 
result = minimize(
    mse,                         # The error function
    initial_location,            # The initial guess
    args=(locations, distances), # Additional parameters for mse
    method='L-BFGS-B',           # The optimisation algorithm
    options={
        'ftol':1e-5,         # Tolerance
        'maxiter': 1e+7      # Maximum iterations
    })

# location base on distance by RSSI
location = result.x
print(location)

# distance between real location and location compute
error = euclidean_distance(location[0],location[1] , gps_location[0], gps_location[1])
error2 = distanceGPS(location[0],location[1] , gps_location[0], gps_location[1])

# distance between 
d1= distancelatlon(gps_location,locations[0])
d2= distancelatlon(gps_location,locations[1])
d3= distancelatlon(gps_location,locations[2])