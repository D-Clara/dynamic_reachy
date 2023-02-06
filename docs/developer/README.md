# 📖 Developer documentation

## ⁉️ Purpose of this documentation

This documentation is intended to the **future developers** re-using your work, e.g. students from next year.
They have the same proficiencies that you have and are interested in understanding how your code is structured and how they can extend it with new features.

## ⁉️ Do we really need to feed this section? 

Maybe not, if your project does not include code or if it is trivial. If so, drop the section and the links.


## ⁉️ What is expected here
Your user documentation must give and overview of the structure of your code. 
Include any information that is needed e.g. ROS topics and services, tweakable parameters, how to update firmwares...
It may include images, usually technical diagrams e.g. UML diagrams (class diagram or activity diagram).



## Reachy SDK server service

Before running any functions or teleoperation you first have to launch the reachy sdk.
If you start the motors before starting Reachy, the SDK will start automatically. If you turn off the motor with Reachy on you will a to restart the SDK after having re turn on the motors.

- To turn on the SDK server :
```
sudo systemctl start reachy_sdk_server.service
```

- To turn off the SDK server :
```
sudo systemctl stop reachy_sdk_server.service
```
- To restart the SDK server :
```
sudo systemctl restart reachy_sdk_server.service
```

- To check the actual status of the SDK server :

```
sudo systemctl status reachy_sdk_server.service
```


Thank to the *reachy_tips* it is possible to launch all the services and show all the logs in real time. It is better to use the command :
```
launch_all
```

You then have to wait for "*READY TO DESTROY THE WORLD!*" to run the other functions.


## Use the teleoperation 

With a new VR headset you can look at the __[Pollen documention](https://docs.pollen-robotics.com/vr/introduction/introduction/)__.

With our VR headset you just have to :
- Sonnect it to the same WIFI network as Reachy
- Launch *----------*
- set Reachy IP adress
<div class="warning">



**Warning**
Make sure to read the __[best-practice](https://docs.pollen-robotics.com/vr/use-teleop/best-practice/)__ before starting





## Record a trajectory
To record a trajectory you have to run get_traj depuis le dossier *src* :
```
python3 get_traj
```

The record will be saved in the *traj* directory with the name :
*date time name*

Some parameters can be changed directly in the file :
- FILENAME_COMMENT : the name add to the filename
- RECORD_FREQUENCY : the frequency at which we get point

## Plot a trajectory
You can show what you trajectory looks like with the *plot_traj* function :

<div align="center"><figure>
  <img src="/home/reachy/dynamic_reachy/docs/images/plot_traj.png"> 
  <figcaption>The trajectory of a ball throw</figcaption>
</figure></div>

The orange represente the movment when the gripper is closed and the blue when it's open.

To use it you have to change the FILEPATH in the *plot_traj.py* with an absolute path.
Then run it use :
```
python3 plot_traj
```

## Reproduce a trajectory

To reproduce a movment you can use the *src/reproduce_traj.py*.

Different parameters can be change in the file :
- FILENAME : the absolute path of the wanted trajectory (.npz)
- RECORD_FREQUENCY : the recording frequency
- PREPROCESSING : *True* or *False*, to activate or not the preprocessing that compensates for the force of gravity 


__[test](/home/reachy/dynamic_reachy/docs/developer/RepairAndUpdate.md)__
```@eval
using Markdown
Markdown.parse_file(joinpath("RepairAndUpdate.md"))
```
```
{include} RepairAndUpdate.md
```

:warning:

**WARNING**

**Warning**