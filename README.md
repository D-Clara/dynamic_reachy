# Dynamic Reachy

**Description:** Using teleoperation with VR headset and dynamic control to plan precise movements, 
in the context of a ball launch with the **Reachy** robot from __[Pollen Robotics](https://www.pollen-robotics.com/)__.

<img alt="" src="docs/images/reachy.jpg"> 

[📖 User documentation](docs/user) • [👨‍💻 Developer documentation](docs/developer) • [📈 Project report](docs/report) • [📚 Bibliography](docs/bibliography) • [⚠️ Risk Analysis](docs/risk)
  
## 📄 This project in short
With the final demonstration idea of a robot unbeatable at beer pong, this project aim to meliorate the dynamic 
behaviour of the robot Reachy.

We also worked on the treatment and characterization of trajectories, with the initial aim of making Reachy able to learn 
and generate his own trajectories, thanks to a database made with VR teleoperation.

The search of precision in the reproduction of a movement led us to study the PID parameters of the robot, and 
constraints such as the torque from gravity applied on the joints.

In parallel, the need of reproducibility for the repetition of one trajectory brought us to search about the causes of 
these different behaviours with the same order.

## 🚀 Quickstart (if relevant)

* **Install instructions**: Everything is already installed on the Intel NUC of Reachy
* **Launch instructions**: To launch correctly the robot, you must do those few steps :
  * Turn on the motors switch on the back (see our repairs on the robot to find them)
  * Turn on Reachy's Intel NUC with the button on the back
  * On ssh (or on the terminal of the NUC), launch the following commands :
    * `cd ~/dynamic_reachy`
    * `source devel/setup.bash`
    * `roslaunch reachy_bringup reachy.launch`
If this is written in user or dev docs, provide links.

## 🔍 About this project

|       |        |
|:----------------------------:|:-----------------------------------------------------------------------:|
| 💼 **Client**                |  Name of your Client *(1)*                                              |
| 🔒 **Confidentiality**       | **Public** or **Private** *(1)*                                         |
| ⚖️ **License**               |  [Choose a license](https://choosealicense.com/) *(1)*                  |
| 👨‍👨‍👦 **Authors**               |  Student names, with a link to their social media profile or website    |


*(1) Refer to your client to make a choice. Then update the repository accordingly: the visibility in the settings and replace the [LICENSE](./LICENSE) file.*

## ✔️ Additional advices

* Do not make **passwords** and secret keys public. If you have to, replace it by a random string and a warning in the doc telling to replace it
* Avoid **long sentences**. Often, bullet points are easier to read
* **Illustrate** your reports. Use colored plots, schematics and pictures. But do not abuse of them
* Do not **duplicate** information. If it may be relevant at several places, make links
* **English** is the universal langage worldwide. Write all engineering documents in English
* Choose carefully **what sections** apply to your project and delete/add anything from the template that you think relevant
* Remove anything that would **pollute** reading, including these instructions and irrelevant sections
