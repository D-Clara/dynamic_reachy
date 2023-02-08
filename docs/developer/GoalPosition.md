# Goal Position in teleoperation

The goal position is the wanted position given by the user in the teleoperation. It is the position that the robot will try to reach.
Unfortunately, the robot is not able to reach the exact position given by the user because of gravity or inertia.

The current position is the position that the robot is actually at.

It is possible at any time to get the current position of the robot by taking the value on the joint of the arm :
```
```
First we try to record a movement made by moving by ourselves the robot arm and then we will try to replay it. To do so we only have to record the current position during the movement and then give these value as the new goal position of the robot to reproduce the movement.
THe reproduction won't be the same due to gravity and inertia.



In teleoperation, the user move the controllers and then the server transmit the controllers position to the robot. The robot will try to reach these positions. If we record the current position, when we replay the movment the trajectory will be different because also of gravity and inertia. But if we  can record directly the goal position given by the user, the trajectory will be really close to the original one.

We faced different problems trying to record the goal position. 
The first one was that the goal position was not updated directly on the joint so we can't record it as we record the current position.
A solution to that was to catch the goal position when the server send the goal position from unity to the robot

The thrid one was that the goal position was updated but not at the same frequency as the current position so we can't record it as we record the current position.


[Back to summary](README.md)