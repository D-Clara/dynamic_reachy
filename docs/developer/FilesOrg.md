# Organisation of our implementation files

## Overview
The project is divided into different folders.
- **docs** : contain the documentation of the project.
- **src** : contain the source code of the project.
- **tst** : contain the test code of the project.
- **traj** : contain registered trajectories.

## Documentation files
Sorted files about our project.
```
docs
├── bibliography
│       └── state of the art
├── developer
│       ├── Doc for futur developers
├── report
│       ├── Short report of our project
├── user
│       ├── Doc for potential users
└── images
        └── Images used in the documentation
```

## Source files
Contains all the source code of our project. 
See the [user documentation](../user/README.md) to know which files to launch.

Below, a explanation about most relevant files.
- `angles_correction.py` : contains correction functions about gravity and torque compensation.
- `api.py` : script to run the api
- `change_PID.py` : script to change the PID parameters
- `get_traj.py` : save the current trajectory, done by the hand or by teleoperation
- `motor_temperature.py` : script to get the temperature of the motors
- `plot_traj.py` : plot the trajectory in the format saved by get_traj.py
- `reproduce_traj.py` : reproduce the trajectory saved by get_traj.py
- `traj_characterizor.py` : class to characterize the trajectory from get_traj to throw_point + vector
- `turn_off.py` : script to make reachy compliant

## Test files
Contains different test implemented during the project.

- `test_dynamixel.py` : different tests directly on the dynamixel motors
- `PID_evaluation_plot.py` : plot step response for PID
- `pid_motor_test.py` : different pid tests for motors one by one
- `pid_traj_error_record.py` : global pids test for all the motor on one throw
- `show_traj_error.py` : plot error for each moteur for one throw
- `torque_control.py` : find relationship between torque and position gap

[Back to summary](README.md)
