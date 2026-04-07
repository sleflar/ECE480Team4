from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Launch args
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Your custom world
    world = PathJoinSubstitution([
        FindPackageShare('gazebo_world'),
        'worlds',
        'my_world.sdf'
    ])

    # Gazebo launch (from ros_gz)
    gz_sim = PathJoinSubstitution([
        FindPackageShare('ros_gz_sim'),
        'launch',
        'gz_sim.launch.py'
    ])

    # TurtleBot3 spawn launch
    tb3_spawn = PathJoinSubstitution([
        FindPackageShare('turtlebot3_gazebo'),
        'launch',
        'robot_state_publisher.launch.py'
    ])

    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true'
        ),

        # Start Gazebo with your world
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_sim),
            launch_arguments={
                'gz_args': world
            }.items()
        ),

        # Spawn TurtleBot3
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(tb3_spawn),
            launch_arguments={
                'use_sim_time': use_sim_time
            }.items()
        ),
    ])