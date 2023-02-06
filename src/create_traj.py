import time
import numpy as np
from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from angles_correction import actif_angles_correction

reachy = ReachySDK('localhost')

FREQUENCY = 100



def manual_goto(goal_pos, duration):
    '''
    Go to a position with a given duration
    goal_pos : list of 7 angles in degrees
    duration : time in seconds
    '''
    number_of_points = int(duration * FREQUENCY)
    all_pos = []
    joints = list(reachy.r_arm.joints.values())[:7]
    init_pos = [joint.present_position for joint in joints]

    for i in range(7):
        pos = np.linspace(init_pos[i], goal_pos[i], number_of_points)
        all_pos.append(pos)
    print(all_pos)
    print(joints, len(joints))
    goal = []
    try :
        reachy.turn_on('r_arm')
        for i in range(number_of_points):
            for j in range(len(joints)):
                joints[j].goal_position = all_pos[j][i]
                print(all_pos[j][i])
                print(joints[j].goal_position)
                print("----------------------------------")
            goal.append([joint.goal_position for name, joint in reachy.r_arm.joints.items()])
            print("=====================================")
            time.sleep(1/FREQUENCY)
        time.sleep(1)
        reachy.turn_off_smoothly('reachy')
        print(goal)
    except :
        reachy.turn_off_smoothly('reachy')
        print('Error')

def manual_goto_angles_correction(goal_pos, duration):
    '''
    Go to a position with a given duration
    goal_pos : list of 7 angles in degrees
    duration : time in seconds
    '''
    number_of_points = int(duration * FREQUENCY)
    all_pos = []
    joints = list(reachy.r_arm.joints.values())[:7]
    init_pos = [joint.present_position for joint in joints]

    for i in range(7):
        pos = np.linspace(init_pos[i], goal_pos[i], number_of_points)
        all_pos.append(pos)
    print(all_pos)
    print(joints, len(joints))
    goal = []

    for i in range(number_of_points):
        a = actif_angles_correction(all_pos[0][i],all_pos[3][i])
        all_pos[0][i] = a[0]
        all_pos[3][i] = a[1]

    try :
        reachy.turn_on('r_arm')
        for i in range(number_of_points):
            for j in range(len(joints)):
                joints[j].goal_position = all_pos[j][i]
                print(all_pos[j][i])
                print(joints[j].goal_position)
                print("----------------------------------")
            goal.append([joint.goal_position for name, joint in reachy.r_arm.joints.items()])
            print("=====================================")
            time.sleep(1/FREQUENCY)
        time.sleep(1)
        reachy.turn_off_smoothly('reachy')
        print(goal)
    except :
        reachy.turn_off_smoothly('reachy')
        print('Error')

if __name__ == '__main__':
    manual_goto([0,0,-90,-60,0,0,0], 3)

