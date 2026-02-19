from setuptools import setup, find_packages

package_name = 'perception_ml_node'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + '/scripts', ['perception_ml_node/scripts/run_yolopv2_demo.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Tushig',
    maintainer_email='you@example.com',
    description='Offline YOLOPv2 perception demo node',
    license='MIT',
)

