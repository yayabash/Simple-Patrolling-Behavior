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
        self.cmd = Twist()
        self.cmd.linear.x = 0.0
        self.cmd.angular.z = 0.0

        # Initialize variables for laser scan data
        self.left_side = 0.0
        self.front = 0.0
        self.right_side = 0.0

        # Constants for distance thresholds
        self.min_distance = 0.35
        self.side_threshold = 0.15

    def sensor_callback(self, msg: LaserScan):
        # Aggregate scan ranges over broader indices for obstacle detection
        self.right_side = min(msg.ranges[180:270])  # Right side (180° to 270°)
        self.front = min(msg.ranges[330:390])      # Front (narrow range near 0°)
        self.left_side = min(msg.ranges[450:540])  # Left side (450° to 540°)


    def command_publisher(self):
        self.get_logger().info(f"Front: {self.front}, Left: {self.left_side}, Right: {self.right_side}")
        max_linear_vel = 0.075
        max_angular_vel = 0.5  # Increased angular velocity for sharper turns

        # Thresholds with hysteresis for smoother control
        front_threshold = 0.4  # Rotate sooner when front obstacle is closer
        side_threshold = 0.2

        linear_vel = max_linear_vel
        angular_vel = 0.0

        # Preemptively rotate for side obstacles
        if self.left_side < side_threshold:
            angular_vel = -max_angular_vel  # Rotate right
            linear_vel *= 0.5  # Reduce forward speed
        elif self.right_side < side_threshold:
            angular_vel = max_angular_vel  # Rotate left
            linear_vel *= 0.5

        # Rotate to avoid front obstacles
        if self.front < front_threshold:
            linear_vel *= 0.25  # Slow down further
            if self.left_side > self.right_side:
                angular_vel = max_angular_vel  # Rotate left
            else:
                angular_vel = -max_angular_vel  # Rotate right

        # Publish velocity command
        self.cmd.linear.x = linear_vel
        self.cmd.angular.z = angular_vel
        self.cmd_pub.publish(self.cmd)


            
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
