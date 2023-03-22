#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import Float64
from cmath import pi
import numpy as np
from std_msgs.msg import Float32MultiArray, Float64


class CPGsub:
    def __init__(self):
        self.sub1 = rospy.Subscriber("leg1x",Float64,self.cb1)
        self.sub2 = rospy.Subscriber("leg2x",Float64,self.cb2)
        
        self.pub1 = rospy.Publisher("leg123",Float32MultiArray,queue_size=10)
        self.pub2 = rospy.Publisher("leg456",Float32MultiArray,queue_size=10)

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

        self.ang1 = 90
        self.ang2 = 90
        rospy.init_node("CPG_sub")
        
        self.m1 = Float32MultiArray()
        self.m2 = Float32MultiArray()

        self.rate = rospy.Rate(10000)

    
    def cb1(self,msg):
        self.ang1 = msg.data
    
    def cb2(self,msg):
        self.ang2 = msg.data

    def main(self):
        while not rospy.is_shutdown():
           

            self.j2=[self.l6j3,self.l6j2,self.l6j1,self.l5j3,self.l5j2,self.l5j1,self.l4j3,self.l4j2,self.l4j1]
            self.j=[self.ang1,self.ang2,self.l1j3,self.ang1,self.ang2,self.l2j3,self.ang1,self.ang2,self.l3j3]

            self.m1.data = self.j
            self.m2.data = self.j2

            self.pub1.publish(self.m1)
            self.pub2.publish(self.m2)

            self.rate.sleep()

if __name__ == "__main__":
    cpgcall = CPGsub()
    cpgcall.main()