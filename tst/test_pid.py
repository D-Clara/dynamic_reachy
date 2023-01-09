from reachy_sdk import ReachySDK

from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory.interpolation import InterpolationMode

reachy = ReachySDK('localhost')


for j in reachy.r_arm.joints.values():
    print(f"{j.name}: PID={j.pid}")