# ROS Controller for Mattro Bock Rovo 2
*Study Project of Galli Davide*

*Free University of Bolzano - Master in Industrial Engineering*
## Introduction to the project
This repository contains a ROS controller written in Python for the Mattro Bock ROVO 2. It exploits the CAN Bus communication to get and send data to the motors' drivers in order to drive the robot. 

## Initial set up the Jetson TX2 ##
To enable CAN Bus, some kernel modules must be loaded, hence in a new terminal, run the following commands:

```
sudo modprobe can
sudo modprobe can_raw
sudo modprobe mttcan
```
Once the modules are loaded, the actual CAN interface can be set up. 

Again, in a terminal run:
```
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0
```
To enable the IMU over USB, in a terminal run:
```
sudo chmod a+rw /dev/ttyUSB
```

## To run the controller

Once the CAN interface is up and running, to launch the controller, run the followin in a terminal:
```
roslaunch bock_controller bock_controller.launch
```
