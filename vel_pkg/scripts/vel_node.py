#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import rospy
from geometry_msgs.msg import Twist


def  velocity_publisher():
    rospy.init_node("velocity_publisher", anonymous=True) 
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    
    vel_msg = Twist()
    vel_msg .linear.x = 0.2
    vel_msg.angular.z = 0.0
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        vel_pub.publish(vel_msg)
        rospy.loginfo("V[%0.2f m/s %0.2f rad/s]",  vel_msg .linear.x, vel_msg.angular.z)
        rate.sleep()



if __name__ == "__mian__":
    try :
        velocity_publisher()
    except rospy.ROSInterruptException:
        pass
