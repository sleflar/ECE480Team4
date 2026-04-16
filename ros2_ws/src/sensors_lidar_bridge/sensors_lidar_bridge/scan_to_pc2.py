#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2
import laser_geometry.laser_geometry as lg

class LaserScanToCloud(Node):
    def __init__(self):
        super().__init__('laser_scan_to_cloud')
        self.lp = lg.LaserProjection()
        self.sub = self.create_subscription(LaserScan, '/lidar/scan_raw', self.callback, 10)
        self.pub = self.create_publisher(PointCloud2, '/scan_points', 10)
        self.get_logger().info("LaserScan → PointCloud2 bridge initialized")

    def callback(self, scan: LaserScan):
        try:
            cloud = self.lp.projectLaser(scan)
            cloud.header.frame_id = scan.header.frame_id
            self.pub.publish(cloud)
        except Exception as e:
            self.get_logger().error(f"Conversion error: {e}")

def main():
    rclpy.init()
    node = LaserScanToCloud()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
