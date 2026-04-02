from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
import xacro

def generate_launch_description():
    # Finner xacro-filen i qube_description
    pkg_share = get_package_share_directory('qube_description')
    urdf_path = os.path.join(pkg_share, 'urdf', 'qube.urdf.xacro')

    # Konverterer xacro til URDF
    robot_description_content = xacro.process_file(urdf_path).toxml()

    # Publiserer URDF-en, oppdaterer leddene
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )

    # Visualisering
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_share, 'config', 'config.rviz')]
    )

    # Slider-GUI for å styre leddene manuelt. Venter 1 sek sånn at robot_state_publisher kjører først.
    joint_gui = TimerAction(
        period=1.0,
        actions=[
            Node(
                package='joint_state_publisher_gui',
                executable='joint_state_publisher_gui',
                name='joint_state_publisher_gui'
            )
        ]
    )

    return LaunchDescription([
        node_robot_state_publisher,
        node_rviz,
        joint_gui
    ])