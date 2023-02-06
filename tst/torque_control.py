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
init_pos = [-0.0, 0.0, 0.0, -45.0, 0.0, 0.0, 0.0, -10.40]
pos = [init_pos[0], 0.0, 0.0, init_pos[3]-10, 0.0, 0.0, 0.0, -10.40]

final_pos = np.copy(pos)
# final_pos[0]=actif_angles_correction_no_empty_hand(pos[0], pos[3])[0]
# final_pos[3]=actif_angles_correction_empty_hand(pos[0], pos[3])[1]
# final_pos[0]=-60.3547

def find_position_for_torque_elbow():
    eps = 0.1

    try:  
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        print(reachy.r_arm.r_elbow_pitch.present_position)
        while(abs(pos[3] - reachy.r_arm.r_elbow_pitch.present_position) > eps):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), init_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), final_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            final_pos[3]+=(pos[3] - reachy.r_arm.r_elbow_pitch.present_position)/2
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

def error_evaluate_elbow():
    try:  
        err = []
        p = []
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        for i in range(10):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), init_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), final_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            err.append(pos[3] - reachy.r_arm.r_elbow_pitch.present_position)
            p.append(reachy.r_arm.r_elbow_pitch.present_position)
        print(err, np.mean(err))
        print(p, np.mean(p))
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

def find_position_for_torque_shoulder():
    eps = 0.1

    try:  
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        print(reachy.r_arm.r_shoulder_pitch.present_position)
        while(abs(pos[0] - reachy.r_arm.r_shoulder_pitch.present_position) > eps):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), init_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), final_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            final_pos[0]+=(pos[0] - reachy.r_arm.r_shoulder_pitch.present_position)/2
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

def error_evaluate_shoulder():
    try:  
        err = []
        err1 = []
        p = []
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), pos)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        for i in range(10):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), init_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), final_pos)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            err.append(pos[0] - reachy.r_arm.r_shoulder_pitch.present_position)
            p.append(reachy.r_arm.r_shoulder_pitch.present_position)
        print(err, np.mean(err))
        print(p, np.mean(p))
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')


   
find_position_for_torque_elbow()
# print(final_pos)
# print(init_pos)
# time.sleep(2)
# error_evaluate_shoulder()


