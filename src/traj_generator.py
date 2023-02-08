import numpy as np
import matplotlib.pyplot as plt

freq = 100  # Hz


def generate_tangent_polynomial(point1, point2, tangent_vector):
    x1, y1, z1 = point1
    x2, y2, z2 = point2

    dx, dy, dz = np.subtract(point2, point1)
    a, b, c = tangent_vector

    # Use the given information to solve for the coefficients of a
    # 2nd degree polynomial that passes through the two points and
    # is tangent to the given vector at the second point
    a2 = 2 * (a - b * dx / dy) / dz
    a1 = (b - a2 * (z1 + z2) / 2) / dy
    a0 = a / dz - a1 * y1 - a2 * z1**2 / 2

    def polynomial(x, y, z):
        return a0 + a1 * y + a2 * z**2 + b * x + c * z

    return polynomial


def plot_tangent_polynomial(point1, point2, tangent_vector):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    # Plot the points and the tangent vector at the second point
    ax.scatter(point1[0], point1[1], point1[2], label='Start')
    ax.scatter(point2[0], point2[1], point2[2], label='Throw')
    ax.quiver(point2[0], point2[1], point2[2], tangent_vector[0], tangent_vector[1], tangent_vector[2], length=0.1,
                normalize=False)
    # Plot the polynomial function
    polynomial = generate_tangent_polynomial(point1, point2, tangent_vector)
    x = np.linspace(point1[0], point2[0], 100)
    y = np.linspace(point1[1], point2[1], 100)
    z = np.linspace(point1[2], point2[2], 100)
    print("X shape : ", x.shape)
    print("Y shape : ", y.shape)
    print("Z shape : ", z.shape)
    print("polynomial  : ", polynomial(x, y, z))
    ax.plot(x, y, polynomial(x, y, z), alpha=0.5)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

if __name__ == '__main__':
    start_point = (1, 1, 1)
    throw_point = (2, 2, 2)
    throw_vector = (3, 2, -2)
    plot_tangent_polynomial(start_point, throw_point, throw_vector)
