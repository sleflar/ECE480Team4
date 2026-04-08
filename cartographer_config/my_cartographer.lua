-- cartographer_2d_config.lua

include "map_builder.lua"
include "trajectory_builder.lua"

-------------------------
-- 1. Enable 2D SLAM
-------------------------


-------------------------
-- 2. General options
-------------------------
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
-------------------------
-- 3. Pose graph configuration
-------------------------
MAP_BUILDER.pose_graph = {
  optimize_every_n_nodes = 90,

  -- Constraint builder: only constraint-related keys
  constraint_builder = {
    sampling_ratio = 0.3,
    max_constraint_distance = 15.0,
    min_score = 0.55,
    global_localization_min_score = 0.6,
    loop_closure_translation_weight = 1e5,
    huber_scale = 1e2,
    acceleration_weight = 1e3,
    rotation_weight = 1e5,
    local_slam_pose_translation_weight = 1e5,
    local_slam_pose_rotation_weight = 1e5,
    odometry_translation_weight = 1e5,
    odometry_rotation_weight = 1e5,
    loop_closure_translation_weight = 1e5,
    loop_closure_rotation_weight = 1e5,
    log_matches = true,
  },

  -- Optimization problem: all weights + log_matches
  optimization_problem = {
    
  },

  -- Publish periods
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 0.005,
  trajectory_publish_period_sec = 0.03,
}

-------------------------
-- 4. 2D Trajectory builder scan matchers
-------------------------
MAP_BUILDER.pose_graph.constraint_builder.fast_correlative_scan_matcher = {
  linear_search_window = 0.1,
  angular_search_window = math.rad(30.),
  branch_and_bound_depth = 7,
}
MAP_BUILDER.pose_graph.constraint_builder.fast_correlative_scan_matcher_3d = {
  linear_xy_search_window = 0.0,
  linear_z_search_window = 0.0,
  angular_search_window = math.rad(30.),
  branch_and_bound_depth = 7,
  full_resolution_depth = 100,
  min_rotational_score = 0.1,       -- number, example typical value
  min_low_resolution_score = 0.55,  -- number, usually required
}
MAP_BUILDER.pose_graph.constraint_builder.ceres_scan_matcher = {
  occupied_space_weight = 20.,
  translation_weight = 10.,
  rotation_weight = 40.,
  ceres_solver_options = {
    use_nonmonotonic_steps = false,
    max_num_iterations = 20,
    num_threads = 1,
  },
}
MAP_BUILDER.pose_graph.constraint_builder.ceres_scan_matcher_3d = {
  only_optimize_yaw = false,
  occupied_space_weight = 20.0,
  translation_weight = 10.0,
  rotation_weight = 40.0,
  ceres_solver_options = {
    use_nonmonotonic_steps = false,
    max_num_iterations = 20,
    num_threads = 1,
  },
}

-------------------------
-- 5. Return the options
-------------------------
return options
