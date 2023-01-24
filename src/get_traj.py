import numpy as np
import time
import datetime

from reachy_sdk import ReachySDK

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

# Global variables
RECORD_FREQUENCY = 100
SAVE_DIRECTORY_PATH = '../traj/'

# traj filenames generator
FILENAME_COMMENT = 'petitmvt'
FILENAME_PREFIX = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
FILENAME_SUFFIX = '.npz'

reachy = ReachySDK('localhost')


def is_pose_reachable(self, pose, is_left_arm=True, precision=0.005, verbose=True):
    """
    Check if a pose is reachable by the arm.
    :param pose: the pose to check
    :param is_left_arm: if True, check the left arm, else check the right arm
    :param precision: the precision to use to check if the pose is reachable
    :param verbose: if True, print some debug messages
    :return: True if the pose is reachable, False otherwise
    """
    angles = []
    joints = {}

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
            if abs(pose[iy, ix] - real_pose[iy, ix]) > precision:
                if verbose:
                    self.get_logger().warning(f"Unreachable pose: {pose}")
                return False, joints

        # Testing if the angular limits are respected
        for j in joints.keys():
            limits = self.angle_limits[j.name]
            if verbose:
                self.get_logger().warning(f"angle limits of {j.name}={limits}")
            angle = joints[j]*np.pi/180.0
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
    """
    Get the current position of the joints
    :return a dict with the joint name and the current position
    """

    items = dict((v,k.present_position) for v, k in reachy.joints.items())
    items = {cle: items[cle] for cle in reachy.r_arm.joints.keys()}
    new_dict = {}
    for cle in items.keys():    
        new_dict[cle] = items[cle]
    return new_dict


def record_trajectory(filename):
    """
    Record the trajectory of the arm and save it in a file
    :param filename: the name of the file to save the trajectory
    """
    traj = []
    pos = []
    goal = []

    while True:
        try:
            traj.append(get_positions())
            pos.append([joint.present_position for name, joint in reachy.r_arm.joints.items()])
            goal.append([joint.goal_position for name, joint in reachy.r_arm.joints.items()])
            time.sleep(1/RECORD_FREQUENCY)
        except KeyboardInterrupt:
            print("End of recording")
            filePath = SAVE_DIRECTORY_PATH + filename + '.npz'
            np.savez_compressed(filePath, traj=traj, pos=pos, goal=goal)
            break


if __name__ == "__main__":
    record_trajectory(FILENAME_PREFIX+'_'+FILENAME_COMMENT+FILENAME_SUFFIX)
