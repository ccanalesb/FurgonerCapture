#!/usr/bin/env python
# from mpu6050 import mpu6050
from time import sleep, clock
import os
from random import randint
import numpy as np #PARA SACAR VARIANZA
import threading
import datetime
import json

array_x = []	
array_y = []
array_z = []
prom_x = 0
prom_y = 0
prom_z = 0
a = 0
test1 = 0
test2 = 0
test3 = 0
alert = 0
cont = 0
cont_1 = 0

def setalert(): #Funcion ql para que no webieara la variable global


	global alert
	alert = 0 

class FirstThread (threading.Thread):

        def run (self):
                while True:
                        if alert == 0 or cont == 20: # Si no hay alerta, o si ya se grabo 20 veces en la bdd se escribe en la bdd
                        	print "TODO BIEN "
                        	cont = 0
                        	setalert()
                        	sleep(2)#Envia datos cada 2 segundos
                        else:	
                        	print "ALERTA ALERTA ALERTA " + str(cont)
                        	cont += 1
                        	sleep(1)#envia datos cada 1 segundo, por 20 segundos cont = 20

# class SecondThread (threading.Thread):
#         def run (self):
#                 while True:
#                         print "Segundo Hilo: " + str(test2)
#                         sleep(1)

f = FirstThread()
f.daemon = True # Daemon se usa para que el proceso muera cuando haga ^C
f.start()

# s = SecondThread()
# s.daemon = True
# s.start()

# def hello_world():
#   threading.Timer(3.0, hello_world).start() # called every minute
#   print("HOLA MUNDO")
# hello_world()
while True: 

	print("Accelerometer data")
	x = int(randint(0, 90))
	y = int(randint(0, 90))
	z = int(randint(0, 90))
	
	array_x.append(x)
	array_y.append(y)
	array_z.append(z)
	
	print("x: " + str(x))
	print("y: " + str(y))
	print("z: " + str(z))

	
	if len(array_x) == 10:
		# prom_x+=1
		test1 = sum(array_x)/len(array_x)
		test2 = sum(array_y)/len(array_y)
		test3 = sum(array_z)/len(array_z)

		print "Promedio X: " + str(sum(array_x)/len(array_x))
		a = str(sum(array_x)/len(array_x))

		print "Promedio Y: " + str(sum(array_y)/len(array_y))	
		b = str(sum(array_y)/len(array_y))		

		print "Promedio Z: " + str(sum(array_z)/len(array_z))
		c = str(sum(array_z)/len(array_z))

		data = {"X":a,"Y":b,"Z":c, "TIMESTAMP": 'Hora: {:%d-%m-%Y %H:%M:%S}'.format(datetime.datetime.now()) }
		json_data = json.dumps(data)

		print json_data

		print ("La varianza es: " + str(np.var(array_x)))

		if np.var(array_x) > 800: #Rango de alerta !
			print "ALARMAAAAAAAaaaaAAAAAAAAAAAAAAAAAAA" #para que se reinicie el contador de tiempo cada vez que haya una alarma	
			cont_1 = 0
			alert = 1
			

		array_x = []
		array_y = []	
		array_z = []

	sleep(0.8)	
	# clear = lambda: os.system('clear')
	# clear()
