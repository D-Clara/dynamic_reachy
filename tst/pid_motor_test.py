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
pid = [[60,10,200],[60,10,200],[60,10,200],[60,10,200],[60,10,200],[20,0,0],[20,0,0]]

ERR = []
ERR2 = []

time.sleep(1)

def setup_pid():
    reachy.r_arm.r_shoulder_pitch.pid = (pid[0][0], pid[0][1], pid[0][2])
    reachy.r_arm.r_shoulder_roll.pid = (pid[1][0], pid[1][1], pid[1][2])
    reachy.r_arm.r_arm_yaw.pid = (pid[2][0], pid[2][1], pid[2][2])
    reachy.r_arm.r_elbow_pitch.pid = (pid[3][0], pid[3][1], pid[3][2])
    reachy.r_arm.r_forearm_yaw.pid = (pid[4][0], pid[4][1], pid[4][2])
    reachy.r_arm.r_wrist_pitch.pid = (pid[5][0], pid[5][1], pid[5][2])
    reachy.r_arm.r_wrist_roll.pid = (pid[6][0], pid[6][1], pid[6][2])
    time.sleep(0.1)

    for j in reachy.r_arm.joints.values():
        print(f"{j.name}: PID={j.pid}")

def erreur():
    #position from where to where reachy makes the move 
    pos = [0, 0, 0, 0, 0, -40, 0, 0]
    pos2 = [0, 0, 0, 0, 0, 40, 0, 0]

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
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

#setup or test pid
i = 1
if(i==0):
    setup_pid()
else:   
    erreur()
    print(np.mean(ERR))
    print(np.mean(ERR2))

