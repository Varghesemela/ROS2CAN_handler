#!/usr/bin/env python3
import rclpy
import can

from rclpy.node import Node
from can_msgs.msg import Frame


class ROS2CANSpitNode(Node):
    def __init__(self):
        super().__init__("ROS2CANSpitNode")
        self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

        self.publisher_ = self.create_publisher(Frame, "CAN/TransmitRequest", 10)
        self.msg_ = Frame()
        self.canmsg_ = Frame()
        self.counter_ = 0
        self.create_timer(3, self.callback_counterloop)
        self.get_logger().info("spit node initialised")
        
    def callback_counterloop(self):
        self.counter_ += 1
        self.msg_.id = 0x101
        self.msg_.data[0] = 1
        self.msg_.header._frame_id = "CAN/TransmitRequest"
        self.msg_.header.stamp = self.get_clock().now().to_msg()
        # canmsg = can.Message(
        #     arbitration_id=self.msg_.id, data=[self.msg_.data[0], self.msg_.data[1], self.msg_.data[2]], is_extended_id=False
        # )
        # self.can0.send(canmsg)
        print("published ---->" + str(self.msg_))
        self.publisher_.publish(self.msg_)        

def main(args=None):
    rclpy.init(args=args)

    node = ROS2CANSpitNode()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()