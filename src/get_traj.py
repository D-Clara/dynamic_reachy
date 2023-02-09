import numpy as np
import time
import datetime
import json

from reachy_sdk import ReachySDK

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

# Global variables
RECORD_FREQUENCY = 100
SAVE_DIRECTORY_PATH = '/home/reachy/dynamic_reachy/traj/'
GOAL_JSON_PATH = '/home/reachy/dynamic_reachy/src/goal.json'
SAVE_JSON_PATH = '/home/reachy/dynamic_reachy/src/save.json'

# traj filenames generator
FILENAME_COMMENT = 'test'
FILENAME_PREFIX = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")


saving = False 


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
    :param element: the goal position to add
    """
    global goal
    goal.append(element)
    
def start_saving():
    '''
    Start saving the trajectory
    '''
    dictionary = {
    "save": True
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open(SAVE_JSON_PATH, "w") as outfile:
        outfile.write(json_object)


def stop_saving():
    '''
    Stop saving the trajectory
    '''
    dictionary = {
    "save": False
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open(SAVE_JSON_PATH, "w") as outfile:
        outfile.write(json_object)


def save_goal(goal_pos,times):
    '''
    Save the goal position
    :param goal_pos: the goal positions
    :param times: the times to reach the goal
    '''

    dictionary = {
    "goal": goal_pos, "times" : times
    }
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
    # Writing to sample.json
    with open(GOAL_JSON_PATH, "w") as outfile:
        outfile.write(json_object)

def load_goal():
    '''
    Load the goal position
    '''
    with open(GOAL_JSON_PATH) as json_file:
        data = json.load(json_file)
    return data['goal'], data['times']




def is_saving():
    '''
    Check if the trajectory is being saved
    '''
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




if __name__ == "__main__":
    reachy = ReachySDK('reachy.local')
    print("You're traj file will be saved in: ")
    print(SAVE_DIRECTORY_PATH+FILENAME_PREFIX+'_'+FILENAME_COMMENT+'.npz')
    record_trajectory(FILENAME_PREFIX+'_'+FILENAME_COMMENT)
