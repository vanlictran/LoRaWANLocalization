# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 04:30:25 2022

@author: sbouro

We used :
    -location of 4 relay: 
        relay_location=[relay1_location, relay2_location, relay3_location, relay4_location] 
    -real end device location : 
        realNodeLocation // TO COMPARE
    -real distance between end device and evry relay: 
        nodeToRelay1RealDistance, nodeToRelay2RealDistance, nodeToRelay3RealDistance, nodeToRelay4RealDistance // TO COMPARE
    -rssi of end device to our 4 relay : 
        rssiEndeviceOnRelay1, rssiEndeviceOnRelay2, rssiEndeviceOnRelay3, rssiEndeviceOnRelay4
To :
    -compute the distance between the node with each of our 4 relay by rssi :
        nodeToRelay1DistanceByRSSI, nodeToRelay2DistanceByRSSI, nodeToRelay3DistanceByRSSI, nodeToRelay4DistanceByRSSI
    -compare the distance by rssi to the real distance between end device and relay
    -Find the position of end device by triangulation using node to relay distance by rssi:
    -compare the position to the real position of end device
      
"""

from location_fonctions import rssiToDistance, distanceWithGps, euclidean_distance, mse
from scipy.optimize import minimize

relay_location = [(16.074591169712548,108.15299798252059),(16.07552046515366,108.15388878942973),(16.074833,108.154114),(16.07527418433303,108.15207714195627)]             #// get by phone gps
real_endDevice_Locations = [(16.075296778694725,108.15288686445291), (16.075230618478724,108.15255664349246)]                   #// get by phone gps
#nodeToRelayRealDistance = [nodeToRelay1RealDistance, nodeToRelay2RealDistance, nodeToRelay3RealDistance, n16.075230618478724,108.15255664349246odeToRelay4RealDistance]  #// https://www.movable-type.co.uk/scripts/latlong.html
rssiOfEndevice_1_ToRelay = [74, -88, -93, -73]
rssiOfEndevice_2_ToRelay = [-72, -79, -92, -74]                                                                                         #// On TTN mapper


#********************************************************************************************#
#********************************************************************************************#

# Array of distance by RSSI
distancesRelaysToEndDevice_1_ByRSSI=[] # for device 1
distancesRelaysToEndDevice_2_ByRSSI=[] # for device 2
for i in range(4):
   distancesRelaysToEndDevice_1_ByRSSI.append(rssiToDistance(rssiOfEndevice_1_ToRelay[i]))
   distancesRelaysToEndDevice_2_ByRSSI.append(rssiToDistance(rssiOfEndevice_2_ToRelay[i]))

    
# Initial point: the point with the closest distance to relay
"""
min_rssi = -128
closest_location = None
for index, rssi in enumerate(rssiOfEndeviceToRelay) :
    # A new closest point!
    if rssi > min_rssi:
        closest_location = relay_location[index]        
initial_location = closest_location
"""
#We used the position of relay 1 like initial location
initial_location = relay_location[1]

### FOR DEVICE 1 ###
result = minimize(
    mse,                                    # The error function
    initial_location,                       # The initial guess
    args=(relay_location, distancesRelaysToEndDevice_1_ByRSSI), # Additional parameters for mse
    method='L-BFGS-B',                      # The optimisation algorithm
    options={
        'ftol':1e-5,                        # Tolerance
        'maxiter': 1e+7                     # Maximum iterations
    })
location = result.x

print('\nlocation of End device 1 estimate by RSSI :')
print(location)

error = euclidean_distance(location[0],location[1] ,real_endDevice_Locations[0][0],real_endDevice_Locations[0][1])
error2 = distanceWithGps((location[0],location[1]) ,real_endDevice_Locations[0])

#print('error: ', error)
print('Distance between real position and position estimate (m): ', error2*1000, 'm\n')

### FOR DEVICE 2 ###
result = minimize(
    mse,                                    # The error function
    initial_location,                       # The initial guess
    args=(relay_location, distancesRelaysToEndDevice_2_ByRSSI), # Additional parameters for mse
    method='L-BFGS-B',                      # The optimisation algorithm
    options={
        'ftol':1e-5,                        # Tolerance
        'maxiter': 1e+7                     # Maximum iterations
    })
location = result.x

print('\nlocation of End device 2 estimate by RSSI :')
print(location)

error = euclidean_distance(location[0],location[1] ,real_endDevice_Locations[1][0],real_endDevice_Locations[1][1])
error2 = distanceWithGps((location[0],location[1]) ,real_endDevice_Locations[1])
#print('error: ', error)
print('Distance between real position and position estimate (m): ', error2*1000, 'm')