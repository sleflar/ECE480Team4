from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'sensors_lidar_bridge'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/lidar.launch.py')),
        (os.path.join('share', package_name, 'launch'), glob('launch/lidar_mapping.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='ROS2 LiDAR bridge (bridge/serial/sim) → /lidar/scan_raw and /sync/lidar',
    license='MIT',
    entry_points={
        'console_scripts': [
            'sensors_lidar_bridge=sensors_lidar_bridge.sensors_lidar_bridge:main',
            'scan_to_pc2=sensors_lidar_bridge.scan_to_pc2:main',
        ],
    },
)
