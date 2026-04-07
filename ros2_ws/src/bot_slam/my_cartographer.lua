include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,

  map_frame = "map",
  tracking_frame = "base_link",
  published_frame = "base_link",
  odom_frame = "odom",

  provide_odom_frame = true,
  use_odometry = false,
  use_imu_data = false,

  num_laser_scans = 1,
  num_multi_echo_laser_scans = 0,

  lookup_transform_timeout_sec = 0.2,
}

MAP_BUILDER.use_trajectory_builder_2d = true
TRAJECTORY_BUILDER_2D.use_imu_data = false

return options
