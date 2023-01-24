import pypot.dynamixel as dm
import time
ports = dm.get_available_ports()
if not ports:
    exit('No port')
dxl_io = dm.DxlIO(ports[0])
print(ports)
print(dxl_io)

motor_id = []
for i in range(50):
    if dxl_io.ping(i):
        motor_id.append(i)
print(motor_id)
ids = dxl_io.scan(motor_id)

while True:
    print(dxl_io.get_present_position(ids))
    time.sleep(1)

# dxl_io.set_joint_mode(motor_id)
# for i in range(10):
#     dxl_io.set_goal_position({motor_id[0]: -45})
#     time.sleep(1)
#     dxl_io.set_goal_position({motor_id[0]: 19})
#     time.sleep(1)

print("done")

# dxl_io.set_torque_limit({motor_id: 100})
# time.sleep(0.5)
# dxl_io.set_goal_position({motor_id: 0})
# time.sleep(1)
# dxl_io.set_torque_limit({motor_id: 0})
