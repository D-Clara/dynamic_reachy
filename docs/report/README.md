

# 📖 Report

## ⁉️ Specifications

In a context of democratisation of robots, and the multiplication of their uses, there is a parallel need of robot being 
able to act like real humans, and of being able to be programmed by non-expert humans.
Therefore, the "programming by demonstration" paradigm is a promising approach to achieve this goal.

*Pollen Robotics*, a startup based in Bordeaux, has made their robot, Reachy, controllable by teleoperation with a VR headset.
The problematic is that the teleoperation is not very precise for the dynamic reproduction of movements.

The goal of this project is to make Reachy unbeatable at a beer pong game, by being able to generate his own trajectories
for a given target. Firstly, we need to study the dynamic of Reachy's movements, to try to meliorate the reproduction of teleoperated trajectories, 
and then we will use teleoperation to construct a dataset of trajectories, and finally we will use this dataset to train a model that will be able to generate new trajectories.

During the project, we have studied the precision of Reachy's motors, and tried different ways to work on them such as PID tuning and gravity torque compensation.
We also used teleoperation to make a demonstration of beer pong game with pre-registered trajectories during the **Aperobot** event.
Finally, we studied the causes of the non-repeatability of the trajectories.

## 🔎 Implemented approach

* [Computing of the torque caused by gravity](../developer/TorqueCompensation.md)
* [Analysis of the impact of PID](../developer/PidImprovement.md)
* [Recording and use of the goal position](../developer/GoalPosition.md)
* [Recording and reproduction of a trajectory](../developer/GlobalUtilisation.md)

## 📈 Analysis of results

* [Quantification of the non-repeatability and parallel with motor's temperatures](./Resultats.md)
* [Analysis of the catching of the ball on the support at the beginning of the throw](./BallCatching.md)

