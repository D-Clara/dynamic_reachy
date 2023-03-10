# PID improvement

## PID test for one motor

<span style="color: #7ECBB7">
First steps
</span>

To get started with PIDs, a method to discover the impact was done. It consists to do small repetitive movements and see shaking and the average of errors to reach the extreme positions. This is done in pid_motor_test.py with *error*.

<span style="color: #7ECBB7">
Problem with the 2 wrist motors
</span>

While trying to do the test for the wrist, a problem occurred, no matter the PID values chosen, the 2 motors of the wrist shook quite strongly, mainly bumps, when the motors are in 0° position. 

https://user-images.githubusercontent.com/74452893/217632740-7753e373-3267-4654-a45c-2b9840cb0ade.mp4

https://user-images.githubusercontent.com/74452893/217632699-ded9f84f-1f62-4645-9163-2c4d73c3cd4f.mp4

So we wanted to check that the engine was working well. The same action was done with a dynamixel setup connected directly to the motor and no shaking was observed. 

https://user-images.githubusercontent.com/74452893/217632053-05c2dbdd-923d-4df6-9876-764cfd4b1bed.mp4

We came to the conclusion that it must be a problem of tension drop at the end of the arm preventing good control of the wrist.

<span style="color: #7ECBB7">
Ziegler and Nichols methode
</span>

After taking in hand the PIDs by the previous method we set up a more theoretical method. 

We try to use the Ziegler and Nichols method but it was not successful.

<span style="color: #7ECBB7">
Study of step response 
</span>

A command in position is sent to the motor and we watch its step response with the function *error_pos* in pid_motor_test.py. The step response can be plotted by launching the file PID_evaluation_plot.py in parallel to the movement. 
> **Note**
> Don't forget to modify the motor name for which the data are collected, in the fonction *get_current_position*.

The first step is to chose proportionnal gain. For this, the gain has been increased until the error in the final position is low while having a reasonable overshoot. 

A step response with a small proportionnal gain (10) with a 40° control:

![pid_petit_Kp](../images/PID10%2C0%2C0_shoulder.png)

A step response with a big proportionnal gain (200) with a 40° control:

![pid_grand_Kp](../images/PID200%2C0%2C0_shoulder.png)

After, integral gain is choosen to reduce the amplitude of the shakings and derival gain to reduce the duration of the shakings. All this modification allow us to obtain this kind of step response for a 40° control: 

![bon_pid](../images/PID64%2C10%2C100_shoulder.png)

So good PID gains for each MX motor are:

- r_shoulder_pitch : 64,10,100
- r_shoulder_roll : 64,10,100
- r_arm_yaw : 20,0,0
- r_elbow_pitch : 64,10,100
- r_forearm_yaw : 20,0,0
- r_wrist_pitch : 20,0,0

## PID test reproducing a trajectoire

After doing it one by one, the idea was to collect the error of each motor during a movement using the function *error* in pid_traj_error_record.py and then display them. Errors are not the same for several identical movements, so errors are stored in files in the directory tst/log_pid. The file show_traj_error.py shows errors from a file in tst/log_pid. 

This type of graph is obtained:

![pid_test](../images/pid_graph.png)

zooming in:

![pid_zoom](../images/pid_graph_zoom.png)

This method lets us see the impact of all the motors together on a typical throw.


## Setup PID

The PID of the right arm can be modified in the file change_PID.py using *change_PID* with an array of pid values for each arm motor in order. 

For instance ```change_PID([[64,10,100],[64,10,100],[20,0,0],[64,10,100],[20,0,0],[20,0,0],[20,0,0]]) ```

There is also the possibility to know the current arm right PID of reachy with *print_PID* in change_PID.py 

> **Warning**
> PIDs are stored in RAM, so the setup needs to be done each time the motors are reset.

[Back to summary](README.md)
