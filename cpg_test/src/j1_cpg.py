import math
import matplotlib.pyplot as plt
import numpy as np
pi = 3.141569
amp = np.array([1,1])
camp = np.array([0.8,0.8])
phase = [pi, -pi/2]
offset = np.array([pi/2,0])
coff = 0.01
frequency = np.array([0.1,0.4])
dt = 0.0001
result = 0
time = np.arange(0,100,dt)
iterations = 1000000

def dp(frequency, idx, phase, phase_offset_target):
    #print("{} = {}".format(idx,frequency))
    if idx == 0:
        return 2 * pi * frequency + 1 * amp[0] * math.sin(phase[1]-phase[0]-phase_offset_target)
    else:
        return 2 * pi * frequency + 1 * amp[1] * math.sin(phase[0]-phase[1]+phase_offset_target)

def da(amp_target):
    return camp * (amp_target - amp)
       

def do(offset_target):
    return coff * (offset_target - offset)

def update_values(amp_target = 0.535, offset_target = np.array([pi/2,7*pi/12]), frequency_target = 0.04, phase_offset_target = pi/2):
    global phase, amp, offset
    for i in range(2):
        # print("{} = {}".format(i,frequency_target[i]))
        phase[i] = phase[i] + dp(frequency_target, i, phase, phase_offset_target) * dt
        
    amp = amp + (camp * (amp_target - amp)) * dt
    offset = offset + do(offset_target)
    
def output():
    return amp * np.sin(phase) + offset

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
    #n2.append(result[1])

out1 = np.array(n1)*180/pi
#out2 = np.array(n2)*180/pi
plt.plot(time, out1)
#lt.plot(time, out2)
plt.show()