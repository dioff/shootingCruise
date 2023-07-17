#include <ros/ros.h>
#include <std_msgs/Int32.h>

void numCallback(const std_msgs::Int32::ConstPtr& msg)
{
    int received_number = msg->data;
    if  (received_number == 1){
        ROS_INFO("received num", received_number);
    }else
    ROS_INFO("no received num", received_number);
}

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "num_sub");
    ros::NodeHandle nh;

    ros::Subscriber sub = nh.subscribe("num_topic", 10, numCallback);
    
    ros::spin();



    return 0;
}
