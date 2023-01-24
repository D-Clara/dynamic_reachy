from reachy_sdk import ReachySDK

reachy = ReachySDK('localhost')

def change_PID():
    '''
    Change the PID of the right arm
    '''

    # reachy.r_arm.r_shoulder_pitch.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_shoulder_roll.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_arm_yaw.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_elbow_pitch.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_forearm_yaw.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_wrist_pitch.pid = (64.0, 10.0, 100)
    # reachy.r_arm.r_wrist_roll.pid = (64.0, 10.0, 100)

    reachy.r_arm.r_shoulder_pitch.pid =(32.0, 0.0, 0.0)
    reachy.r_arm.r_shoulder_roll.pid =(32.0, 0.0, 0.0)
    reachy.r_arm.r_arm_yaw.pid =(32.0, 0.0, 0.0)
    reachy.r_arm.r_elbow_pitch.pid =(32.0, 0.0, 0.0)
    reachy.r_arm.r_forearm_yaw.pid =(32.0, 0.0, 0.0)
    reachy.r_arm.r_wrist_pitch.pid =(32.0, 0.0, 0.0)
    reachy.r_arm.r_wrist_roll.pid =(32.0, 0.0, 0.0)
    reachy.r_arm.r_gripper.pid =(32.0, 0.0, 0.0)


def print_PID()
    '''
    Print the PID of the right arm
    '''
    for j in reachy.r_arm.joints.values():
        print(f"{j.name}: PID={j.pid}")
    

if __name__ == main():
    change_PID()
    #print_PID()