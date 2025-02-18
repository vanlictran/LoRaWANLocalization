# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 06:21:56 2022

@author: van lic and sbouro
"""
import os
import numpy as np
import pandas as pd
import math
from scipy.optimize import minimize, rosen, rosen_der


def rssiToDistance(rssi):
   A= -31

   n=4.335
   return pow(10, (A-rssi) / (10 * n))/1000

def distanceWithGps( origin  ,destination):
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
    distanceFromNodeToRelay = radius * c

    return distanceFromNodeToRelay

def euclidean_distance(x1, y1, x2, y2):
    p1 = np.array((x1 ,y1))
    p2 = np.array((x2, y2))
    return np.linalg.norm(p1-p2)

# Mean Square Error
def mse(x, locations, distances):
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = distanceWithGps((x[0], x[1]), (location[0], location[1]))
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(distances)
