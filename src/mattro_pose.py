#!/usr/bin/env python3

# Filename:                     mattro_pose.py
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
#                       /pozyx
#                       
# Outputs [publishers]: /mattro/orientation
#                  
#...........................................Included Libraries and Message Types.........................................
from turtle import pos
import rospy

import numpy as np

from geometry_msgs.msg import QuaternionStamped
from geometry_msgs.msg import TwistStamped
from geometry_msgs.msg import Pose


#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
header_info = [0,0,0]

quat = np.zeros(4)

position = np.zeros(3)
#.....................................................End of Global Variables............................................
 
#......................................................Callback Functions ...............................................   
def ImuCallback(msg): # Read data from the IMU
    global quat, header_info
    
    header_info[0] = msg.header.seq
    header_info[1] = msg.header.stamp
    header_info[2] = "mattro_bock"

    quat[0] = msg.quaternion.x
    quat[1] = msg.quaternion.y
    quat[2] = msg.quaternion.z
    quat[3] = msg.quaternion.w

def ImuCallback(msg): # Read data fom Pozyx
    global position
    
    position[0] = msg.point.x
    position[1] = msg.point.y
    position[2] = msg.point.z
#...................................................End of Callback Functions ...........................................

#...................................................User-defined Functions ..............................................
def Quaternion2Euler(quat):

    x = quat[0]
    y = quat[1]
    z = quat[2]
    w = quat[3]

    ysqr = y * y

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + ysqr)
    X = np.degrees(np.arctan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = np.where(t2>+1.0,+1.0,t2)
    #t2 = +1.0 if t2 > +1.0 else t2

    t2 = np.where(t2<-1.0, -1.0, t2)
    #t2 = -1.0 if t2 < -1.0 else t2
    Y = np.degrees(np.arcsin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (ysqr + z * z)
    Z = np.degrees(np.arctan2(t3, t4))

    euler = np.array([X, Y, Z])
    
    return euler

def publish_pose():
    global header_info, quat, position
    print("IMUDataNode: up and running")

    # Create a Pose message
    pose_msg = TwistStamped()
    
    while not rospy.is_shutdown():

        eul = Quaternion2Euler(quat)
        
        pose_msg.header.seq = header_info[0]
        pose_msg.header.stamp = header_info[1]
        pose_msg.header.frame_id = header_info[2]

        pose_msg.twist.linear.x = position[0]
        pose_msg.twist.linear.y = position[1]
        pose_msg.twist.linear.z = position[2]

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
        sub1 = rospy.Subscriber("/filter/quaternion", QuaternionStamped, ImuCallback)
        sub2 = rospy.Subscriber("/pozyx", Pose, PozyxCallback)
        pub1 = rospy.Publisher("/mattro/pose", TwistStamped, queue_size = 10)
        
        publish_pose()

    except rospy.ROSInterruptException:
        print("Node terminated")
#................................................End of Main Function......................................................... 
