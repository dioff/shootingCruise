#!/user/bin/env python
#coding: utf-8

from math import dist
import rospy
from sensor_msgs.msg import LaserScan

def LidarCallback(msg):
    disit = msg.range[180]
    rospy.loginfo("前方测距 ranges[180] = %f 米", dist)

if __name__ =="__main__":
    rospy.init_node("lidar_node")
    lidar_sub = rospy.Subscriber("/scan", LaserScan, LidarCallback,queue_size=10)
    rospy.spin()
