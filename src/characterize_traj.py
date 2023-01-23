# To construct datas in order to create a database for our futur learning algorithm,
# we need to characterize the trajectories.
# To do so, we'll need to define a trajectory with a vector and a throw point.
import numpy as np
import matplotlib.pyplot as plt

from reachy_sdk import ReachySDK

reachy = ReachySDK('localhost')


def characterize_traj_v1(joint_orders):
    """
    This function characterize a trajectory form a list of point to a vector and point tuple.
    :param joint_orders: list of joints target positions
    :return: a tuple (vector, point)
    """
    # Parameters of this characterization
    nb_points = 100  # Number of point's coordinates to use to characterize the trajectory
    ploy_deg = 3  # Degree of the polynomial used to characterize the trajectory


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
    for order in joint_orders[release_index-nb_points:release_index]:
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
    # We'll use a polynomial regression to do so

    # First passing from X, Y, Z coordinates to x, z
    x = np.sqrt(X ** 2 + Y ** 2)
    z = Z

    # Then fitting the polynomial
    coeffs = np.polyfit(x, z, ploy_deg)
    ffit = np.poly1d(coeffs)
    fderiv = ffit.deriv()
    print("coeffs : ", coeffs, "\nffit : ", ffit, "\nfderiv : ", fderiv)

    # And apply the derivative on the release point
    release_point = x[-1], z[-1]
    velocity = fderiv(release_point[0])

    # Show the points and the fitted function
    plt.plot(x, z, 'o', x, ffit(x), '-')
    plt.show()

    return velocity, traj[-1]


def characterize_traj_v2(joint_orders):
    """
    This function characterize a trajectory form a list of point to 3 vectors and point tuple (for each axe projection)
    :param joint_orders: list of joints target positions
    :return: an array of 3 tuple (vector, point)
    """
    # Parameters of this characterization
    nb_points = 100  # Number of point's coordinates to use to characterize the trajectory
    ploy_deg = 3  # Degree of the polynomial used to characterize the trajectory

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
    for order in joint_orders[release_index - nb_points:release_index]:
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
    # We'll use a polynomial regression to do so

    points = [X, Y, Z]
    release_point = X[-1], Y[-1], Z[-1]
    for axe in range(3):
        coeffs = np.polyfit(points[axe], points[axe+1 % 3], ploy_deg)
        ffit = np.poly1d(coeffs)
        fderiv = ffit.deriv()
        print(axe, ", coeffs : ", coeffs, "\nffit : ", ffit, "\nfderiv : ", fderiv)
        velocity = fderiv(release_point[0])
        plt.plot(points[axe], points[axe+1 % 3], 'o', points[axe], ffit(points[axe]), '-')

    # And apply the derivative on the release point

    # Show the points and the fitted function
    plt.show()
    velocity = 0
    return velocity, traj[-1]
