#!/usr/bin/env python2
# -*- coding:utf-8 -*-


import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped, Twist

class CarContoller:
	def __init__(self):
		rospy.init_node('car_controller')
		self.target_pose = None
		self.current_pose = None
		self.velocity_pub = rospy.Publisher(' /cmd_vel', Twist, queue_size=10)
		self.pose_sub = rospy.Subscriber(' /amcl_pose', PoseWithCovarianceStamped, self.pose_callback)
	def pose_callback(self, msg):
		self.current_pose = msg.pose.pose
	def set_target_pose(self, target_pose):
		self.target_pose = target_pose
	def run(self):
		rate = rospy.Rate(10)
		
		while not rospy.is_shutdown():
			if self.target_pose is not None and self.current_pose is not None:
				distance = self.calculate_distaance(self.current_pose, self.target_pose)
				
				threshold = 0.1
				
				if distance <= threshold:
					
					velocity_cmd = Twist()
					velocity_cmd.linear.x = 1.0
					velocity_cmd.angular.z = 0.0
					self.velocity_pub.publish(velocity_cmd)
					rospy.loginfo("Reached")
					self.target_pose = None
				rate.sleep()
	def calculate_distance(self, pose1, pose2):
		
		dx = pose1.position.x - pose2.position.x
		dy = pose1.position.y - pose2.position.y
		distance = (dx **2 + dy **2) **0.5
if __name__ == 'main':
	try:
		controller = CarController()
		target_pose = PoseWithCovarianceStamped()
		target_pose.pose.pose.position.x = 1.12
		target_pose.pose.pose.position.y = -0.36
		controller.set_target_pose(target_pose.pose.pose)

		controller.run()
	except rospy.ROSInterrupException:
		pass
	


