#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped
from std_msgs.msg import Bool
from std_msgs.msg import Float64
from sensor_msgs.msg import LaserScan
import math
import time
import numpy as np


class FollowPurePursuit(Node):
    def __init__(self):
        super().__init__('follow_pure_pursuit')
        
        self.x_prev = -1
        self.y_prev = -1
        
        # Sub: ground point (lane center)
        self.subscription = self.create_subscription(
            PointStamped,
            '/ground_point',
            self.pure_pursuit_callback,
            1)
            
            
        # Sub: lidar scan  
        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/lidar/scan_raw',
            self.lidar_callback,
            1)

        # Sub: obstacle detection flag
        self.obstacle_sub = self.create_subscription(
            Bool,
            '/front_obstacle',
            self.obstacle_callback,
            10)

        # Pub: REAL CAR COMMAND TOPICS (Float64)
        self.pub_speed = self.create_publisher(Float64, '/commands/motor/speed', 10)
        self.pub_steer = self.create_publisher(Float64, '/commands/servo/position', 10)

        # Fixed motor speed command (VESC expects high Float64 values)
        self.motor_speed_command = 5000.0
        self.spot_count = 0

        # State machine
        self.reached_end = False
        self.start_time = None
        self.end_time = None
        self.no_lane_threshold = 0.001

        # Obstacle flag
        self.front_obstacle = False

        self.get_logger().info("Pure Pursuit node initialized")


    # ============================================================
    # OBSTACLE CALLBACK
    # ============================================================
    def obstacle_callback(self, msg: Bool):
        self.front_obstacle = msg.data

        if self.front_obstacle:
            self.get_logger().info("[OBSTACLE] Stopping vehicle.")
            self.stop_robot()
            
  
    def get_closest_in_range(self, msg, min_angle, max_angle):
        closest_dist = float('inf')
        closest_angle = None

        for i, r in enumerate(msg.ranges):
            if not math.isfinite(r):
                continue
            if r < msg.range_min or r > msg.range_max:
                continue

            angle = msg.angle_min + i * msg.angle_increment

            if min_angle <= angle <= max_angle:
                if r < closest_dist:
                    closest_dist = r
                    closest_angle = angle

        if closest_angle is None:
            return None, None

        return closest_dist, closest_angle
        
        
    def lidar_callback(self, msg):
        left_dist, left_ang = self.get_closest_in_range(
            msg,
            math.radians(30),
            math.radians(150)
        )

        right_dist, right_ang = self.get_closest_in_range(
            msg,
            -math.radians(150),
            -math.radians(30)
        )

        self.get_logger().info(
            f"Left: {left_dist}, Right: {right_dist}"
        )


    # ============================================================
    # MAIN PURE PURSUIT
    # ============================================================
    def pure_pursuit_callback(self, msg: PointStamped):

        # If obstacle → STOP immediately
        if self.front_obstacle:
            self.stop_robot()
            return

        # Start timer when we see the first lane point
        if self.start_time is None and not self.is_zero_point(msg.point):
            self.start_time = time.time()
            self.get_logger().info('Started lane following!')

        # Lane disappears → STOP and record time
        #if self.is_zero_point(msg.point):
            #if not self.reached_end and self.start_time is not None:
                #self.stop_robot()
                #self.reached_end = True
                #self.end_time = time.time()
                #elapsed = self.end_time - self.start_time

                #print("\n" + "="*40)
                #print("LANE FOLLOWING COMPLETE!")
                #print("="*40)
                #print(f"Speed Command: {self.motor_speed_command}")
                #print(f"Time to complete: {elapsed:.2f} seconds")
                #print("="*40 + "\n")

                #self.get_logger().info(f"Completed course in {elapsed:.2f} seconds")
            #return
        
        if self.reached_end:
            return

        # Extract lane center point
        x = msg.point.x
        y = msg.point.y
        
        if self.x_prev == -1 and self.y_prev == -1:
            self.x_prev = x
            self.y_prev = y
        
        #alpha = 0.3
        #x = alpha * x + (1-alpha) * self.x_prev
        #y = alpha * y + (1-alpha) * self.y_prev
        
        #self.x_prev = x
        #self.y_prev = y

        L = math.sqrt(x * x + y * y)
        if L < 0.01:
            self.stop_robot()
            return

        # Pure Pursuit curvature → steering
        curvature = 2.0 * y / (L * L + 1e-6) #Get rid of 1e-6 later if messing up
        steering = 290*curvature    # You can scale this later if needed
        

            
        
        

        self.spot_count += 1
        
        if self.spot_count <= 500:
            self.motor_speed_command = 10.0 * self.spot_count
        else:
            self.motor_speed_command = 5000.0

        # ================================
        # PUBLISH COMMANDS (Float64)
        # ================================
        self.pub_speed.publish(Float64(data=self.motor_speed_command))
        self.pub_steer.publish(Float64(data=float(steering)))


    # ============================================================
    def is_zero_point(self, point):
        return (abs(point.x) < self.no_lane_threshold and
                abs(point.y) < self.no_lane_threshold)


    # ============================================================
    def stop_robot(self):
        """Stop motor and steering."""
        self.pub_speed.publish(Float64(data=0.0))
        self.pub_steer.publish(Float64(data=0.0))


def main(args=None):
    rclpy.init(args=args)
    node = FollowPurePursuit()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
