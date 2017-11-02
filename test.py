#!/usr/bin/env python
# from mpu6050 import mpu6050
from time import sleep
import os
from random import randint

array_prom = []	
array_y = []
array_z = []

def promlista_x(array_prom):
    sum=0
    for i in range(0,len(array_prom)):
        sum=sum+array_prom[i]
 
    print sum/len(array_prom)


def promlista_y(array_y):
    sum=0
    for i in range(0,len(array_y)):
        sum=sum+array_y[i]
 
    print sum/len(array_y)


def promlista_z(array_z):
   	sum=0
   	for i in range(0,len(array_z)):
		sum=sum+array_z[i]
 
   	print sum/len(array_z)

while True:
	print("Accelerometer data")
	x = int(randint(0, 90))
	y = int(randint(0, 90))
	z = int(randint(0, 90))
	
	array_prom.append(x)
	array_y.append(y)
	array_z.append(z)
	
	print("x: " + str(x))
	print("y: " + str(y))
	print("z: " + str(z))
	
	if len(array_prom) == 10:
		promlista_x(array_prom)
		promlista_y(array_y)
		promlista_z(array_z)
		array_prom = []
		array_y = []	
		array_z = []

	sleep(0.5)	
	clear = lambda: os.system('clear')
	clear()
