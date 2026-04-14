<<<<<<< HEAD
# Install script for directory: /mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/src/gazebo_world

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/mnt/ffs24/home/ramosriv/av/ECE480Team4/install/gazebo_world")
=======
# Install script for directory: /home/eceteam4/ECE480Team4/ros2_ws/src/gazebo_world

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/eceteam4/ECE480Team4/install/gazebo_world")
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

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

<<<<<<< HEAD
if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
=======
if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
<<<<<<< HEAD
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world" TYPE DIRECTORY FILES
    "/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/src/gazebo_world/launch"
    "/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/src/gazebo_world/worlds"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/package_run_dependencies" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_index/share/ament_index/resource_index/package_run_dependencies/gazebo_world")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/parent_prefix_path" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_index/share/ament_index/resource_index/parent_prefix_path/gazebo_world")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world/environment" TYPE FILE FILES "/opt/ros/humble/share/ament_cmake_core/cmake/environment_hooks/environment/ament_prefix_path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world/environment" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_environment_hooks/ament_prefix_path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world/environment" TYPE FILE FILES "/opt/ros/humble/share/ament_cmake_core/cmake/environment_hooks/environment/path.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world/environment" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_environment_hooks/path.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_environment_hooks/local_setup.bash")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_environment_hooks/local_setup.sh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_environment_hooks/local_setup.zsh")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_environment_hooks/local_setup.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_environment_hooks/package.dsv")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ament_index/resource_index/packages" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_index/share/ament_index/resource_index/packages/gazebo_world")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world/cmake" TYPE FILE FILES
    "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_core/gazebo_worldConfig.cmake"
    "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/ament_cmake_core/gazebo_worldConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gazebo_world" TYPE FILE FILES "/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/src/gazebo_world/package.xml")
=======
>>>>>>> 9dcdb3f839bcf62dc81c195d20256160f57d338c
  include("/home/eceteam4/ECE480Team4/build/gazebo_world/ament_cmake_symlink_install/ament_cmake_symlink_install.cmake")
>>>>>>> d7d4bd6415b85d674601d5be4de5f809193d7f1c
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
<<<<<<< HEAD
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/home/eceteam4/ECE480Team4/build/gazebo_world/install_local_manifest.txt"
=======
<<<<<<< HEAD
file(WRITE "/mnt/ffs24/home/ramosriv/av/ECE480Team4/build/gazebo_world/${CMAKE_INSTALL_MANIFEST}"
=======
file(WRITE "/home/eceteam4/ECE480Team4/build/gazebo_world/${CMAKE_INSTALL_MANIFEST}"
>>>>>>> d7d4bd6415b85d674601d5be4de5f809193d7f1c
>>>>>>> 9dcdb3f839bcf62dc81c195d20256160f57d338c
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
if(CMAKE_INSTALL_COMPONENT)
  if(CMAKE_INSTALL_COMPONENT MATCHES "^[a-zA-Z0-9_.+-]+$")
    set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
  else()
    string(MD5 CMAKE_INST_COMP_HASH "${CMAKE_INSTALL_COMPONENT}")
    set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INST_COMP_HASH}.txt")
    unset(CMAKE_INST_COMP_HASH)
  endif()
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/home/eceteam4/ECE480Team4/build/gazebo_world/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
