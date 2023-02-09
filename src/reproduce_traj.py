import time
import numpy as np
from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode
from angles_correction import actif_angles_correction
from get_traj import load_goal


DEBUT = [-6.57, -4.99, 0.84, -79.16, -8.36, -4.7, 11.29, -44.79]
PRESENT_POSITION = 'pos'
GOAL_POSITION = 'goal'

# MODIFY HERE
#FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_08:28:47_test.npz'
#FILENAME = "/home/reachy/dynamic_reachy/traj/2023-02-08_11:42:54_test.npz"
FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-08_10:22:00_test.npz'
RECORD_FREQUENCY = 100
PREPROCESSING = True
TYPE_OF_POSITION = PRESENT_POSITION




def pre_traitement_couple(filename, method=PRESENT_POSITION, init_torque_shoulder=0, init_torque_elbow=0):
    '''
    Preprocess the trajectory to correct the angles
    :param filename: the name of the file to read
    :param method: the method to use to reproduce the trajectory (PRESENT_POSITION ou GOAL_POSITION)
    :param init_torque_shoulder: the initial torque of the shoulder
    :param init_torque_elbow: the initial torque of the elbow
    '''
    traj = np.load(filename, allow_pickle=True)[method]
    for t in traj:
        [t[0], t[3]] = actif_angles_correction(t[0], t[3], init_torque_shoulder, init_torque_elbow)
    return traj


def goal_preprocessing(filename,reachy):
    '''
    Preprocess the trajectory to get the goal position
    :param filename: the name of the file to read
    :param reachy: the reachy object
    '''
    file_load = np.load(filename, allow_pickle=True)
    times = file_load["times"]
    times[0] = 0
    pos = file_load['pos']
    traj = file_load['goal']

    t = -0.18
    gripper = [pos[0][7] for i in range(len(times))]
    print(pos[0][7])

    for i in range(len(times)):  
        t += times[i]
        index = round(t*RECORD_FREQUENCY)
        #print(index, len(pos))
        if index < len(pos):
            value = pos[index][7]
            if value > 60.0 or value < -60.0:
                gripper[i] = 5.0
            else :
                gripper[i] = value
            print(gripper[i])
    #print(gripper)
    print(len(gripper), len(traj), len(times))

    joints = [name for name, joint in reachy.r_arm.joints.items()]
    poses = []
    #print(traj)
    #print(pos[0])
    for i in range(len(traj)):
        pos = []
        for j in range(len(joints)-1):
            angle = traj[i][joints[j]] * 180 / np.pi
            pos.append(angle)
        pos.append(gripper[i])
        poses.append(pos)

    #print(poses)
    return poses, times

def reproduce_traj(filename, reachy, method=PRESENT_POSITION, preprocessing=True, init_torque_shoulder=0, init_torque_elbow=0):
    '''
    Reproduce a trajectory from a file
    :param filename: the name of the file to read
    :param method: the method to use to reproduce the trajectory (PRESENT_POSITION ou GOAL_POSITION)    
    '''

    try:
        reachy.turn_on('r_arm')
        if not(preprocessing):
            traj = np.load(filename, allow_pickle=True)[method]
        else:
            traj = pre_traitement_couple(filename, method, init_torque_shoulder, init_torque_elbow)
        #print(traj)
        #print(len(traj), len(traj))
        # reproduce the trajectory
        goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), DEBUT)}, duration=2.0)
        goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), traj[0])}, duration=2.0)
        for t in traj:
            for joint, pos in zip(reachy.r_arm.joints.values(), t):
                joint.goal_position = pos
                print(pos)
            print('------------------')
            time.sleep(1 / RECORD_FREQUENCY)
        reachy.turn_off_smoothly('reachy')

    except :
        reachy.turn_off_smoothly('reachy')
        print("Interrupted")


def reproduce_traj_bis(filename, reachy, method=GOAL_POSITION, preprocessing=False, init_torque_shoulder=1.5, init_torque_elbow=0.5):
    '''
    Reproduce a trajectory from a file
    :param filename: the name of the file to read
    :param method: the method to use to reproduce the trajectory (PRESENT_POSITION ou GOAL_POSITION)    
    '''

    try:
        reachy.turn_on('r_arm')
        traj, times = goal_preprocessing(filename,reachy)
        #print(len(traj), len(times))
        # reproduce the trajectory
        goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), DEBUT)}, duration=2.0)
        goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), traj[0])}, duration=2.0)
        for i in range(len(traj)):
            print(times[i])
            time.sleep(times[i])
            for joint, pos in zip(reachy.r_arm.joints.values(), traj[i]):
                joint.goal_position = pos
                print(pos)
            print('------------------')
            
        reachy.turn_off_smoothly('reachy')

    except Exception as e:
        print(e)
        reachy.turn_off_smoothly('reachy')
        print("Interrupted")
    except :
        reachy.turn_off_smoothly('reachy')
        print("Interrupted")
        

if __name__ == '__main__':
    
    robot = ReachySDK('localhost')
    if TYPE_OF_POSITION == PRESENT_POSITION:
        reproduce_traj(FILENAME, robot, preprocessing=PREPROCESSING)
    else:
        reproduce_traj_bis(FILENAME, robot)
    





########################## DEPRECATED TEST TRAJECTORIES ###################################

# 1 bas gauche
#FILENAME = '/home/reachy/dynamic_reachy/traj/2023-01-30_17:41:16_test.npz'

# 2 milieu bien
#FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_08:28:47_test.npz'

# 3 trop a droite
# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_08:27:25_test.npz'

# 4 add goto au debut
# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_08:26:32_test.npz'

# 6 en vrai 4 droit mais loin (ou peut etre 4 et 5 avec rebond)
# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_08:29:04_test.npz'

# proche du bord
# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-01-31_08:20:42_test.npz'

# très loin
# TROPLOIN = '/home/reachy/dynamic_reachy/traj/2023-01-31_08:40:51_test.npz'

# loin a gauche
# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_08:27:40_test.npz'

# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_16:12:50_test.npz'
# 6 long

# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_16:13:29_test.npz'
# 1 bof

# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_16:13:48_test.npz'
# 5 a froid plus 3 mauvaise prise

# CINQ = '/home/reachy/dynamic_reachy/traj/2023-02-01_16:14:07_test.npz'
# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_16:14:24_test.npz'
# FILENAME = '/home/reachy/dynamic_reachy/traj/2023-02-01_16:14:38_test.npz'

