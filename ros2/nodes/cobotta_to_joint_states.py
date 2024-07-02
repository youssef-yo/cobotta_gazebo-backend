import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Bool
import random

from cobotta_utils import *

class RobotStatePublisher(Node):

    def __init__(self, client, hRobot):
        super().__init__('robot_state_publisher')
        self.publisher_ = self.create_publisher(JointState, 'joint_statesW', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.client = client
        self.hRobot = hRobot
        
        # Mock joint names; replace with actual joint names
        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']

        # if active then jointState is send
        self.active = True

        self.subscription = self.create_subscription(
            Bool,
            'activeStatusCobotta',
            self.listener_callback,
            10)
    
    def listener_callback(self, msg):
        self.active = msg.data
        self.get_logger().info(f'Received active status: {self.active}')

    def get_robot_joint_states(self):
        # Replace this mock method with the actual method to get joint states
        # For demonstration, it returns random joint positions
        
        response_angle_joints = get_angle_joints(self.client, self.hRobot)
        # print("Angle joints: ", response_angle_joints)

        return response_angle_joints
        # getPos from Cobotta
        #return [random.uniform(-1.57, 1.57) for _ in self.joint_names]
        
    def timer_callback(self):
        if self.active:
            joint_positions = self.get_robot_joint_states()
            
            msg = JointState()
            msg.name = self.joint_names
            msg.position = joint_positions
            msg.header.stamp = self.get_clock().now().to_msg()
            
            self.publisher_.publish(msg)
            self.get_logger().info('Published joint states: {}'.format(joint_positions))

def main(args=None):
    rclpy.init(args=args)

    # Connect to Cobotta
    client, _, hRobot = connect("192.168.0.1", 5007, 5000)

    node = RobotStatePublisher(client, hRobot)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
