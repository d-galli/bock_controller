#!/usr/bin/env python

# Filename:                     pub_odom_tf.py
# Creation Date:                24/05/2022
# Last Revision Date:           24/05/2022
# Author(s) [email]:			Davide Galli [dgalli@unibz.it]
# Revisor(s) {Date}:        	
# Organization/Institution:	Free Univerisity of Bozen/Bolzano
# Status:                       Not working

#.............................................About wildlife_odom.py.....................................................
# This code is aimed to read data from motors' encoders and compute the tf transformations, as well as, the odometry.
# Then  it publishes them over '/mattro/tf' and '/mattro/odom' accordingly.
# some information about robot's status over the topic "/mattro/bock_status".
# At the same time, it reads the datat pusblished on the same topic "/mattro/bock_status", and converts them into a CAN
# message to control the motors' drivers.

# Inputs [subscribers]: bock_status
#                       
# Outputs [publishers]: /mattro/tf
#                       /mattro/odom'
#...........................................Included Libraries and Message Types.........................................
import rospy
import roslib
from msg import BockStatus

from math import sin, cos, pi

from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from tf.broadcaster import TransformBroadcaster
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
operating = False

speed_left = 0.0
speed_right = 0.0
#.....................................................End of Global Variables............................................

#......................................................Callback Functions ...............................................   
def BockStatusCallback(status_msg):
    global operating, speed_left, speed_right
    
    operating = status_msg.operating

    speed_left = status_msg.speed_left
    speed_right = status_msg.speed_right
#...................................................End of Callback Functions ...........................................
 
#...................................................User-defined Functions ..............................................
def update_odom(t_next, then):
    global operating, speed_left, speed_right
    
    odomBroadcaster = TransformBroadcaster()
    
    x = 0                  # position in xy plane 
    y = 0
    z = 0
    theta = 0  
    dx = 0                 # speeds in x/rotation
    dr = 0

    while not rospy.is_shutdown():
        now = rospy.Time.now()
        if now > t_next:
            elapsed = now - then
            then = now
            elapsed = elapsed.to_sec()
            
            # calculate odometry
            if self.enc_left == None:
                d_left = 0
                d_right = 0
            else:
                d_left = (self.left - self.enc_left) / self.ticks_meter
                d_right = (self.right - self.enc_right) / self.ticks_meter
            self.enc_left = self.left
            self.enc_right = self.right
           
            # distance traveled is the average of the two wheels 
            d = ( d_left + d_right ) / 2
            # this approximation works (in radians) for small angles
            th = ( d_right - d_left ) / self.base_width
            # calculate velocities
            self.dx = d / elapsed
            self.dr = th / elapsed
           
             
            if (d != 0):
                # calculate distance traveled in x and y
                x = cos( th ) * d
                y = -sin( th ) * d
                # calculate the final position of the robot
                self.x = self.x + ( cos( self.th ) * x - sin( self.th ) * y )
                self.y = self.y + ( sin( self.th ) * x + cos( self.th ) * y )
            if( th != 0):
                self.th = self.th + th
                
            # publish the odom information
            quaternion = Quaternion()
            quaternion.x = 0.0
            quaternion.y = 0.0
            quaternion.z = sin( self.th / 2 )
            quaternion.w = cos( self.th / 2 )
            self.odomBroadcaster.sendTransform(
                (self.x, self.y, 0),
                (quaternion.x, quaternion.y, quaternion.z, quaternion.w),
                rospy.Time.now(),
                self.base_frame_id,
                self.odom_frame_id
                )
            
            odom = Odometry()
            odom.header.stamp = now
            odom.header.frame_id = self.odom_frame_id
            odom.pose.pose.position.x = self.x
            odom.pose.pose.position.y = self.y
            odom.pose.pose.position.z = 0
            odom.pose.pose.orientation = quaternion
            odom.child_frame_id = self.base_frame_id
            odom.twist.twist.linear.x = self.dx
            odom.twist.twist.linear.y = 0
            odom.twist.twist.angular.z = self.dr
            self.odomPub.publish(odom)
            pub1.publish(status_msg)
    
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':
    nodeRate = 10

    try:
        rospy.loginfo("Try running node")
        rospy.init_node('pub_odom_tf', anonymous=True)

        loop_rate = rospy.Rate(nodeRate)      
        base_frame_id = rospy.get_param('~base_frame_id','base_link') # the name of the base frame of the robot
        odom_frame_id = rospy.get_param('~odom_frame_id', 'odom') # the name of the odometry reference frame

        # Define ROS publishers and Subscribers
        pub1 = rospy.Publisher("/mattro/odom", Odometry, queue_size=10)
        sub1 = rospy.Subscriber("/mattro/bock_status", BockStatus, BockStatusCallback)

        t_next = rospy.Time.now() + rospy.Duration(1.0/loop_rate)
        then = rospy.Time.now()

        update_odom(t_next, then)

    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")
#................................................End of Main Function......................................................... 
