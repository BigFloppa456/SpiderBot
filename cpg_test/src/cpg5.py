import math
import matplotlib.pyplot as plt
import numpy as np
pi = 3.141569
amp = 1
camp = 0.8
phase = [0,0]
offset = np.array([0,0])
coff = 0.01
frequency = 0.1
dt = 0.0001
result = 0
dt = 0.0001
time = np.arange(0,100,dt)
iterations = 1000000

def dp(frequency, idx, phase, phase_offset_target):
    if idx == 0:
        return 2 * pi * frequency + 1 * amp * math.sin(phase[1]-phase[0]-phase_offset_target)
    else:
        return 2 * pi * frequency + 1 * amp * math.sin(phase[0]-phase[1]+phase_offset_target)

def da(amp_target):
    return camp * (amp_target - amp)
       

def do(offset_target):
    return coff * (offset_target - offset)

def update_values(amp_target = 0.2, offset_target = np.array([1.5,1.5]), frequency_target =  [0.4,0.4], phase_offset_target = pi/2):
    global phase, amp, offset
    for i in range(2):
        phase[i] = phase[i] + dp(frequency_target[i], i, phase, phase_offset_target) * dt
        
    amp = amp + da(amp_target) * dt
    offset = offset + do(offset_target)
    
def output():
    return amp * np.sin(phase) + offset
    # return amp * 1/3 * (np.sin(np.array(phase)) + np.sin(0.3*np.array(phase)) + np.sin(0.5*np.array(phase)))**2 + offset

outputs = []
n1 = []
n2 = []
for i in range(iterations):
    # if i < iterations / 3:
    #     update_values()
    # elif i < 2 * iterations / 3:
    #     update_values(offset_target = np.array([1,1]), phase_offset_target = pi + 1.57)
    # else:
    #     update_values(offset_target = np.array([1,1]), phase_offset_target = 2*pi)
    update_values()
    result = output()
    n1.append(result[0])
    n2.append(result[1])


plt.plot(time, n1)
plt.plot(time, n2)
plt.show()