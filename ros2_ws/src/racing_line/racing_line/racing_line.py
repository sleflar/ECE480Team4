#!/usr/bin/env python3
import math
import numpy as np
import rclpy
from rclpy.node import Node

from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import PointStamped, Point
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA
from builtin_interfaces.msg import Duration

import tf2_ros
import tf2_geometry_msgs

from scipy.ndimage import distance_transform_edt, binary_dilation, binary_erosion
from scipy.interpolate import splprep, splev
from skimage.morphology import skeletonize

# ─────────────────────────────────────────
# PARAMETERS
# ─────────────────────────────────────────
LOOKAHEAD_DISTANCE_M = 1.2
OBSTACLE_INFLATION_M = 0.25
MIN_CLEARANCE_CELLS  = 3
SPLINE_SMOOTH        = 10.0
SPLINE_SAMPLES       = 500
UNKNOWN_AS_FREE      = True
SCAN_MAX_RANGE_M     = 5.0


class RacingLineNode(Node):

    def __init__(self):
        super().__init__('racing_line_node')

        self.map_msg = None
        self.scan_msg = None
        self.racing_line = None
        self.map_dirty = False

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.create_subscription(OccupancyGrid, '/map', self.map_callback, 1)
        self.create_subscription(LaserScan, '/scan', self.scan_callback, 1)

        self.pub_point = self.create_publisher(PointStamped, '/ground_point', 10)
        self.pub_marker = self.create_publisher(Marker, '/racing_line_markers', 10)

        self.create_timer(0.05, self.publish_target)

    # ─────────────────────────────────────────
    # CALLBACKS
    # ─────────────────────────────────────────
    def map_callback(self, msg):
        self.map_msg = msg
        self.map_dirty = True

    def scan_callback(self, msg):
        self.scan_msg = msg

    # ─────────────────────────────────────────
    # MAIN LOOP
    # ─────────────────────────────────────────
    def publish_target(self):
        if self.map_msg is None:
            return

        if self.map_dirty:
            self.racing_line = self._compute_racing_line(self.map_msg, self.scan_msg)
            self.map_dirty = False

            if self.racing_line is not None:
                self._publish_marker(self.racing_line, self.map_msg.header.frame_id)

        if self.racing_line is None:
            return

        robot_pos = self._get_robot_position()
        if robot_pos is None:
            return

        lookahead = self._find_lookahead(self.racing_line, robot_pos)
        if lookahead is None:
            return

        pt = PointStamped()
        pt.header.frame_id = self.map_msg.header.frame_id
        pt.header.stamp = self.get_clock().now().to_msg()
        pt.point.x = float(lookahead[0])
        pt.point.y = float(lookahead[1])

        self.pub_point.publish(pt)

    # ─────────────────────────────────────────
    # RACING LINE PIPELINE
    # ─────────────────────────────────────────
    def _compute_racing_line(self, map_msg, scan_msg):

        info = map_msg.info
        res = info.resolution
        W, H = info.width, info.height

        raw = np.array(map_msg.data, dtype=np.int8).reshape((H, W))
        free = (raw == 0)

        if UNKNOWN_AS_FREE:
            free |= (raw == -1)

        if scan_msg is not None:
            free = self._apply_lidar(free, scan_msg, map_msg)

        edt = distance_transform_edt(free)
        passable = edt >= MIN_CLEARANCE_CELLS

        skeleton = skeletonize(passable)
        path = self._extract_centerline(skeleton)

        if len(path) < 10:
            return None

        origin_x = info.origin.position.x
        origin_y = info.origin.position.y

        pts = np.array([
            [c[1] * res + origin_x, c[0] * res + origin_y]
            for c in path
        ])

        normals = self._compute_normals(pts)
        optimized = self._optimize_line(pts, edt, normals, res, origin_x, origin_y)

        try:
            tck, _ = splprep([optimized[:,0], optimized[:,1]], s=SPLINE_SMOOTH, per=True)
            u = np.linspace(0,1,SPLINE_SAMPLES)
            sx, sy = splev(u, tck)
            return np.column_stack([sx, sy])
        except:
            return optimized

    # ─────────────────────────────────────────
    # CENTERLINE EXTRACTION
    # ─────────────────────────────────────────
    def _extract_centerline(self, skeleton):
        pts = list(zip(*np.where(skeleton)))
        if not pts:
            return []

        visited = set()
        path = [pts[0]]

        while True:
            cur = path[-1]
            visited.add(cur)

            r, c = cur
            neighbors = [
                (r+dr, c+dc)
                for dr in (-1,0,1)
                for dc in (-1,0,1)
                if not (dr == 0 and dc == 0)
            ]

            next_pts = [n for n in neighbors if n in pts and n not in visited]

            if not next_pts:
                break

            path.append(next_pts[0])

        return path

    # ─────────────────────────────────────────
    # NORMALS
    # ─────────────────────────────────────────
    def _compute_normals(self, pts):
        dx = np.gradient(pts[:,0])
        dy = np.gradient(pts[:,1])

        tangents = np.stack([dx, dy], axis=1)
        norms = np.linalg.norm(tangents, axis=1, keepdims=True)
        tangents /= (norms + 1e-6)

        normals = np.stack([-tangents[:,1], tangents[:,0]], axis=1)
        return normals

    # ─────────────────────────────────────────
    # OPTIMIZATION
    # ─────────────────────────────────────────
    def _optimize_line(self, pts, edt, normals, res, ox, oy):

        optimized = pts.copy()

        for i in range(1, len(pts)-1):

            best = pts[i]
            best_cost = float('inf')

            for offset in np.linspace(-0.5, 0.5, 7):
                candidate = pts[i] + offset * normals[i]

                col = int((candidate[0] - ox)/res)
                row = int((candidate[1] - oy)/res)

                if not (0 <= row < edt.shape[0] and 0 <= col < edt.shape[1]):
                    continue

                if edt[row, col] < MIN_CLEARANCE_CELLS:
                    continue

                prev = optimized[i-1]
                next_ = pts[i+1]

                v1 = candidate - prev
                v2 = next_ - candidate

                angle = np.arccos(
                    np.clip(np.dot(v1,v2)/(np.linalg.norm(v1)*np.linalg.norm(v2)+1e-6), -1,1)
                )

                cost = angle**2 - 0.1*edt[row,col]

                if cost < best_cost:
                    best_cost = cost
                    best = candidate

            optimized[i] = best

        return optimized

    # ─────────────────────────────────────────
    # LIDAR
    # ─────────────────────────────────────────
    def _apply_lidar(self, free, scan_msg, map_msg):

        try:
            tf = self.tf_buffer.lookup_transform(
                map_msg.header.frame_id,
                scan_msg.header.frame_id,
                rclpy.time.Time()
            )
        except:
            return free

        tx = tf.transform.translation.x
        ty = tf.transform.translation.y
        yaw = self._quat_to_yaw(tf.transform.rotation)

        res = map_msg.info.resolution
        ox = map_msg.info.origin.position.x
        oy = map_msg.info.origin.position.y

        mask = np.zeros_like(free, dtype=bool)

        angles = np.arange(len(scan_msg.ranges))*scan_msg.angle_increment + scan_msg.angle_min

        for r, a in zip(scan_msg.ranges, angles):
            if not math.isfinite(r) or r > SCAN_MAX_RANGE_M:
                continue

            lx = r*math.cos(a)
            ly = r*math.sin(a)

            mx = lx*math.cos(yaw) - ly*math.sin(yaw) + tx
            my = lx*math.sin(yaw) + ly*math.cos(yaw) + ty

            col = int((mx - ox)/res)
            row = int((my - oy)/res)

            if 0 <= row < free.shape[0] and 0 <= col < free.shape[1]:
                mask[row,col] = True

        mask = binary_dilation(mask, iterations=2)
        return free & ~mask

    # ─────────────────────────────────────────
    # LOOKAHEAD
    # ─────────────────────────────────────────
    def _find_lookahead(self, line, robot):
        rx, ry = robot

        dists = np.hypot(line[:,0]-rx, line[:,1]-ry)
        idx = np.argmin(dists)

        for i in range(idx, len(line)):
            if dists[i] > LOOKAHEAD_DISTANCE_M:
                return line[i]

        return line[-1]

    def _get_robot_position(self):
        try:
            tf = self.tf_buffer.lookup_transform(
                self.map_msg.header.frame_id,
                'base_footprint',
                rclpy.time.Time()
            )
            return (tf.transform.translation.x, tf.transform.translation.y)
        except:
            return None

    def _quat_to_yaw(self, q):
        return math.atan2(2*(q.w*q.z+q.x*q.y),1-2*(q.y*q.y+q.z*q.z))

    # ─────────────────────────────────────────
    # RVIZ
    # ─────────────────────────────────────────
    def _publish_marker(self, line, frame):
        m = Marker()
        m.header.frame_id = frame
        m.type = Marker.LINE_STRIP
        m.scale.x = 0.05
        m.color = ColorRGBA(r=1.0, g=0.3, b=0.0, a=1.0)

        for p in line:
            m.points.append(Point(x=float(p[0]), y=float(p[1])))

        self.pub_marker.publish(m)


def main(args=None):
    rclpy.init(args=args)
    node = RacingLineNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

