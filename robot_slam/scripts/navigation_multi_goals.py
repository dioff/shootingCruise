#!/usr/bin/env python

#coding: utf-8

import rospy
import actionlib
from actionlib_msgs.msg import *
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf_conversions import transformations
from math import pi
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from ar_track_alvar_msgs.msg import AlvarMarker
from geometry_msgs.msg  import Point
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import os

music_path="~/'00.mp3'"
id = 255
flog0 = 255
flog1 = 255
flog2 = 255
flog3 = 255
flog4 = 255
flog5 = 255
flog6 = 255
flog7 = 255
flog8 = 255
count = 0
move_flog = 0

class navigation_demo:
    def __init__(self):
        self.set_pose_pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=5)
        self.arrive_pub = rospy.Publisher('/voiceWords',String,queue_size=10)
        self.ar_sub = rospy.Subscriber('/object_position', Point, self.ar_cb);
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        self.move_base.wait_for_server(rospy.Duration(60))
    
    def ar_cb(self, data):
        global id  
        global flog0 , flog1 ,flog2,count,move_flog,flog3,flog4,flog5,flog6,flog7,flog8
        id =255
        point_msg = data
        #rospy.loginfo('z = %d', point_msg.z)
    
        if (point_msg.z != 255  and move_flog == 0) :
            if(point_msg.z>=1 and point_msg.z<=20 and flog0 ==255):
                id = 0
                flog0 = 0 
            elif(point_msg.z>=21 and point_msg.z<=40 and flog1 ==255):
                id = 1
                flog1 = 1 
            elif(point_msg.z>=41 and point_msg.z<=60 and flog2 ==255):
                id = 2
                flog2 = 2
            elif(point_msg.z>=61 and point_msg.z<=80 and flog3 ==255):
                id = 3
                flog3 = 3
            elif(point_msg.z>=81 and point_msg.z<=100 and flog4 ==255):
                id = 4
                flog4 = 4
            
            elif(point_msg.z>=101 and point_msg.z<=120 and flog5 ==255):
                id = 5
                flog5 = 5 
            
            elif(point_msg.z>=121 and point_msg.z<=140 and flog6 ==255):
                id = 6
                flog6 = 6 
           
            elif(point_msg.z>=141 and point_msg.z<=160 and flog7 ==255):
                id = 7
                flog7 = 7
            
            elif(point_msg.z>=161 and point_msg.z<=180 and flog8 ==255):
                id = 8
                flog8 = 8
       
        elif (point_msg.z != 255 and move_flog == 1):
            if (point_msg.z>=1 and point_msg.z<=20):
                id = 0
            elif(point_msg.z>=21 and point_msg.z<=40):
                id = 1
            elif(point_msg.z>=41 and point_msg.z<=60):
                id = 2
            elif(point_msg.z>=61 and point_msg.z<=80):
                id = 3
               
            elif(point_msg.z>=81 and point_msg.z<=100):
                id = 4
            
            elif(point_msg.z>=101 and point_msg.z<=120):
                id = 5
            
            elif(point_msg.z>=121 and point_msg.z<=140):
                id = 6
            
            elif(point_msg.z>=141 and point_msg.z<=160):
                id = 7
            
            elif(point_msg.z>=161 and point_msg.z<=180):
                id = 8
       
        #print flog0 , flog1 , flog2
        #rospy.loginfo('id = %d', id)
    def set_pose(self, p):
        if self.move_base is None:
            return False

        x, y, th = p

        pose = PoseWithCovarianceStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = 'map'
        pose.pose.pose.position.x = x
        pose.pose.pose.position.y = y
        q = transformations.quaternion_from_euler(0.0, 0.0, th/180.0*pi)
        pose.pose.pose.orientation.x = q[0]
        pose.pose.pose.orientation.y = q[1]
        pose.pose.pose.orientation.z = q[2]
        pose.pose.pose.orientation.w = q[3]

        self.set_pose_pub.publish(pose)
        return True

    def _done_cb(self, status, result):
        rospy.loginfo("navigation done! status:%d result:%s"%(status, result))
        arrive_str = "arrived to traget point"
        self.arrive_pub.publish(arrive_str)

    def _active_cb(self):
        rospy.loginfo("[Navi] navigation has be actived")

    def _feedback_cb(self, feedback):
        msg = feedback
        #rospy.loginfo("[Navi] navigation feedback\r\n%s"%feedback)

    def goto(self, p):
        rospy.loginfo("[Navi] goto %s"%p)
        #arrive_str = "going to next point"
        #self.arrive_pub.publish(arrive_str)
        goal = MoveBaseGoal()

        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = p[0]
        goal.target_pose.pose.position.y = p[1]
        q = transformations.quaternion_from_euler(0.0, 0.0, p[2]/180.0*pi)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3]

        self.move_base.send_goal(goal, self._done_cb, self._active_cb, self._feedback_cb)
        result = self.move_base.wait_for_result(rospy.Duration(60))
        if not result:
            self.move_base.cancel_goal()
            rospy.loginfo("Timed out achieving goal")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("reach goal %s succeeded!"%p)
        return True

    def cancel(self):
        self.move_base.cancel_all_goals()
        return True
if __name__ == "__main__":
    rospy.init_node('navigation_demo',anonymous=True)
    goalListX = rospy.get_param('~goalListX', '2.0, 2.0')
    goalListY = rospy.get_param('~goalListY', '2.0, 4.0')
    goalListYaw = rospy.get_param('~goalListYaw', '0, 90.0')

    goals = [[float(x), float(y), float(yaw)] for (x, y, yaw) in zip(goalListX.split(","),goalListY.split(","),goalListYaw.split(","))]
    print ('Please 1 to continue: ')
    input = raw_input()
    print (goals)
    r = rospy.Rate(1)
    r.sleep()
    navi = navigation_demo()

    if (input == '1'):
        navi.goto(goals[0])
        rospy.sleep(5)
	print(flog0)
	print(flog1)
	print(flog3)
    if (flog0+flog3+flog1 <= 255):
        move_flog=1
        os.system('mplayer %s' % music_path)  
        navi.goto(goals[1])
        rospy.sleep(3) 

        count = 0
        navi.goto(goals[2])
        rospy.sleep(3)         
        if (id == flog0 or id == flog1 or id == flog3 ):    
            os.system('mplayer ~/0%s.mp3' % str(int(id) + 1))
            navi.goto(goals[3])
            rospy.sleep(2)
   	    count += 1
            if count ==  3:
		print(count)
                navi.goto(goals[14])
		rospy.sleep(30)          
        
        navi.goto(goals[4])   
        rospy.sleep(3)  
        if (id == flog0 or id == flog1 or id == flog3 ):
            os.system('mplayer ~/0%s.mp3' % str(int(id) + 1))
            navi.goto(goals[5])
            rospy.sleep(2)
            count += 1
            if count ==  3:
		print(count)
                navi.goto(goals[14])
		rospy.sleep(30)
        navi.goto(goals[6])   
        rospy.sleep(3)  
        if (id == flog0 or id == flog1 or id == flog3 ):
            os.system('mplayer ~/0%s.mp3' % str(int(id) + 1))
            navi.goto(goals[7])
            rospy.sleep(2) 
            count += 1
            if count ==  3:
		print(count)
                navi.goto(goals[14])
		rospy.sleep(30)
        navi.goto(goals[8])   
        rospy.sleep(3)  
        if (id == flog0 or id == flog1 or id == flog3 ):
            os.system('mplayer ~/0%s.mp3' % str(int(id) + 1))
            navi.goto(goals[9])
            rospy.sleep(2)
            count += 1
            if count ==  3:
		print(count)
                navi.goto(goals[14])
		rospy.slepp(30)
        navi.goto(goals[10])   
        rospy.sleep(3)  
        if (id == flog0 or id == flog1 or id == flog3 ):
            os.system('mplayer ~/0%s.mp3' % str(int(id) + 1))
            navi.goto(goals[11])
            rospy.sleep(2)
            count += 1
            if count ==  3:
		print(count)
                navi.goto(goals[14])  
        	rospy.slepp(30)
        navi.goto(goals[12])   
        rospy.sleep(4)  
        if (id == flog0 or id == flog1 or id == flog3 ):
            os.system('mplayer ~/0%s.mp3' % str(int(id) + 1))
            navi.goto(goals[13])
            rospy.sleep(2)
            count += 1
            if count ==  3:
		print(count)
                navi.goto(goals[14]) 
		rospy.slepp(30)
        navi.goto(goals[14])

        
    while not rospy.is_shutdown():
        r.sleep()
