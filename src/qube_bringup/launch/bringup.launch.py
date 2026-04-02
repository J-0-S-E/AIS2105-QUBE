import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # Henter install-stier til pakkene vi bruker
    qube_bringup_pkg = get_package_share_directory('qube_bringup')
    qube_driver_pkg = get_package_share_directory('qube_driver')
    qube_description_pkg = get_package_share_directory('qube_description')

    # Default values; kan endres fra terminalen, f.eks: simulation:=false, device:=/dev/ttyACM0
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

    # Kjører xacro ved oppstart. Sender argumentene inn i URDF-en.
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

    # Publiserer URDF-en og oppdaterer ledd-transformasjonene
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
    )

    # Starter controller_manager, joint_state_broadcaster og velocity_controller
    qube_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(qube_driver_pkg, 'launch', 'qube_driver.launch.py')
        )
    )

    # Visualisering i rviz med konfig fra qube_description
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