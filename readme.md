

# Experimental Robotics Laboratory - Assignment 2
## Riccardo Lastrico - 4070551

### Assignment contents 
<p>The assignment content is an exercise based on ROS about a finite state machine that represent a pet-like robot behavior; this robot moves in a 3D simulation using Gazebo and is equipped with an RGB camera. Using that camera, is able to recognize a ball that moves around in the environment, following the user's commands.

Map of the environment:

![map](./map_area.png)
</p>

### System architecture
<p>
This is a graph of the system architecture (obtained via rqt-graph):

![System Architecture](./system_architecture.png)


</p>



#####  Implemented nodes
<p>

The node <code>state_miro</code> contains the state machine that will be described right after this paragraph.
The node <code>cmd_generator</code> sends commands to the ball's action server (<code>reaching_goal</code>) and moves it in the space or makes it disappear; the commands could be sent by the user or could be random.
The node <code>image_feature</code> receives the image from the camera and if detects a ball sends a message to the <code>state_miro</code> node; when the state machine will change state, this node will also send <code>cmd_vel</code> messages to the robot depending on the distance from the ball.
The node <code>reaching_goal2</code> is the robot action server.
### System states
<p>
This is a graph of the possible states (obtained via smach-viewer):

![System Architecture](./state_machine.png)

The possible states are: 
<ul>
<li><code>SLEEP</code>, the robot is sleeping and so it wont respond to any command. After a while in any other state, even if not commanded to do so, it reaches location [-6,-6]. After some amount of time, the robot goes again in state <code>NORMAL</code>. </li>
<li><code>NORMAL</code>, the robot is in the predefined state, it moves randomly around the map until he detects the ball in his lane of sight: the robot will than pass to the <code>PLAY</code> state. </li>

<li><code>PLAY</code>, the robot enters in this state from the <code>NORMAL</code> one after seeing the ball: it chases it until it stops moving, than moves his head 45° to the left and to the right, then it continues staring the ball until it moves. If the ball disappears, the robot will go back to the <code>NORMAL</code> state.

</li>
</ul>
</p>

#####  Packages and file list
<p>
The only package that is present is <code>exp_assignment2</code>, which contains all the executable files.
In particular, we have:

 - `src` folder:
	 
	 - `moveclient.cpp`: contains the code to rotate the robot neck of a certain angle;

 - `scripts` folder:
	 - `state_machine_miro_ext.py`: is the state machine of the robot;
	 - `ball_c.py` and `ball_c_random.py` that are responsible for the generation of the command for the ball, the first program recevies input from the user and the second generates them randomly, the node is called `cmd_generator`.
     - `go_to_point_action.py`: contains the code for the action server of the robot, reads the goal from the `reaching_goal2/goal` topic, where the node `miro_state machine` writes a coordinate; the node is called `reaching_goal2`.
     - `go_to_point_ball.py`: contains the code for the action server of the ball, reads the goal from the `reaching_goal/goal` topic, where the node `cmd_generator` writes a coordinate;the node is called `reaching_goal`.
     - `robot_following3.py`: contains the code `image_feature`, this node perform the blob detection on the image from the camera and if the robot is in the `PLAY` state also sends `cmd_vel` commands to the robot.
 - `launch` folder:
     - `display.launch`: launch file that launches Rviz to check the model of the robot;
     - `gazebo_world2.launch`: launches the simulation where commands are received from the user;
     - `gazebo_world2_random.launch`: launches the simulation where commands are generated randomly;

</p>

### Installation 
<p>This is a ROS package, so it will be necessary to clone this repository into the <code>src</code> folder of a ROS workspace (here is assumed to be named <code>my_ros</code>):
    
	
    cd ~/my_ros/src
    git clone
    catkin_make --pkg exp_assignment2

    
Some packages are needed:

    smach-viewer
    cv_bridge
    actionlib
    actionlib_msgs
    image_transport
</p>

### Run the simulation 
<p>To easily run the simulation i created a launch file, that can be used this way:

    
    source ~/my_ros/devel/setup.bash 
    roslaunch exp_assignment2 gazebo_world2_random.launch

This runs the random simulation, the state of the robot will be outputted on the shell with the information about the command received and an eventual change of state.

If you want to interact with the simulation by giving direct commands you have to run:
    
    source ~/my_ros/devel/setup.bash 
    roslaunch exp_assignment2 gazebo_world2.launch

and then open a new shell and run:

    source ~/my_ros/devel/setup.bash 
    rosrun exp_assignment2 ball_c.py 
A command line interface willconsent to send commands to move the ball or make it disappear.

For both, an additional window will open: this contains the output image from the robot's camera:

![cameraview](./cameraview.png)
</p>

### System features 
<p>
The system features a finite-state machine using the <code>Smach</code> packet and a simulation done via Gazebo: the robot contains a "navigation by following" appproach, using "color blob recognition" to recognize a green ball in the image provied by the camera; the robot itself features the camera, two actuated joints (the wheels) and an additional one, the neck, that can be moved around the roll axis. 
The system also features the possibility to be controlled by the user or behave fully randomly.

This is the robot:

![robot](./robot.png)


</p>

### System limitation
<p>
Sometimes the ball movement makes the robot "roll over" itself and goes into a position where it cannot move anymore and have to be "flipped" manually from the user. Other times, in the generation of the random movements, more request of actions overlap and the action server so do not properly behave as planned; time delays did not solve the problem, this is not actually a big issue because the movement should be random, nevertheless is a non desired behavior. 
</p>

### Possible improvements
<p>
Add a velocity control for the robot when the ball moves really close to it and find a way to avoid the overlap of the action requests.
Speaking of the velocity control, the robot itself is a bit slow, the control of the velocity could be improved by accelerating slowly at the beginning and then increase when it is moving, to avoid a big acceleration at the beginning that will flip the robot. I added a tail that could possibly avoid the flipping and improve the robot stability while accelerating but i haven't done a lot of testing to see if it is effective.
</p>

### Documentation
<p>
The documentation is accessible in:

    ./doc/html/index.html

</p>

### Contacts
<p>
Riccardo Lastrico - 4070551

Email: riky.lastrico@gmail.com
</p>
