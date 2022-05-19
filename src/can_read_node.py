#!/usr/bin/env python


import rospy
import mattro_bock
import os
import can
from can import Message
import time
from std_msgs.msg import String

class MattroBock:
    
    def __init__(self, channel = 'can0'):
        self.bock_can = can.interface.Bus(channel = channel, bustype = 'socketcan_ctypes')
        
        self.speed_left_target = 0
        self.speed_right_target = 0
        self.gear_target = 0
        
        self.state_of_activation = 0
        self.random_number = 0
        self.shift_value = 0
        self.activation_code = 0
        self.gear = 0
        self.state_of_charge = 0
        self.speed_left = 0
        self.speed_right = 0
        
        self._running_read = 1
        self._running_write = 1
    
    def read_threading(self):
        while self._running_read:
            # Read a message from can bus
            msg = self.bock_can.recv()
            
            # Parse messages
            if msg.arbitration_id == 0x215:
                self.state_of_activation = msg.data[0]
                self.activation_code = (msg.data[1]>>msg.data[2])
                self.gear = msg.data[5]
                self.state_of_charge = ((msg.data[7]<<8)+msg.data[6])/10.
            elif msg.arbitration_id == 0x315:
                self.speed_left = (msg.data[3]<<24)+(msg.data[2]<<16)+(msg.data[1]<<8)+msg.data[0]
                self.speed_right = (msg.data[7]<<24)+(msg.data[6]<<16)+(msg.data[5]<<8)+msg.data[4]




def read_can():

    while not rospy.is_shutdown():
            

            # Read a message from can bus
            msg = self.bock_can.recv()
            
            # Parse messages
            if msg.arbitration_id == 0x215:
                self.state_of_activation = msg.data[0]
                self.activation_code = (msg.data[1]>>msg.data[2])
                self.gear = msg.data[5]
                self.state_of_charge = ((msg.data[7]<<8)+msg.data[6])/10.
            elif msg.arbitration_id == 0x315:
                self.speed_left = (msg.data[3]<<24)+(msg.data[2]<<16)+(msg.data[1]<<8)+msg.data[0]
                self.speed_right = (msg.data[7]<<24)+(msg.data[6]<<16)+(msg.data[5]<<8)+msg.data[4]

if __name__ == '__main__':
    nodeRate = 10
    try:
        rospy.loginfo("Try running node")
        rospy.init_node('can_read', anonymous=True)
        loop_rate = rospy.Rate(nodeRate)
        pub1 = rospy.Publisher("/mattro/can_read", String, queue_size = 10)

        bock = mattro_bock.MattroBock()

        read_can(bock)

    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")