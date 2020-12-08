#!/usr/bin/env python

import roslib
import rospy
import smach
import smach_ros
import time
import random
import std_msgs
import geometry_msgs
from rospy.numpy_msg import numpy_msg


from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, Point, Pose
from nav_msgs.msg import Odometry
from tf import transformations
import math
import actionlib
import actionlib_msgs.msg
import actionlib.msg
import motion_plan.msg 
import time
from  std_msgs.msg import Int32
from actionlib_msgs.msg import GoalID


# INSTALLATION
# - create ROS package in your workspace:
#          $ catkin_create_pkg smach_tutorial std_msgs rospy
# - move this file to the 'smach_tutorial/scr' folder and give running permissions to it with
#          $ chmod +x state_machine.py
# - run the 'roscore' and then you can run the state machine with
#          $ rosrun smach_tutorial state_machine.py
# - install the visualiser using
#          $ sudo apt-get install ros-kinetic-smach-viewer
# - run the visualiser with
#          $ rosrun smach_viewer smach_viewer.py
# source ~/my_ros/devel/setup.bash 

rec_cmd = 'goNormal'
tgx = 0
tgy = 0

global detected
detected = 0
global status
status = 0

def detectedCallback(data):
    global detected
    detected = data.data




def random_coord():
    """Generates a random coordinate

    Returns:
        [int]: [integer coordinate]
    """
    return random.choice([-6, -4, -2, 0, 2, 4, 6])

def cmdCallback(data):
    global status
    if data.status_list:
        statuslist =  data.status_list
        #print(statuslist)
        #print(statuslist[0].status)
        #rospy.loginfo(rospy.get_caller_id() + "I heard %s",  statuslist[1])
        status = statuslist[0].status
    else:
        status = 0

# define state Sleep
class Sleep(smach.State):
    """Defines the state SLEEP

    
    """
    def __init__(self):
        # initialisation function, it should not wait
        smach.State.__init__(self, 
                             outcomes=['goSleep','goNormal'],
                             input_keys=['sleep_counter_in'],
                             output_keys=['sleep_counter_out'])
        self.pub = rospy.Publisher('miro_state', std_msgs.msg.Int32 , queue_size=1)
        self.pubgoal = rospy.Publisher('/reaching_goal2/goal', motion_plan.msg.PlanningActionGoal, queue_size=10)
        global status
        
    def execute(self, userdata):
        # function called when exiting from the node, it can be blacking
        hello_str = 0
        #rospy.loginfo(hello_str)
        self.pub.publish(hello_str)
        plan = motion_plan.msg.PlanningActionGoal()
        plan.goal.target_pose.pose.position.x = -6
        plan.goal.target_pose.pose.position.y = -6 
        self.pubgoal.publish(plan)
        rospy.loginfo('SLEEP, miro is tired, commands will be ignored for some time')
        #time.sleep(15)
        while status!=3:
            #rospy.loginfo("status is %d"%status)
            time.sleep(1)
        time.sleep(5)
        
        userdata.sleep_counter_out = 0
        return 'goNormal'
    

# define state NORMAL
class Normal(smach.State):
    """Defines the state NORMAL

    
    """
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['goSleep','goNormal', 'goPlay'],
                             input_keys=['sleep_counter_in'],
                             output_keys=['sleep_counter_out'])
        self.Normal_counter = 0
        self.pub = rospy.Publisher('miro_state', std_msgs.msg.Int32 , queue_size=1)
        #rospy.Subscriber("ext_command", assignment1.msg.Command, cmdCallback)
        global detected
        self.pubgoal = rospy.Publisher('/reaching_goal2/goal', motion_plan.msg.PlanningActionGoal, queue_size=10)
        rospy.Subscriber("/reaching_goal2/status",  actionlib_msgs.msg.GoalStatusArray, cmdCallback)
        global status
        self.canc_goalpub = rospy.Publisher('/reaching_goal2/cancel', GoalID , queue_size=1)

        self.rate = rospy.Rate(200)  # Loop at 200 Hz
    
    def execute(self, userdata):
        while not rospy.is_shutdown():  
            rospy.Subscriber("object_detection", Int32, detectedCallback)
            plan = motion_plan.msg.PlanningActionGoal()
            #check to see if previous planning action has suceeded
            if detected == 0 and (status==0 or status ==3):

                plan.goal.target_pose.pose.position.x = random_coord()
                plan.goal.target_pose.pose.position.y = random_coord()
                #rospy.loginfo('going to point')
                self.pubgoal.publish(plan)
                time.sleep(1)

            if detected == 1:
                #cancel the actual command and go to play state
                canc = GoalID()
                
                self.canc_goalpub.publish(canc)
                return  'goPlay'


            hello_str = 1
            #rospy.loginfo(hello_str)
            self.pub.publish(hello_str)
            time.sleep(1)
            userdata.sleep_counter_out = userdata.sleep_counter_in + 1
            if (userdata.sleep_counter_in+1>120):
                return  'goSleep'

            self.Normal_counter += 1
            self.rate.sleep

class Play(smach.State):
    """Defines the state PLAY

    
    """
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['goSleep','goNormal', 'goPlay'],
                             input_keys=['sleep_counter_in'],
                             output_keys=['sleep_counter_out'])
        self.Play_counter = 0
        self.pub = rospy.Publisher('miro_state', std_msgs.msg.Int32 , queue_size=1)
        self.rate = rospy.Rate(200)  # Loop at 200 Hz

    def execute(self, userdata):
        while not rospy.is_shutdown():  

            hello_str = 2
            #rospy.loginfo(hello_str)
            self.pub.publish(hello_str)
            rospy.loginfo('PLAY, chasing ball')
            time.sleep(1)
            userdata.sleep_counter_out = userdata.sleep_counter_in + 1
            if (userdata.sleep_counter_in+1>120):
                return  'goSleep'
            #if the ball stops being detected count and after some time if nothing is detected go back to normal state
            if detected == 0:
                self.Play_counter = self.Play_counter +1
            if detected == 1:
                self.Play_counter = 0
            
            
            if self.Play_counter > 5:
                self.Play_counter = 0
                return  'goNormal'
            
            self.rate.sleep



def main():
    """Initialization of the finite state machine
    """
    rospy.init_node('miro_state_machine')

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['container_interface'])
    sm.userdata.sm_counter = 0


   

    # Open the container
    with sm:
       
        smach.StateMachine.add('NORMAL', Normal(), 
                               transitions={'goSleep':'SLEEP', 
                                            'goNormal':'NORMAL',
                                            'goPlay':'PLAY'},
                               remapping={'sleep_counter_in':'sm_counter', 
                                          'sleep_counter_out':'sm_counter'})
        smach.StateMachine.add('SLEEP', Sleep(), 
                               transitions={'goSleep':'SLEEP', 
                                            'goNormal':'NORMAL'},
                               remapping={'sleep_counter_in':'sm_counter',
                                          'sleep_counter_out':'sm_counter'})
        smach.StateMachine.add('PLAY', Play(), 
                               transitions={'goSleep':'SLEEP', 
                                            'goNormal':'NORMAL',
                                            'goPlay':'PLAY',},
                               remapping={'sleep_counter_in':'sm_counter',
                                          'sleep_counter_out':'sm_counter'})
        
                                                    
                                    

    # Create and start the introspection server for visualization
    sis = smach_ros.IntrospectionServer('server_miro', sm, '/SM_ROOT')
    sis.start()

    # Execute the state machine
    outcome = sm.execute()
   

    # Wait for ctrl-c to stop the application
    rospy.spin()
    sis.stop()


if __name__ == '__main__':
    main()

