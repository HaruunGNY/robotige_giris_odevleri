cmake_minimum_required(VERSION 3.0.2)
project(final_odev)

find_package(catkin REQUIRED COMPONENTS
  rospy
  actionlib
  move_base_msgs
  sensor_msgs
  geometry_msgs
  std_msgs
  cv_bridge
)

catkin_package()

catkin_install_python(PROGRAMS
  src/task_manager.py
  src/qr_reader.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
