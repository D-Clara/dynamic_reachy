import numpy as np
import time

from reachy_sdk import ReachySDK

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

reachy = ReachySDK('localhost')

traj = []
pos = []

def get_positions():
    #print("-----------------------------------")
    #print(reachy.joints.values)
    #print(reachy.r_arm.joints.values())
    #print([joint.present_position for name, joint in reachy.r_arm.joints.items()])
    
    #items = dict((v,k.present_position) for v, k in reachy.joints.items())
    #items = {cle: items[cle] for cle in ["r_shoulder_pitch", "r_shoulder_roll","r_arm_yaw","r_elbow_pitch","r_forearm_yaw","r_wrist_pitch","r_wrist_roll","r_gripper"]}
    #make a copy of the dict with new keynames
    
    #print(items)
    #print(new_dict)
    items = dict((v,k.present_position) for v, k in reachy.joints.items())
    items = {cle: items[cle] for cle in reachy.r_arm.joints.keys()}
    new_dict = {}
    for cle in items.keys():    
    #     new_keyname = "reachy.r_arm." + cle
        new_dict[cle] = items[cle]
    return new_dict

while(True):
    try:
        traj.append(get_positions())
        pos.append([joint.present_position for name, joint in reachy.r_arm.joints.items()])
        time.sleep(0.01)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        #print(traj)
        #save the trajectory in traj folder
        #np.save('traj/traj.npy', np.array[traj,pos])
        #np.savez_compressed('traj/traj.npz', traj=traj, pos=pos)
        #save list pos and traj in the same file
        np.savez_compressed('traj/traj.npz', traj=traj, pos=pos)
        break