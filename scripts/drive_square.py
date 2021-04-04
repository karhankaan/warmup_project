#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from math import pi

class DriveSquare(object):

    #initialize the velocity publisher and the velocity message 
    def __init__(self):
        rospy.init_node('drive_square')
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.vel_msg = Twist()

    '''
    This function publishes the current velocity message for a certain duration 
    '''
    def go_for_duration(self, duration):
        r = rospy.Rate(1)
        while not rospy.is_shutdown():

            # make sure that the number of connections is positive so that no message is lost
            if self.vel_pub.get_num_connections() > 0:
                self.vel_pub.publish(self.vel_msg)
                break

            # if no connetions, wait until the connection is established. 
            else:
                r.sleep()
        
        rospy.sleep(duration)

    # drives on a straight line for 5 seconds at 0.3 speed 
    def go_straight(self):
        duration = 5
        self.vel_msg.linear.x = 0.3

        #drive
        self.go_for_duration(duration)

        #stop
        self.vel_msg.linear.x = 0
        self.vel_pub.publish(self.vel_msg)
        rospy.sleep(2)

    # turn 90 degrees anticlockwise
    def turn90(self):
        duration = 4

        #calculate the speed necessary for pi/2 turn 
        self.vel_msg.angular.z = pi/(2*duration)

        self.go_for_duration(duration)

        #stop
        self.vel_msg.angular.z = 0
        self.vel_pub.publish(self.vel_msg)
        rospy.sleep(2)

    # go straight and turn 90 four times to complete a square 
    def run(self):
        self.go_straight()
        self.turn90()
        self.go_straight()   
        self.turn90()
        self.go_straight()
        self.turn90()
        self.go_straight()
        rospy.spin()

if __name__ == '__main__':
    node = DriveSquare()
    node.run()
