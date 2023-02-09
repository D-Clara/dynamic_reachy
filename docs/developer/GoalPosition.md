# Goal Position in teleoperation

There are various variables related to the arm motors that are accessible: 
- The current position : where the motor is currently 
- The goal position : where the motor is supposed to be 

To record a movement by manually moving the arm, the values of the current position of the motors are recorded at each instant and to reproduce this movement, the values obtained are applied to the goal position of the motors. The movement obtained is not identical due to gravity and inertia.

For teleoperation, the principle is slightly different. The user moves the controllers and the data is sent to the robot through the SDK server. These data will therefore be transmitted to the robot as the goal position. Similarly to the previous case, by recording the current position, a movement is obtained that is not identical to the original movement. To reproduce the original movement, it would therefore be necessary to record the goal position transmitted by the user.

We wanted to retrieve these goal positions in order to be able to compare the movements reproduced with the goal positions (supposed to represent the original movement) and the movements reproduced from the improved current positions thanks to PID and the modification of the torque.

We encountered several problems in retrieving these goal positions:

- The goal values were not updated in real-time, so it was impossible to get them as we get the current position, so we decided to catch them directly in the SDK server function by intercepting the goal position transmitted from the Unity application.

- In order to compare the goal position and the current position, both must be recorded at the same time, so by launching the get_pos function. However, it was not possible to access the global variables of the get_pos function from the outside. We therefore had to create two external JSON files in order to transmit the data.

- The recording frequency is not the same as the current and is not constant, so the reproduction of the movement as it was does not work, so we recorded the time between two points to use it as the reproduction frequency in a new reproduction function reproduce_traj_bis.

- The goal position data is retrieved at the moment the server calls the inverse kinematics, so there is no data for the gripper, so we decided to use the current position data for the gripper.

- The use of the gripper current position data is not evident because the goal position and current position recording frequencies are not the same. The current position data that is closest in time to the point we want is choosen.

- There is a delay between the moment when the goal position order is given and the moment when the robot actually performs the movement. This therefore implies a temporal offset between the goal position values and the current position. Thus, the gripper catches and releases the ball in advance that completely distorte the throw. To solve this problem, we tried to correct it manually by adding a delay in the goal positions (around 0.3 seconds). Unfortunately, we realized that this delay was not constant from one throw to another as it depends on the connection at the time of recording.

The trajectory reproduced by the robot's arm from the goal position corresponds well to the movement obtained in VR but the landing point does not correspond because it is difficult to correctly set the delay.






[Back to summary](README.md)