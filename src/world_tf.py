#!/usr/bin/env python3
from turtle import position
import rospy
import tf
import tf2_ros
import geometry_msgs.msg
from geometry_msgs.msg import Pose
import numpy as np

position = np.zeros(3)

def PozyxCallback(msg): # Read data fom Pozyx
    global position
    
    position[0] = msg.position.x
    position[1] = msg.position.y
    position[2] = msg.position.z

def world_tf():
    global position

    print("World TF broadcasting: up and running")

    while not rospy.is_shutdown():
        broadcaster = tf2_ros.StaticTransformBroadcaster()
        static_transformStamped = geometry_msgs.msg.TransformStamped()

        static_transformStamped.header.stamp = rospy.Time.now()
        static_transformStamped.header.frame_id = "world"
        static_transformStamped.child_frame_id = "world_imu"
        static_transformStamped.transform.translation.x = position[0]
        static_transformStamped.transform.translation.y = position[1]
        static_transformStamped.transform.translation.z = + 0.600 #position[2]


        quat = tf.transformations.quaternion_from_euler(0.0, 0.0, 0.0)
        static_transformStamped.transform.rotation.x = quat[0]
        static_transformStamped.transform.rotation.y = quat[1]
        static_transformStamped.transform.rotation.z = quat[2]
        static_transformStamped.transform.rotation.w = quat[3]

        broadcaster.sendTransform(static_transformStamped)


if __name__ == '__main__':
    rospy.init_node('world_tf_braodcaster')
    sub1 = rospy.Subscriber("/zyx", Pose, PozyxCallback)


    try:
        world_tf()
        rospy.spin()

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        pass