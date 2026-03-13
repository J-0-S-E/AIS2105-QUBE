import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    qube_driver_pkg = get_package_share_directory('qube_driver')
    qube_bringup_pkg = get_package_share_directory('qube_bringup')

    urdf = xacro.process_file(
        os.path.join(qube_bringup_pkg, 'urdf', 'controlled_qube.urdf.xacro')
    )
    robot_description = {'robot_description': urdf.toxml()}

    qube_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(qube_driver_pkg, 'launch', 'qube_driver.launch.py')
        )
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description]
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
    )

    return LaunchDescription([
        qube_driver_launch,
        robot_state_publisher,
        rviz,
    ])