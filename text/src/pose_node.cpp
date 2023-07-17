#include <ros/ros.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>

void poseCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg)
{
    // 提取位置信息
    double x = msg->pose.pose.position.x;
    double y = msg->pose.pose.position.y;
    double z = msg->pose.pose.position.z;

    // 输出位置信息
    ROS_INFO("Position: x = %.2f, y = %.2f, z = %.2f", x, y, z);
}

int main(int argc, char** argv)
{
    ros::init(argc, argv, "position_subscriber_node");
    ros::NodeHandle nh;

    // 创建订阅器，订阅位置信息的话题
    ros::Subscriber pose_sub = nh.subscribe<geometry_msgs::PoseWithCovarianceStamped>("/amcl_pose", 10, poseCallback);

    // 执行ROS循环
    ros::spin();

    return 0;
}