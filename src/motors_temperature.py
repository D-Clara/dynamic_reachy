# You can launch the script with to register the temperature of the motors in a file before reproducing a trajectory :
#   python3 motors_temperature.py >> data/temperature.log ; python3 reproduce_traj.py
#
# Else it will print the current temperature of the motors in your shell
from reachy_sdk import ReachySDK

reachy = ReachySDK(host='127.0.0.1')

for joint in reachy.r_arm.joints.items():
    print(f'Joint "{joint[0]}" temperature is {joint[1].temperature} degree.')

print("------------------")
# reachy.turn_off('r_arm')
