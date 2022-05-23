#!/usr/bin/env python

# Filename:                     bock_control_fms.py
# Creation Date:                23/05/2022
# Last Revision Date:           23/05/2022
# Author(s) [email]:			Davide Galli [dgalli@unibz.it]
# Revisor(s) {Date}:        	
# Organization/Institution:	Free Univerisity of Bozen/Bolzano
# Status:                       Work in progress

#.............................................About wildlife_odom.py.....................................................
# This node contains the Finite State Machine which manages the Mattro Bock operation.

# Inputs [subscribers]: bock_status
# Outputs [publishers]: bock_status
#                       messages over CAN
#...........................................Included Libraries and Message Types.........................................
import rospy
import can
from can import Message
from msg import BockStatus
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
speed_left_target = 0.0
speed_right_target = 0.0
gear_target = 0

speed_left = 0.0
speed_right = 0.0
        
state_of_activation = 0
random_number = 0.0
shift_value = 0
activation_code = 0
gear = 0
state_of_charge = 0.0

running_read = False
running_write = False
#.....................................................End of Global Variables............................................

#......................................................Callback Functions ...............................................   
def StatusCallback(data):
    global speed_left_target, speed_right_target, gear_target, speed_left, speed_right, state_of_activation
    global random_number, shift_value, activation_code, gear, state_of_charge, running_read, running_write

    # Parse the message
    speed_left_target = data.speed_left_target
    speed_right_target = data.speed_right_target
    gear_target = data.gear_target

    speed_left = data.speed_left
    speed_right = data.speed_right
        
    state_of_activation = data.state_of_activation
    random_number = data.random_number
    shift_value = data.shift_value
    activation_code = data.activation_code
    gear = data.gear
    state_of_charge = data.state_of_charge

    running_read = data.running_read
    running_write = data.running_write
#...................................................End of Callback Functions ...........................................

#...................................................User-defined Functions ..............................................
    
#.............................................End of User-defined Functions .............................................

#.................................................Finite State Machine...................................................
def Bock_FMS():
    # Import all the global variables
    global speed_left_target, speed_right_target, gear_target, speed_left, speed_right, state_of_activation
    global random_number, shift_value, activation_code, gear, state_of_charge, running_read, running_write
    
    # Initilise the Finite State Machine
    state = 0

    # Define CAN network
    bock_can = can.interface.Bus(channel = 'can0', bustype = 'socketcan_ctypes')

    # Create a BockStatus message
    status_msg = BockStatus()

    while not rospy.is_shutdown():
        if True:
            if state == 0: # Initialise the node
                rospy.loginfo("State: Initalise")
                print("Node initiated")
                # Initialise local variables
                state_of_activation = 0
                state = 1
            
            if state == 2: # Connect to Mattro Bock
                rospy.loginfo("State: Connect")
                print("Connecting to the Bock...")
                # Send request of activation
                connect_msg = Message(arbitration_id=0x195, data=[0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
                bock_can.send(connect_msg)
                print("Activation request sent")

                # Start reading CAN messages
                status_msg.running_read = True

                # Publish the ROS message
                pub1.publish(status_msg)
        
                # Wait for "state_of_activation==2"
                while state_of_activation != 2:
                    bock_can.send(connect_msg)
                    rospy.sleep(0.1)
                    print("State of activation: ", state_of_activation," Activation code: ", activation_code)
                    pass
        
                # Send the activation message
                activ_msg = Message(arbitration_id=0x195, data=[0x02, 0x00, 0x00, activation_code, 0x00, 0x00, 0x00, 0x00])
                bock_can.send(activ_msg)
                print("Activation message sent")
                
                # Wait for "state_of_activation==3"
                while state_of_activation != 3:
                    pass

                print("Bock connected")
                state = 3
            
            if state == 3:
                rospy.loginfo("State: operate")
                state = 4
            
            if state == 4:
                rospy.loginfo("State: Disconnect")
                print("Disconnecting from the Bock...")
                
        
                # Set the speed to zero
                status_msg.speed_left_target = 0
                status_msg.speed_right_target = 0
                
                # Publish the ROS message
                pub1.publish(status_msg)

                # Put the robot in park mode as soon the speed is zero
                while(speed_left > 0 or speed_right > 0):
                    pass

                status_msg.gear_target = 0
                # Publish the ROS message
                pub1.publish(status_msg)

                while(gear != 0):
                    pass
            
                # Stop all the threads
                status_msg.running_read = False
                status_msg.running_write = False

                # Publish the ROS message
                pub1.publish(status_msg)
                
                print("Bock disconnected")
                state = 5

            if state == 5:
                rospy.loginfo("State: Terminate")
                print("Node ready to be terminated")        
            
            if state == 50:
                rospy.loginfo("State: Error")
                pass

#.............................................End of Finite State Machine.................................................

#......................................................Main Function......................................................
if __name__ == '__main__':
    nodeRate = 10

    try:
        rospy.loginfo("Try running node")
        rospy.init_node('can_read', anonymous=True)
        loop_rate = rospy.Rate(nodeRate)

        # Define ROS publishers and Subscribers
        pub1 = rospy.Publisher("/mattro/bock_status", BockStatus, queue_size = 10)
        sub1 = rospy.Subscriber("/mattro/bock_status", BockStatus, StatusCallback)
        
        Bock_FMS()

    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")
#................................................End of Main Function......................................................... 
