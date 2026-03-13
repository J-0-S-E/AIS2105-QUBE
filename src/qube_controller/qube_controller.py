import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray


class QubeController(Node):

    def __init__(self):
        super().__init__('qube_controller')

        self.kp = 2.0
        self.ki = 0.1
        self.kd = 0.5

        self.target_position = 0.0

        self.prev_error = 0.0
        self.integral = 0.0
        self.prev_time = None

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/velocity_controller/commands',
            10
        )

    def joint_state_callback(self, msg: JointState):
        position = msg.position[0]
        velocity = msg.velocity[0]

        now = self.get_clock().now()
        if self.prev_time is None:
            self.prev_time = now
            return
        dt = (now - self.prev_time).nanoseconds / 1e9
        self.prev_time = now

        error = self.target_position - position
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0.0
        self.prev_error = error

        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        cmd = Float64MultiArray()
        cmd.data = [output]

        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = QubeController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()