import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import struct
import time


# -----------------------
# CRC16-CCITT function
# -----------------------
def crc16_ccitt(data: bytes) -> int:
    crc = 0xFFFF
    for b in data:
        crc ^= b << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc

# -----------------------
# Make a VESC SetRPM packet
# -----------------------
def make_rpm_packet(rpm: int) -> bytes:
    """
    Build a VESC SetRPM packet.
    rpm: signed integer, positive = forward
    """
    COMM_SET_RPM = 5  # VESC command ID for setting RPM
    payload = struct.pack(">B i", COMM_SET_RPM, rpm)  # command byte + 32-bit RPM
    length = len(payload)
    crc = crc16_ccitt(payload)

    # Packet format: 0x02 | len | payload | crc16 | 0x03
    packet = struct.pack(">B B", 0x02, length) + payload + struct.pack(">H B", crc, 0x03)
    return packet

# -----------------------
# ROS2 Node
# -----------------------
class VESCBridge(Node):
    def __init__(self):
        super().__init__('vesc_bridge')

        # Serial port to VESC (adjust as needed)
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)

        # Subscribe to /cmd_vel
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.get_logger().info("VESC Bridge node started")

    def cmd_vel_callback(self, msg: Twist):
        # Convert linear.x to RPM
        # Adjust scaling factor for your motor
        rpm = int(msg.linear.x * 1000)  # Example: 1 m/s -> 1000 RPM

        packet = make_rpm_packet(rpm)
        self.get_logger().info(f"Sending RPM: {rpm}, Packet: {packet.hex()}")
        try:
            self.ser.write(packet)
            self.ser.flush()
        except Exception as e:
            self.get_logger().error(f"Failed to send to VESC: {e}")

# -----------------------
# Main
# -----------------------
def main(args=None):
    rclpy.init(args=args)
    node = VESCBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
