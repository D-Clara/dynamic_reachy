from reachy_sdk import ReachySDK
import time
import numpy as np

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

def reproduce_traj(filename):
    reachy = ReachySDK('localhost')
    # end_pos = {'reachy.r_arm.r_shoulder_pitch': -15.54, 'reachy.r_arm.r_shoulder_roll': 0.46, 'reachy.r_arm.r_arm_yaw': 37.23, 'reachy.r_arm.r_elbow_pitch': -48.31, 'reachy.r_arm.r_forearm_yaw': -20.97, 'reachy.r_arm.r_wrist_pitch': -48.92, 'reachy.r_arm.r_wrist_roll': 8.36}
    end_pos2 = [-9.65, 3.28, 22.29, -55.87, -0.15, -23.87, -1.61, 6.23]
    #with np.load(filename, allow_pickle=True) as data:
    #    print(data['pos'])
    #load the data in the file filename


    # reachy.r_arm.r_shoulder_pitch.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_shoulder_roll.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_arm_yaw.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_elbow_pitch.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_forearm_yaw.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_wrist_pitch.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_wrist_roll.pid = (64.0, 10.0, 100)

    for j in reachy.r_arm.joints.values():
        print(f"{j.name}: PID={j.pid}")


    #print(traj)

    try:
        
        
        reachy.turn_on('r_arm')
        #read trajectory in traj/traj.npy
        traj = np.load(filename, allow_pickle=True)['pos']
        #reproduce the trajectory
        print(traj)
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), traj[0])}, duration=3.0)
        for t in traj:  
            for joint, pos in zip(reachy.r_arm.joints.values(), t):
                joint.goal_position = pos
            time.sleep(0.01)
            #goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), t)}, duration=0.1)
        # goto(end_pos, duration=3, interpolation_mode=InterpolationMode.LINEAR)
        # time.sleep(3)
        # for t in traj:  
        #     goto(t, duration=0.1, interpolation_mode=InterpolationMode.LINEAR)
        # goto(end_pos, duration=3, interpolation_mode=InterpolationMode.LINEAR)
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), end_pos2)}, duration=3.0)
        reachy.turn_off_smoothly('reachy')
    except Exception as e:
        print("error",e)
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), end_pos2)}, duration=3.0)
        reachy.turn_off_smoothly('reachy')

reproduce_traj('traj/traj_coralie3.npz')
#reproduce_traj('traj/vr_shot.npy')
