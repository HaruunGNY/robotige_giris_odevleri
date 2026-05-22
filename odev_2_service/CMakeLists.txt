cmake_minimum_required(VERSION 3.0.2)
project(odev_2_service)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

add_service_files(
  FILES
  DikdortgenAlan.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs message_runtime
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

catkin_install_python(PROGRAMS
  scripts/alan_sunucu.py
  scripts/alan_istemci.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
