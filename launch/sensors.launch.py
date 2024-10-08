from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch_ros.actions import Node
from os.path import join

def generate_launch_description():
    pkg_path = get_package_share_directory('krytn')
    realsense = IncludeLaunchDescription(join(pkg_path, 'launch','rs_launch.launch.py'))

    rp_lidar = Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            name='rplidar_node',           
            output='screen',
            parameters=[{'frame_id':'rplidar'}])
    

    return LaunchDescription([realsense, 
                rp_lidar])