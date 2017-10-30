#!/usr/bin/env python
# from mpu6050 import mpu6050
from time import sleep
import os
from random import randint

while True:

    print("Accelerometer data")
    print("x: " + str(int(randint(0, 9))))
    print("y: " + str(int(randint(0, 9))))
    print("z: " + str(int(randint(0, 9))))
    sleep(0.1)	
    clear = lambda: os.system('clear')
    clear()