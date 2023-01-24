from reachy_sdk import ReachySDK
import time
import numpy as np

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

SAVE_DIRECTORY_PATH = '../traj/'
FILENAME = 'test'
END_POS_1 = [21.83, -4.99, 24.48, -114.15, -8.06, -9.71, 0.15, 3.01]
END_POS_2 = [10.05, -0.68, 22.99, -65.27, -1.61, -46.64, -15.1, 2.86]
PRESENT_POSITION = 'pos'
GOAL_POSITION = 'goal'
RECORD_FREQUENCY = 100

reachy = ReachySDK('localhost')

def reproduce_traj(filename, method = PRESENT_POSITION):
    '''
    Reproduce a trajectory from a file
    :param filename: the name of the file to read
    :param method: the method to use to reproduce the trajectory (PRESENT_POSITION ou GOAL_POSITION)    
    '''

    try:
        reachy.turn_on('r_arm')
        traj = np.load(filename, allow_pickle=True)[method]
        print(traj)

        #reproduce the trajectory
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), traj[0])}, duration=3.0)
        for t in traj:  
            for joint, pos in zip(reachy.r_arm.joints.values(), t):
                joint.goal_position = pos
            time.sleep(1/RECORD_FREQUENCY)
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), END_POS_1)}, duration=3.0)
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), END_POS_2)}, duration=1.0)

        reachy.turn_off_smoothly('reachy')

    except:
        print("Interrupted")
        reachy.turn_off_smoothly('reachy')
    


if __name__ == '__main__':
    filename = SAVE_DIRECTORY_PATH + FILENAME + '.npz'
    reproduce_traj(filename)

