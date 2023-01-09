import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from reachy_sdk import ReachySDK

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

reachy = ReachySDK('localhost')
print("eeee")

#read trajectory in traj/traj.npy
traj = np.load('traj/traj_coralie3.npz', allow_pickle=True)["traj"]
poses = []
grip = []

print(traj)
for t in traj:
    #print(t)
    #t = np.array(t)
    #print(t['r_shoulder_pitch'])
    #print(reachy.r_arm.forward_kinematics())
    #print({cle: t[cle] for cle in ["r_shoulder_pitch", "r_shoulder_roll","r_arm_yaw","r_elbow_pitch","r_forearm_yaw","r_wrist_pitch","r_wrist_roll"]})
    poses.append(reachy.r_arm.forward_kinematics({cle: t[cle] for cle in ["r_shoulder_pitch", "r_shoulder_roll","r_arm_yaw","r_elbow_pitch","r_forearm_yaw","r_wrist_pitch","r_wrist_roll"]}.values()))
    grip.append(t["r_gripper"])
    #print(reachy.r_arm.joints.values())
    #reachy.r_arm.joints.keys()
    #print({a: b for a,b in zip(reachy.r_arm.joints.keys(), t[:7])})
    #poses.append(reachy.r_arm.forward_kinematics({a: b for a,b in zip(reachy.r_arm.joints.keys(), t[:7])}))
times= np.linspace(0, 1, len(poses))

print(poses)
#print(grip)


X = [p[0,3] for p in poses]
Y = [p[1,3] for p in poses]
Z = [p[2,3] for p in poses]
#plt.plot(times, , label='x')
#plt.plot(times, , label='x')
#plt.plot(times, [p[2,3] for p in poses], label='x')
#plt.show()
#print (X,Y,Z)
print(len(X),len(Y),len(Z), len(grip))

X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)

X1 = []
Y1 = []
Z1 = []
X2 = []
Y2 = []
Z2 = []

# Création de la figure
#fig = plt.figure()
#ax = Axes3D(fig)

#find the index of first element > -12 in the grip array
#grip = np.array(grip)
#index = np.where(grip < -12)[0][0]
#print(index)
#print(grip[index], grip[index+1])
for i in range(len(grip)):
    if grip[i] < -12:
        X1.append(X[i])
        Y1.append(Y[i])
        Z1.append(Z[i])
    else:   
        X2.append(X[i])
        Y2.append(Y[i])
        Z2.append(Z[i])


#index = 0

# X1 = X[:index]
# Y1 = Y[:index]
# Z1 = Z[:index]
# X2 = X[index:]
# Y2 = Y[index:]
# Z2 = Z[index:]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')  # Affichage en 3D
ax.scatter(X1, Y1, Z1, label='Courbe')
ax.scatter(X2, Y2, Z2, label='Courbe')
minax = min([min(X), min(Y), min(Z)])
manax = max([max(X), max(Y), max(Z)]) 
manax += 0.1
minax -= 0.1
plt.xlim(minax, manax)
plt.ylim(minax, manax)
ax.set_zlim(minax, manax)


#surf = ax.plot_trisurf(X, Y, Z, linewidth=0, antialiased=False)
# Tracé de la surface
#ax.plot_surface(X, Y, Z, cmap='viridis')

# Affichage du graphique
plt.show()