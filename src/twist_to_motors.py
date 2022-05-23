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
from geometry_msgs.msg import Twist 
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
dx = 0.0
dy = 0.0
dr = 0.0

operating = False
#.....................................................End of Global Variables............................................

#......................................................Callback Functions ...............................................   
def TwistCallback(msg):
    global dx, dy, dr
    
    dx = msg.linear.x
    dy = msg.linear.y
    dr = msg.angular.z

def BockStatusCallback(status_msg):
    global operating
    
    operating = status_msg.operating
#...................................................End of Callback Functions ...........................................
 
#...................................................User-defined Functions ..............................................
def motor_spin(loop_rate):
    global dx, dy, dr

    then = rospy.Time.now()

    # Create a BockStatus message
    status_msg = BockStatus()
    
    while not rospy.is_shutdown() and operating:
            
        status_msg.speed_right_target = 1.0 * dx + dr * wheel_space / 2
        status_msg.speed_left_target = 1.0 * dx - dr * wheel_space / 2

        pub1.publish(status_msg)
        
        loop_rate.sleep()
    
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':

    try:
        rospy.loginfo("Try running node")
        rospy.init_node('twist_to_motor', anonymous=True)

        # Get ros parameters from the launch file
        loop_rate = rospy.get_param("~rate")
        wheel_space = rospy.get_param("~base_width")

        # Define ROS publishers and Subscribers
        pub1 = rospy.Publisher("/mattro/bock_status", BockStatus, queue_size = 10)
        sub1 = rospy.Subscriber("/mattro/bock_status", BockStatus, BockStatusCallback)
        sub2 = rospy.Subscriber('/mattro/cmd_vel', Twist, TwistCallback)

        motor_spin(loop_rate)

    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")
#................................................End of Main Function......................................................... 