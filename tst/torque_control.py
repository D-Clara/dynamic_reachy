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
POS = [INIT_POS[0], 0.0, 0.0, INIT_POS[3], 0.0, 0.0, 0.0, -10.40]

FINAL_POS = np.copy(POS)

def find_position_for_elbow_torque():
    POS[3] -= 10
    eps = 0.1
    try:  
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), POS)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        while(abs(POS[3] - reachy.r_arm.r_elbow_pitch.present_position) > eps):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), INIT_POS
        )}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), FINAL_POS)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            FINAL_POS[3]+=(POS[3] - reachy.r_arm.r_elbow_pitch.present_position)/2
        print("Position to be given" + FINAL_POS)
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

def elbow_error_evaluate(final_angle):
    POS[3] -= 10
    FINAL_POS[3] = final_angle
    try:  
        err = []
        p = []
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), POS)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        for i in range(10):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), INIT_POS
        )}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), FINAL_POS)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            err.append(POS[3] - reachy.r_arm.r_elbow_pitch.present_position)
            p.append(reachy.r_arm.r_elbow_pitch.present_position)
        print("The average of the errors" + np.mean(err))
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

def find_position_for_shoulder_torque():
    POS[0] -= 10
    eps = 0.1
    try:  
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), POS)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        print(reachy.r_arm.r_shoulder_pitch.present_position)
        while(abs(POS[0] - reachy.r_arm.r_shoulder_pitch.present_position) > eps):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), INIT_POS
        )}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), FINAL_POS)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            FINAL_POS[0]+=(POS[0] - reachy.r_arm.r_shoulder_pitch.present_position)/2
        print("Position to be given" + FINAL_POS)
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

def shoulder_error_evaluate(final_angle):
    POS[0] -= 10
    FINAL_POS[0] = final_angle
    try:  
        err = []
        p = []
        reachy.turn_on('r_arm')
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), POS)}, duration=2, interpolation_mode=InterpolationMode.MINIMUM_JERK)
        for i in range(10):
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), INIT_POS
        )}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), FINAL_POS)}, duration=3/90*10, interpolation_mode=InterpolationMode.MINIMUM_JERK)
            time.sleep(1)
            err.append(POS[0] - reachy.r_arm.r_shoulder_pitch.present_position)
            p.append(reachy.r_arm.r_shoulder_pitch.present_position)
        print("The average of the errors" + np.mean(err))
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')


   
find_position_for_shoulder_torque()
time.sleep(2)
shoulder_error_evaluate(FINAL_POS[0])
