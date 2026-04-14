#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np

class LiDARRacingSimple(Node):
    def __init__(self):
        super().__init__('lidar_racing_simple')
        
        self.declare_parameter('max_speed', 0.5)
        self.declare_parameter('lookahead', 1.5)
        
        self.max_speed = self.get_parameter('max_speed').value
        self.lookahead = self.get_parameter('lookahead').value
        
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.get_logger().info('Simple LiDAR racing started')
    
    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)
        angles = np.arange(len(ranges)) * msg.angle_increment + msg.angle_min
        
        # Filter valid points
        valid = (ranges < np.inf) & (ranges > 0.1)
        ranges = ranges[valid]
        angles = angles[valid]
        
        if len(ranges) == 0:
            self.stop()
            return
        
        # Convert to cartesian
        x = ranges * np.cos(angles)
        y = ranges * np.sin(angles)
        
        # Find left and right boundaries
        left = y > 0.1
        right = y < -0.1
        
        if not np.any(left) or not np.any(right):
            self.stop()
            return
        
        # Find closest points at lookahead distance
        left_x = x[left]
        left_y = y[left]
        right_x = x[right]
        right_y = y[right]
        
        # Target: between left and right, biased toward inside of turn
        target_x = np.mean([np.mean(left_x), np.mean(right_x)])
        target_y = np.mean([np.mean(left_y), np.mean(right_y)])
        
        # Detect turn direction
        if abs(target_y) > 0.2:  # Turning
            # Bias toward inside
            if target_y > 0:  # Left turn
                target_y *= 0.7  # Move right (inside)
            else:  # Right turn
                target_y *= 0.7  # Move left (inside)
        
        # Compute steering
        angle = np.arctan2(target_y, target_x)
        
        # Compute speed based on angle
        speed = self.max_speed * (1.0 - 0.5 * abs(angle))
        speed = max(0.2, speed)
        
        # Publish command
        cmd = Twist()
        cmd.linear.x = speed
        cmd.angular.z = 2.0 * angle
        self.cmd_pub.publish(cmd)
        
        self.get_logger().info(f'Speed: {speed:.2f}, Angle: {angle:.2f}', throttle_duration_sec=1.0)
    
    def stop(self):
        cmd = Twist()
        self.cmd_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = LiDARRacingSimple()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()