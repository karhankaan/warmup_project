#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import pi


def argmin(iterable):
    return min(enumerate(iterable), key=lambda x: x[1])[0]

class PersonFollower(object):

    #initialize the velocity publisher, velocity message, and scan subscriber 
    def __init__(self):
        rospy.init_node('drive_square')
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.process_scan)
        self.vel_msg = Twist()

    # def location(self, scan_value):
    #     if scan_value

    def process_scan(self, msg):
        scan_value = min(msg.ranges)
        location = argmin(msg.ranges)

        if location <= 25 or location >= 335:
            self.state = "front"
        elif location > 25 and location <= 135:
            self.state = "left"
        elif location > 135 and location <= 180:
            self.state = "behind_left"
        elif location > 180 and location <= 225:
            self.state = "behind_right"
        else:
            self.state = "right"

        if scan_value < 1:
            if self.state == "front":
                self.state = "stop"
            elif self.state == "left" or self.state == "behind_left": 
                self.state = "behind_left"
            elif self.state == "right" or self.state == "behind_right":
                self.state == "behind_right"



    # go straight and turn 90 four times to complete a square 
    def run(self):
        rospy.sleep(2)
        r = rospy.Rate(20)
        while not rospy.is_shutdown():
            if self.state == "stop":
                self.vel_msg.linear.x = 0
                self.vel_msg.angular.z = 0

            if self.state == "front":
                self.vel_msg.angular.z = 0
                self.vel_msg.linear.x = 0.6
            if self.state == "left":
                self.vel_msg.angular.z = 0.8
            if self.state == "right":
                self.vel_msg.angular.z = -0.8
            if self.state == "behind_left":
                self.vel_msg.linear.x = 0
                self.vel_msg.angular.z = 1.5
            if self.state == "behind_right":
                self.vel_msg.linear.x = 0
                self.vel_msg.angular.z = -1.5

            self.vel_pub.publish(self.vel_msg)
            r.sleep()
            
        rospy.spin()

if __name__ == '__main__':
    node = PersonFollower()
    node.run()
