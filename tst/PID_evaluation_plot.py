from reachy_sdk import ReachySDK
import time
from reachy_sdk.trajectory import goto
import matplotlib.pyplot as plt


def get_current_position(Reachy):
    """
    Get the current position of the right arm
    """
    # Recovery of the current position of the requested motor
    return time.time()-TIME, Reachy.r_arm.r_forearm_yaw.present_position


def plot_positions(Reachy):
    pos = []
    # try:
    while time.time()-TIME < 4:
        pos.append(get_current_position(Reachy))
    # except KeyboardInterrupt:
    plt.plot(*zip(*pos))
    plt.show()


if __name__ == '__main__':
    TIME = time.time()
    reachy = ReachySDK('localhost')
    plot_positions(reachy)