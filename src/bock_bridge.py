#!/usr/bin/env python3

# Filename:                     bock_bridge.py
# Creation Date:                30/04/2022
# Last Revision Date:           30/05/2022
# Author(s) [email]:			Davide Galli [dgalli@unibz.it]
# Revisor(s) {Date}:        	
# Organization/Institution:	    Free Univerisity of Bozen/Bolzano
# Status:                       Ready for testing
# Notes:

#.............................................About can_write.py.....................................................
# This is a rough implementation of the python scripts written by Carabin, simply converted as ROS node
# to control the motors' drivers.

# Inputs [subscribers]: /'mattro/bock_status
#                       
# Outputs [publishers]: messages over CAN
#...........................................Included Libraries and Message Types.........................................
import rospy

from bock_controller.msg import BockStatus
from bock_controller.src.utils import mattro_bock
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
speed_left_target = 0.0
speed_right_target = 0.0
gear_target = 0

speed_left = 0.0
speed_right = 0.0
    
state_of_activation = 0
random_number = 0.0
shift_value = 0
activation_code = 0
gear = 0
state_of_charge = 0.0

state = 0

reading = False
#.....................................................End of Global Variables............................................

#......................................................Callback Functions ...............................................   
def BockStatusCallback(status_msg):
    global speed_left_target, speed_right_target, gear_target, speed_left, speed_right, state_of_activation, speed_right
    global random_number, shift_value, activation_code, gear, state_of_charge, state, reading

    speed_left_target = status_msg.speed_left_target
    speed_right_target = status_msg.speed_right_target
    gear_target = status_msg.gear_target

    speed_left = status_msg.speed_left
    speed_right = status_msg.speed_right
        
    state_of_activation = status_msg.state_of_activation
    random_number = status_msg.random_number
    shift_value = status_msg.shift_value
    activation_code = status_msg.activation_code
    gear = status_msg.gear
    state_of_charge = status_msg.state_of_charge

    state = status_msg.state

    reading = status_msg.running_read
    
#...................................................End of Callback Functions ...........................................
 
#...................................................User-defined Functions ..............................................
def bock_control():
    global speed_left_target, speed_right_target, gear_target, speed_left, speed_right, state_of_activation, speed_right
    global random_number, shift_value, activation_code, gear, state_of_charge, state, reading

    bock = mattro_bock.MattroBock()
    # Connect to the robot
    print("Connecting to the Bock...")
    bock.connect()
    print("Bock connected")

    while not rospy.is_shutdown():
        # Set the speed
        bock.gear_target = 1
        bock.speed_left_target = speed_left_target
        bock.speed_right_target = speed_right_target
        rospy.sleep()
    
    # Stop the bock
    bock.speed_left_target = 0
    bock.speed_right_target = 0


    # Disconnect from the bock
    bock.disconnect()
    print("Bock disconnected.")
    print("Node terminated")       
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':
    nodeRate = 10

    try:
        print("Try running node")
        rospy.init_node('bock_bridge', anonymous=True)
        loop_rate = rospy.Rate(nodeRate)

        # Define ROS publishers and Subscribers
        sub1 = rospy.Subscriber("/mattro/bock_status", BockStatus, BockStatusCallback)
        
       
        bock_control()

    except rospy.ROSInterruptException:
        print("Node terminated")
#................................................End of Main Function......................................................... 