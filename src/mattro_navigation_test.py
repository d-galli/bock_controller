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
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Twist
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
header_info = [0,0,0]

euler = np.zeros(3)
position = np.zeros(3)
#.....................................................End of Global Variables............................................

#.........................................................Global Constants...............................................
EDGE_LENGHT = 2 # [m]
ANGULAR_ROTATION = 90 # [deg]
#.....................................................End of Global Constants............................................

#......................................................Callback Functions ...............................................   
def PoseCallback(msg): # Read the pose of the mattro
    global euler, position, header_info

    header_info[0] = msg.header.seq
    header_info[1] = msg.header.stamp
    header_info[2] = msg.header.frame_id

    position[0] = msg.twist.linear.x
    position[1] = msg.twist.linear.y
    position[2] = msg.twist.linear.z

    euler[0] = msg.twist.angular.x
    euler[1] = msg.twist.angular.y
    euler[2] = msg.twist.angular.z
#...................................................End of Callback Functions ...........................................

#...................................................User-defined Functions ..............................................
def square_path(loop_rate):
    global header_info, euler, position
    print("SquarePathNode: up and running")

    # Create a Twist message
    cmd_vel_msg = Twist()
    travel = 0
    
    while not rospy.is_shutdown():

        for i in range(4):
            if state == 0:
                starting_position = np.array([position[0], position[1]])

                cmd_vel_msg.linear.x = 0.0
                cmd_vel_msg.linear.y = 0.0
                cmd_vel_msg.linear.z = 0.0

                cmd_vel_msg.angular.x = 0.0
                cmd_vel_msg.angular.y = 0.0
                cmd_vel_msg.angular.z = 0.0

                state = 1

            if state == 1:
                current_position = np.array([position[0], position[1]])
                travel = np.linalg.norm(current_position - starting_position)
                
                if travel >= EDGE_LENGHT:
                    cmd_vel_msg.linear.x = 0.0
                    cmd_vel_msg.linear.y = 0.0
                    cmd_vel_msg.linear.z = 0.0

                    cmd_vel_msg.angular.x = 0.0
                    cmd_vel_msg.angular.y = 0.0
                    cmd_vel_msg.angular.z = 0.0

                    state = 2

                cmd_vel_msg.linear.x = 0.1
                cmd_vel_msg.linear.y = 0.0
                cmd_vel_msg.linear.z = 0.0

                cmd_vel_msg.angular.x = 0.0
                cmd_vel_msg.angular.y = 0.0
                cmd_vel_msg.angular.z = 0.0
            
            if state == 3:
                starting_heading = euler[3]
                
                cmd_vel_msg.linear.x = 0.0
                cmd_vel_msg.linear.y = 0.0
                cmd_vel_msg.linear.z = 0.0

                cmd_vel_msg.angular.x = 0.0
                cmd_vel_msg.angular.y = 0.0
                cmd_vel_msg.angular.z = 0.0
                
                state = 4
            
            if state == 4:
                current_heading = euler[3]
                rotation = current_heading - starting_heading
                
                if rotation >= ANGULAR_ROTATION:
                    cmd_vel_msg.linear.x = 0.0
                    cmd_vel_msg.linear.y = 0.0
                    cmd_vel_msg.linear.z = 0.0

                    cmd_vel_msg.angular.x = 0.0
                    cmd_vel_msg.angular.y = 0.0
                    cmd_vel_msg.angular.z = 0.0

                    state = 0
                    i += 1

                cmd_vel_msg.linear.x = 0.0
                cmd_vel_msg.linear.y = 0.0
                cmd_vel_msg.linear.z = 0.0

                cmd_vel_msg.angular.x = 0.0
                cmd_vel_msg.angular.y = 0.0
                cmd_vel_msg.angular.z = 0.1

            # Publish the ROS message
            pub1.publish(cmd_vel_msg)
            loop_rate.sleep()
        
    print("Shutting down ...")
    print("\n Node terminated")
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':
    nodeRate = 10

    try:
        print("Try running node")
        rospy.init_node('mattro_navigation_test', anonymous=True)
        loop_rate = rospy.Rate(nodeRate)

        # Define ROS publishers and Subscribers
        sub1 = rospy.Subscriber("/mattro/pose", TwistStamped, PoseCallback)
        pub1 = rospy.Publisher("/mattro/cmd_vel", Twist, queue_size = 10)
        
        square_path(loop_rate)

    except rospy.ROSInterruptException:
        print("Node terminated")
#................................................End of Main Function......................................................... 