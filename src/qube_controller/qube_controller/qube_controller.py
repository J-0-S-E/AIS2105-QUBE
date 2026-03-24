import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
from rcl_interfaces.msg import SetParametersResult


class QubeController(Node):
    """PID-kontroller for Quanser QUBE.

    Abonnerer på /joint_states for posisjon og hastighet,
    og publiserer hastighetspådrag til /velocity_controller/commands.

    Alle parametere kan endres ved runtime:
        ros2 param set /qube_controller target_position 1.57
        ros2 param set /qube_controller kp 3.0
    """

    def __init__(self):
        super().__init__('qube_controller')

        # Deklarer parametere slik at de kan endres ved runtime
        self.declare_parameter('kp', 2.0)
        self.declare_parameter('ki', 0.1)
        self.declare_parameter('kd', 0.5)
        self.declare_parameter('target_position', 0.0)

        self.kp = self.get_parameter('kp').value
        self.ki = self.get_parameter('ki').value
        self.kd = self.get_parameter('kd').value
        self.target_position = self.get_parameter('target_position').value

        self.prev_error = 0.0
        self.integral = 0.0
        self.prev_time = None

        # Callback for å oppdatere parametere ved runtime
        self.add_on_set_parameters_callback(self.parameter_callback)

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

        self.get_logger().info(
            f'Qube controller startet. Target: {self.target_position:.3f} rad, '
            f'PID: kp={self.kp}, ki={self.ki}, kd={self.kd}'
        )

    def parameter_callback(self, params):
        """Oppdaterer parametere når de endres med ros2 param set."""
        for param in params:
            if param.name == 'kp':
                self.kp = param.value
            elif param.name == 'ki':
                self.ki = param.value
            elif param.name == 'kd':
                self.kd = param.value
            elif param.name == 'target_position':
                self.target_position = param.value
                self.integral = 0.0  # Nullstill integralleddet ved ny referanse
                self.get_logger().info(f'Ny referansevinkel: {self.target_position:.3f} rad')
        return SetParametersResult(successful=True)

    def joint_state_callback(self, msg: JointState):
        """Leser posisjon fra joint_states og beregner PID-pådrag."""
        # Finn motor_joint i meldingen
        try:
            idx = msg.name.index('motor_joint')
        except ValueError:
            return

        position = msg.position[idx]

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

        # Publiser hastighetspådrag
        cmd = Float64MultiArray()
        cmd.data = [output]
        self.publisher.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = QubeController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()