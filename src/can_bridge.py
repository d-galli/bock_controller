#!/usr/bin/env python

# Filename:                     can_bridge.py
# Creation Date:                20/04/2022
# Last Revision Date:           23/05/2022
# Author(s) [email]:			Davide Galli [dgalli@unibz.it]
# Revisor(s) {Date}:        	
# Organization/Institution:	Free Univerisity of Bozen/Bolzano
# Status:                       Work in progress

#.............................................About wildlife_odom.py.....................................................
# This code is aimed to connect the ROS network and the CAN network. It reads the data transmitted over CAN and publishes
# some information about robot's status over the topic "/mattro/bock_status".
# At the same time, it reads the datat pusblished on the same topic "/mattro/bock_status", and converts them into a CAN
# message to control the motors' drivers.

# Inputs [subscribers]: CAN message
#                       target speeds for the two motors
# Outputs [publishers]: bock_status
#                       messages over CAN
#...........................................Included Libraries and Message Types.........................................
import rospy
import os
import can
from can import Message
from msg import BockStatus
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
running_read = False
#.....................................................End of Global Variables............................................

#......................................................Callback Functions ...............................................   
def BockStatusCallback(status_msg):
    global running_read
    
    running_read = status_msg.running_read

    # Define CAN network
    bock_can = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')
    
    drivemode = 0b00000011
    
    if status_msg.speed_left_target > 0:
        drivemode = drivemode | 0b00010000
    else:
        drivemode = drivemode | 0b00100000
    
    if status_msg.speed_right_target > 0:
        drivemode = drivemode | 0b01000000
    else:
        drivemode = drivemode | 0b10000000
        
    speed_left_H = (int(abs(status_msg.speed_left_target)*10)>>8)
    speed_left_L = (int(abs(status_msg.speed_left_target)*10)) & 0xff
    speed_right_H = (int(abs(status_msg.speed_right_target)*10)>>8)
    speed_right_L = (int(abs(status_msg.speed_right_target)*10)) & 0xff
    
    # Create a CAN message to be published
    can_msg = Message(arbitration_id=0x295, data=[drivemode, speed_left_L, speed_left_H, speed_right_L, speed_right_H, status_msg.gear_target, 0x00, 0x00])#, extended_id=False)
    # Send the message over CAN
    bock_can.send(can_msg)

    # Wait 5 milliseconds
    rospy.sleep(0.005)
        
    # Send request of deactivation
    deact_msg = Message(arbitration_id=0x195, data=[0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])#, extended_id=False)
    bock_can.send(deact_msg)

#...................................................End of Callback Functions ...........................................
 
#...................................................User-defined Functions ..............................................
def read_can():
    
    bock_can = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')

    while not rospy.is_shutdown():
        while running_read:

            # Read a message from can bus
            can_msg = bock_can.recv()

            # Create a BockStatus message
            status_msg = BockStatus()
                
            # Parse the message
            if can_msg.arbitration_id == 0x215:
                status_msg.state_of_activation = can_msg.data[0]
                status_msg.activation_code = (can_msg.data[1]>>can_msg.data[2])
                status_msg.gear = can_msg.data[5]
                status_msg.state_of_charge = ((can_msg.data[7]<<8) + can_msg.data[6])/10.
            
            elif can_msg.arbitration_id == 0x315:
                status_msg.speed_left = (can_msg.data[3]<<24) + (can_msg.data[2]<<16) + (can_msg.data[1]<<8) + can_msg.data[0]
                status_msg.speed_right = (can_msg.data[7]<<24) + (can_msg.data[6]<<16) + (can_msg.data[5]<<8) + can_msg.data[4]

            # Publish the ROS message
            pub1.publish(status_msg)
    
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':
    nodeRate = 10

    try:
        rospy.loginfo("Try running node")
        rospy.init_node('can_read', anonymous=True)
        loop_rate = rospy.Rate(nodeRate)

        # Define ROS publishers and Subscribers
        pub1 = rospy.Publisher("/mattro/bock_status", BockStatus, queue_size = 10)
        sub1 = rospy.Subscriber("/mattro/bock_status", BockStatus, BockStatusCallback)

        read_can()

    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")
#................................................End of Main Function......................................................... 
