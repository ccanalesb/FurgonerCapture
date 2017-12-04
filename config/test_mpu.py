#!/usr/bin/env python
"""Released under the MIT License
Copyright 2015, 2016 MrTijn/Tijndagamer
"""

from mpu6050 import mpu6050
from time import sleep
import os

sensor = mpu6050(0x68)

while True:
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    temp = sensor.get_temp()

    print("Accelerometer data")
    print("x: " + str(int(accel_data['x'])))
    print("y: " + str(int(accel_data['y'])))
    print("z: " + str(int(accel_data['z'])))

    print("Gyroscope data")
    print("x: " + str(int(gyro_data['x'])))
    print("y: " + str(int(gyro_data['y'])))
    print("z: " + str(int(gyro_data['z'])))

    print("Temp: " + str(temp) + " C")
    sleep(0.1)  
    clear = lambda: os.system('clear')
    clear()

