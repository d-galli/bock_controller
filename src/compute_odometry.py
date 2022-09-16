#!/usr/bin/env python3

# Filename:                     mattro_navigation_test.py
# Creation Date:                11/08/2022
# Last Revision Date:           11/08/2022
# Author(s) [email]:			Davide Galli [dgalli@unibz.it]
# Revisor(s) {Date}:        	
# Organization/Institution:	    Free Univerisity of Bozen/Bolzano
# Status:                       To be tested
# Notes:                        

#.............................................About can_read.py.....................................................
# This code is aimed to make the mattro rovo 2 move along a squared shaped path by means of data from the pozyx 
# system and the IMU.
#
#
# Inputs [subscribers]: /mattro/pose
#                       
# Outputs [publishers]: /mattro/cmd_vel
#                  
#...........................................Included Libraries and Message Types.........................................
import rospy
import numpy as np
from bock_controller.msg import BockStatus
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
v_r_raw = 0.0
v_l_raw = 0.0
#.....................................................End of Global Variables............................................

#.........................................................Global Constants...............................................
ERROR_THRESHOLD = 0.1 # [deg]
#.....................................................End of Global Constants............................................

#......................................................Callback Functions ...............................................   
def SpeedCallback(msg): # Read the pose of the mattro
    global v_r_raw, v_l_raw

    v_l_raw = msg.speed_left
    v_r_raw = msg.speed_right
#...................................................End of Callback Functions ...........................................

#...................................................User-defined Functions ..............................................
def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def compute_odometry(loop_rate, wheel_space):
    global v_r_raw, v_l_raw
    print("ComputeOdometryNode: up and running")

    X = 0.0
    Y = 0.0
    theta = 0.0
    irc = np.zeros((2, 1))
    dt = 0.1 # [sec]

    while not rospy.is_shutdown():
        v_l = map_range(v_l_raw, -1000.0, 1000.0, -20.0, 20.0)/ 3.6
        v_r = map_range(v_r_raw, -1000.0, 1000.0, -20.0, 20.0)/ 3.6
        print("Speeds: ", v_l , v_r)
        v = (v_l + v_r)/2
        omega = (v_r - v_l)/wheel_space
        if v_r != 0.0 and v_l != 0.0:
            bendingRadius = (wheel_space/2)*((v_r + v_l)/(v_r - v_l))
            irc = np.array([[X - bendingRadius*np.sin(theta)], 
                            [Y + bendingRadius*np.cos(theta)]])

        X = X + v * np.cos(theta) * dt
        Y = Y + v * np.sin(theta) * dt
        theta = theta + omega * dt

        #print("X: ", X, " Y: ", Y, " theta: ", theta, end = "\r")
        
        loop_rate.sleep()

    # Publish the ROS message
    print("Shutting down ...")
    print("\n Node terminated")
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':
    nodeRate = 10

    try:
        print("Try running node")
        rospy.init_node('mattro_navigation_test', anonymous=True)

        # Read the parameters from the launch file
        rate = rospy.get_param("~rate", 10)
        loop_rate = rospy.Rate(rate)
        wheel_space = rospy.get_param("~base_width", 0.644)

        # Define ROS publishers and Subscribers
        sub1 = rospy.Subscriber("/mattro/bock_status", BockStatus, SpeedCallback)
        
        compute_odometry(loop_rate, wheel_space)

    except rospy.ROSInterruptException:
        print("Node terminated")
#................................................End of Main Function......................................................... 