from reachy_sdk import ReachySDK
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

reachy = ReachySDK('localhost')
#pid = [[25,0,0],[45,0,0],[0.1,0,0],[0.5,0,0],[40,0,0],[32,0,0],[32,0,0]]
#pid = [[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100]]
#pid = [[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0]]
#pid = [[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0]]
# PID = [[60,10,200],[60,10,200],[60,10,200],[60,10,200],[60,10,200],[20,0,0],[20,0,0]]
PID = [[64,10,100],[64,10,100],[20,0,0],[64,10,100],[20,0,0],[20,0,0],[20,0,0]]

ERR = []
ERR2 = []

time.sleep(1)

def setup_pid():
    reachy.r_arm.r_shoulder_pitch.pid = (PID[0][0], PID[0][1], PID[0][2])
    reachy.r_arm.r_shoulder_roll.pid = (PID[1][0], PID[1][1], PID[1][2])
    reachy.r_arm.r_arm_yaw.pid = (PID[2][0], PID[2][1], PID[2][2])
    reachy.r_arm.r_elbow_pitch.pid = (PID[3][0], PID[3][1], PID[3][2])
    reachy.r_arm.r_forearm_yaw.pid = (PID[4][0], PID[4][1], PID[4][2])
    reachy.r_arm.r_wrist_pitch.pid = (PID[5][0], PID[5][1], PID[5][2])
    reachy.r_arm.r_wrist_roll.pid = (1.0, 1.0, 32.0, 32.0)
    reachy.r_arm.r_gripper.pid = (1.0, 1.0, 32.0, 32.0)
    time.sleep(0.1)

    for j in reachy.r_arm.joints.values():
        print(f"{j.name}: PID={j.pid}")

def error():
    #position from where to where reachy makes the move
    pos = [0, 0, 0, 0, 0, 0, -30, 0]
    pos2 = [0, 0, 0, 0, 0, 0, 30, 0]

    #record error
    try:
        reachy.turn_on('r_arm')
        for i in range(10):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos2)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(0.01)
            ERR2.append(pos2[5] - reachy.r_arm.r_wrist_pitch.present_position)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(0.01)
            ERR.append(pos[5] - reachy.r_arm.r_wrist_pitch.present_position)
        print(np.mean(ERR))
        print(np.mean(ERR2))
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

def error_pos():
    #position from where to where reachy makes the move
    pos = [0, 0, 0, 0, -30, 0, 0, 0]

    #record error
    try:
        reachy.turn_on('r_arm')
        reachy.r_arm.r_shoulder_pitch.goal_position = pos[0]
        reachy.r_arm.r_shoulder_roll.goal_position = pos[1]
        reachy.r_arm.r_arm_yaw.goal_position = pos[2]
        reachy.r_arm.r_elbow_pitch.goal_position = pos[3]
        reachy.r_arm.r_forearm_yaw.goal_position = pos[4]
        reachy.r_arm.r_wrist_pitch.goal_position = pos[5]
        reachy.r_arm.r_wrist_roll.goal_position = pos[6]
        reachy.r_arm.r_gripper.goal_position = pos[7]
        time.sleep(5)
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

#setup or test pid
setup_pid()
time.sleep(2)
error_pos()

