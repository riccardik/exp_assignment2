#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

from  exp_assignment2.msg import PlanningActionGoal

import time
import random



def talker():
    """ 
    initialize a ROS publisher. 
  
    The function takes from the shell input (or generates randomly) a command and a point (if necessary) and publish it into the topic 
  
  
    """
    pub = rospy.Publisher('/reaching_goal/goal', PlanningActionGoal, queue_size=10)
    rospy.init_node('cmd_generator', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    sendcmd = 0
    

    while not rospy.is_shutdown():
        rospy.loginfo('Command: (m)ove ball, (d)isappear ball:')
        cmdt = raw_input()
        if cmdt=='m':
            cmd = PlanningActionGoal()
            rospy.loginfo('insert x and y')
            cmdt = raw_input()
            cmd.goal.target_pose.pose.position.x = float(cmdt)
            cmdt = raw_input()
            cmd.goal.target_pose.pose.position.y = float(cmdt)
            cmd.goal.target_pose.pose.position.z = 0.5
            pub.publish(cmd)        
        elif cmdt=='d':
            cmd = PlanningActionGoal()
            cmd.goal.target_pose.pose.position.z = -0.5
            pub.publish(cmd) 
        else:
           rospy.loginfo('Wrong command')

    #""" hello_str1 = "hello world %s" % hello_str
     #   rospy.loginfo(hello_str1)
#
  #      cmd = Command()
 #       cmd.command = 'reach' """
        
        
        
        
        """ cmd.command = ''
        pub.publish(cmd) """
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass