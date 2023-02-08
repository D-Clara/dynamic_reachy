# To construct datas in order to create a database for our futur learning algorithm,
# we need to characterize the trajectories.
# To do so, we'll need to define a trajectory with a vector and a throw point.

import numpy as np
import matplotlib.pyplot as plt
from reachy_sdk import ReachySDK


class TrajectoryCharacterizor:
    """
    Taking a trajectory as obtained with get_traj.py, this class compute
    """
    def __init__(self, joint_orders, reachY, nb_points=25, ply_deg=2):
        self.reachy = reachY
        self.joint_orders = joint_orders
        self.nb_points = nb_points
        self.ply_deg = ply_deg
        self.traj = []
        self.release_index = None
        self.X = None
        self.Y = None
        self.Z = None
        self.time = np.arange(nb_points)
        self.coeffs = None
        self.ffit = None
        self.fderiv = None
        self.velocity = None

    def __find_release_index(self):
        for i in range(len(self.joint_orders) - 600):
            if self.joint_orders[600 + i]["r_gripper"] < -12:
                self.release_index = i + 600
                break
        if self.release_index is None:
            raise ValueError("No release point found in trajectory")
        return self.release_index

    def __joints_to_cartesian(self):
        for order in self.joint_orders[self.release_index - self.nb_points:self.release_index]:
            self.traj.append(self.reachy.r_arm.forward_kinematics({cle: order[cle] for cle in
                                                              ["r_shoulder_pitch", "r_shoulder_roll", "r_arm_yaw",
                                                               "r_elbow_pitch", "r_forearm_yaw", "r_wrist_pitch",
                                                               "r_wrist_roll"]}.values()))
        self.X = np.array([p[0, 3] for p in self.traj])
        self.Y = np.array([p[1, 3] for p in self.traj])
        self.Z = np.array([p[2, 3] for p in self.traj])
        return self.X, self.Y, self.Z

    def __fit_polynomial(self):
        self.coeffs = (np.polyfit(self.time, self.X, self.ply_deg),  # X=f(t)
                       np.polyfit(self.time, self.Y, self.ply_deg),  # Y=f(t)
                       np.polyfit(self.time, self.Z, self.ply_deg))  # Z=f(t)
        self.ffit = (np.poly1d(self.coeffs[0]),
                     np.poly1d(self.coeffs[1]),
                     np.poly1d(self.coeffs[2]))
        self.fderiv = (self.ffit[0].deriv(),
                       self.ffit[1].deriv(),
                       self.ffit[2].deriv())
        return self.coeffs

    def plot_fitted_curve(self):
        if self.X is None or self.ffit is None:
            print("You need to process the trajectory first")
            return
        plt.plot(self.time, self.X, 'o', self.time, self.ffit[0](self.time), 'r-')
        # plt.axis('scaled')
        plt.title('X=f1(t)')
        plt.show()

        plt.plot(self.time, self.Y, 'o', self.time, self.ffit[1](self.time), 'r-')
        # plt.axis('scaled')
        plt.title('Y=f1(t)')
        plt.show()

        plt.plot(self.time, self.Z, 'o', self.time, self.ffit[2](self.time), 'r-')
        # plt.axis('scaled')
        plt.title('Z=f1(t)')
        plt.show()

    def plot_3d_trajectory(self):
        if self.X is None:
            print("You need to process the trajectory first")
            return
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(self.X, self.Y, self.Z, label='Courbe')
        # draw 3D vector from self.release_point to self.release_point + self.velocity
        ax.quiver(self.X[-1], self.Y[-1], self.Z[-1], self.velocity[0], self.velocity[1], self.velocity[2], length=0.1,
                  normalize=True)
        minax = min([min(self.X), min(self.Y), min(self.Z)])
        manax = max([max(self.X), max(self.Y), max(self.Z)])
        manax += 0.1
        minax -= 0.1
        plt.xlim(minax, manax)
        plt.ylim(minax, manax)
        ax.set_zlim(minax, manax)
        plt.show()

    def process(self):
        self.__find_release_index()
        self.__joints_to_cartesian()
        # self.plot_3d_trajectory()
        self.__fit_polynomial()
        # self.plot_fitted_curve()

        release_point = self.X[-1], self.Y[-1], self.Z[-1]
        # print("Release point: ", release_point)
        # print(self.fderiv[0])
        # print("X.shape :", self.X.shape)
        # print("ffit", self.ffit[0](self.X).shape)
        self.velocity = self.fderiv[0](self.time[-1]), self.fderiv[1](self.time[-1]), self.fderiv[2](self.time[-1])
        return self.velocity, release_point


if __name__ == "__main__":
    import os

    curr_dir = os.getcwd()
    if curr_dir != '/home/reachy/dynamic_reachy/src/Learning':
        print("Please run this script from the ~/dynamic_reachy/src/Learning folder")
        exit(0)

    reachy = ReachySDK('localhost')

    t = TrajectoryCharacterizor(joint_orders=np.load('../../traj/traj_coralie3.npz', allow_pickle=True)["traj"],
                                reachY=reachy,
                                nb_points=25,
                                ply_deg=3)
    v, pt = t.process()
    t.plot_3d_trajectory()
    t.plot_fitted_curve()
    print("Velocity: ", v)
    print("Release point: ", pt)
