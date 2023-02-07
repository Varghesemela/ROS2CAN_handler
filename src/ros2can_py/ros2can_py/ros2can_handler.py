#!/usr/bin/env python3
import rclpy
import can

from rclpy.node import Node
from can_msgs.msg import Frame


class ROS2CANHandlerNode(Node):
    def __init__(self):
        super().__init__("ROS2CANHandlerNode")
        self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

        self.receive_ = self.create_publisher(Frame, "CAN/BusData", 10)
        self.subscriber_ = self.create_subscription(Frame, "CAN/TransmitRequest", self.callback_txrequest, 10)
        self.msg_ = Frame()
        self.canmsg_ = Frame()
        self.counter_ = 0
        self.create_timer(1/3, self.callback_canreceive)
        self.get_logger().info("publisher node initialised")

    def callback_canreceive(self):
        canmsg = self.can0.recv(0.1) 
        if canmsg is not None:
            self.canmsg_.data = canmsg.data
            self.canmsg_.dlc = canmsg.dlc
            self.canmsg_.err = canmsg.error_state_indicator
            self.canmsg_.eff = canmsg.is_extended_id
            self.canmsg_.id  = canmsg.arbitration_id
            self.canmsg_.header.stamp = self.get_clock().now().to_msg()
            self.canmsg_.header.frame_id = "CAN/BusData"
            print("CAN receive ---->" + str(self.get_clock().now().to_msg()))
            self.receive_.publish(self.canmsg_)
        else:
            print("No Data")

    def callback_txrequest(self, msg):
        canmsg = can.Message(
            arbitration_id = msg.id, data = [msg.data[0], msg.data[1], msg.data[2]], is_extended_id=False
        )
        self.can0.send(canmsg)     
        print("Sent on CAN ---->" + str(msg))
        

def main(args=None):
    rclpy.init(args=args)

    node = ROS2CANHandlerNode()

    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()