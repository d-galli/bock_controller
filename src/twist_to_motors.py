#!/usr/bin/env python

# Filename:                     twist_to_motors.py
# Creation Date:                23/04/2022
# Last Revision Date:           24/05/2022
# Author(s) [email]:			Davide Galli [dgalli@unibz.it]
# Revisor(s) {Date}:        	
# Organization/Institution:	Free Univerisity of Bozen/Bolzano
# Status:                       To be tested

#.............................................About wildlife_odom.py.....................................................
# This code convets a Twist message from '/mattro/cmd_vel' into the motors' target velocities published as BockStatus 
# messages over '/mattro/bock_status'. Inbetwee, it also runs a PID controller to set the target velocities.
#
# Inputs [subscribers]: /mattro/cmd_vel
# Outputs [publishers]: bock_status
#...........................................Included Libraries and Message Types.........................................
import rospy
from msg import BockStatus
from geometry_msgs.msg import Twist 
#...........................................End of Included Libraries and Message Types..................................

#.........................................................Global Variables...............................................
dx = 0.0
dy = 0.0
dr = 0.0

target = 0
motor = 0
vel = 0
integral = 0
error = 0
derivative = 0
previous_error = 0
wheel_prev = 0
wheel_latest = 0
wheel_mult = 0
prev_encoder = 0

operating = False

speed_left_target = 0.0
speed_right_target = 0.0
gear_target = 0

speed_left = 0.0
speed_right = 0.0

operating = False
#.....................................................End of Global Variables............................................

#......................................................Callback Functions ...............................................   
def TwistCallback(msg):
    global dx, dy, dr
    
    dx = msg.linear.x
    dy = msg.linear.y
    dr = msg.angular.z

def BockStatusCallback(status_msg):
    global operating, speed_left_target, speed_right_target, gear_target, speed_left, speed_right
    
    operating = status_msg.operating

    speed_left_target = status_msg.speed_left_target
    speed_right_target = status_msg.speed_right_target
    gear_target = status_msg.gear_target
    speed_left = status_msg.speed_left
    speed_right = status_msg.speed_right
#...................................................End of Callback Functions ...........................................
 
#...................................................User-defined Functions ..............................................
def motor_spin(loop_rate, Kp, Ki, Kd, out_min, out_max):
    global dx, dy, dr, operating, speed_left, speed_right
    

    prev_pid_time = rospy.Time.now()

    # Create a BockStatus message
    status_msg = BockStatus()
    
    while not rospy.is_shutdown() and operating:
            
        speed_right_diff_drive = 1.0 * dx + dr * wheel_space / 2
        speed_left_diff_drive = 1.0 * dx - dr * wheel_space / 2

        status_msg.speed_right_target, status_msg.speed_left_target = doPid(out_min, out_max, Kp, Ki, Kd, speed_left_diff_drive, speed_right_diff_drive, speed_left, speed_right)
        
        pub1.publish(status_msg)
        
        loop_rate.sleep()

def doPid(out_min, out_max, Kp, Ki, Kd, speed_left_target, speed_right_target, speed_left, speed_right):
    
    pid_dt_duration = rospy.Time.now() - prev_pid_time
    pid_dt = pid_dt_duration.to_sec()
    prev_pid_time = rospy.Time.now()
        
    right_error = speed_right_target - speed_right
    left_error = speed_left_target - speed_left
    
    right_integral = right_integral + (right_error * pid_dt)
    left_integral = left_integral + (left_error * pid_dt)

    right_derivative = (right_error - right_previous_error) / pid_dt
    left_derivative = (left_error - left_previous_error) / pid_dt
    
    right_previous_error = right_error
    left_previous_error = left_error
    
    right_motor = Kp * right_error + Ki * right_integral + Kd * right_derivative
    left_motor = Kp * left_error + Ki * left_integral + Kd * left_derivative
    
    if right_motor > out_max:
        right_motor = out_max
        right_integral = right_integral - (right_error * pid_dt)
        
    if right_motor < out_min:
        right_motor = out_min
        right_integral = right_integral - (right_error * pid_dt)
      
    if speed_right_target == 0:
        right_motor = 0
    
    if speed_left_target == 0:
        left_motor = 0
    
    return right_motor, left_motor
#.............................................End of User-defined Functions ..............................................

#......................................................Main Function......................................................
if __name__ == '__main__':

    try:
        rospy.loginfo("Try running node")
        rospy.init_node('twist_to_motor', anonymous=True)

        # Get ros parameters from the launch file
        loop_rate = rospy.get_param("~rate")
        wheel_space = rospy.get_param("~base_width")

        Kp = rospy.get_param('~Kp')
        Ki = rospy.get_param('~Ki')
        Kd = rospy.get_param('~Kd')
        
        out_min = rospy.get_param('~out_min')
        out_max = rospy.get_param('~out_max')


        # Define ROS publishers and Subscribers
        pub1 = rospy.Publisher("/mattro/bock_status", BockStatus, queue_size = 10)
        sub1 = rospy.Subscriber("/mattro/bock_status", BockStatus, BockStatusCallback)
        sub2 = rospy.Subscriber('/mattro/cmd_vel', Twist, TwistCallback)

        motor_spin(loop_rate, Kp, Ki, Kd, out_min, out_max)

    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated")
#................................................End of Main Function......................................................... 