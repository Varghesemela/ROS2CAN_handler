#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

class CANHandlerNode : public rclcpp::Node
{
    public:
        CANHandlerNode() : Node("ros2can_handler")
        {
            RCLCPP_INFO(this->get_logger(), "Publisher node is initialised");
            publisher_ = this->create_publisher<example_interfaces::msg::Int64>("CAN_transmit", 10);
            timer_ = this->create_wall_timer(std::chrono::milliseconds(500), std::bind(&CANHandlerNode::publish_CAN_data, this));
            
        }

    private:

        void publish_CAN_data(){
           auto msg = example_interfaces::msg::Int64();
           counter_ += 1;
           msg.data = counter_;
           publisher_->publish(msg);
        }

        rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
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