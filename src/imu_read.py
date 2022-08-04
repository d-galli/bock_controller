#!/usr/bin/env python3

# Filename:                     imu_read.py
# Creation Date:                04/07/2022
# Last Revision Date:           04/07/2022
# Author(s) [email]:			Davide Galli [dgalli@unibz.it]
# Revisor(s) {Date}:        	
# Organization/Institution:	    Free Univerisity of Bozen/Bolzano
# Status:                       To be tested
# Notes:                        

#.............................................About can_read.py.....................................................
# This code is aimed to read the data from the IMU and adapt them according to the robot set up. Then, this information
# are publihed over the topic "/mattro/orientation".
#
#
# Inputs [subscribers]: /filtered/quaternions
#                       
# Outputs [publishers]: /mattro/orientation
#                  
#...........................................Included Libraries and Message Types.........................................
from turtle import pos
import rospy

import numpy as np

from scipy.spatial.transform import Rotation
from geometry_msgs.msg import QuaternionStamped
from geometry_msgs.msg import TwistStamped


#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
header_info = []

quat = np.zeros(4)
#.....................................................End of Global Variables............................................
 
#......................................................Callback Functions ...............................................   
def QuaternionCallback(msg): # Read data form /filter/quaternion
    global quat, header_info
    
    header_info[0] = msg.header.seq
    header_info[1] = msg.header.stamp
    header_info[2] = "mattro_bock"

    quat[0] = msg.quaternion.x
    quat[1] = msg.quaternion.y
    quat[2] = msg.quaternion.z
    quat[3] = msg.quaternion.z
#...................................................End of Callback Functions ...........................................

#...................................................User-defined Functions ..............................................
def Quaternion2Euler(quat):

    rot = Rotation.from_quat(quat)
    euler = rot.as_euler('xyz', degrees = True)
    
    return np.array(euler)

def publish_pose():
    global header_info, quat
    print("IMUDataNode: up and running")

    # Create a Pose message
    pose_msg = TwistStamped()
    
    while not rospy.is_shutdown():

        eul = Quaternion2Euler(quat)
        
        pose_msg.header.seq = header_info[0]
        pose_msg.header.time = header_info[1]
        pose_msg.header.frame_id = header_info[2]

        pose_msg.twist.linear.x = 0.0
        pose_msg.twist.linear.y = 0.0
        pose_msg.twist.linear.z = 0.0

        pose_msg.twist.angular.x = eul[0]
        pose_msg.twist.angular.y = eul[1]
        pose_msg.twist.angular.z = eul[2]

        # Publish the ROS message
        pub1.publish(pose_msg)

    print("\n Node terminated")
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':
    nodeRate = 10

    try:
        print("Try running node")
        rospy.init_node('imu_read', anonymous=True)
        loop_rate = rospy.Rate(nodeRate)

        # Define ROS publishers and Subscribers
        sub1 = rospy.Subscriber("/filter/quaternion", QuaternionStamped, QuaternionCallback)
        pub1 = rospy.Publisher("/mattro/pose", TwistStamped, queue_size = 10)
        
        publish_pose()

    except rospy.ROSInterruptException:
        print("Node terminated")
#................................................End of Main Function......................................................... 
