# generated from
# ament_cmake_core/cmake/symlink_install/ament_cmake_symlink_install_uninstall_script.cmake.in

<<<<<<< HEAD
set(install_manifest "/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/build/gazebo_world/symlink_install_manifest.txt")
=======
set(install_manifest "/home/eceteam4/ECE480Team4/ros2_ws/build/gazebo_world/symlink_install_manifest.txt")
>>>>>>> d7d4bd6415b85d674601d5be4de5f809193d7f1c
if(NOT EXISTS "${install_manifest}")
  message(FATAL_ERROR "Cannot find symlink install manifest: ${install_manifest}")
endif()

file(READ "${install_manifest}" installed_files)
string(REGEX REPLACE "\n" ";" installed_files "${installed_files}")
foreach(installed_file ${installed_files})
  if(EXISTS "${installed_file}" OR IS_SYMLINK "${installed_file}")
    message(STATUS "Uninstalling: ${installed_file}")
    file(REMOVE "${installed_file}")
    if(EXISTS "${installed_file}" OR IS_SYMLINK "${installed_file}")
      message(FATAL_ERROR "Failed to remove '${installed_file}'")
    endif()

    # remove empty parent folders
    get_filename_component(parent_path "${installed_file}" PATH)
    ament_cmake_uninstall_target_remove_empty_directories("${parent_path}")
  endif()
endforeach()
