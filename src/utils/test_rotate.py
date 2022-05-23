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
print("SOC = %f" %(bock.state_of_charge))


# Set the speed
bock.gear_target = 1
bock.speed_left_target = +1.0
bock.speed_right_target = -1.0

time.sleep(40.0)

# Stop the bock
bock.speed_left_target = 0
bock.speed_right_target = 0


# Disconnect from the bock
bock.disconnect()
print("Bock disconnected.")

