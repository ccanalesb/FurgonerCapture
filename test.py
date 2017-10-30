#!/usr/bin/env python
# from mpu6050 import mpu6050
from time import sleep
import os
from random import randint

while True:
    print("Accelerometer data")
    x = int(randint(0, 9))
    y = int(randint(0, 9))
    z = int(randint(0, 9))
    print("x: " + str(x))
    print("y: " + str(y))
    print("z: " + str(z))
    sleep(0.1)	
    clear = lambda: os.system('clear')
    clear()