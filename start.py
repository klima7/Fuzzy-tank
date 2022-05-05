import vrep
import sys
import time 
import numpy as np
from tank import *
from fuzzy_soft import get_new_soft_velocity
from fuzzy_sharp import get_new_sharp_velocity

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

while (time.time()-t) < 30:
    err_code, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(clientID, ps_handle, vrep.simx_opmode_streaming)
    distance = np.linalg.norm(detectedPoint)
    velocity = tank.readVelocity()
    new_velocity = get_new_soft_velocity(velocity, distance)
    tank.forward(new_velocity)
    print(f'{distance:10} {velocity:10} -> {new_velocity}')

vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot) # stop the simulation in vrep
