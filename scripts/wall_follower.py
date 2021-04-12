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

    def find_wall(self):
        self.vel_msg.linear.x = 0.5

    

    def process_scan(self, msg):

        front_val = min(min(msg.ranges[0:45]), min(msg.ranges[315:360]))
        self.right_val = min(msg.ranges[225:300])

        if front_val < 0.7: 
            self.state = "turn"
        elif self.right_val < 1.5:
            self.state = "follow_wall"
        else:
            self.state = "find_wall"

        # self.scan_value = min(msg.ranges)
        # arg = argmin(msg.ranges)

        # if arg <= 70 or arg >= 290:
        #     location = "front"
        # elif arg > 90 and arg <= 135:
        #     location = "left"
        # elif arg > 135 and arg <= 180:
        #     location = "behind_left"
        # elif arg > 180 and arg <= 225:
        #     location = "behind_right"
        # else:
        #     location = "right"

        # if self.scan_value < 1:
        #     if location == "front":
        #         self.state = "turn"
        #     if location == "right":
        #         self.state = "follow_wall"
        # else:
        #     self.state = "find_wall"



    # go straight and turn 90 four times to complete a square 
    def run(self):
        self.state = "find_wall"
        rospy.sleep(2)
        r = rospy.Rate(20)
        while not rospy.is_shutdown():
            print(self.state)
            if self.state == "find_wall":
                self.vel_msg.angular.z = 0
                self.vel_msg.linear.x = 0.3

            if self.state == "turn":
                self.vel_msg.linear.x = 0
                self.vel_msg.angular.z = 0.4
            
            if self.state == "follow_wall":
                error = 0.6 - self.right_val
                print(error)
                kp = 0.5
                self.vel_msg.angular.z = error*kp
                self.vel_msg.linear.x = 0.3

            self.vel_pub.publish(self.vel_msg)
            r.sleep()
            
        rospy.spin()

if __name__ == '__main__':
    node = WallFollower()
    node.run()
