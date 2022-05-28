#!/usr/bin/env python3

# Filename:                     can_read.py
# Creation Date:                20/04/2022
# Last Revision Date:           28/05/2022
# Author(s) [email]:			Davide Galli [dgalli@unibz.it]
# Revisor(s) {Date}:        	
# Organization/Institution:	    Free Univerisity of Bozen/Bolzano
# Status:                       Up and Ready
# Notes:                        

#.............................................About can_read.py.....................................................
# This code is aimed to connect the ROS network and the CAN network. It reads the data transmitted over CAN and publishes
# some information about robot's status over the topic "/mattro/bock_status".
#
#
# Inputs [subscribers]: CAN message
#                       target speeds for the two motors
# Outputs [publishers]: bock_status
#                       messages over CAN
#...........................................Included Libraries and Message Types.........................................
import rospy
import os
import can
from can import Message
from bock_controller.msg import BockStatus
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
#.....................................................End of Global Variables............................................

#......................................................Callback Functions ...............................................   

#...................................................End of Callback Functions ...........................................
 
#...................................................User-defined Functions ..............................................
def read_can():
    
    bock_can = can.interface.Bus(channel = 'can0', bustype = 'socketcan') #socketcan_ctypes
    print("Node up and running")
    battery = 0
    current_gear = 0
    # Create a BockStatus message
    status_msg = BockStatus()
    
    while not rospy.is_shutdown():
            
        # Read a message from can bus
        can_msg = bock_can.recv()


        # Parse the message
        if can_msg.arbitration_id == 0x215:
            status_msg.state_of_activation = can_msg.data[0]
            status_msg.activation_code = (can_msg.data[1]>>can_msg.data[2])
            current_gear = can_msg.data[5]
            status_msg.gear = current_gear
            battery = ((can_msg.data[7]<<8) + can_msg.data[6])/10.
            status_msg.state_of_charge = battery
        
        elif can_msg.arbitration_id == 0x315:
            s_left = (can_msg.data[3]<<24) + (can_msg.data[2]<<16) + (can_msg.data[1]<<8) + can_msg.data[0]
            status_msg.speed_left = s_left
            s_right = (can_msg.data[7]<<24) + (can_msg.data[6]<<16) + (can_msg.data[5]<<8) + can_msg.data[4]
            status_msg.speed_right = s_right

            print("Battery", battery, "% Right speed: ", s_right," Left speed: ", s_left, "Gear ", current_gear, end = "\r")
        
        # Publish the ROS message
        pub1.publish(status_msg)

    print("\n Node terminated")
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':
    nodeRate = 10

    try:
        print("Try running node")
        rospy.init_node('can_read', anonymous=True)
        loop_rate = rospy.Rate(nodeRate)

        # Define ROS publishers and Subscribers
        pub1 = rospy.Publisher("/mattro/bock_status", BockStatus, queue_size = 10)
        
        read_can()

    except rospy.ROSInterruptException:
        print("Node terminated")
#................................................End of Main Function......................................................... 
