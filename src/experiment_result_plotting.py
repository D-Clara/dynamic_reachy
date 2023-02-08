import numpy as np
import matplotlib.pyplot as plt

GOAL = np.array([
    [17.0, 22.5],  # 1
    [15.8, 18.0],
    [33.1, 17.0],
    [33.0, 11.2],
    [34.8, 14.5],  # 5
    [26.5, 12.8],
    [7.6, 15.0],
    [14.4, 18.0],
    [19.0, 21.0],
    [27.5, 13.4],  # 10
    [25.5, 11.5],
    [30.3, 11.2],
    [35.5, 13.4],
    [16.3, 23.0],
    [30.0, 16.0],  # 15
    [16.5, 25.0],
    [28.5, 14.3],
    [19.8, 21.6],
    [18.5, 19.5],
    [35.0, 12.0],  # 20
])
GOAL_right = GOAL[GOAL[:, 0] > 23]
print("With GOAL positions :")
print("mean = ", np.mean(GOAL, axis=0))
print("var = ", np.var(GOAL, axis=0))

print("With GOAL positions, without 'retouch' cases :")
print("mean = ", np.mean(GOAL_right, axis=0))
print("var = ", np.var(GOAL_right, axis=0))

fig, ax = plt.subplots()
for i in range(len(GOAL_right)):
    ax.scatter(GOAL_right[i][0], GOAL_right[i][1], label=i)
ax.legend()
ax.grid(True)
plt.show()


COUPLE = np.array([
    [8.8, 9.6],  # 1
    [18.0, 14.8],
    [15.5, 13.0],
    [15.3, 12.4],
    [7.0, 6.0],  # 5
    [17.5, 12.5],
    [10.9, 10.2],
    [14.2, 12.4],
    [14.4, 13.3],
    [11.5, 8.5],  # 10
    [16.5, 13.0],
    [10.0, 11.0],
    [10.8, 7.4],
    [16.3, 13.6],
    [9.9, 6.0],  # 15
    [20.3, 15.0],
    [14.7, 13.4],
    [16.2, 11.9],
    [0.5, 4.0],
    [5.6, 9.3],  # 20
])

print("With TORQUE compensation :")
print("mean = ", np.mean(COUPLE, axis=0))
print("var = ", np.var(COUPLE, axis=0))

fig, ax = plt.subplots()

for i in range(len(COUPLE)):
    ax.scatter(COUPLE[i][0], COUPLE[i][1], label=i)
ax.legend()
ax.grid(True)
plt.show()


COUPLE_PID = np.array([
    [23.2, 15.5],  # 1
    [21.4, 12.0],
    [18.6, 12.0],
    [23.7, 16.3],
    [26.0, 13.7],  # 5
    [16.8, 4.8],
    [22.5, 13.4],
    [19.3, 8.5],
    [21.5, 11.2],
    [15.7, 11.6],  # 10
    [17.5, 11.1],
    [23.3, 11.8],
    [25.3, 14.4],
    [21.5, 18.7],
    [22.8, 11.6],  # 15
    [14.9, 10.2],
    [21.8, 10.7],
    [19.2, 11.7],
    [19.2, 10.4],
    [26.7, 13.5],  # 20
])

print("With PID and TORQUE compensation :")
print("mean = ", np.mean(COUPLE_PID, axis=0))
print("var = ", np.var(COUPLE_PID, axis=0))

fig, ax = plt.subplots()

for i in range(len(COUPLE_PID)):
    ax.scatter(COUPLE_PID[i][0], COUPLE_PID[i][1], label=i)
ax.legend()
ax.grid(True)
plt.show()


plt.scatter(COUPLE[:, 0], COUPLE[:, 1], label="COUPLE")
plt.scatter(COUPLE_PID[:, 0], COUPLE_PID[:, 1], label="COUPLE_PID")
plt.scatter(GOAL[:, 0], GOAL[:, 1], label="GOAL")
plt.scatter(16.3, 13.6, label="TELEOP")
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()