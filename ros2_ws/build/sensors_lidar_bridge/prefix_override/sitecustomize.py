import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/mnt/home/leflarsa/av/ECE480Team4/ros2_ws/install/sensors_lidar_bridge'
