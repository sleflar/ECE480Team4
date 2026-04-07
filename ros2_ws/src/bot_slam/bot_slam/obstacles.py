#!/usr/bin/env python
import rclpy
from rclpy.node import Node
from rclpy.duration import Duration
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Pose, Point, Quaternion
from visualization_msgs.msg import Marker, MarkerArray
import numpy as np

class Obstacles(Node):
    def __init__(self, delta_r=0.25):
        super().__init__('bus_monitor')             
        self.delta_r = delta_r

        self.publisher = self.create_publisher(MarkerArray, 'obstacles', 1)    
        self.subscription = self.create_subscription(LaserScan, 'scan', self.lidar_centroids, 1)
        self.subscription

    def lidar_centroids(self, msg):       
        ranges = np.array(msg.ranges)  # Convert to Numpy array for vector operations
        if len(ranges)==0:
            return
        angles = np.arange(len(ranges)) * msg.angle_increment + msg.angle_min # Angle of each ray
        x = ranges * np.cos(angles) # vector arithmatic is much faster than iterating
        y = ranges * np.sin(angles)
        good = ranges < np.inf  # get all finite returns

        if not np.any(good):
            return
        N = len(ranges)
        clusters = []          # list of lists of indices
        current_cluster = []
        # Create your list of obstacles here:
        for i in range(N):
            if not good[i]:
                # invalid ray: terminate current cluster if exists
                if current_cluster:
                    clusters.append(current_cluster)
                    current_cluster = []
                continue

            # if current cluster empty, start it
            if not current_cluster:
                current_cluster = [i]
                continue

            # test adjacency with previous valid point (index prev = current_cluster[-1])
            prev = current_cluster[-1]
            # Only connect if prev is exactly previous index; if there are invalid rays between, do not connect
            if i == prev + 1:
                # check range difference threshold
                if abs(ranges[i] - ranges[prev]) <= self.delta_r:
                    current_cluster.append(i)
                else:
                    # finalize previous cluster and start a new one
                    clusters.append(current_cluster)
                    current_cluster = [i]
            else:
                # non-consecutive due to invalid rays, start new cluster
                clusters.append(current_cluster)
                current_cluster = [i]

        # append the last cluster if exists
        if current_cluster:
            clusters.append(current_cluster)
        
        if len(clusters) >= 2:
            first = clusters[0]
            last = clusters[-1]
            # both must be non-empty and both endpoints valid; compare last index to first index via wrap
            i_last = last[-1]
            i_first = first[0]
            # Only consider wrap if they are truly neighbours in circular scan (i_last == N-1 and i_first == 0)
            if i_last == (N - 1) and i_first == 0:
                # ensure both rays are valid (should be)
                if good[i_last] and good[i_first]:
                    if abs(ranges[i_first] - ranges[i_last]) <= self.delta_r:
                        # merge last and first
                        merged = last + first
                        # replace last and first with merged cluster
                        clusters = [merged] + clusters[1:-1] if len(clusters) > 2 else [merged]
        # ...
         # compute centroids of clusters that meet min_points
        centroids_x = []
        centroids_y = []
        centroid_ids = []

        for idx, cluster in enumerate(clusters):
            if len(cluster) < 2:
                continue
            # Use x,y coordinates for indices in cluster
            xs = x[cluster]
            ys = y[cluster]
            # Sometimes ranges may produce NaN if angle range weird; guard against that
            mask_xy = np.isfinite(xs) & np.isfinite(ys)
            if not np.any(mask_xy):
                continue
            xs = xs[mask_xy]
            ys = ys[mask_xy]
            if xs.size == 0:
                continue
            xcen = float(np.mean(xs))
            ycen = float(np.mean(ys))
            centroids_x.append(xcen)
            centroids_y.append(ycen)
            centroid_ids.append(len(centroid_ids))  # simple sequential ids starting at 0

        # Convert centroid list to points for publishing
        if len(centroids_x) == 0:
            # still publish empty MarkerArray to clear previous markers
            self.pub_centroids([], [], msg.header)
            return

        points = np.column_stack((centroids_x, centroids_y, np.zeros_like(centroids_x))).tolist()
        # let's say xcen and ycen are np arrays of obstacle centroids,
        # then convert them to a list of points like this:

        # Create unique IDs for each point:
        ids = np.arange(len(points)).astype(int)

        # publish the centroids:
        self.pub_centroids(points, ids, msg.header)

      
    def pub_centroids(self, points, ids, header):

        ma = MarkerArray()

        for id, p in zip(ids, points):
            mark = Marker()            
            mark.header = header
            mark.id = id.item()
            mark.type = Marker.SPHERE
            mark.pose = Pose(position=Point(x=p[0],y=p[1],z=p[2]), orientation=Quaternion(x=0.,y=0.,z=0.,w=1.))
            mark.scale.x = 0.25
            mark.scale.y = 0.25
            mark.scale.z = 0.25
            mark.color.a = 0.75
            mark.color.r = 0.25
            mark.color.g = 1.
            mark.color.b = 0.25
            mark.lifetime = Duration(seconds=0.4).to_msg()
            ma.markers.append(mark)

        self.publisher.publish( ma )

def main(args=None):

    rclpy.init(args=args)

    node = Obstacles()
    rclpy.spin(node) 

    node.destroy_node()
    rclpy.shutdown()