from reachy_sdk import ReachySDK
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

#PID = [[25,0,0],[45,0,0],[0.1,0,0],[0.5,0,0],[40,0,0],[32,0,0],[32,0,0]]
# PID = [[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100]]
#PID = [[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0]]
#PID = [[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0]]
# PID = [[64,0,0],[64,0,0],[64,0,0],[150,0,0],[64,0,0],[64,0,0],[64,0,0]]
# PID = [[32,0,0],[32,0,0],[32,0,0],[30,0,0],[1,1,32],[32,0,0],[1,1,32]]
# PID = [[10,0,0],[60,10,200],[60,10,200],[60,10,200],[60,10,200],[20,0,0],[20,0,0]]
# PID = [[64,10,100],[64,10,100],[64,10,100],[60,10,100],[60,10,200],[20,0,0],[20,0,0]]
PID = [[64,10,100],[64,10,100],[20,0,0],[64,10,100],[20,0,0],[20,0,0],[20,0,0]]

ERR = []
JS = []

#error during a movement
def error(filename):
    """
    Record error for each motor during a throw
    :param param1 name of the filename of the throw in the directory traj 
    """
    reachy = ReachySDK('localhost')

    #change pid value

    # end_pos2 = [-9.65, 3.28, 22.29, -55.87, -0.15, -23.87, -1.61, 6.23]
    end_pos = [21.83, -4.99, 24.48, -114.15, -8.06, -9.71, 0.15, 3.01]
    end_pos2 = [10.05, -0.68, 22.99, -65.27, -1.61, -46.64, -15.1, 2.86]

    reachy.r_arm.r_shoulder_pitch.pid = (PID[0][0], PID[0][1], PID[0][2])
    reachy.r_arm.r_shoulder_roll.pid = (PID[1][0], PID[1][1], PID[1][2])
    reachy.r_arm.r_arm_yaw.pid = (PID[2][0], PID[2][1], PID[2][2])
    reachy.r_arm.r_elbow_pitch.pid = (PID[3][0], PID[3][1], PID[3][2])
    reachy.r_arm.r_forearm_yaw.pid = (PID[4][0], PID[4][1], PID[4][2])
    reachy.r_arm.r_wrist_pitch.pid = (PID[5][0], PID[5][1], PID[5][2])
    reachy.r_arm.r_wrist_roll.pid = (1.0, 1.0, 32.0, 32.0)
    reachy.r_arm.r_gripper.pid = (1.0, 1.0, 32.0, 32.0)

    time.sleep(2)

    for j in reachy.r_arm.joints.values():
        print(f"{j.name}: PID={j.pid}")

    try: 
        reachy.turn_on('r_arm')
        #read trajectory in traj/traj.npy
        traj = np.load(filename, allow_pickle=True)['pos']
        print(traj)
        
        #goto to initial position
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), traj[0])}, duration=3.0)

        #reproduce the trajectory
        for t in traj:  
            for joint, pos in zip(reachy.r_arm.joints.values(), t):
                joint.goal_position = pos
            time.sleep(0.01)

            #error calculation
            e = []
            joints = []
            i=0
            for joint in reachy.r_arm.joints.values():
                e.append(t[i] - joint.present_position )
                joints.append(joint.present_position)
                i+=1
            ERR.append(e)
            JS.append(joints)


        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), end_pos)}, duration=3.0)
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), end_pos2)}, duration=1.0)
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

#save data
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
name = '2023-01-30_17:41:16_test'
error('/home/reachy/dynamic_reachy/traj/'+name+'.npz')
np.save('/home/reachy/dynamic_reachy/tst/log_pid/err_{}_{}'.format(now,name), ERR)
np.save('/home/reachy/dynamic_reachy/tst/log_pid/pos_{}_{}'.format(now,name), JS)
np.save('/home/reachy/dynamic_reachy/tst/log_pid/pid_{}_{}'.format(now,name), PID)

#plot error
plt.figure()    
x=np.linspace(0,1,len(ERR))
print(np.mean([array[0] for array in ERR]))
plt.plot(x,[array[0] for array in ERR], label='shoulder_pitch')
plt.plot(x,[array[1] for array in ERR], label='shoulder_roll')
plt.plot(x,[array[2] for array in ERR], label='arm_yaw')
plt.plot(x,[array[3] for array in ERR], label='elbow_pitch')
plt.plot(x,[array[4] for array in ERR], label='forearm_yaw')
plt.plot(x,[array[5] for array in ERR], label='wrist_pitch')
plt.plot(x,[array[6] for array in ERR], label='wrist_roll')
plt.plot(x,[array[7] for array in ERR], label='grip')
plt.legend()
plt.show()
