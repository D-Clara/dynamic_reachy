import time
import numpy as np
from reachy_sdk import ReachySDK

reachy = ReachySDK(host='127.0.0.1') 



A = np.array([
  [0, 0, -1, 0.3],
  [0, 1, 0, -0.4],  
  [1, 0, 0, -0.3],
  [0, 0, 0, 1],  
])

B = np.array([
  [0, 0, -1, 0.3],
  [0, 1, 0, -0.4],  
  [1, 0, 0, 0.0],
  [0, 0, 0, 1],  
])

C = np.array([
  [0, 0, -1, 0.3],
  [0, 1, 0, -0.1],  
  [1, 0, 0, 0.0],
  [0, 0, 0, 1],  
])

D = np.array([
  [0, 0, -1, 0.3],
  [0, 1, 0, -0.1],  
  [1, 0, 0, -0.3],
  [0, 0, 0, 1],  
])

joint_pos_A = reachy.r_arm.inverse_kinematics(A)
joint_pos_B = reachy.r_arm.inverse_kinematics(B)
joint_pos_C = reachy.r_arm.inverse_kinematics(C)
joint_pos_D = reachy.r_arm.inverse_kinematics(D)



# put the joints in stiff mode
reachy.turn_on('r_arm')

# use the goto function
goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), joint_pos_A)}, duration=1.0)
time.sleep(0.5)
goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), joint_pos_B)}, duration=1.0)
time.sleep(0.5)
goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), joint_pos_C)}, duration=1.0)
time.sleep(0.5)
goto({joint: pos for joint,pos in zip(reachy.r_arm.joints.values(), joint_pos_D)}, duration=1.0)

# put the joints back to compliant mode
# use turn_off_smoothly to prevent the arm from falling hard
reachy.turn_off_smoothly('r_arm')