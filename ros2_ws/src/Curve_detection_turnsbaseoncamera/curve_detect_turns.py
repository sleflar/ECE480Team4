import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32, String
from cv_bridge import CvBridge
import cv2
import numpy as np


class CameraTurnDetector(Node):
    def __init__(self):
        super().__init__('camera_turn_detector')

        # Subscribe to camera image topic
        # If this topic name is different in your system, change it
        self.image_sub = self.create_subscription(
            Image,                 # message type
            '/camera/image_raw',   # camera topic name
            self.image_callback,   # callback function
            10
        )

        # Publish numeric turn error
        self.curve_pub = self.create_publisher(Float32, '/curve_error', 10)

        # Publish text turn hint: left / right / straight
        self.turn_pub = self.create_publisher(String, '/turn_hint', 10)

        # Convert ROS image messages to OpenCV images
        self.bridge = CvBridge()

        # HSV range for orange track
        # You may need to tune these values depending on Gazebo lighting
        self.lower_orange = np.array([5, 100, 100], dtype=np.uint8)
        self.upper_orange = np.array([20, 255, 255], dtype=np.uint8)

        # Region of interest (bottom part of the image)
        # We only use the lower part because that is the road area in front of the car
        self.roi_start_ratio = 0.30
        self.roi_end_ratio = 1.00

        # Two sample rows inside the ROI
        # near_row = closer to the car
        # far_row  = farther ahead
        self.near_row_ratio = 0.80
        self.far_row_ratio = 0.35

        # Minimum number of detected orange pixels needed in a row
        self.min_pixels_per_row = 20

        # Threshold for determining left/right/straight
        self.turn_threshold = 20.0

        # Smoothing factor
        self.prev_curve_error = 0.0
        self.alpha = 0.7

        self.get_logger().info('Camera turn detector started.')

    def find_row_center(self, mask, row_index):
        # Find the x-center of all detected orange pixels in one row

        xs = np.where(mask[row_index] > 0)[0]

        if len(xs) < self.min_pixels_per_row:
            return None

        return float(np.mean(xs))

    def image_callback(self, msg):
        # This function runs every time a new camera image is received

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().warn(f'Image conversion failed: {e}')
            return

        # Get image size
        height, width = frame.shape[:2]

        # Crop the region of interest
        roi_start = int(height * self.roi_start_ratio)
        roi_end = int(height * self.roi_end_ratio)
        roi = frame[roi_start:roi_end, :]

        # Convert ROI from BGR to HSV
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Keep only orange pixels
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)

        # Clean up noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Choose a near row and a far row inside the ROI
        roi_h = mask.shape[0]
        near_row = int(roi_h * self.near_row_ratio)
        far_row = int(roi_h * self.far_row_ratio)

        # Find the center of the orange region in both rows
        x_near = self.find_row_center(mask, near_row)
        x_far = self.find_row_center(mask, far_row)

        if x_near is None or x_far is None:
            self.get_logger().warn('Not enough orange pixels detected in near/far rows.')
            return

        # Compute curve error
        # Positive means the road is moving to the right
        # Negative means the road is moving to the left
        raw_curve_error = x_far - x_near

        # Smooth the output
        curve_error = self.alpha * self.prev_curve_error + (1.0 - self.alpha) * raw_curve_error
        self.prev_curve_error = curve_error

        # Determine turn direction
        if curve_error > self.turn_threshold:
            turn_hint = 'right'
        elif curve_error < -self.turn_threshold:
            turn_hint = 'left'
        else:
            turn_hint = 'straight'

        # Publish numeric curve error
        curve_msg = Float32()
        curve_msg.data = float(curve_error)
        self.curve_pub.publish(curve_msg)

        # Publish turn hint
        turn_msg = String()
        turn_msg.data = turn_hint
        self.turn_pub.publish(turn_msg)

        # Debug information in terminal
        self.get_logger().info(
            f'x_near={x_near:.1f}, x_far={x_far:.1f}, '
            f'curve_error={curve_error:.2f}, turn={turn_hint}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = CameraTurnDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

