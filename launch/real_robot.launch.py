from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from os.path import join
from launch.substitutions import Command

def generate_launch_description():

    # Create a robot in the world.
    # Steps: 
    # 1. Process a file using the xacro tool to get an xml file containing the robot description.
    # 2. Publish this robot description using a ros topic so all nodes can know about the joints of the robot. 
    # 3. Spawn a simulated robot in the gazebo simulation using the published robot description topic. 

    # Step 1. Process robot file. 
    robot_file = join(get_package_share_directory("krytn"), "robot_description","krytn","krytn.urdf.xacro")
    robot_xml = Command(["xacro ",robot_file, " ","gazebo:=False"])

    #Step 2. Publish robot file to ros topic /robot_description & static joint positions to /tf
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[{'robot_description':robot_xml, 
                     }],
        namespace="/krytn"        
    )

    # Step 5: Enable the ros2 controllers
    manager  = Node(
                package="controller_manager",
                executable="ros2_control_node",
                output="screen",
                parameters=[join(get_package_share_directory('krytn'),'config','diffdrive_control.yaml')],
                namespace="/krytn"

            )

    # Step 5: Enable the ros2 controllers
    start_controllers  = Node(
                package="controller_manager",
                executable="spawner",
                arguments=[ '-c', "/krytn/controller_manager",
                    'joint_state_broadcaster', 'diff_drive_base_controller'],
                output="screen",
            )
    
    twister = Node(
        package="twist_stamper",
        executable="twist_stamper",
        remappings=[("/cmd_vel_in",'/cmd_vel'),("/cmd_vel_out","/diff_drive_base_controller/cmd_vel")]
    )
    
    return LaunchDescription([ manager, robot_state_publisher, 
                               start_controllers, twister])