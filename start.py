import vrep
import math
import sys
import time 
import numpy as np
from tank import *
from fuzzy_soft import get_new_soft_velocity
from fuzzy_sharp import get_new_sharp_velocity
import matplotlib.pyplot as plt

vrep.simxFinish(-1)
clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

if clientID != -1:
    print("Connected to remote API server")
else:
    print("Not connected to remote API server")
    sys.exit("Could not connect")

tank = Tank(clientID)

err_code, ps_handle = vrep.simxGetObjectHandle(clientID, "Proximity_sensor", vrep.simx_opmode_blocking)

t = time.time()

vrep.simxStartSimulation(clientID,vrep.simx_opmode_oneshot)

drivers = {
    'soft': get_new_soft_velocity,
    'sharp': get_new_sharp_velocity,
}

# --------------------
driver_name = 'soft'
# --------------------

ds = []
real_vs = []
ideal_vs = []

while (time.time()-t) < 25:
    err_code, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ps_handle, vrep.simx_opmode_streaming)
    distance = np.linalg.norm(detectedPoint)
    if distance == 0:
        continue
    velocity = tank.readVelocity()
    new_velocity = drivers[driver_name](velocity, distance)
    tank.forward(new_velocity)

    print(f'{distance:5.2f} {velocity:5.2f} -> {new_velocity:.2f}')

    ds.append(distance)
    real_vs.append(velocity)
    ideal_vs.append(new_velocity)

vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot) # stop the simulation in vrep

# showing velocity graph
fig, ax = plt.subplots()
ax.plot(ds, real_vs, label='Real velocity')
ax.plot(ds, ideal_vs, label='Desired velocity')
ax.set_xlabel('Distance')
ax.set_ylabel('Velocity')
ax.legend()
fig.show()
plt.show()
