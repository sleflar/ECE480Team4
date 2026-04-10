import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/install/racing_line'
