import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    navigation = LaunchConfiguration("navigation")
    slam = LaunchConfiguration("slam")
    is_public_sim = LaunchConfiguration("is_public_sim")

    tiago_gazebo_share = get_package_share_directory("tiago_gazebo")

    custom_world_path = os.path.join(
        tiago_gazebo_share,
        "worlds",
        "hospital_3.world"
    )

    base_launch_path = os.path.join(
        tiago_gazebo_share,
        "launch",
        "tiago_gazebo.launch.py"
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            "navigation",
            default_value="True"
        ),

        DeclareLaunchArgument(
            "slam",
            default_value="False"
        ),

        DeclareLaunchArgument(
            "is_public_sim",
            default_value="True"
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(base_launch_path),
            launch_arguments={
                "world_name": custom_world_path,
                "navigation": navigation,
                "slam": slam,
                "is_public_sim": is_public_sim,
            }.items(),
        ),
    ])
