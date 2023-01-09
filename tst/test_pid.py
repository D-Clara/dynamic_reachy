from reachy_sdk import ReachySDK
import time
import numpy as np

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

def erreur(filename):
    reachy = ReachySDK('localhost')
    end_pos2 = [-9.65, 3.28, 22.29, -55.87, -0.15, -23.87, -1.61, 6.23]

    reachy.r_arm.r_shoulder_pitch.pid = (64.0, 10.0, 100)
    reachy.r_arm.r_shoulder_roll.pid = (64.0, 10.0, 100)
    reachy.r_arm.r_arm_yaw.pid = (64.0, 10.0, 100)
    reachy.r_arm.r_elbow_pitch.pid = (64.0, 10.0, 100)
    reachy.r_arm.r_forearm_yaw.pid = (64.0, 10.0, 100)
    reachy.r_arm.r_wrist_pitch.pid = (64.0, 10.0, 100)
    reachy.r_arm.r_wrist_roll.pid = (64.0, 10.0, 100)

    for j in reachy.r_arm.joints.values():
        print(f"{j.name}: PID={j.pid}")

    try: 
        reachy.turn_on('r_arm')
        #read trajectory in traj/traj.npy
        traj = np.load(filename, allow_pickle=True)['pos']
        #reproduce the trajectory
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), traj[0])}, duration=3.0)
        for t in traj:  
            for joint, pos in zip(reachy.r_arm.joints.values(), t):
                joint.goal_position = pos
            time.sleep(0.01)
            e = []
            for joint in reachy.r_arm.joints.values():
                e.append(t - joint.present_position )
                print(t,joint.present_position)
                print("-----------------------------------")
            err.append(e)


        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), end_pos2)}, duration=3.0)
        reachy.turn_off_smoothly('reachy')
    except Exception as e:
        print("error",e)
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), end_pos2)}, duration=3.0)
        reachy.turn_off_smoothly('reachy')

err = []
erreur('../traj/traj_coralie3.npz')
print(err)
#reproduce_traj('traj/vr_shot.npy')
