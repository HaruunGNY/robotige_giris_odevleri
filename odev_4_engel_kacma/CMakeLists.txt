cmake_minimum_required(VERSION 3.0.2)
project(odev_4_engel_kacma)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  geometry_msgs
)

catkin_package()

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/engel_kacinma.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
