#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int32.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>

ros::Publisher vel_pub;
bool reached_target = false;

void LidarCallback(const sensor_msgs::LaserScan::ConstPtr& msg)
{
    if (!reached_target) {
        return;  // 如果未到达目标位置，则不发送速度消息
    }

    float fMidDist = msg->ranges[0];
    float fMidDist1 = msg->ranges[90];
    ROS_INFO("后方测距 range[0] = %f m, 左方距离 range[90] = %f m", fMidDist, fMidDist1);

    geometry_msgs::Twist vel_cmd;
    if (fMidDist > 0.39)
    {
        vel_cmd.linear.x = -0.1;
        if (fMidDist1 > 0.35)
            vel_cmd.linear.y = -0.1;
    }
    if (fMidDist < 0.37)
    {
	vel_cmd.linear.x = 0;
	if (fMidDist1 < 0.25)
            vel_cmd.linear.y = -0;
    }
	
    vel_pub.publish(vel_cmd);
}

void poseCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg)
{
    double x = msg->pose.pose.position.x;
    double y = msg->pose.pose.position.y;
    double z = msg->pose.pose.position.z;

    ROS_INFO("Position: x = %.2f, y = %.2f, z = %.2f", x, y, z);

    // 设置目标位置的范围，允许0.05m的误差
    double target_x = 0.460;  // 目标位置的x坐标
    double target_y = -2.79;  // 目标位置的y坐标
    double tolerance = 0.16;  // 允许的误差范围

    // 在此处添加判断逻辑，确定是否达到目标位置
    if (x >= target_x - tolerance && x <= target_x + tolerance &&
        y >= target_y - tolerance && y <= target_y + tolerance) {
        reached_target = true;
        ROS_INFO("Reached target position!");
    }
}

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "combined_node");
    ros::NodeHandle nh;

    ros::Subscriber lidar_sub = nh.subscribe<sensor_msgs::LaserScan>("/scan", 10, LidarCallback);
    ros::Subscriber pose_sub = nh.subscribe<geometry_msgs::PoseWithCovarianceStamped>("/amcl_pose", 10, poseCallback);

    vel_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 10);

    ros::spin();

    return 0;
}
