#!/usr/bin/env python3
import rospy
import tf
import tf2_ros
import geometry_msgs.msg
import numpy as np


def mattro_tf():
    print("Mattro Bock TF broadcasting: up and running")

    while not rospy.is_shutdown():
        broadcaster = tf2_ros.StaticTransformBroadcaster()
        static_transformStamped = geometry_msgs.msg.TransformStamped()

        static_transformStamped.header.stamp = rospy.Time.now()
        static_transformStamped.header.frame_id = "control_box_link"
        static_transformStamped.child_frame_id = "mattro_base_link"
        static_transformStamped.transform.translation.x = -0.1600
        static_transformStamped.transform.translation.y = +0.2000
        static_transformStamped.transform.translation.z = +0.1850

        quat = tf.transformations.quaternion_from_euler(np.pi, 0.0, 0.0)
        static_transformStamped.transform.rotation.x = quat[0]
        static_transformStamped.transform.rotation.y = quat[1]
        static_transformStamped.transform.rotation.z = quat[2]
        static_transformStamped.transform.rotation.w = quat[3]

        broadcaster.sendTransform(static_transformStamped)


if __name__ == '__main__':
    rospy.init_node('mattro_tf_braodcaster')


    try:
        mattro_tf()
        rospy.spin()

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        pass