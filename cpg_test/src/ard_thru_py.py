import pyfirmata
import math
import numpy as np
import matplotlib.pyplot as plt

board = pyfirmata.Arduino('/dev/ttyACM0')

pi = 3.141569
amp = 1
camp = 0.8
phase = [pi,-pi]
offset = np.array([0,0])
coff = 0.01
frequency = 0.1
dt = 0.0001
time = np.arange(0,100,dt)
result = 0

iterations = 1000000

servo_pin = 9
board.digital[servo_pin].mode = pyfirmata.SERVO

servo_pin1 = 10
board.digital[servo_pin1].mode = pyfirmata.SERVO


def dp(frequency, idx, phase, phase_offset_target):
    if idx == 0:
        return 2 * pi * frequency + 1 * amp * math.sin(phase[1]-phase[0]-phase_offset_target)
    else:
        return 2 * pi * frequency + 1 * amp * math.sin(phase[0]-phase[1]+phase_offset_target)

def da(amp_target):
    return camp * (amp_target - amp)

def do(offset_target):
    return coff * (offset_target - offset)

def update_values(amp_target = 1.56, offset_target = np.array([0,0]), frequency_target = [0.5,0.5], phase_offset_target = 3*pi/4):
    global phase, amp, offset

    for i in range(2):
        phase[i] = phase[i] + dp(frequency_target[i], i, phase, phase_offset_target) * dt
        
    amp = amp + da(amp_target) * dt
    offset = offset + do(offset_target)
    
def output():
    return amp * np.sin(phase) + offset
    

def set_angle(angle):
    board.digital[servo_pin].write(angle)


def set_angle1(angle):
    board.digital[servo_pin1].write(angle)

def print1(angle):
    return (angle*(180/pi)+90)

def rescale(val):
    in_min = -pi
    in_max = pi
    out_min = 0
    out_max = 2*pi
    return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))



outputs = []
n1 = []
n2 = []

# for i in range(iterations):
#     if i < iterations / 3:
#         update_values()
#     elif i < 2 * iterations / 3:
#         update_values(offset_target = np.array([1,1]), phase_offset_target = pi + 1.57)
#     else:
#         update_values(offset_target = np.array([1,1]), phase_offset_target = 2*pi)
while True:
    update_values()
    result = output()
    # n1.append(result[0])
    # n2.append(result[1])

    # set_angle(print1(rescale(result[0])))
    set_angle(print1((result[0])))
    # time.sleep(100)
    # set_angle1(print1(rescale(result[1])))
    set_angle1(print1((result[1])))
    #print(print1(result[0] + "," +  print1(result[1])))
    print("{}, {}".format(print1(result[0]),print1(result[1])))
    # print(result[1])
    # time.sleep(100)




