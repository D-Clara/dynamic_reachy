import numpy as np
import time
import datetime
import json

from reachy_sdk import ReachySDK

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

from constants_and_flags import incr, decr, flagg

# Global variables
RECORD_FREQUENCY = 100
SAVE_DIRECTORY_PATH = '/home/reachy/dynamic_reachy/traj/'
GOAL_JSON_PATH = '/home/reachy/dynamic_reachy/src/goal.json'
SAVE_JSON_PATH = '/home/reachy/dynamic_reachy/src/save.json'

# traj filenames generator
FILENAME_COMMENT = 'test'
FILENAME_PREFIX = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


saving = False  # variable globale déclarée à l'extérieur de toutes les méthodes de la classe


def __init__():
    pass

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


def add_goal(element):
    """
    Add a goal to the trajectory
    """
    global goal
    goal.append(element)
    
def start_saving():
    dictionary = {
    "save": True
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open(SAVE_JSON_PATH, "w") as outfile:
        outfile.write(json_object)


def stop_saving():
    dictionary = {
    "save": False
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open(SAVE_JSON_PATH, "w") as outfile:
        outfile.write(json_object)


def save_goal(goal_pos,times):
    dictionary = {
    "goal": goal_pos, "times" : times
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open(GOAL_JSON_PATH, "w") as outfile:
        outfile.write(json_object)

def load_goal():
    with open(GOAL_JSON_PATH) as json_file:
        data = json.load(json_file)
    return data['goal'], data['times']




def is_saving():
    with open(SAVE_JSON_PATH) as json_file:
        data = json.load(json_file)
    return data['save']


def record_trajectory(filename):
    """
    Record the trajectory of the arm and save it in a file
    :param filename: the name of the file to save the trajectory
    """
    traj = []
    pos = []
    goal = []
    times = []
    start_saving()
    while True:
        try:
            #print(is_saving())
            #print(test, is_saving())
            traj.append(get_positions())
            pos.append([joint.present_position for name, joint in reachy.r_arm.joints.items()])
            print([joint.present_position for name, joint in reachy.r_arm.joints.items()])
            #goal.append([joint.goal_position for name, joint in reachy.r_arm.joints.items()])
            time.sleep(1/RECORD_FREQUENCY)
        except KeyboardInterrupt:
            stop_saving()
            time.sleep(1)
            #print(goal)
            print("End of recording")        
            filePath = SAVE_DIRECTORY_PATH + filename + '.npz'
            goal, times = load_goal()
            np.savez_compressed(filePath, traj=traj, pos=pos, goal=goal, times=times)
            break








# def is_pose_reachable(pose, is_left_arm=True, precision=0.005, verbose=True):
#     """
#     Check if a pose is reachable by the arm.
#     :param pose: the pose to check
#     :param is_left_arm: if True, check the left arm, else check the right arm
#     :param precision: the precision to use to check if the pose is reachable
#     :param verbose: if True, print some debug messages
#     :return: True if the pose is reachable, False otherwise
#     """
#     angles = []
#     joints = {}

#     try:
#         if is_left_arm:
#             angles = reachy.l_arm.inverse_kinematics(pose)
#             real_pose = reachy.l_arm.forward_kinematics(angles)
#             joints = {joint: pos for joint, pos in zip(reachy.l_arm.joints.values(), angles)}
#         else:
#             angles = reachy.r_arm.inverse_kinematics(pose)
#             real_pose = reachy.r_arm.forward_kinematics(angles)
#             joints = {joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), angles)}
#         # Testing if the forward kinematics matches
#         for iy, ix in np.ndindex(pose.shape):
#             if abs(pose[iy, ix] - real_pose[iy, ix]) > precision:
#                 if verbose:
#                     get_logger().warning(f"Unreachable pose: {pose}")
#                 return False, joints

#         # Testing if the angular limits are respected
#         for j in joints.keys():
#             limits = angle_limits[j.name]
#             if verbose:
#                 get_logger().warning(f"angle limits of {j.name}={limits}")
#             angle = joints[j]*np.pi/180.0
#             valid = is_valid_angle(angle, limits)
#             if not valid:
#                 if verbose:
#                     get_logger().warning(f"{j.name} are {limits}rad, asked for unreachable angle: {angle}rad")
#                 return False, joints
#     except Exception:
#         get_logger().error(traceback.format_exc())
#         return False, joints

#     return True, joints




if __name__ == "__main__":
    reachy = ReachySDK('reachy.local')
    print("You're traj file will be saved in: ")
    print(SAVE_DIRECTORY_PATH+FILENAME_PREFIX+'_'+FILENAME_COMMENT+'.npz')
    record_trajectory(FILENAME_PREFIX+'_'+FILENAME_COMMENT)
