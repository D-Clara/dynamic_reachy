from reachy_sdk import ReachySDK

def change_PID(pid):
    '''
    Change the PID of the right arm
    '''

    reachy.r_arm.r_shoulder_pitch.pid = (pid[0][0], pid[0][1], pid[0][2])
    reachy.r_arm.r_shoulder_roll.pid = (pid[1][0], pid[1][1], pid[1][2])
    reachy.r_arm.r_arm_yaw.pid = (pid[2][0], pid[2][1], pid[2][2])
    reachy.r_arm.r_elbow_pitch.pid = (pid[3][0], pid[3][1], pid[3][2])
    reachy.r_arm.r_forearm_yaw.pid = (pis[4][0], pid[4][1], pid[4][2])
    reachy.r_arm.r_wrist_pitch.pid = (pid[5][0], pid[5][1], pid[5][2])
    reachy.r_arm.r_wrist_roll.pid = (1.0, 1.0, 32.0, 32.0)
    reachy.r_arm.r_gripper.pid = (1.0, 1.0, 32.0, 32.0)


def print_PID():
    '''
    Print the PID of the right arm
    '''
    for j in reachy.r_arm.joints.values():
        print(f"{j.name}: PID={j.pid}")
    

if __name__ == '__main__':
    reachy = ReachySDK('localhost')
    change_PID([[64,10,100],[64,10,100],[20,0,0],[64,10,100],[20,0,0],[20,0,0],[20,0,0]])
    #print_PID()