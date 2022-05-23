#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 10:50:24 2022
@author: @dgalli
Institution: Free University of Bozen/Bolzano
Degree: Master in Industrial Mechanical Engineer
"""

import rospy
from geometry_msgs.msg import Twist
import mattro_bock
import time


def velocity_callback(data):
    msg = Twist()
    angular = [msg.angualr.x, msg.angular.y, msg.angular.z]
    linear = [msg.linear.x, msg.linear.y, msg.linear.z]


def velocity_controller:
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
    bock.speed_right_target = +1.0
    
    time.sleep(15.0)
    
    # Stop the bock
    bock.speed_left_target = 0
    bock.speed_right_target = 0
    
    
    
    # Disconnect from the bock
    bock.disconnect()
    print("Bock disconnected.")
    
def listener():

    rospy.init_node('BockVelocityController', anonymous=True)

    rospy.Subscriber("cmd_vel", Twist, velocity_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()