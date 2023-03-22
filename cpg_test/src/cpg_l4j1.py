#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import Float64
from cmath import pi
import numpy as np
from std_msgs.msg import Float32MultiArray, Float64


class CPG:
    def __init__(self):
        self.pi = 3.141569
        self.amp = 1
        self.camp = 0.8
        self.phase = [self.pi,-self.pi]
        self.offset = np.array([0,0])
        self.coff = 0.1
        self.frequency = 0.1
        self.dt = 0.001
        self.time = np.arange(0,100,self.dt)
        self.result = []
        self.tf_res = [0,0]
        self.msg1 = Float32MultiArray()
        self.msg2 = Float32MultiArray()
        self.angl = 0
        self.iterations = 1000000
        

        self.l1j1 = 90
        self.l1j2 = 110
        self.l1j3 = 105
        self.l2j1 = 90
        self.l2j2 = 110
        self.l2j3 = 105
        self.l3j1 = 90
        self.l3j2 = 110
        self.l3j3 = 105

        # Variables for leg angles for leg 4 5 6
        self.l6j3 = 105
        self.l6j2 = 110
        self.l6j1 = 90
        self.l5j3 = 105
        self.l5j1 = 90
        self.l5j2 = 110

        self.l4j3 = 105
        self.l4j2 = 110
        self.l4j1 = 90

        rospy.init_node("CPGl4j1")
        #rate = rospy.Rate(76800)
        self.rate = rospy.Rate(10000)
        self.j2=[self.l6j3,self.l6j2,self.l6j1,self.l5j3,self.l5j2,self.l5j1,self.l4j3,self.l4j2,self.l4j1]

        self.pub1 = rospy.Publisher("leg4j1",Float64,queue_size=10)
    
    def dp(self,frequency, idx, phase_offset_target):
        if idx == 0:
            return 2 * self.pi * frequency + 1 * self.amp * math.sin(self.phase[1]-self.phase[0]-phase_offset_target)
        else:
            return 2 * self.pi * frequency + 1 * self.amp * math.sin(self.phase[0]-self.phase[1]+phase_offset_target)
    
    def da(self,amp_target):
        return self.camp * (amp_target - self.amp)

    def do(self,offset_target):
        return self.coff * (offset_target - self.offset)

    def update_values(self,amp_target = 0.535, offset_target = np.array([pi/2,pi/2]), frequency_target = [0.04,0.04], phase_offset_target = pi):

        for i in range(2):
            self.phase[i] = self.phase[i] + self.dp(frequency_target[i], i, phase_offset_target) * self.dt
            
        self.amp = self.amp + self.da(amp_target) * self.dt
        self.offset = self.offset + self.do(offset_target)
        
    def output(self):
        self.result = self.amp * np.sin(self.phase) + self.offset
        
        
    def print1(self,angle):
        return (angle*(180/self.pi))
    
    def convangs(arr):
        jts = np.array(np.float_(arr))
        
        return jts #returns a np array after converting string array to a float array
    
    def main(self):
        count = 0
        while not rospy.is_shutdown():
            self.update_values()
            self.output()
            self.tf_res[1] = self.print1(self.result[1])
            
            self.msg1 = Float64()
            # self.msg1.data = self.print1(self.result[0])
            # self.msg2.data = self.print1(self.result[1])

            self.msg1.data = self.tf_res[1]
            #print(self.tf_res[0])
            
            self.pub1.publish(self.msg1)

            self.rate.sleep()

if __name__ == "__main__":
    cpgcall = CPG()
    cpgcall.main()