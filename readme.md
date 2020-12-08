

# Experimental Robotics Laboratory - Assignment 1
## Riccardo Lastrico - 4070551

### Assignment contents 
<p>The assignment content is an exercise based on ROS about a finite state machine that represent a pet-like robot behavior.
The robot moves into a 2D space and can receive external commands that may change its behavior.

</p>

### System architecture
<p>
This is a graph of the system architecture (obtained via rqt-graph):

![System Architecture](./system_architecture.png)


</p>

##### Implemented msgs
<p>
I implemented two messages:
<ul>
<li><code>Command.msg</code> which is used to send the message from the user to the robot:
<ul>
<li><code>Command</code>, string, is the name of the command to send;</li>
<li><code>a</code>, integer, is the <code>x</code> coordinate if the command <code>goLocation</code> is sent;</li>
<li><code>b</code>, integer, same as before, for the <code>y</code>coordinate.</li></ul>
</li>
<li><code>TargetPoint.msg</code> used to send the Target Point to the simulation viewer:
<ul>
<li><code>a</code>, integer, <code>x</code> coordinate;</li>
<li><code>b</code>, integer, <code>y</code> coordinate.</li></ul>
</li></ul>
</p>

#####  Implemented nodes
<p>

The node <code>state_miro</code> contains the state machine that will be described right after this paragraph. It receives message of the type <code>Command</code> from the <code>send_cmds</code> node (that can be random or user controlled) and sends message of the type <code>std_msgs.Integer</code> and <code>TargetPoint</code> at the node <code>velocity_control</code>; this node is responsible to perform the simulation and control the robot depending by its state.
</p>

### System states
<p>
This is a graph of the possible states (obtained via smach-viewer):

![System Architecture](./state_machine.png)

The possible states are: `sad`
<ul>
<li><code>SLEEP</code>, the robot is sleeping and so it wont respond to any command. After a while in any other state, even if not commanded to do so, it reaches this state for a certain amount of time and it reach location [-3,-4]. After that amount of time, the robot goes again in state NORMAL .</li>
<li><code>NORMAL</code>, the robot is in the predefined state, it moves randomly around the map, avaiting the <code>goPlay</code> command from the user. </li>

<li><code>PLAY</code>, the robot enters in this state from the <code>NORMAL</code> one after the <code>goPlay</code> command; the robot will reach the [0, 0] location and will wait for some time for an other istruction, if this instruction doesn't come it goes back to <code>NORMAL</code>. The possible commands are:
<ul>
<li><code>goNormal</code>, the robot goes back to the <code>NORMAL</code> state;</li>
<li><code>goPlay</code>, the robot stays in the <code>PLAY</code> state;</li>
<li><code>goSleep</code>, the robot goes to the <code>SLEEP</code> state;</li>
<li><code>goLocation</code>, the robot goes to the <code>REACH</code> state;</li>
</ul>
</li>
<li><code>REACH</code>, together with this command the robot will receive a coordinate of a 2D point and will reach it. After that, it will go back to the <code>PLAY</code> state.</li></ul>
</p>

#####  Packages and file list
<p>
The only package that is present is <code>assignment1</code>, which contains all the executable files.
In particular, we have:

 - `src` folder:
	 
	 - `exercise1.cpp`: contains the code that runs the simulator, the `velocity_control` node, that is an interface between the velocity control of the robot and the state machine;
	 - `state_machine_miro_ext.py`: is the state machine of the robot, which can receive commands from the extern, the node `state_miro`; that is an interface between the velocity 
	 - `state_c.py` and `state_c_random.py` that are responsible for the generation of the command, the first program recevies input from the user and the second generates them randomly, the node is called `send_cmds`.
 - <code>msg</code> folder:
     - `Command.msg`, described above;
     - `Targetpoint.msg`, described above.
 - `srv`folder:
     - `Genrandom.srv`, service impemented in class to generate a random point in the `NORMAL` behavior, could be simply avoided by implementing the function inside the `velocity_control` node.
 - <code>world</code> folder:
     - `exercise.world`, the map used in the `stage-ros` simulation;
     - `uoa_robotics_map.png`, image to visually represent the map.

</p>

### Installation 
<p>This is a ROS package, so it will be necessary to clone this repository into the <code>src</code> folder of a ROS workspace (here is assumed to be named <code>my_ros</code>):
    
	
    cd ~/my_ros/src
    git clone
    catkin_make --pkg assignment1

It happens that the compilation fails the first time because the files are compiled in the wrong order, doing it a couple of time should work.
    
There are two packages to be installed to see the state-machine changing and the robot moving in the map:

    smach-viewer
    stage-ros

</p>

### Run the simulation 
<p>To easily run the simulation i created a launch file, that can be used this way:

    
    source ~/my_ros/devel/setup.bash 
    roslaunch assignment1 miro_random.launch

This runs the random simulation, the state of the robot and its position in the space will be outputted on the shell with the information about the command received and an eventual change of state.
Smach-viewer from time to time stops to receive any update, even if the state-machine continues running, so it has to be close and restarted if happens so.

If you want to interact with the simulation by givin commands you have to run:
    
    source ~/my_ros/devel/setup.bash 
    roslaunch assignment1 miro_controlled.launch

and then open a new shell and run:

    source ~/my_ros/devel/setup.bash 
    roslaunch assignment1 state_c.py
A command line interface willconsent to send commands to the state machine.
</p>

### System features 
<p>
The system features a finite-state machine using the <code>Smach</code> packet and a simulation environment map using the <code>Stage-ros</code> packet; the simulation is the one of the classes esercitations that i modified to serve my purposes. The system also features the possibility to be controlled by the user or behave fully randomly.

This is the map of the simulation:

![map](./map.jpg)


</p>

### System limitation
<p>
Some parts of the system works by considering time delays instead of a closed control feedback, like the target reaching or the going to sleep function. This is done for semplicity and the time delays are chosen by observing statistically how the system behaves for a map of the chosen dimension, of course they could be not suitable for a bigger map. Also, sometimes some command in the <code>PLAY</code> state is ignored.
</p>

### Possible improvements
<p>
An improvement which would improve the overall system could be to overcome the control feedback problem by implementing it and not just using predefined time delays.
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
