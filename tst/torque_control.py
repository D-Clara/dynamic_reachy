from reachy_sdk import ReachySDK
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

import sys 
import os
sys.path.append(os.path.abspath("/home/reachy/dynamic_reachy/src"))
from angles_correction import actif_angles_correction_empty_hand, actif_angles_correction_no_empty_hand 

reachy = ReachySDK('localhost')
INIT_POS = [-0.0, 0.0, 0.0, -45.0, 0.0, 0.0, 0.0, -10.40]

def find_position_for_elbow_torque():
    pos = np.copy(INIT_POS)
    final_pos = np.copy(INIT_POS)
    pos[3] -= 10
    final_pos[3] -= 10
    eps = 0.1
    try:  
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        while(abs(pos[3] - reachy.r_arm.r_elbow_pitch.present_position) > eps):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), INIT_POS)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), final_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            final_pos[3]+=(pos[3] - reachy.r_arm.r_elbow_pitch.present_position)/2
        print("Position to be given")
        print(final_pos)
        reachy.turn_off_smoothly('reachy')
        return final_pos
    except:
        reachy.turn_off_smoothly('reachy')

def elbow_error_evaluate(final_angle):
    pos = np.copy(INIT_POS)
    final_pos = np.copy(INIT_POS)
    pos[3] -= 10
    final_pos[3] = final_angle
    try:  
        err = []
        p = []
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        for i in range(10):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), INIT_POS
        )}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), final_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            err.append(pos[3] - reachy.r_arm.r_elbow_pitch.present_position)
            p.append(reachy.r_arm.r_elbow_pitch.present_position)
        print("The average of the errors")
        print(np.mean(err))
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

def find_position_for_shoulder_torque():
    pos = np.copy(INIT_POS)
    final_pos = np.copy(INIT_POS)
    pos[0] -= 10
    final_pos[0] -= 10
    eps = 0.1
    try:  
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        while(abs(pos[0] - reachy.r_arm.r_shoulder_pitch.present_position) > eps):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), INIT_POS
        )}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), final_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            final_pos[0]+=(pos[0] - reachy.r_arm.r_shoulder_pitch.present_position)/2
        print("Position to be given")
        print(final_pos)
        reachy.turn_off_smoothly('reachy')
        return final_pos
    except:
        reachy.turn_off_smoothly('reachy')

def shoulder_error_evaluate(final_angle):
    pos = np.copy(INIT_POS)
    final_pos = np.copy(INIT_POS)
    pos[0] -= 10
    final_pos[0] = final_angle
    try:  
        err = []
        p = []
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        for i in range(10):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), INIT_POS
        )}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), final_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            err.append(pos[0] - reachy.r_arm.r_shoulder_pitch.present_position)
            p.append(reachy.r_arm.r_shoulder_pitch.present_position)
        print("The average of the errors")
        print(np.mean(err))
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')


   
final_pos = find_position_for_elbow_torque()
time.sleep(2)
elbow_error_evaluate(final_pos[3])
time.sleep(2)
final_pos = find_position_for_shoulder_torque()
time.sleep(2)
shoulder_error_evaluate(final_pos[0])
