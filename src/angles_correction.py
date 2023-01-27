import numpy as np

def sign(i):
    if i >= 0:
        return 1
    else:
        return -1

def actif_angles_correction_empty_hand(shoulder_angle, elbow_angle):
    if elbow_angle > 0:
        elbow_angle = 0
    g = 9.81
    l_forearm = 0.36
    l_arm = 0.293
    m_forearm = 0.6
    m_arm = 0.6
    shoulder_torque = -g*(m_arm*l_arm/2*np.sin(shoulder_angle*np.pi/180)+m_forearm*l_forearm/2*np.sin((shoulder_angle+elbow_angle)*np.pi/180)+m_forearm*l_arm*np.sin(shoulder_angle*np.pi/180)) 
    elbow_torque = -g*m_forearm*l_forearm/2*np.sin(elbow_angle*np.pi/180)
    # shoulder_angle += -0.86139*shoulder_torque+0.348547*sign(shoulder_angle)
    shoulder_angle += -0.8298166*shoulder_torque
    # elbow_angle += -1.54423*elbow_torque-0.504432
    elbow_angle += -1.945815*elbow_torque-0.0394932
    return [shoulder_angle, elbow_angle]

if __name__ == '__main__':
    a = actif_angles_correction_empty_hand(-30,0)
    print(a)