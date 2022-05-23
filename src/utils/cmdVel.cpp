//  Filename:											      cmdVel.cpp
//  Creation Date:								      06/05/2022
//  Last Revision Date:						      06/05/2022
//  Author(s) [email]:								  Davide Galli [dgalli@unibz.it]
//  Organization/Institution:				   	Free Univeristy of Bozen/Bolzano - FiRST Lab
// 
// ...............................About cmdVel.cpp......................................
//  
//
//  Inputs and Outputs of the CPP file
//				Inputs [subscribers]: 
//				Outputs [publishers]: 


//................................................Included Libraries and Message Types..........................................

#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <iostream>
//...........................................End of Included Libraries and Message Types....................................


//.................................................................Constants.................................................
#define PI 3.14159265
#define MAX_TRACK_SPEED 20    // [km/h]
#define OUTER_WIDTH 1230      // [mm]
#define INNER_WIDTH 644       // [mm]
#define MAX_PERCENTAGE 1000   // [%]
//............................................................End of Constants...............................................

//..............................................................Global Variables.............................................
float X;        // [m/s]
float Y;        // [m/s]
float Z;        // [m/s]

float phi;     // [rad/s] -> Roll
float theta;   // [rad/s] -> Pitch
float psi;     // [rad/s] -> Yaw

double MAX_SPEED = MAX_TRACK_SPEED * 1000 / 3600; // [m/s]
double RADIOUS = 0.5 * INNER_WIDTH + 0.5 * (OUTER_WIDTH - INNER_WIDTH); // [mm] -> track middle axis 
//..............................................................End of Global Variables......................................

//..................................................................Functions................................................
void cmdVelCallback(const geometry_msgs::Twist::ConstPtr& vel_msg)
{ 

  X = vel_msg->linear.x;
  Y = vel_msg->linear.y;
  Z = vel_msg->linear.z;

  phi = vel_msg->angular.x;
  theta = vel_msg->angular.y;
  psi = vel_msg->angular.z;

  double left_track_speed = X + 0.5 * psi * RADIOUS;
  double right_track_speed =  X - 0.5 * psi * RADIOUS;

  double left_track_percentage = left_track_speed / MAX_SPEED * 100;
  double right_track_percentage = right_track_speed / MAX_SPEED * 100;

  //ROS_INFO("X: %f, Y: %f, Z: %f, Phi: %f, Theta: %f, Psi: %f", X, Y, Z, phi, theta, psi);
  //ROS_INFO("Right track speed: %d [m/s] \nLeft track speed: %d [m/s]", right_track_speed, left_track_speed);
  //std::cout << "Right track speed: "<< right_track_speed <<" [m/s]\nLeft track speed: " << left_track_speed << " [m/s]" << std::endl;
  if (left_track_percentage > MAX_PERCENTAGE){
    left_track_percentage = MAX_PERCENTAGE;
    }
  
  if (left_track_percentage < - MAX_PERCENTAGE){
    left_track_percentage = - MAX_PERCENTAGE;
    }

  if (right_track_percentage > MAX_PERCENTAGE){
    right_track_percentage = MAX_PERCENTAGE;
    }
  
  if (right_track_percentage < - MAX_PERCENTAGE){
    right_track_percentage = - MAX_PERCENTAGE;
    }

  std::cout << "Right track speed: "<< right_track_percentage <<" [%]\nLeft track speed: " << left_track_percentage << " [%]" << std::endl;
}

//..............................................................End of Functions.............................................

int main(int argc, char **argv)
{

  ros::init(argc, argv, "velocityListener");

  ros::NodeHandle node_handle;

  ros::Subscriber sub = node_handle.subscribe("cmd_vel", 1, &cmdVelCallback);

  ros::spin();

  return 0;
}
