# PID improvement

## PID test reproducing a trajectoire

The first idea was to collect the error of each motor during a movement using function *error* in pid_traj_error_record.py and then display them. Error are not the same for several identical movements, so errors are store in files in directory tst/log_pid. The file show_traj_error.py allow to show errors from a file in tst/log_pid. 

This type of graph is obtained:

![pid_test](../images/pid_graph.png)

zooming in:

![pid_zoom](../images/pid_graph_zoom.png)

The change of curve appearance according to the pid is not very visible and speaking especially that each engine influences the others. 

## PID test for one motor

To improve the detection of pid improvement of each motor, a second methode was done. It consiste to done small repetitive mouvement and see shaking and the average of errors to reach the extreme positions. This is done in pid_motor_test.py. The throw being only in one plane we decided to do it only for the elbow, the shoulder and the wrist.

### Shoulder motor

### Elbow motor

### Problem with the 2 wrist motors

While trying to do the test for the wrist, a problem occurred, no matter the pid values chosen, the 2 motors of the wrist shake quite strongly. 

So we wanted to check that the engine was working well. The same action was done with a dynamixel setup connect directly to the motor and no shaking was observed. 

We came to the conclusion that it must be a problem of tension drop at the end of the arm preventing good control of the wrist.

## Setup PID

The pid of the right arm can by modify in the file change_PID.py using *change_PID* with a array of pid values for each arm motor in order. 

For instance ```change_PID([[25,0,0],[45,0,0],[0.1,0,0],[0.5,0,0],[40,0,0],[32,0,0],[32,0,0]]) ```

There is also the possibility to know the current arm right PID of reachy with *print_PID* in change_PID.py 