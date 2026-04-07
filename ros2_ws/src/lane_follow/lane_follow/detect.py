#!/usr/bin/env python3

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
        #0,20,60
        #80,150,200
        self.lower_orange_bgr = np.array([0, 20, 60])  # Complete with appropriate values
        self.upper_orange_bgr = np.array([80, 150, 220])
        
        # BGR for black (allowing for shadows/gray)
        #0,0,0
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
        self.point_pub = self.create_publisher(PointStamped, '/ground_point', 10)

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
        
        # ROI vertical range: 20% to 50% from bottom
        roi_bottom = int(height * 0.2)  # 20% from bottom
        roi_top    = int(height * 0.5)  # 50% from bottom
        usable_height = roi_top - roi_bottom
        
        roi_offset = int(0.2*height)

        num_slices = 50  # number of trajectory points
        roi_height = usable_height // num_slices
        trajectory_points = []

        for i in range(num_slices):
            y_start = height - roi_top + i * roi_height
            y_end   = height - roi_top + (i + 1) * roi_height
            roi = cv_image[y_start:y_end, :]

            # Masks
            mask_orange = cv2.inRange(roi, self.lower_orange_bgr, self.upper_orange_bgr)
            mask_black  = cv2.inRange(roi, self.lower_black_bgr, self.upper_black_bgr)
            mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_OPEN, self.morph_kernel)
            mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_CLOSE, self.morph_kernel)
            mask_black  = cv2.morphologyEx(mask_black, cv2.MORPH_OPEN, self.morph_kernel)
            mask_black  = cv2.morphologyEx(mask_black, cv2.MORPH_CLOSE, self.morph_kernel)

            # Get centroids
            left_centroid  = self.get_centroid(mask_orange, "left", width)
            right_centroid = self.get_centroid(mask_black,  "right", width)

            if left_centroid:
                left_centroid = (int(left_centroid[0]), int(left_centroid[1] + y_start))
            if right_centroid:
                right_centroid = (int(right_centroid[0]), int(right_centroid[1] + y_start))

            # Compute lane center for this slice, filters out strays
            if left_centroid and right_centroid:
                lane_width = right_centroid[0] - left_centroid[0]
                # Horizontal lane width sanity check
                if not (0.5 * self.last_known_lane_width < lane_width < 1.5 * self.last_known_lane_width):
                    continue  # skip this slice, likely stray
                center = ((left_centroid[0] + right_centroid[0]) // 2,
                          (left_centroid[1] + right_centroid[1]) // 2)
                self.last_known_lane_width = lane_width
            elif left_centroid:
                center = (left_centroid[0] + self.last_known_lane_width // 2, left_centroid[1])
            elif right_centroid:
                center = (right_centroid[0] - self.last_known_lane_width // 2, right_centroid[1])
            else:
                continue  # skip slice if neither line is detected

            trajectory_points.append(center)
        
        # Smoothing the trajectory lane
        SMOOTH_WINDOW = 3  # number of neighboring points to average
        smoothed_trajectory = []
        for i in range(len(trajectory_points)):
            x_vals = [trajectory_points[j][0] for j in range(max(0, i-SMOOTH_WINDOW),
                                                             min(len(trajectory_points), i+SMOOTH_WINDOW+1))]
            y_vals = [trajectory_points[j][1] for j in range(max(0, i-SMOOTH_WINDOW),
                                                             min(len(trajectory_points), i+SMOOTH_WINDOW+1))]
            smoothed_trajectory.append((int(np.mean(x_vals)), int(np.mean(y_vals))))

        trajectory_points = smoothed_trajectory
        


        # --- Visualization ---
        annotated = cv_image.copy()
        for pt in trajectory_points:
            cv2.circle(annotated, pt, 6, (0, 0, 255), -1)  # red dots for trajectory

        # Draw rectangles to visualize ROI slices (optional)
        for i in range(num_slices):
            y_start = height - roi_offset - (i + 1) * roi_height
            y_end   = height - roi_offset - i * roi_height
            cv2.rectangle(annotated, (0, y_start), (width - 1, y_end), (100, 100, 100), 1)

        # --- Publish closest trajectory point for steering ---
        if trajectory_points:
            self.publish_point(msg, trajectory_points[0][0], trajectory_points[0][1], 0.0)
        else:
            # No lane points detected → publish zero point
            self.publish_point(msg, 0.0, 0.0, 0.0)
            cv2.putText(annotated, "NO LANES DETECTED", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        # --- Publish annotated image ---
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
        """Publish a PointStamped message."""
        pt = PointStamped()
        pt.header = img_msg.header
        pt.point.x = float(x)
        pt.point.y = float(y)
        pt.point.z = float(z)
        self.point_pub.publish(pt)

    def publish_image(self, cv_image, img_msg):
        """Publish an annotated image to /image_processed."""
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


