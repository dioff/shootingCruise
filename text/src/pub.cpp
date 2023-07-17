#include <ros/ros.h>
#include <std_msgs/Int32.h>


int main(int argc, char *argv[])
{
    ros::init(argc, argv, "num_pub");
    ros::NodeHandle nh;

    ros::Publisher pub = nh.advertise<std_msgs::Int32>("num_topic", 10);
    ros::Rate rate(1);
    while (ros::ok())
    {
        std_msgs::Int32 msg;
        msg.data = 1;
        pub.publish(msg);
        ROS_INFO("yifasong %d", msg);
        ros::spinOnce();
        rate.sleep();
    }
    
    return 0;
}
