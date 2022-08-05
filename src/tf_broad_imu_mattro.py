#!/usr/bin/env python3
import roslib
import rospy

import tf
import geometry_msgs.msg
import numpy as np

def control_box_pose():
    while not rospy.is_shutdown():

        br = tf.TransformBroadcaster()
        br.sendTransform((-0.249, -0.229, 32.5), # in m
                        tf.transformations.quaternion_from_euler(0,+ 180, 0),
                        rospy.Time.now(),
                        'control_box_link',
                        'link0')



if __name__ == '__main__':
    rospy.init_node('control_box_tf_braodcaster')


    try:
        print("Broadcasting ...")
        control_box_pose()
        rospy.spin()

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        pass