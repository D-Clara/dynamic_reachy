from reachy_sdk import ReachySDK

reachy = ReachySDK(host='127.0.0.1') 

for name, joint in reachy.joints.items():
    print(f'Joint "{name}" position is {joint.present_position} degree.')
reachy.turn_off('r_arm')

