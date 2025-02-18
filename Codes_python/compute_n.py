# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 23:28:43 2022

@author: van lic and sbouro
"""
# Import math Library
import math
# Import statistics Library
import statistics

def computeN(A,distanceArray,rssiArray):
    ni=[]
    for index,distance in enumerate(distanceArray):
        ni.append((A-rssiArray[index])/(10)*math.log(distance))
    print(ni)
    return statistics.mean(ni)

# for relay 3
A=-31
d=[2, 3, 4, 5, 6, 7, 8, 9, 10, 12]
rssi=[-41, -44, -45, -49, -52, -55, -60, -61, -62, -64]

print(len(d), len(rssi))

n=computeN(A, d, rssi)
print(n)
