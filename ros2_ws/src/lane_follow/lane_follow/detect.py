import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped, Point
from cv_bridge import CvBridge
import cv2
import numpy as np
import os


class DetectNode(Node):
    """
    A ROS2 node to detect lane lines using OpenCV HSV color masking
    and publish a target point.
    """
    def __init__(self):
        super().__init__('detect_node')
        
        self.bridge = CvBridge()
        
        # Color Ranges for Line Detection in HSV Space (as opposed to RGB)---
        # HSV for Orange
        self.lower_orange = np.array([5, 150, 150])     # H, S, V
        self.upper_orange = np.array([25, 255, 255])

        self.lower_white = np.array([0, 0, 190])
        self.upper_white = np.array([179, 50, 255])

        # Kernel for morphological operations (for noise reduction)
        self.morph_kernel = np.ones((5, 5), np.uint8)
        
        # Lane Width Memory to Handle Sharp Turns ---
        # Initial guess for lane width in pixels. This will be updated
        # automatically whenever both lines are detected.
        self.DEFAULT_LANE_WIDTH_PX = 700 
        self.last_known_lane_width = self.DEFAULT_LANE_WIDTH_PX

        # Create Subscriber and Publishers ---
        # This allows publishing to /camera/image_processed. Messages will be of type image
        self.image_processed_pub = self.create_publisher(Image, '/camera/image_processed', 10)
        self.debug_pub = self.create_publisher(Image, '/lane/debug_image', 10)
        self.target_pub = self.create_publisher(PointStamped, '/lane_point', 10)

        """ Whenever an image is published from the topic /camera/image_raw, this subscriber will 
        recieve it and call the function image_callback. Messages are of type Image"""
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)

        self.get_logger().info('Lane detection node started (using BGR + Memory for sharp turns).')


    def image_callback(self, msg):
        """
        Callback function for the image subscriber.
        Processes the image to find the target point.
        """
        try:
            # Convert ROS Image message to OpenCV image (BGR8)
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f'Failed to convert image: {e}')
            return
        # Define Region of Interest (ROI)
        height, width, _ = cv_image.shape

        roi = cv_image[int(height * 0.8):, :]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # Detect Lines using OpenCV BGR Masking  and optionally cv2.morphologyEx ---
        mask_orange = cv2.inRange(hsv, self.lower_orange, self.upper_orange)
        mask_white = cv2.inRange(hsv, self.lower_white, self.upper_white)

        # Morphological cleanup
        mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_OPEN, self.morph_kernel)
        mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, self.morph_kernel)
        # Find Centroids ---
        def get_centroid(mask):
            M = cv2.moments(mask)
            if M["m00"] > 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                return (cx, cy)
            return None

        orange_center = get_centroid(mask_orange)
        white_center = get_centroid(mask_white)
        if white_center and orange_center and white_center[0] < orange_center[0]:
            white_center=None
        # Define PointStamped message to publish
        target_point = None
        if orange_center and white_center:
            # Both lines detected — midpoint between centroids
            lane_width_px = abs(orange_center[0] - white_center[0])
            if lane_width_px > 100:
                self.last_known_lane_width = lane_width_px  # Update lane width memory
            self.get_logger().info(str(lane_width_px))
            target_x = int((orange_center[0] + white_center[0]) / 2)
            target_y = int((orange_center[1] + white_center[1]) / 2)
            target_point = (target_x, target_y)
            debug_msg = "Both orange and white lines detected."
        elif orange_center:
            # Only orange line — estimate lane center using last known width
            target_x = orange_center[0] + int(self.last_known_lane_width/2)
            target_y = orange_center[1]
            target_point = (target_x, target_y)
            debug_msg = "Only orange line detected — extrapolated lane center."
        elif white_center:
            # Only white line — estimate lane center using last known width
            target_x = white_center[0] - int(self.last_known_lane_width/2)
            target_y = white_center[1]
            target_point = (target_x, target_y)
            debug_msg = "Only white line detected — extrapolated lane center."
        else:
            debug_msg = "No lane lines detected."
            point_msg = PointStamped()
            point_msg.header.stamp = self.get_clock().now().to_msg()
            point_msg.header.frame_id = "camera"
            point_msg.point.x = 0.0
            point_msg.point.y = 0.0
            point_msg.point.z = 0.0
            self.target_pub.publish(point_msg)

        self.get_logger().info(debug_msg)
        # Depending on whether orange or white or both or neither lines are detected,
        # compute the target point accordingly 

        self.get_logger().debug('Output the which lines were detected as a debug message.')

        # Draw visualization dot ONLY if we have a valid (non-zero) point
        vis_image = cv_image.copy()

        # Draw lane centroids (orange & white)
        if orange_center:
            cv2.circle(vis_image, orange_center, 5, (0, 140, 255), -1)
        if white_center:
            cv2.circle(vis_image, white_center, 5, (255, 255, 255), -1)

        # Draw the red dot at lane center
        if target_point:
            target_point = (target_point[0], int(height * 0.8))
            cv2.circle(vis_image, target_point, 6, (0, 0, 255), -1)

        # --- Publish visualization image to /image_processed ---
        processed_msg = self.bridge.cv2_to_imgmsg(vis_image, encoding='bgr8')
        processed_msg.header.stamp = self.get_clock().now().to_msg()
        processed_msg.header.frame_id = "camera"
        self.image_processed_pub.publish(processed_msg)
        # Publish the detected point
        if target_point:
            point_msg = PointStamped()
            point_msg.header.stamp = self.get_clock().now().to_msg()
            point_msg.header.frame_id = "camera"
            point_msg.point.x = float(target_point[0])
            point_msg.point.y = float(target_point[1])
            point_msg.point.z = 0.0
            self.target_pub.publish(point_msg)
        # Publish the processed image for detected center visualization
        debug_msg = self.bridge.cv2_to_imgmsg(vis_image, encoding='bgr8')
        self.debug_pub.publish(debug_msg)
    

def main(args=None):
    rclpy.init(args=args)
    
    detect_node = DetectNode()
    
    try:
        rclpy.spin(detect_node)
    except KeyboardInterrupt:
        pass
    finally:
        # Destroy the node explicitly
        if rclpy.ok():
            detect_node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()


