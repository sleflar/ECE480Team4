import os
import launch
import launch_ros.actions
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    
    # Find the path to the package and specify the JSON file relative to this
    json_path = os.path.join(
        get_package_share_directory('bot_slam'),
        'config',
        'waypoints.json'
    )

    # Launch the nodes
    return launch.LaunchDescription([
        launch_ros.actions.Node(
            package='bot_slam',
            executable='waypoint_follower',  
            name='waypoint_follower',  # override default node name
            parameters=[{'waypoint_file_path': json_path}],
        )
    ])
