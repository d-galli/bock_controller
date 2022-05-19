# mattro_bock_ros
This repository contains a possible ROS controller for the Mattro Bock ROVO 2 which exploits CAN communication to get and send data to the motors' drivers.
## To set up the Jetson ##
In a new termina run the following commands:

```
sudo modprobe can
sudo modprobe can_raw
sudo modprobe mttcan
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0
```