import matplotlib.pyplot as plt
import numpy as np

name = 'traj_coralie3.npz'
now = "2023-01-13 10:19:28"

#load error file

err = np.load('/home/reachy/dynamic_reachy/tst/log_pid/err_{}_{}.npy'.format(now,name), allow_pickle=True)
js = np.load('/home/reachy/dynamic_reachy/tst/log_pid/pos_{}_{}.npy'.format(now,name), allow_pickle=True)
pid = np.load('/home/reachy/dynamic_reachy/tst/log_pid/pid_{}_{}.npy'.format(now,name), allow_pickle=True)

print(err)

#plot error

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