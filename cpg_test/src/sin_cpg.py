#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import Float64

pi = 3.141569
amp = np.array([1,1])
camp = np.array([0.8,0.8])
phase = [pi,-pi/3]
offset = np.array([0,0])
coff = 0.01
frequency = 0.1
dt = 0.0001
time = np.arange(0,100,dt)
result = 0

iterations = 1000000

rospy.init_node("CPGx")
#rate = rospy.Rate(76800)
rate = rospy.Rate(100000000)

pub1 = rospy.Publisher("leg1x",Float64,queue_size=10)
pub2 = rospy.Publisher("leg2x",Float64,queue_size=10)

def dp(frequency, idx, phase, phase_offset_target):
    if idx == 0:
        return 2 * pi * frequency + 1 * amp[0] * math.sin(phase[1]-phase[0]-phase_offset_target)
    else:
        return 2 * pi * frequency + 1 * amp[1] * math.sin(phase[0]-phase[1]+phase_offset_target)

def da(amp_target):
    return camp * (amp_target - amp)

def do(offset_target):
    return coff * (offset_target - offset)

def update_values(amp_target = [0.53,0.27], offset_target = np.array([pi/2,7*pi/12]), frequency_target = [0.04,0.04], phase_offset_target = pi/2):
    global phase, amp, offset

    for i in range(2):
        phase[i] = phase[i] + dp(frequency_target[i], i, phase, phase_offset_target) * dt
        
    amp = amp + da(amp_target) * dt
    offset = offset + do(offset_target)
    
def output():
    return amp * np.sin(phase) + offset
    
def print1(angle):
    return (angle*(180/pi))

outputs = []
n1 = []
n2 = []


# for i in range(iterations):
while not rospy.is_shutdown():
    # if i < iterations / 3:
    #     update_values()
    # elif i < 2 * iterations / 3:
    #     update_values(2,offset_target = np.array([1,5]),frequency_target = 0.2,phase_offset_target = pi + 1.57)
    # else:
    #     update_values(offset_target = np.array([1,1]), phase_offset_target = 2*pi+1.57)
    update_values()


    result = output()
    msg1 = Float64()
    msg2 = Float64()

    msg1.data = print1(result[0])
    msg2.data = print1(result[1])

    print(print1(result[0]))

    pub1.publish(msg1)
    pub2.publish(msg2)
    # n1.append(result[0])
    # n2.append(result[1])
    rate.sleep()


# plt.plot(time, n1)
# plt.plot(time, n2)
# plt.show()