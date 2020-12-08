#!/usr/bin/env python
# license removed for brevity
import rospy

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


global status 
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

def talker():
    """ 
    initialize a ROS publisher. 
  
    The function takes from the shell input (or generates randomly) a command and a point (if necessary) and publish it into the topic 
  
  
    """
    pub = rospy.Publisher('/reaching_goal2/goal', motion_plan.msg.PlanningActionGoal, queue_size=10)
    rospy.init_node('cmd_generator', anonymous=True)
    rate = rospy.Rate(1) # 10hz



    rospy.Subscriber("/reaching_goal2/status",  actionlib_msgs.msg.GoalStatusArray, cmdCallback)


    sendcmd = 0
    plan = motion_plan.msg.PlanningActionGoal()
    rospy.loginfo("going to 0 0")
    plan.goal.target_pose.pose.position.x = 0
    plan.goal.target_pose.pose.position.y = 0
    pub.publish(plan)
    time.sleep(1)
    global status
    while not rospy.is_shutdown():
        """ plan = motion_plan.msg.PlanningActionGoal()
        plan.goal.target_pose.pose.position.x = -3
        plan.goal.target_pose.pose.position.y = -3
        pub.publish(plan) """
        rospy.loginfo("going to asdasd")
        while status!=3:
            rospy.loginfo("status is %d"%status)
            rate.sleep()
        rate.sleep()
        rospy.loginfo("going to 3 3")
        plan.goal.target_pose.pose.position.x = 3
        plan.goal.target_pose.pose.position.y = 3
        pub.publish(plan)
        while status!=1:
            rospy.loginfo("status is %d"%status)
            rate.sleep()

        while status!=3:
            rospy.loginfo("status is %d"%status)
            rate.sleep()
        rate.sleep()
        rospy.loginfo("going to -3 3")
        plan.goal.target_pose.pose.position.x = -3
        plan.goal.target_pose.pose.position.y = 3
        pub.publish(plan)
        while status!=1:
            rospy.loginfo("status is %d"%status)
            rate.sleep()

        while status!=3:
            rospy.loginfo("status is %d"%status)
            rate.sleep()
        rate.sleep()
        rospy.loginfo("going to -3 -3")
        plan.goal.target_pose.pose.position.x = -3
        plan.goal.target_pose.pose.position.y = -3
        pub.publish(plan)
        while status!=1:
            rospy.loginfo("status is %d"%status)
            rate.sleep()


        while status!=3:
            rospy.loginfo("status is %d"%status)
            rate.sleep()
        rate.sleep()
        rospy.loginfo("going to 3 -3")
        plan.goal.target_pose.pose.position.x = 3
        plan.goal.target_pose.pose.position.y = -3
        pub.publish(plan)
        while status!=1:
            rospy.loginfo("status is %d"%status)
            rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass