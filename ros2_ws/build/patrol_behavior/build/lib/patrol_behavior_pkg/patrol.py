import rclpy
# import the ROS2 python libraries
from rclpy.node import Node
# import the TwistStamped module from geometry_msgs interface
from geometry_msgs.msg import Twist
# import the LaserScan module from sensor_msgs interface
from sensor_msgs.msg import LaserScan
from rclpy.qos import ReliabilityPolicy, QoSProfile

class Patrol(Node):

    def __init__(self):
        # Here we have the class constructor
        # call the class constructor
        super().__init__('patrol_node')

        # create a subscription to laser scan data
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.sensor_callback,
            10)

        #Create publisher for publishing velocity commands
        self.cmd_pub = self.create_publisher(
            Twist,
            'cmd_vel',
            5)

        #Create timer for controlling robots movement
        self.contol_timer = self.create_timer(
            0.1,   #100 ms
            self.command_publisher)

        # Initialize the velocity command massage
        self.cmd = Twist
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.0

        # Initialize variables for laser scan data
        self.left_side = 0.0
        self.front = 0.0
        self.right_side = 0.0

        # Constants for distance thresholds
        self.min_distance = 0.35
        self.side_threshold = 0.15

    def sensor_callback(self,msg:LaserScan):
        # process laser scan data and extract values for different sections
        # of robot's surroundings
        self.right_side = msg.ranges[230]
        self.front = msg.ranges[360]
        self.left_side = msg.ranges[490]

    def command_publisher(self):
        # control robot's movement based on laser scan data
        #define linear velocity
        linear_vel = 0.075

        # Determine robot's movement based on obstacle detection
        if self.left_side < self.side_threshold and self.front > self.min_distance:
            self.cmd.linear.x = linear_vel * 0.5
            self.cmd.angular.z = -0.15
        elif self.right_side < self.side_threshold and self.front > self.min_distance:
            self.cmd.linear.x = linear_vel * 0.5
            self.cmd.angular.z = 0.15
        elif self.front > self.min_distance:
           self.cmd.linear.x = linear_vel
           self.cmd.angular.z = 0.0
        elif self.front < self.min_distance:
            if self.compare_sides(self.left_side, self.right_side):
                self.cmd.linear.x = linear_vel * 0.25
                self.cmd.angular.z = 0.35
            else:
                self.cmd.linear.x = linear_vel * 0.25
                self.cmd.angular.z = -0.35

        # Publish velocity command
        self.cmd_pub.publish(self.cmd)

    def compare_sides(self,left,right):
        return left >= right

            
def main(args=None):
    # initialize the ROS communication
    rclpy.init(args=args)
    # declare the node constructor
    patrol_node = Patrol()     

    try:
        # spin the node to hundle callbacks
        rclpy.spin(patrol_node)
    except KeyboardInterrupt:
        pass
    finally:
        # Explicity destroy the node
        patrol_node.destroy_node()
        # shutdown the ROS communication
        rclpy.shutdown()

if __name__ == '__main__':
    main()