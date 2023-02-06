#include "rclcpp/rclcpp.hpp"
// #include "example_interfaces/msg/int64.hpp"
#include "can_msg_frame/msg/frame.hpp"

class CANHandlerNode : public rclcpp::Node
{
    public:
        CANHandlerNode() : Node("ros2can_handler")
        {
            RCLCPP_INFO(this->get_logger(), "Publisher node is initialised");
            // publisher_ = this->create_publisher<example_interfaces::msg::Int64>("CAN_transmit", 10);

            publisher_ 	= this->create_publisher<can_msg_frame::msg::Frame>("CAN_transmit", 10);
            // subscription_ 	= this->create_subscription<can_msgs::msg::Frame>("CAN_receive", std::bind(&ros2socketcan::CanPublisher, this, _1));

            timer_ = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&CANHandlerNode::CANPublisher, this));
            
        }

    private:

        void CANPublisher(){
            auto msg = can_msg_frame::msg::Frame();
            msg.header.stamp = this->get_clock()->now();
            msg.id  = 0x101;
            msg.dlc = 8;
            msg.eff = 0x11;
            msg.rtr = 0x1;
            msg.err = 0x0;
            msg.data[0]= counter_;
            counter_++;
            publisher_->publish(msg);
        }

        rclcpp::Publisher<can_msg_frame::msg::Frame>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_;
        int counter_ = 0;
};

int main(int argc, char **argv)
{

    rclcpp::init(argc, argv);
    auto node = std::make_shared<CANHandlerNode>();

    rclcpp::spin(node);

    rclcpp::shutdown();
    return 0;
}