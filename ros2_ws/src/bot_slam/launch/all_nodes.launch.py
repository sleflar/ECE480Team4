import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    config_dir = '/home/eceteam4/ECE480Team4/cartographer_config'
    config_file = 'my_robot.lua'

    args = [
        ('mode', 'bridge'),                 # bridge | serial | sim
        ('frame_id', 'laser_frame'),
        ('scan_topic_in', '/scan'),
        ('raw_topic', '/lidar/scan_raw'),
        ('sync_topic', '/sync/lidar'),
        ('serial_port', '/dev/ttyUSB0'),
        ('serial_baud', '115200'),
        ('sim_rate_hz', '10.0'),
        ('sim_angle_min', '-3.14159'),
        ('sim_angle_max', '3.14159'),
        ('sim_angle_increment', '0.00436'),
        ('sim_range_min', '0.15'),
        ('sim_range_max', '8.0'),
    ]
    declares = [DeclareLaunchArgument(k, default_value=v) for k, v in args]
    params = {k: LaunchConfiguration(k) for k, _ in args}
    # Start the static transform publisher immediately
    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        output='screen',
        arguments=['0.2', '0', '0.1', '0', '0', '0', 'base_link', 'laser']
    )
    sensors_camera_node = Node(
            package='sensors_camera_node',
            executable='sensors_camera_node',          # console script name
            name='sensors_camera_node',
            output='screen'
    )

        # Lane Detection Node
    detect_node = Node(
            package='lane_follow',
            executable='detect',          # console script name
            name='detect_node',
            output='screen'
    )
    # Launch VESC to odom node immediately
    lidar_node = Node(
            package='sensors_lidar_bridge',
            executable='sensors_lidar_bridge',
            name='sensors_lidar_bridge',
            output='screen',
            parameters=[params],
        )
    scan_to_pc2 = Node(
            package='sensors_lidar_bridge',
            executable='scan_to_pc2',
            name='scan_to_pc2',
            output='screen',
        )
    lidar_driver = Node(
            package='urg_node',
            executable='urg_node_driver',
            name='hokuyo_driver',
            output='screen',
            parameters=[{
                'ip_address': '192.168.0.10',  # replace with your LIDAR IP
                'frame_id': 'laser_frame',
                'scan_topic': '/scan',
                "ip_port": 10940,
            }]
        )
    # Delay Cartographer nodes by a few seconds to ensure TF and odom are available
    cartographer_node = TimerAction(
        period=3.0,  # wait 3 seconds
        actions=[
            Node(
                package='cartographer_ros',
                executable='cartographer_node',
                name='cartographer_node',
                output='screen',
                arguments=[
                    '-configuration_directory', config_dir,
                    '-configuration_basename', config_file
                ],
                remappings=[
                    ('/odom', '/kiss/odometry')
                ]
            )
        ]
    )

    cartographer_occupancy_node = TimerAction(
        period=3.0,  # same delay
        actions=[
            Node(
                package='cartographer_ros',
                executable='cartographer_occupancy_grid_node',
                name='cartographer_occupancy_grid_node',
                output='screen',
                arguments=[
                    '-configuration_directory', config_dir,
                    '-configuration_basename', config_file
                ],
                remappings=[
                    ('/odom', '/kiss/odometry')
                ]
            )
        ]
    )

    racing_line = TimerAction(
        period=3.0,  # same delay
        actions=[
            Node(
                package='racing_line',
                executable='lidar_racing_line_real_car',
                name='lidar_racing_line_real_car',
                output='screen',
            )
        ]
    )

    vesc_driver = TimerAction(
        period=6.0,  # same delay
        actions=[
            Node(
                package='vesc_driver',
                executable='vesc_driver_node',
                name='vesc_driver_node',
                output='screen',
            )
        ]
    )

    return LaunchDescription([
        *declares,
        static_tf_node,
        cartographer_node,
        cartographer_occupancy_node,
        lidar_node,
        scan_to_pc2,
        lidar_driver,
        vesc_driver,
        sensors_camera_node,
        detect_node,
        racing_line,
    ])
