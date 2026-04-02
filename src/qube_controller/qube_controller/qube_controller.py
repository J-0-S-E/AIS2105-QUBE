import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from rcl_interfaces.msg import SetParametersResult


class QubeController(Node):
    # PID-kontroller for Quanser QUBE.

    def __init__(self):
        super().__init__('qube_controller')

        # PID-verdier. Kan endres via terminal eller rqt_reconfigure
        self.declare_parameter('kp', 2.0)
        self.declare_parameter('ki', 0.1)
        self.declare_parameter('kd', 0.5)
        self.declare_parameter('target_position', 0.0)

        self.kp = self.get_parameter('kp').value
        self.ki = self.get_parameter('ki').value
        self.kd = self.get_parameter('kd').value
        self.target_position = self.get_parameter('target_position').value

        self.prev_error = 0.0  # forrige feil
        self.integral = 0.0   # akkumulert feil
        self.prev_time = None  # settes ved første melding

        self.add_on_set_parameters_callback(self.parameter_callback)

        # Leser posisjon og hastighet fra joint_state_broadcaster
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # Sender PID-pådraget til velocity_controller
        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/velocity_controller/commands',
            10
        )

        # Gir en bekreftelse i terminalen ved oppstart
        self.get_logger().info(
            f'Qube controller startet. Target: {self.target_position:.3f} rad, '
            f'PID: kp={self.kp}, ki={self.ki}, kd={self.kd}'
        )

    def parameter_callback(self, params):
        # Oppdaterer parametere når de endres. (ros2 param set)
        for param in params:
            if param.name == 'kp':
                self.kp = param.value
            elif param.name == 'ki':
                self.ki = param.value
            elif param.name == 'kd':
                self.kd = param.value
            elif param.name == 'target_position':
                self.target_position = param.value
                self.integral = 0.0  # Nullstill i-leddet ved ny referanse
                self.get_logger().info(f'Ny referansevinkel: {self.target_position:.3f} rad')
        return SetParametersResult(successful=True)

    def joint_state_callback(self, msg: JointState):
        # Leser posisjon fra joint_states og beregner PID-pådrag.
        # Finn motor_joint
        try:
            idx = msg.name.index('motor_joint')
        except ValueError:
            return

        position = msg.position[idx]

        # Antall sekunder siden forrige melding
        now = self.get_clock().now()
        if self.prev_time is None:
            self.prev_time = now
            return
        dt = (now - self.prev_time).nanoseconds / 1e9
        self.prev_time = now

        if dt <= 0:
            return

        # PID-beregning
        error = self.target_position - position
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        self.prev_error = error

        output = self.kp * error + self.ki * self.integral + self.kd * derivative

        # Publiser PID-pådrag
        cmd = Float64MultiArray()
        cmd.data = [output]
        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args) # starter ROS2
    node = QubeController() # oppretter noden
    rclpy.spin(node) # kjører til den stoppes
    node.destroy_node() # lukker subscriptions og publishers
    rclpy.shutdown()