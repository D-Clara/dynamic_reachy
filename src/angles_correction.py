import numpy as np

G = 9.81
L_FOREARM = 0.36
L_ARM = 0.293
M_FOREARM = 0.6
M_ARM = 0.6


def sign(i):
    if i >= 0:
        return 1
    else:
        return -1

def actif_angles_correction(shoulder_angle, elbow_angle, empty_hand=True, init_torque_shoulder=0, init_torque_elbow=0):
    if elbow_angle > 0:
        elbow_angle = 0
    if empty_hand:
        l_forearm = L_FOREARM/2
    else:
        l_forearm = L_FOREARM
    shoulder_torque = init_torque_shoulder -G*((M_ARM * L_ARM/2+ M_FOREARM * L_ARM)*np.sin(shoulder_angle * np.pi/180) + M_FOREARM * l_forearm *np.sin((shoulder_angle + elbow_angle) * np.pi/180))
    elbow_torque = init_torque_elbow -G * M_FOREARM *l_forearm * np.sin((shoulder_angle + elbow_angle) * np.pi/180)
    shoulder_angle += -0.86139*shoulder_torque+0.348547*sign(shoulder_angle)
    elbow_angle += -1.54423*elbow_torque-0.504432
    return [shoulder_angle, elbow_angle]

if __name__ == '__main__':
    a = actif_angles_correction(-30,0)
    print(a)