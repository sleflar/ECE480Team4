Formula 1 is an expensive and potentially dangerous sport due to the high speeds and precision required. This project focuses on developing a reliable and high-performance autonomous racing system using a 1/10th-scale F1 vehicle. The smaller scale provides a safer and more cost-effective platform for testing critical technologies such as camera and LiDAR-based perception, object detection, and lane tracking. 
The main objective of this project is to build upon the existing F1-Tenth platform and autonomous software developed by the Fall 2025 ECE 480 team. This includes verifying all hardware components such as the Jetson Nano, sensors, electronics, and controllers, and evaluating current software performance in perception, localization, mapping, and path tracking. Necessary software improvements will be developed and tested in Gazebo simulation before deployment on the physical vehicle. A complete ROS-based autonomous driving stack will be implemented, including SLAM, path planning, navigation, and obstacle avoidance, along with thorough documentation for system operation and maintenance. 
ECE480 Team 4 Setup and Running

**Setup (Only First Time)**
1.	Configure Visual Studio Code to connect to SSH. Instructions can be found here (complete steps 1-4)
2.	Once this is complete, you should see this screen:
   <img width="835" height="317" alt="image" src="https://github.com/user-attachments/assets/61929db9-e6ed-4c45-b51b-03fda23324e2" />

3.  Select Open Folder…, and then select the home folder (/mnt/home/<netid>)
4.	Go to https://ondemand.hpcc.msu.edu, on top menu bar select Interactive Apps-> Interactive Desktop. Here you can change settings for the session, but the default settings should work fine. Select launch to start session.
5.	Once your session is ready, you can open your remote desktop. Access the menu in the top left corner and select System Tools->AT&T KornShell to pull up a terminal.
6.	To clone the GitHub repo into your workstation, use command:
   git clone git@github.com:sleflar/ECE480Team4.git (if using SSH keys) OR 
git clone https://github.com/sleflar/ECE480Team4.git (if using GitHub PAT)
7.	In VS Code, you should now see the GitHub Repo inside of your home folder. Move the .bashrc and .rosinit files from the top level of the repo to your home folder.
8.	From anywhere in your terminal, enter command: source ~/.bashrc
This will open the bash terminal and allow you to run many different tasks 
9.	Once you have the bash terminal open, enter command: humble_pull.
10.	Enter command: humble_shell. This will make a new line Singularity> appear. When it does, enter command: source ~/.rosinit. This will open a ROS shell in the terminal that will allow you to run ROS nodes.


**Running (Every Time)**

1.	Go to https://ondemand.hpcc.msu.edu, on top menu bar select Interactive Apps-> Interactive Desktop. Here you can change settings for the session, but the default settings should work fine. Select launch to start session.
2.	Once your session is ready, you can open your remote desktop. Access the menu in the top left corner, and select System Tools->AT&T KornShell to pull up a terminal.
3.	From anywhere in your terminal, enter command: source ~/.bashrc
4.	Enter command: humble_shell. This will make a new line <Singularity> appear. When it does, enter command: source ~/.rosinit. 
5.	Navigate to ros_ws in the project repository
6.	From the ros_ws folder, enter command: colcon build --symlink-install. This builds all packages in the workspace (can also add --packages-select <package names> if you only want to build specific packages). Building is only necessary after files have been added or deleted.
7.	After building, enter command: source install/setup.bash
8.	To run the launch file that will launch the simulation (lane detection, curvy_road, and follow_pid), enter command: ros2 launch lane_follow lane_follow.launch.py. (individual nodes can be ran using ros2 run <package name> <node name>)

