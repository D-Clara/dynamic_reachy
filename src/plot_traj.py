import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from reachy_sdk import ReachySDK

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

SAVE_DIRECTORY_PATH = '../traj/'
FILENAME = 'test'
reachy = ReachySDK('localhost')


def ploat_trajectory(filename):
    '''Ploat a trajectory from a file
    :param filename: the name of the file to read
    '''

    #loadd trajectory in traj/traj.npy
    traj = np.load(filename, allow_pickle=True)["traj"]
    poses = []
    grip = []
    print(traj)
    for t in traj:
        poses.append(reachy.r_arm.forward_kinematics({cle: t[cle] for cle in ["r_shoulder_pitch", "r_shoulder_roll","r_arm_yaw","r_elbow_pitch","r_forearm_yaw","r_wrist_pitch","r_wrist_roll"]}.values()))
        grip.append(t["r_gripper"])
    X = [p[0,3] for p in poses]
    Y = [p[1,3] for p in poses]
    Z = [p[2,3] for p in poses]
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    # Split the trajectory in two parts : one for the gripper closed and one for the gripper open
    X1 = []
    Y1 = []
    Z1 = []
    X2 = []
    Y2 = []
    Z2 = []
    for i in range(len(grip)):
        if grip[i] < -12:
            X1.append(X[i])
            Y1.append(Y[i])
            Z1.append(Z[i])
        else:   
            X2.append(X[i])
            Y2.append(Y[i])
            Z2.append(Z[i])

    # Plot the trajectory
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')  # Affichage en 3D
    ax.scatter(X1, Y1, Z1, label='Courbe')
    ax.scatter(X2, Y2, Z2, label='Courbe')
    minax = min([min(X), min(Y), min(Z)])
    manax = max([max(X), max(Y), max(Z)]) 
    manax += 0.1
    minax -= 0.1
    plt.xlim(minax, manax)
    plt.ylim(minax, manax)
    ax.set_zlim(minax, manax)
    plt.show()



if __name__ == '__main__':
    filename = SAVE_DIRECTORY_PATH + FILENAME + '.npz'
    print_trajectory(filename)