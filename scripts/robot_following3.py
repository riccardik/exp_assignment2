#!/usr/bin/env python

# Python libs
import sys
import time

# numpy and scipy
import numpy as np
from scipy.ndimage import filters

import imutils

# OpenCV
import cv2

# Ros libraries
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
import std_msgs
from  std_msgs.msg import Float64
from  std_msgs.msg import Int32
VERBOSE = False

global reached
global mirostate
mirostate = 1
reached = 1

class image_feature:

    def __init__(self):
        '''Initialize ros publisher, ros subscriber'''
        rospy.init_node('image_feature', anonymous=True)
     # topic where we publish
        self.image_pub = rospy.Publisher("/robot2/output/image_raw/compressed",
                                         CompressedImage, queue_size=1)
        self.vel_pub = rospy.Publisher("robot2/cmd_vel",
                                       Twist, queue_size=1)
        self.ang_pub = rospy.Publisher("/robot2/joint1_position_controller/command",
                                           Float64,  queue_size=3)
        self.detection_pub = rospy.Publisher("object_detection",
                                           Int32,  queue_size=3)
        # subscribed Topic
        self.subscriber = rospy.Subscriber("robot2/camera1/image_raw/compressed",
                                           CompressedImage, self.callback,  queue_size=1)
        
        self.substate = rospy.Subscriber("miro_state",
                                           Int32, self.statecallback,  queue_size=1)

    def statecallback(self, data):
        global mirostate
        mirostate = data.data

    def callback(self, ros_data):
        '''Callback function of subscribed topic. 
        Here images get converted and features detected
        If the ball is detected a message will be setn to the state machine
        when the state machine will commute to the PLAY state the function will send
        cmd_vel msg to the robot'''
        if VERBOSE:
            print ('received image of type: "%s"' % ros_data.format)

        #### direct conversion to CV2 ####
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # OpenCV >= 3.0:

        greenLower = (50, 50, 20)
        greenUpper = (70, 255, 255)

        blurred = cv2.GaussianBlur(image_np, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        #cv2.imshow('mask', mask)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None

        global reached
        # only proceed if at least one contour was found
        if len(cnts) > 0 :
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            detected = Int32()
            detected.data = 1
            self.detection_pub.publish(detected)
            #print ('mirostate: [%d]' % mirostate)
            # only proceed if the radius meets a minimum size
            if radius > 10 and mirostate == 2:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(image_np, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(image_np, center, 5, (0, 0, 255), -1)
                vel = Twist()
                vel.angular.z = -0.002*(center[0]-400)
                vel.linear.x = -0.01*(radius-100)
                self.vel_pub.publish(vel)
                
                #rospy.loginfo('%d'%reached)
                if  vel.angular.z < 0.05 and vel.angular.z > -0.05 and vel.linear.x < 0.05 and vel.linear.x > -0.05 and reached == 0:
                    rospy.loginfo('Moving head')
                    vel.angular.z = 0
                    vel.linear.x = 0
                    self.vel_pub.publish(vel)
                    ang1 = Float64()
                    ang1.data = 0
                    self.ang_pub.publish(ang1)
                    time.sleep(2)
                    ang1.data = -0.7
                    self.ang_pub.publish(ang1)
                    time.sleep(2)
                    ang1.data = 0
                    self.ang_pub.publish(ang1)
                    time.sleep(1)
                    ang1.data = 0.7
                    self.ang_pub.publish(ang1)
                    time.sleep(2)
                    ang1.data = 0
                    self.ang_pub.publish(ang1)
                    reached = 1
                elif  vel.angular.z > 0.05 and vel.linear.x > 0.05 :
                    
                    reached = 0

            else:
                if  mirostate == 2:
                    #aligned
                    vel = Twist()
                    vel.linear.x = 0.5
                    self.vel_pub.publish(vel)
                    reached = 0

        else:
            #green not found
            """  vel = Twist()
            vel.angular.z = 0.5
            self.vel_pub.publish(vel)
            reached = 0 """
            detected = Int32()
            detected.data = 0
            self.detection_pub.publish(detected)
            reached = 0

        cv2.imshow('window', image_np)
        cv2.waitKey(2)

        # self.subscriber.unregister()


def main(args):
    '''Initializes and cleanup ros node'''
    ic = image_feature()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print ("Shutting down ROS Image feature detector module")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
