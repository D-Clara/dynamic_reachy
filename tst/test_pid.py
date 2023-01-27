from reachy_sdk import ReachySDK
import time
import numpy as np
import matplotlib.pyplot as plt
import datetime

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

#pid = [[25,0,0],[45,0,0],[0.1,0,0],[0.5,0,0],[40,0,0],[32,0,0],[32,0,0]]
#pid = [[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100],[64,10,100]]
#pid = [[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0],[20,0,0]]
#pid = [[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0],[64,0,0]]
pid = [[64,0,0],[64,0,0],[64,0,0],[150,0,0],[64,0,0],[64,0,0],[64,0,0]]


def erreur(filename):
    reachy = ReachySDK('localhost')
    # end_pos2 = [-9.65, 3.28, 22.29, -55.87, -0.15, -23.87, -1.61, 6.23]
    end_pos = [21.83, -4.99, 24.48, -114.15, -8.06, -9.71, 0.15, 3.01]
    end_pos2 = [10.05, -0.68, 22.99, -65.27, -1.61, -46.64, -15.1, 2.86]

    reachy.r_arm.r_shoulder_pitch.pid = (pid[0][0], pid[0][1], pid[0][2])
    reachy.r_arm.r_shoulder_roll.pid = (pid[1][0], pid[1][1], pid[1][2])
    reachy.r_arm.r_arm_yaw.pid = (pid[2][0], pid[2][1], pid[2][2])
    reachy.r_arm.r_elbow_pitch.pid = (pid[3][0], pid[3][1], pid[3][2])
    reachy.r_arm.r_forearm_yaw.pid = (pid[4][0], pid[4][1], pid[4][2])
    reachy.r_arm.r_wrist_pitch.pid = (pid[5][0], pid[5][1], pid[5][2])
    reachy.r_arm.r_wrist_roll.pid = (pid[6][0], pid[6][1], pid[6][2])

    time.sleep(0.1)

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
            joints = []
            i=0
            for joint in reachy.r_arm.joints.values():
                e.append(t[i] - joint.present_position )
                joints.append(joint.present_position)
                i+=1
            err.append(e)
            js.append(joints)


        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), end_pos)}, duration=3.0)
        goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), end_pos2)}, duration=1.0)
        reachy.turn_off_smoothly('reachy')
    except:
        reachy.turn_off_smoothly('reachy')

err = []
js = []
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
name = 'traj_gui2'
erreur('../traj/'+name+'.npz')
np.save('log_pid/err_{}_{}'.format(now,name), err)
np.save('log_pid/pos_{}_{}'.format(now,name), js)
np.save('log_pid/pid_{}_{}'.format(now,name), pid)

plt.figure()    
x=np.linspace(0,1,len(err))
plt.plot(x,[array[0] for array in err], label='shoulder_pitch')
plt.plot(x,[array[1] for array in err], label='shoulder_roll')
plt.plot(x,[array[2] for array in err], label='arm_yaw')
plt.plot(x,[array[3] for array in err], label='elbow_pitch')
plt.plot(x,[array[4] for array in err], label='forearm_yaw')
plt.plot(x,[array[5] for array in err], label='wrist_pitch')
plt.plot(x,[array[6] for array in err], label='wrist_roll')
plt.plot(x,[array[7] for array in err], label='grip')
plt.legend()
plt.show()
