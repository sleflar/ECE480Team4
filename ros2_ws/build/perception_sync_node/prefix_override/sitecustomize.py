import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/mnt/home/leflarsa/av/autonomous-vehicle-project/ros2_ws/install/perception_sync_node'
