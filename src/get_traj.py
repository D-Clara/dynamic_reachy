import numpy as np
import time

from reachy_sdk import ReachySDK

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

reachy = ReachySDK('localhost')

traj = []
pos = []
goal = []


def is_pose_reachable(self, pose, is_left_arm=True, precision=0.005, verbose=True):
        angles = []
        joints = {}
        # Note: in this version, the same precision is used to compare meters and degrees...
        # Not ideal but shouldn't matter since it's often either almost identical, or not at all
        try:
            if is_left_arm:
                angles = self.reachy.l_arm.inverse_kinematics(pose)
                real_pose = self.reachy.l_arm.forward_kinematics(angles)
                joints = {joint: pos for joint, pos in zip(self.reachy.l_arm.joints.values(), angles)}
            else:
                angles = self.reachy.r_arm.inverse_kinematics(pose)
                real_pose = self.reachy.r_arm.forward_kinematics(angles)
                joints = {joint: pos for joint, pos in zip(self.reachy.r_arm.joints.values(), angles)}
            # Testing if the forward kinematics matches
            for iy, ix in np.ndindex(pose.shape):
                if (abs(pose[iy, ix]-real_pose[iy, ix]) > precision):
                    if verbose:
                        self.get_logger().warning(f"Unreachable pose: {pose}")
                    return False, joints

            # Testing if the angular limits are respected
            for j in joints.keys():
                limits = self.angle_limits[j.name]
                if verbose:
                    self.get_logger().warning(f"angle limits of {j.name}={limits}")
                angle = joints[j]*math.pi/180.0
                valid = self.is_valid_angle(angle, limits)
                if not valid:
                    if verbose:
                        self.get_logger().warning(f"{j.name} are {limits}rad, asked for unreachable angle: {angle}rad")
                    return False, joints
        except Exception:
            self.get_logger().error(traceback.format_exc())
            return False, joints

        return True, joints

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
        goal.append([joint.goal_position for name, joint in reachy.r_arm.joints.items()])
        #print(pos)
        time.sleep(0.01)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        #print(traj)
        #save the trajectory in traj folder
        #np.save('traj/traj.npy', np.array[traj,pos])
        #np.savez_compressed('traj/traj.npz', traj=traj, pos=pos)
        #save list pos and traj in the same file
        np.savez_compressed('../traj/traj_gui3.npz', traj=traj, pos=pos, goal=goal)
        break