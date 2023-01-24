# To construct datas in order to create a database for our futur learning algorithm,
# we need to characterize the trajectories.
# To do so, we'll need to define a trajectory with a vector and a throw point.

# On regarde à partir du 600e pt de la traj pour trouver le pt de relachement

import numpy as np
import matplotlib.pyplot as plt


class TrajectoryCharacterizor:
    def __init__(self, joint_orders, nb_points=25, ply_deg=2):
        self.joint_orders = joint_orders
        self.nb_points = nb_points
        self.ply_deg = ply_deg
        self.traj = []
        self.release_index = None
        self.X = None
        self.Y = None
        self.Z = None
        self.coeffs = None
        self.ffit = None
        self.fderiv = None

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
            self.traj.append(reachy.r_arm.forward_kinematics({cle: order[cle] for cle in
                                                              ["r_shoulder_pitch", "r_shoulder_roll", "r_arm_yaw",
                                                               "r_elbow_pitch", "r_forearm_yaw", "r_wrist_pitch",
                                                               "r_wrist_roll"]}.values()))
        self.X = np.array([p[0, 3] for p in self.traj])
        self.Y = np.array([p[1, 3] for p in self.traj])
        self.Z = np.array([p[2, 3] for p in self.traj])
        return self.X, self.Y, self.Z

    def plot_3d_trajectory(self):
        if self.X is None:
            if self.release_index is None:
                self.__find_release_index()
            self.__joints_to_cartesian()
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(self.X, self.Y, self.Z, label='Courbe')
        minax = min([min(self.X), min(self.Y), min(self.Z)])
        manax = max([max(self.X), max(self.Y), max(self.Z)])
        manax += 0.1
        minax -= 0.1
        plt.xlim(minax, manax)
        plt.ylim(minax, manax)
        ax.set_zlim(minax, manax)
        plt.show()

    def __fit_polynomial(self):
        self.coeffs = np.polyfit(self.X, self.Y, self.ply_deg), np.polyfit(self.X, self.Z, self.ply_deg)
        self.ffit = np.poly1d(self.coeffs[0]), np.poly1d(self.coeffs[1])
        self.fderiv = self.ffit[0].deriv(), self.ffit[1].deriv()
        return self.coeffs

    def plot_fitted_curve(self):
        plt.plot(self.X, self.Y, 'o', self.X, self.ffit[0](self.X), 'r-')
        plt.axis('scaled')
        plt.title('y=f1(x)')
        plt.show()

        plt.plot(self.X, self.Z, 'o', self.X, self.ffit[1](self.X), 'r-')
        plt.axis('scaled')
        plt.title('z=f2(x)')
        plt.show()

        # fig = plt.figure()
        # ax = fig.add_subplot(projection='3d')
        # ax.scatter(self.X, self.Y, self.Z, label='Coords')
        # ax.plot(self.X, self.ffit[0](self.X), self.Z, 'r-', label='FFunc')
        # ax.plot(self.X, self.Y, self.ffit[1](self.X), 'b-', label='FFunc')
        # minax = min([min(self.X), min(self.Y), min(self.Z)])
        # manax = max([max(self.X), max(self.Y), max(self.Z)])
        # manax += 0.1
        # minax -= 0.1
        # plt.xlim(minax, manax)
        # plt.ylim(minax, manax)
        # ax.set_zlim(minax, manax)
        # plt.show()

    def process(self):
        self.__find_release_index()
        self.__joints_to_cartesian()
        # self.plot_3d_trajectory()
        self.__fit_polynomial()
        # self.plot_fitted_curve()
        release_point = self.X[-1], self.Y[-1], self.Z[-1]
        print("Release point: ", release_point)
        print(self.fderiv[0])
        print("X.shape :", self.X.shape)
        print("ffit", self.ffit[0](self.X).shape)
        velocity = self.fderiv[0](release_point[0]), self.fderiv[1](release_point[0])
        return velocity, release_point


if __name__ == "__main__":
    import os

    curr_dir = os.getcwd()
    if curr_dir != '/home/reachy/dynamic_reachy/src':
        print("Please run this script from the ~/dynamic_reachy/src/ folder")
        exit(0)

    from reachy_sdk import ReachySDK

    reachy = ReachySDK('localhost')

    t = TrajectoryCharacterizor(joint_orders=np.load('../traj/traj_coralie3.npz', allow_pickle=True)["traj"],
                                nb_points=25,
                                ply_deg=2)
    t.plot_3d_trajectory()
    t.process()
    t.plot_fitted_curve()
