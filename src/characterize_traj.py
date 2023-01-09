# To construct datas in order to create a database for our futur learning algorithm,
# we need to characterize the trajectories.
# To do so, we'll need to define a trajectory with a vector and a throw point.
import numpy as np
import matplotlib.pyplot as plt

from reachy_sdk import ReachySDK

reachy = ReachySDK('localhost')


def characterize_traj(joint_orders):
    """
    This function caracterize a trajectory form a list of point to a vector and point tuple.
    :param joint_orders: list of joints target positions
    :return: a tuple (vector, point)
    """
    # We need to find the points where the robot release the ball
    release_index = None
    for i in range(len(joint_orders)):
        if joint_orders[i]["r_gripper"] >= -12:
            release_index = i
            break
    if release_index is None:
        raise ValueError("No release point found in trajectory")

    # Now we want to have the trajectory in robot referential with the direct kinematics function
    traj = []
    for order in joint_orders[release_index-100:release_index]:
        traj.append(reachy.r_arm.forward_kinematics({cle: order[cle] for cle in
                                                     ["r_shoulder_pitch", "r_shoulder_roll", "r_arm_yaw",
                                                      "r_elbow_pitch", "r_forearm_yaw", "r_wrist_pitch",
                                                      "r_wrist_roll"]}.values()))

    X = np.array([p[0, 3] for p in traj])
    Y = np.array([p[1, 3] for p in traj])
    Z = np.array([p[2, 3] for p in traj])

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')  # Affichage en 3D
    ax.scatter(X, Y, Z, label='Courbe')
    minax = min([min(X), min(Y), min(Z)])
    manax = max([max(X), max(Y), max(Z)])
    manax += 0.1
    minax -= 0.1
    plt.xlim(minax, manax)
    plt.ylim(minax, manax)
    ax.set_zlim(minax, manax)
    plt.show()
    # We want to fit a function in this list of coordinates
    # We'll use a linear regression to do so

