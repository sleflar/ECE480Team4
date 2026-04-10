<<<<<<< HEAD
# Install script for directory: /mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/src/gazebo_world

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/install/gazebo_world")
=======
# Install script for directory: /home/eceteam4/ECE480Team4/ros2_ws/src/gazebo_world

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/eceteam4/ECE480Team4/ros2_ws/install/gazebo_world")
>>>>>>> d7d4bd6415b85d674601d5be4de5f809193d7f1c
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
<<<<<<< HEAD
  include("/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/build/gazebo_world/ament_cmake_symlink_install/ament_cmake_symlink_install.cmake")
=======
  include("/home/eceteam4/ECE480Team4/ros2_ws/build/gazebo_world/ament_cmake_symlink_install/ament_cmake_symlink_install.cmake")
>>>>>>> d7d4bd6415b85d674601d5be4de5f809193d7f1c
endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
<<<<<<< HEAD
file(WRITE "/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/build/gazebo_world/${CMAKE_INSTALL_MANIFEST}"
=======
file(WRITE "/home/eceteam4/ECE480Team4/ros2_ws/build/gazebo_world/${CMAKE_INSTALL_MANIFEST}"
>>>>>>> d7d4bd6415b85d674601d5be4de5f809193d7f1c
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
