import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    qube_bringup_pkg = get_package_share_directory('qube_bringup')
    qube_driver_pkg = get_package_share_directory('qube_driver')
    qube_description_pkg = get_package_share_directory('qube_description')

    # Launch-argumenter for enkel bytte mellom simulering og fysisk hardware
    simulation_arg = DeclareLaunchArgument(
        'simulation', default_value='true',
        description='Bruk simulert hardware (true) eller fysisk QUBE (false)'
    )
    device_arg = DeclareLaunchArgument(
        'device', default_value='/dev/ttyACM0',
        description='Seriell enhet for QUBE (f.eks. /dev/ttyACM0)'
    )
    baud_rate_arg = DeclareLaunchArgument(
        'baud_rate', default_value='115200',
        description='Baud rate for seriellkommunikasjon'
    )

    # Prosesser URDF med xacro ved launch-tid slik at argumentene sendes videre
    xacro_file = os.path.join(qube_bringup_pkg, 'urdf', 'controlled_qube.urdf.xacro')
    robot_description = ParameterValue(
        Command([
            'xacro ', xacro_file,
            ' simulation:=', LaunchConfiguration('simulation'),
            ' device:=', LaunchConfiguration('device'),
            ' baud_rate:=', LaunchConfiguration('baud_rate'),
        ]),
        value_type=str
    )

    # Robot state publisher - publiserer robot_description til /robot_description topic
    # som ros2_control_node abonnerer på for å laste hardware-interface
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
    )

    # Inkluder qube_driver launch (controller_manager + joint_state_broadcaster + velocity_controller)
    qube_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(qube_driver_pkg, 'launch', 'qube_driver.launch.py')
        )
    )

    # RViz med ferdig konfigurert visning
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(qube_description_pkg, 'config', 'config.rviz')],
    )

    return LaunchDescription([
        simulation_arg,
        device_arg,
        baud_rate_arg,
        robot_state_publisher,
        qube_driver_launch,
        rviz,
    ])