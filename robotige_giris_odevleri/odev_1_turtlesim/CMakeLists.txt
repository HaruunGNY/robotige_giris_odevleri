cmake_minimum_required(VERSION 3.0.2)
project(odev_1_turtlesim)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  geometry_msgs
  turtlesim
)

catkin_package(
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/kaplumbaga_takip_ve_hareket.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
