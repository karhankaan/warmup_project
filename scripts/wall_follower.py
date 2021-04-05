#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from math import pi


def argmin(iterable):
    return min(enumerate(iterable), key=lambda x: x[1])[0]

class WallFollower(object):

    #initialize the velocity publisher, velocity message, and scan subscriber 
    def __init__(self):
        rospy.init_node('drive_square')
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.sub = rospy.Subscriber('/scan', LaserScan, self.process_scan)
        self.vel_msg = Twist()

    # def location(self, scan_value):
    #     if scan_value

    def find_wall(self):
        self.vel_msg.linear.x = 0.5

    

    def process_scan(self, msg):
        scan_value = min(msg.ranges)
        arg = argmin(msg.ranges)

        if arg <= 25 or arg >= 335:
            location = "front"
        elif arg > 25 and arg <= 135:
            location = "left"
        elif arg > 135 and arg <= 180:
            location = "behind_left"
        elif arg > 180 and arg <= 225:
            location = "behind_right"
        else:
            location = "right"

        if scan_value < 1.5:
            if location == "front":
                self.state = "turn"
            if location == ""



    # go straight and turn 90 four times to complete a square 
    def run(self):
        rospy.sleep(2)
        r = rospy.Rate(20)
        while not rospy.is_shutdown():
            if self.state == "find_wall":
                self.vel_msg.linear.x = 0.5

            if self.state == "turn":
                self.vel_msg.angular.z = 0.2
            
            if self.state == "follow_wall":
                self.vel_msg.angular.z = 0
                self.vel_msg.linear.x = 0.5

            self.vel_pub.publish(self.vel_msg)
            r.sleep()
            
        rospy.spin()

if __name__ == '__main__':
    node = WallFollower()
    node.run()
