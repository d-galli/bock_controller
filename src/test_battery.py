#!/bin/python3


import mattro_bock
import time





# Robot object
bock = mattro_bock.MattroBock()

# Connect to the robot
print("Connecting to the Bock...")
bock.connect()
print("Bock connected.")

# Print the SOC level
for i in range (100):
    print("SOC = %f" %(bock.state_of_charge))

# Disconnect from the bock
bock.disconnect()
print("Bock disconnected.")
