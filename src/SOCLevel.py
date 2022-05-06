#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 11:15:30 2022
@author: @dgalli
Institution: Free University of Bozen/Bolzano
Degree: Master in Industrial Mechanical Engineer
"""

import rospy
from std_msgs.msg import Float32

def SOClevel():
    
    # create robot object
    bock = mattro_bock.MattroBock()

    # Connect to the robot
    rospy.loginfo("Connecting to the Bock...")
    bock.connect()
    rospy.loginfo("Bock connected.")
    
    # Print the SOC level
        
    level_str = bock.state_of_charge
        
    pub.publish(level_str)
    rate.sleep()

if __name__ == '__main__':
    try:
        pub = rospy.Publisher('SOC_level', Float32, queue_size=10)
        rospy.init_node('talker', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
        SOClevel()
    except rospy.ROSInterruptException:
        pass