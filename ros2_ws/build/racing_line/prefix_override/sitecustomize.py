import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
<<<<<<< HEAD
    sys.prefix = sys.exec_prefix = '/mnt/ffs24/home/ramosriv/av/ECE480Team4/ros2_ws/install/racing_line'
=======
    sys.prefix = sys.exec_prefix = '/home/eceteam4/ECE480Team4/ros2_ws/install/racing_line'
>>>>>>> d7d4bd6415b85d674601d5be4de5f809193d7f1c
