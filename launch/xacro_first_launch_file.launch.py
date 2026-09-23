import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # Packages
    pkg_share = get_package_share_directory('xacro_first')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Fichiers
    xacro_file = os.path.join(
        pkg_share,
        'urdf',
        'my_robot.urdf.xacro'
    )

    world_file = os.path.join(
        pkg_share,
        'world',
        'my_robot.sdf'
    )

    bridge_config = os.path.join(
        pkg_share,
        'parametres',
        'parametres.yaml'
    )

    # Robot description
    robot_description = Command([
        'xacro ',
        xacro_file
    ])

    # =========================
    # Gazebo
    # =========================

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_ros_gz_sim,
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={'gz_args': '-s ' + world_file}.items()
    )

    # =========================
    # Launch description
    # =========================

    return LaunchDescription([

        # Gazebo
        gazebo,

        # =========================
        # Robot State Publisher
        # =========================

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',

            parameters=[
                {
                    'robot_description': ParameterValue(
                        robot_description,
                        value_type=str
                    ),
                    'use_sim_time': True
                }
            ]
        ),

        # =========================
        # Spawn du robot dans Gazebo
        # =========================

        Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_my_robot',
            output='screen',

            arguments=[
                '-topic',
                'robot_description',

                '-name',
                'my_robot',

                '-z',
                '0.1'
            ],

            parameters=[
                {
                    'use_sim_time': True
                }
            ]
        ),

        # =========================
        # ROS 2 <-> Gazebo Bridge
        # =========================

        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='ros_gz_bridge',
            output='screen',

            parameters=[
                {
                    'config_file': bridge_config,
                    'use_sim_time': True
                }
            ]
        ),
    ])