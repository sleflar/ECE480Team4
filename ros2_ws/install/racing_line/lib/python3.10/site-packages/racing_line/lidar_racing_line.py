#!/usr/bin/env python3
import math
import numpy as np

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


class LiDARRacingLine(Node):
    def __init__(self):
        super().__init__('lidar_racing_line')

        # Parameters
        self.declare_parameter('max_speed', 1.0)
        self.declare_parameter('min_speed', 0.25)

        self.declare_parameter('near_lookahead', 1.0)
        self.declare_parameter('far_lookahead', 2.0)
        self.declare_parameter('lookahead_window', 0.25)

        self.declare_parameter('front_angle_deg', 120.0)
        self.declare_parameter('wall_offset', 0.10)
        self.declare_parameter('track_half_width_guess', 0.6)

        self.declare_parameter('steering_gain', 1.8)
        self.declare_parameter('max_steering', 1.2)
        self.declare_parameter('steering_smooth_alpha', 0.35)

        self.declare_parameter('racing_offset_gain', 0.5)
        self.declare_parameter('max_racing_offset', 0.35)

        self.declare_parameter('min_range', 0.08)
        self.declare_parameter('max_range', 10.0)
        self.declare_parameter('emergency_stop_distance', 0.30)

        self.max_speed = float(self.get_parameter('max_speed').value)
        self.min_speed = float(self.get_parameter('min_speed').value)

        self.near_lookahead = float(self.get_parameter('near_lookahead').value)
        self.far_lookahead = float(self.get_parameter('far_lookahead').value)
        self.lookahead_window = float(self.get_parameter('lookahead_window').value)

        self.front_angle_deg = float(self.get_parameter('front_angle_deg').value)
        self.wall_offset = float(self.get_parameter('wall_offset').value)
        self.track_half_width_guess = float(self.get_parameter('track_half_width_guess').value)

        self.steering_gain = float(self.get_parameter('steering_gain').value)
        self.max_steering = float(self.get_parameter('max_steering').value)
        self.steering_smooth_alpha = float(self.get_parameter('steering_smooth_alpha').value)

        self.racing_offset_gain = float(self.get_parameter('racing_offset_gain').value)
        self.max_racing_offset = float(self.get_parameter('max_racing_offset').value)

        self.min_range = float(self.get_parameter('min_range').value)
        self.max_range = float(self.get_parameter('max_range').value)
        self.emergency_stop_distance = float(self.get_parameter('emergency_stop_distance').value)

        self.prev_steering = 0.0
        self.prev_center_y = 0.0

        self.scan_sub = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10
        )
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        self.get_logger().info('LiDAR racing line node started')

    def get_center_at_lookahead(self, x, y, lookahead):
        band = np.abs(x - lookahead) < self.lookahead_window

        left_mask = band & (y > self.wall_offset)
        right_mask = band & (y < -self.wall_offset)

        left_y = None
        right_y = None

        if np.any(left_mask):
            left_y = float(np.median(y[left_mask]))
        if np.any(right_mask):
            right_y = float(np.median(y[right_mask]))

        if left_y is not None and right_y is not None:
            center_y = 0.5 * (left_y + right_y)
        elif left_y is not None:
            center_y = left_y - self.track_half_width_guess
        elif right_y is not None:
            center_y = right_y + self.track_half_width_guess
        else:
            center_y = self.prev_center_y

        return center_y, left_y, right_y

    def scan_callback(self, msg: LaserScan):
        ranges = np.array(msg.ranges, dtype=np.float32)
        angles = msg.angle_min + np.arange(len(ranges)) * msg.angle_increment

        valid = np.isfinite(ranges)
        valid &= (ranges > self.min_range)
        valid &= (ranges < self.max_range)

        if not np.any(valid):
            self.stop("No valid scan points")
            return

        ranges = ranges[valid]
        angles = angles[valid]

        x = ranges * np.cos(angles)
        y = ranges * np.sin(angles)

        front_half_angle = math.radians(self.front_angle_deg / 2.0)
        front_mask = (np.abs(angles) < front_half_angle) & (x > 0.0)

        if not np.any(front_mask):
            self.stop("No forward points")
            return

        x = x[front_mask]
        y = y[front_mask]

        # Emergency stop check
        narrow_front = np.abs(np.arctan2(y, x)) < math.radians(15.0)
        if np.any(narrow_front):
            front_dist = np.min(np.sqrt(x[narrow_front] ** 2 + y[narrow_front] ** 2))
            if front_dist < self.emergency_stop_distance:
                self.stop("Obstacle too close ahead")
                return

        # Find centerline at near and far distances
        near_center_y, near_left_y, near_right_y = self.get_center_at_lookahead(
            x, y, self.near_lookahead
        )
        far_center_y, far_left_y, far_right_y = self.get_center_at_lookahead(
            x, y, self.far_lookahead
        )

        self.prev_center_y = near_center_y

        # Estimate turn direction from centerline change
        # Positive curve value => track bends left
        # Negative curve value => track bends right
        curve_direction = far_center_y - near_center_y

        # Racing line offset:
        # For a left turn, start from the right side (negative offset)
        # For a right turn, start from the left side (positive offset)
        racing_offset = -self.racing_offset_gain * curve_direction
        racing_offset = max(-self.max_racing_offset, min(self.max_racing_offset, racing_offset))

        # Final target is shifted from center
        target_x = self.near_lookahead
        target_y = near_center_y + racing_offset

        heading_error = math.atan2(target_y, max(target_x, 0.1))

        steering = self.steering_gain * heading_error
        steering = max(-self.max_steering, min(self.max_steering, steering))

        # Smooth steering
        steering = (
            self.steering_smooth_alpha * steering
            + (1.0 - self.steering_smooth_alpha) * self.prev_steering
        )
        self.prev_steering = steering

        # Speed control
        turn_factor = max(0.3, 1.0 - 0.6 * abs(steering) / max(self.max_steering, 1e-6))
        speed = self.max_speed * turn_factor
        speed = max(self.min_speed, min(self.max_speed, speed))

        cmd = Twist()
        cmd.linear.x = speed
        cmd.angular.z = steering
        self.cmd_pub.publish(cmd)

        self.get_logger().info(
            f"speed={speed:.2f}, steer={steering:.2f}, "
            f"near_center={near_center_y:.2f}, far_center={far_center_y:.2f}, "
            f"curve={curve_direction:.2f}, offset={racing_offset:.2f}",
            throttle_duration_sec=1.0
        )

    def stop(self, reason="Stopping"):
        cmd = Twist()
        self.cmd_pub.publish(cmd)
        self.get_logger().warn(reason, throttle_duration_sec=1.0)


def main(args=None):
    rclpy.init(args=args)
    node = LiDARRacingLine()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()