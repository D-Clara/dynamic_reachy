import pypot.dynamixel as dm
import time
import numpy as np

# Connect to the usb port and dynamixel "controller"
ports = dm.get_available_ports()
if not ports:
    exit('No port')
dxl_io = dm.DxlIO(ports[0])
print(ports)
print(dxl_io)

# Search for the available motors
motor_id = []
for i in range(50):
    if dxl_io.ping(i):
        motor_id.append(i)
print(motor_id)
ids = dxl_io.scan(motor_id)

######################################################
# Get the current position of the motors connected
######################################################
# while True:
#     print(dxl_io.get_present_position(ids))
#     time.sleep(1)

######################################################
# Put the fisrt connected motor to 0 degrees
######################################################
# dxl_io.set_goal_position({motor_id[0]: 0})

######################################################
# Test on the wrist motor
######################################################
angles = np.linspace(-45, 19, 50)
dxl_io.set_joint_mode(motor_id)
for i in range(10):
    for j in angles:
        dxl_io.set_goal_position({motor_id[0]: j})
        time.sleep(0.01)
    time.sleep(0.5)
    for j in angles[::-1]:
        dxl_io.set_goal_position({motor_id[0]: j})
        time.sleep(0.01)
    time.sleep(0.5)

######################################################
# Compliant test on a motor
######################################################
# dxl_io.set_torque_limit({motor_id: 100})
# time.sleep(0.5)
# dxl_io.set_goal_position({motor_id: 0})
# time.sleep(1)
# dxl_io.set_torque_limit({motor_id: 0})

print("done")
