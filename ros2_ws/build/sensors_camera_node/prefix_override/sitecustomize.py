import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/eceteam4/ECE480Team4/ros2_ws/install/sensors_camera_node'
