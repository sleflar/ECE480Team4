#!/usr/bin/env python3
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped, Point
from cv_bridge import CvBridge
import cv2
import numpy as np
import os


class DetectNode(Node):
    A ROS2 node to detect lane lines using OpenCV RGB/BGR color masking
    and publish a target point.
    def __init__(self):
        super().__init__('detect_node')
        
        self.bridge = CvBridge()
        
        # Color Ranges for Line Detection in BGR Space ---
        # BGR for Orange
        #0,20,60
        #80,150,200
        self.lower_orange_bgr = np.array([0, 20, 60])  # Complete with appropriate values
        self.upper_orange_bgr = np.array([80, 150, 220])
        
        # BGR for black (allowing for shadows/gray)
        #0,0,
        #180,255,80
        self.lower_black_bgr = np.array([0, 0, 0])
        self.upper_black_bgr = np.array([180, 255, 80])

        # Kernel for morphological operations (for noise reduction)
        self.morph_kernel = np.ones((5, 5), np.uint8)
        
        # Lane Width Memory to Handle Sharp Turns ---
        # Initial guess for lane width in pixels. This will be updated
        # automatically whenever both lines are detected.
        self.DEFAULT_LANE_WIDTH_PX = 700 
        self.last_known_lane_width = self.DEFAULT_LANE_WIDTH_PX

        # Create Subscriber and Publishers ---
        #/camera/image_raw
        #'/camera/camera/color/image_raw'
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.image_pub = self.create_publisher(Image, '/image_processed', 10)
        self.point_pub = self.create_publisher(PointStamped, '/lane_point', 10)

        self.get_logger().info('Lane detection node started (using BGR + Memory for sharp turns).')
    

    def image_callback(self, msg):
        Callback function for the image subscriber.
        Processes the image to find the target point.
        try:
            # Convert ROS Image message to OpenCV image (BGR8)
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f'Failed to convert image: {e}')
            return
        self.get_logger().info('Image Callback')
        # Define Region of Interest (ROI)
        height, width, _ = cv_image.shape

        # roi = 
        #roi_height = int(height * 0.2)  # bottom 20% of image
        if self.last_known_lane_width < 600:
            roi_height = int(height * 0.5)  # look higher up if lane is narrow (turn)
        else:
            roi_height = int(height * 0.2)  # normal
        roi = cv_image[height - roi_height:height, :]
        
        # Detect Lines using OpenCV BGR Masking  and optionally cv2.morphologyEx ---
        mask_orange = cv2.inRange(roi, self.lower_orange_bgr, self.upper_orange_bgr)
        mask_black = cv2.inRange(roi, self.lower_black_bgr, self.upper_black_bgr)

        mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_OPEN, self.morph_kernel)
        mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_CLOSE, self.morph_kernel)
        mask_black = cv2.morphologyEx(mask_black, cv2.MORPH_OPEN, self.morph_kernel)
        mask_black = cv2.morphologyEx(mask_black, cv2.MORPH_CLOSE, self.morph_kernel)

        # Find Centroids ---
        left_centroid = self.get_centroid(mask_orange,"left",width)
        right_centroid = self.get_centroid(mask_black, "right", width)

        # Convert ROI coordinates to full-image coordinates
        if left_centroid is not None:
            left_centroid = (int(left_centroid[0]), int(left_centroid[1] + (height - roi_height)))
        if right_centroid is not None:
            right_centroid = (int(right_centroid[0]), int(right_centroid[1] + (height - roi_height)))


        # Define PointStamped message to publish
        lane_center = None
        if left_centroid and right_centroid:
            # both lines detected
            lane_center = ((left_centroid[0] + right_centroid[0]) // 2,
                           (left_centroid[1] + right_centroid[1]) // 2)
            self.last_known_lane_width = abs(right_centroid[0] - left_centroid[0])
        elif left_centroid and not right_centroid:
            # only left line detected
            lane_center = (left_centroid[0] + self.last_known_lane_width // 2, left_centroid[1])
        elif right_centroid and not left_centroid:
            # only right line detected
            lane_center = (right_centroid[0] - self.last_known_lane_width // 2, right_centroid[1])
        else:
            # neither line detected → end of curvy road
            self.publish_point(msg, 0.0, 0.0, 0.0)
            annotated = cv_image.copy()
            cv2.putText(annotated, "NO LANES DETECTED", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            self.publish_image(annotated, msg)
            return
        
        # Depending on whether orange or white or both or neither lines are detected,
        # compute the target point accordingly 

        self.get_logger().debug('Output the which lines were detected as a debug message.')

        # Draw visualization dot ONLY if we have a valid (non-zero) point
        annotated = cv_image.copy()
        cv2.rectangle(annotated, (0, height - roi_height), (width - 1, height - 1), (60, 60, 60), 2)
        if left_centroid:
            cv2.circle(annotated, left_centroid, 6, (0, 255, 0), -1)
        if right_centroid:
            cv2.circle(annotated, right_centroid, 6, (255, 0, 0), -1)
        if lane_center:
            cv2.circle(annotated, lane_center, 8, (0, 0, 255), -1)

        # Publish the detected point
        self.publish_point(msg, lane_center[0], lane_center[1], 0.0)

        # Publish the processed image for detected center visualization
        self.publish_image(annotated, msg)


    # ---------------- Helper functions ---------------- # 
    def get_centroid(self, mask, side, width):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None

        candidates = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < 50:
                continue

            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue

            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # enforce LEFT or RIGHT half
            if side == "left" and cx < width // 2:
                candidates.append((area, (cx, cy)))
            elif side == "right" and cx >= width // 2:
                candidates.append((area, (cx, cy)))

        # no valid contours on that side
        if not candidates:
            return None

        # return largest-area contour centroid from that side
        candidates.sort(reverse=True)
        return candidates[0][1]

    def publish_point(self, img_msg, x, y, z):
        #Publish a PointStamped message.
        self.get_logger().info('Publish point')
        pt = PointStamped()
        pt.header = img_msg.header
        pt.point.x = float(x)
        pt.point.y = float(y)
        pt.point.z = float(z)
        self.point_pub.publish(pt)

    def publish_image(self, cv_image, img_msg):
        #Publish an annotated image to /image_processed.
        img_msg_out = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
        img_msg_out.header = img_msg.header
        self.image_pub.publish(img_msg_out)


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

"""
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
    A ROS2 node to detect lane lines using OpenCV RGB/BGR color masking
    and publish a target point.
    """
    def __init__(self):
        super().__init__('detect_node')
        
        self.bridge = CvBridge()
        
        # Color Ranges for Line Detection in BGR Space ---
        # BGR for Orange
        self.lower_orange = np.array([5, 150, 150])     # H, S, V
        self.upper_orange = np.array([25, 255, 255])

        self.lower_white = np.array([0, 0, 220])
        self.upper_white = np.array([160, 30, 245])

        # Kernel for morphological operations (for noise reduction)
        self.morph_kernel = np.ones((5, 5), np.uint8)
        
        # Lane Width Memory to Handle Sharp Turns ---
        # Initial guess for lane width in pixels. This will be updated
        # automatically whenever both lines are detected.
        self.DEFAULT_LANE_WIDTH_PX = 700 
        self.last_known_lane_width = self.DEFAULT_LANE_WIDTH_PX

        # Create Subscriber and Publishers ---
        self.image_processed_pub = self.create_publisher(Image, '/camera/image_processed', 10)
        self.debug_pub = self.create_publisher(Image, '/lane/debug_image', 10)
        self.target_pub = self.create_publisher(PointStamped, '/lane_point', 10)
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
        # Define PointStamped message to publish
        target_point = None
        if orange_center and white_center:
            # Both lines detected — midpoint between centroids
            lane_width_px = abs(orange_center[0] - white_center[0])
            self.last_known_lane_width = lane_width_px  # Update lane width memory
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


