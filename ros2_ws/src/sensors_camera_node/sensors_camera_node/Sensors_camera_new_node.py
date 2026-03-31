import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from std_msgs.msg import Float32
from cv_bridge import CvBridge

import cv2
import numpy as np


class MultiSectionCameraNode(Node):
    def __init__(self):
        super().__init__('multi_section_camera_node')

        # ===== Parameters =====
        self.declare_parameter('image_topic', '/camera/image_raw')
        self.declare_parameter('debug_view', True)
        self.declare_parameter('use_multiple_rows', True)

        image_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        self.debug_view = self.get_parameter('debug_view').get_parameter_value().bool_value
        self.use_multiple_rows = self.get_parameter('use_multiple_rows').get_parameter_value().bool_value

        # ===== ROS interfaces =====
        self.subscription = self.create_subscription(
            Image,
            image_topic,
            self.image_callback,
            10
        )

        self.error_pub = self.create_publisher(Float32, '/lane_error', 10)

        self.bridge = CvBridge()

        self.get_logger().info('Multi-section camera node started.')

        # ===== HSV threshold for orange track =====
        # You may need to tune these values based on your lighting
        self.lower_orange = np.array([5, 100, 100])
        self.upper_orange = np.array([25, 255, 255])

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'CV Bridge error: {e}')
            return

        debug_frame, lane_error = self.process_frame(frame)

        # Publish lane error
        error_msg = Float32()
        error_msg.data = float(lane_error)
        self.error_pub.publish(error_msg)

        # Show debug window
        if self.debug_view:
            cv2.imshow("Multi-Section Lane Detection", debug_frame)
            cv2.waitKey(1)

    def process_frame(self, frame):
        """
        Process the image and compute lane error using multiple front sections.
        """
        h, w = frame.shape[:2]

        # Optional: use only lower portion of image
        roi_top = int(h * 0.35)
        roi = frame[roi_top:h, :].copy()
        roi_h, roi_w = roi.shape[:2]

        # Convert to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Threshold orange color
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange) #only maintain the orange section

        # Morphological filtering to reduce noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Prepare debug frame
        debug_roi = roi.copy()

        # Divide into sections
        # 3 columns: left, center, right
        col_edges = [0, roi_w // 3, 2 * roi_w // 3, roi_w]

        # Either 3 rows or just 1 row
        if self.use_multiple_rows:
            row_edges = [0, roi_h // 3, 2 * roi_h // 3, roi_h]
        else:
            row_edges = [0, roi_h]

        section_scores = []
        section_centers = []

        # Analyze each section
        for r in range(len(row_edges) - 1):
            for c in range(len(col_edges) - 1):
                y1, y2 = row_edges[r], row_edges[r + 1]
                x1, x2 = col_edges[c], col_edges[c + 1]

                section_mask = mask[y1:y2, x1:x2]
                #each section calculate how many orange pixel in each little grid
                nonzero_count = cv2.countNonZero(section_mask)

                # Store score
                section_scores.append({
                    'row': r,
                    'col': c,
                    'count': nonzero_count,
                    'x1': x1, 'x2': x2,
                    'y1': y1, 'y2': y2
                })

                # Draw section boundaries
                cv2.rectangle(debug_roi, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # Put count text
                cv2.putText(
                    debug_roi,
                    str(nonzero_count),
                    (x1 + 10, y1 + 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )

                # Find centroid within section if enough pixels
                if nonzero_count > 50:
                    M = cv2.moments(section_mask)
                    if M['m00'] != 0:
                        cx_local = int(M['m10'] / M['m00'])
                        cy_local = int(M['m01'] / M['m00'])

                        cx = x1 + cx_local
                        cy = y1 + cy_local

                        section_centers.append((cx, cy, nonzero_count))

                        cv2.circle(debug_roi, (cx, cy), 5, (0, 0, 255), -1)

        # Compute weighted lane center
        lane_center_x = None

        left_points = []
        right_points = []

        for cx, cy, count in section_centers:
            if cx < roi_w / 2:
                left_points.append((cx, cy, count))
            else:
                right_points.append((cx, cy, count))

        left_center_x = None
        right_center_x = None

        # Compute weighted left track center
        if len(left_points) > 0:
            left_sum = 0.0
            left_weight_total = 0.0
            for cx, cy, count in left_points:
                distance_weight = 1.0 + (cy / max(roi_h, 1))
                weight = count * distance_weight
                left_sum += cx * weight
                left_weight_total += weight
            if left_weight_total > 0:
                left_center_x = left_sum / left_weight_total

        # Compute weighted right track center
        if len(right_points) > 0:
            right_sum = 0.0
            right_weight_total = 0.0
            for cx, cy, count in right_points:
                distance_weight = 1.0 + (cy / max(roi_h, 1))
                weight = count * distance_weight
                right_sum += cx * weight
                right_weight_total += weight
            if right_weight_total > 0:
                right_center_x = right_sum / right_weight_total

        # Corridor center = midpoint between left track and right track
        if left_center_x is not None and right_center_x is not None:
            lane_center_x = (left_center_x + right_center_x) / 2.0
        elif left_center_x is not None:
            # only left track seen
            lane_center_x = left_center_x + roi_w * 0.25
        elif right_center_x is not None:
            # only right track seen
            lane_center_x = right_center_x - roi_w * 0.25
        else:
            lane_center_x = None

        # Default image center
        image_center_x = roi_w / 2.0

        # Compute error
        if lane_center_x is not None:
            lane_error = lane_center_x - image_center_x
        else:
            lane_error = 0.0

        # Draw lane center and image center
        cv2.line(debug_roi, (int(image_center_x), 0), (int(image_center_x), roi_h), (0, 255, 0), 2)

        if lane_center_x is not None:
            cv2.line(debug_roi, (int(lane_center_x), 0), (int(lane_center_x), roi_h), (0, 0, 255), 2)
            cv2.putText(
                debug_roi,
                f"Lane Center: {lane_center_x:.1f}",
                (10, roi_h - 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        cv2.putText(
            debug_roi,
            f"Error: {lane_error:.1f}",
            (10, roi_h - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        # Put processed ROI back into original frame for viewing
        debug_frame = frame.copy()
        debug_frame[roi_top:h, :] = debug_roi

        return debug_frame, lane_error


def main(args=None):
    rclpy.init(args=args)
    node = MultiSectionCameraNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()