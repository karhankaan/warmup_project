
# Driving in a Square


![square](./square.gif)

**Description:**

My approach consisted of moving the robot straight and taking 90 degree turns successively. Going straight and turning 4 times makes the robot travel in a square. Every straight and turning movement has the same speed and duration, which ensures that the path is a square.

**Code Explanation:**

* The init method initializes the publisher and the velocity message.
* The go_for_duration() method takes a duration argument and publishes a velocity message for that duration. It checks the publisher's connections to make sure that no message is wasted.
* go_straight() method makes the robot travel on a straight line for 5 seconds at 0.3 speed by setting the linear twist parameter and publishing using the go_for_duration method.
* turn90() method makes the robot turn 90 degrees anticlockwise. It turns in 4 seconds and the angular velocity is calculated by pi/(2*duration) since pi/2 is 90 degrees. This again uses the go_for_duration method to publish the velocity message.
* In the run() method we go straight and turn four times to complete a square.


**Challenges:**

The main challenge I changed was in trying to make the robot turn 90 degrees. For this to happen, the robot has to set a precise velocity for a precise duration. I noticed that even though the formulas were correct, the robot was not turning a full 90 degrees. It turned out that it takes a while for the publisher to establish a connection, which messes with the turning time duration. I fixed this by checking that a connection is made before making the robot turn. This ensured a precise 90 degree turn.

**Future Work:**

Because of the friction in the environment, the robot drifts every time it halts and every time it starts moving. This causes it to not move in a perfect square and end up a couple of inches away from where it started. I would try to fix this problem. 
