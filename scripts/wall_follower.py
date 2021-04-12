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
    
    #Process the Lidar scanner data
    def process_scan(self, msg):

        front_val = min(min(msg.ranges[0:45]), min(msg.ranges[315:360]))
        self.right_val = min(msg.ranges[225:300])
        
        #set states of the vehicle
        if front_val < 0.7: 
            self.state = "turn"
        elif self.right_val < 1.5:
            self.state = "follow_wall"
        else:
            self.state = "find_wall"

    def run(self):
        self.state = "find_wall"
        rospy.sleep(2)
        r = rospy.Rate(20)
        while not rospy.is_shutdown():
            print(self.state)

            #set velocity according to the state
            if self.state == "find_wall":
                self.vel_msg.angular.z = 0
                self.vel_msg.linear.x = 0.3

            #turn around the corners
            if self.state == "turn":
                self.vel_msg.linear.x = 0
                self.vel_msg.angular.z = 0.4
            
            # set and correct the distance from the wall
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
