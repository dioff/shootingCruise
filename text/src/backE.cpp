#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int32.h>

ros::Publisher vel_pub;
bool received_number = false;
bool send_velocity = false;

void LidarCallback(const sensor_msgs::LaserScan::ConstPtr& msg)
{
    float fMidDist = msg->ranges[0];
    float fMidDist1 = msg->ranges[90];
    ROS_INFO("range[0] = %f m,range[90] = %f m", fMidDist, fMidDist1);

    if  (!send_velocity){
        return;
    }
    geometry_msgs::Twist vel_cmd;
    if (fMidDist > 0.35)
    {
        vel_cmd.linear.x = -0.3;
        if (fMidDist1 > 0.30)
            vel_cmd.linear.y = -0.3;
    }
    
    vel_pub.publish(vel_cmd);
}

void numCallback(const std_msgs::Int32::ConstPtr& msg)
{
    int received_num = msg->data;
    if (received_num == 1)
     {
        ROS_INFO("Received num: %d", received_num);
        received_number = true;
        send_velocity = true;
    } else {
        ROS_INFO("No received num: %d", received_num);
        received_number = false;
        send_velocity = false;
    }
}

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "combined_node");
    ros::NodeHandle nh;

    ros::Subscriber lidar_sub = nh.subscribe<sensor_msgs::LaserScan>("/scan", 10, LidarCallback);
    ros::Subscriber num_sub = nh.subscribe<std_msgs::Int32>("num_topic", 10, numCallback);

    vel_pub = nh.advertise<geometry_msgs::Twist>("/cmd_vel", 10);

    ros::spin();

    return 0;
}
