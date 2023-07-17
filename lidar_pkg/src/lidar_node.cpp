#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include<geometry_msgs/Twist.h>

ros::Publisher vel_pub;

void LidarCallback(const sensor_msgs::LaserScan msg)
{
    float fMidDist = msg.ranges[180];
    ROS_INFO("前方测距 range[180] = %f m", fMidDist);


    geometry_msgs::Twist vel_cmd;
    if (fMidDist< 1.5 && fMidDist >0.5)
    {
        vel_cmd. linear.x = 0.1;
    }
    else
    {
        vel_cmd.linear.x = 0.0;
    }
}
int main(int argc, char *argv[])
{
    setlocale(LC_ALL,"");
    ros::init(argc, argv, "lidar_node");


    ros::NodeHandle n;
    ros::Subscriber lidar_sub = n.subscribe("/scan", 10, &LidarCallback);
    vel_pub = n.advertise<geometry_msgs::Twist>("/cmd_vel", 10); 
    ros::spin();
    return 0;
}
