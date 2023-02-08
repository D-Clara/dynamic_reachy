import numpy as np
import matplotlib.pyplot as plt

freq = 100  # Hz
traj_dist = 0.2  # m


def generate_rectilign_traj(point, vector):
    norm = np.linalg.norm(vector)  # velocity
    normalized = vector / norm  # normalized direction vector
    start_point = point - normalized * traj_dist  # start point of our trajectory
    # Generate the trajectory
    time = np.linspace(0.01, 1, freq)
    traj = np.array([start_point + normalized * traj_dist * t for t in time])
    return traj


def plot_traj(traj):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(traj[0 ,0], traj[0, 1], traj[0, 2], label='start')
    ax.scatter(traj[-1, 0], traj[-1, 1], traj[-1, 2], label='throw')
    ax.scatter(traj[:, 0], traj[:, 1], traj[:, 2])
    plt.show()


if __name__ == '__main__':
    throw_pt = np.array([1, 1, 1])
    throw_vect = np.array([1, 2, 3])
    trajectory = generate_rectilign_traj(throw_pt, throw_vect)
    plot_traj(trajectory)

# def generate_tangent_polynomial(point1, point2, tangent_vector):
#     x1, y1, z1 = point1
#     x2, y2, z2 = point2
#
#     dx, dy, dz = np.subtract(point2, point1)
#     a, b, c = tangent_vector
#
#     # Use the given information to solve for the coefficients of a
#     # 2nd degree polynomial that passes through the two points and
#     # is tangent to the given vector at the second point
#     a2 = 2 * (a - b * dx / dy) / dz
#     a1 = (b - a2 * (z1 + z2) / 2) / dy
#     a0 = a / dz - a1 * y1 - a2 * z1**2 / 2
#
#     def polynomial(x, y, z):
#         return a0 + a1 * y + a2 * z**2 + b * x + c * z
#
#     return polynomial
#
#
# def plot_tangent_polynomial(point1, point2, tangent_vector):
#     fig = plt.figure()
#     ax = fig.add_subplot(projection='3d')
#     # Plot the points and the tangent vector at the second point
#     ax.scatter(point1[0], point1[1], point1[2], label='Start')
#     ax.scatter(point2[0], point2[1], point2[2], label='Throw')
#     ax.quiver(point2[0], point2[1], point2[2], tangent_vector[0], tangent_vector[1], tangent_vector[2], length=0.1,
#                 normalize=True)
#     # Plot the polynomial
#     polynomial = generate_tangent_polynomial(point1, point2, tangent_vector)
#     x = np.linspace(point1[0], point2[0], 100)
#     y = np.linspace(point1[1], point2[1], 100)
#     z = np.linspace(point1[2], point2[2], 100)
#     X, Y, Z = np.meshgrid(x, y, z)
#     ax.scatter(X, Y, polynomial(X, Y, Z), alpha=0.5)
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Z')
#     plt.show()
#
# if __name__ == '__main__':
#     start_point = (1, 2, 3)
#     throw_point = (4, 5, 6)
#     throw_vector = (7, 8, 9)
#     print(generate_tangent_polynomial(start_point, throw_point, throw_vector)(0, 0, 0))
#
#     plot_tangent_polynomial(start_point, throw_point, throw_vector)
