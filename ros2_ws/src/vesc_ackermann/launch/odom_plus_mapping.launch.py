import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    config_dir = '/home/eceteam4/ECE480Team4/cartographer_config'
    config_file = 'my_robot.lua'

    # Start the static transform publisher immediately
    static_tf_node = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='static_transform_publisher',
        output='screen',
        arguments=['0.2', '0', '0.1', '0', '0', '0', 'base_link', 'laser']
    )

    # Launch VESC to odom node immediately
    vesc_node = ExecuteProcess(
        cmd=['ros2', 'launch', 'vesc_ackermann', 'vesc_to_odom_node.launch.xml'],
        output='screen'
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
                ('/kiss/odometry', '/odom')
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
                ('/kiss/odometry', '/odom')
            ]
            )
        ]
    )

    return LaunchDescription([
        static_tf_node,
        vesc_node,
        cartographer_node,
        cartographer_occupancy_node
    ])
