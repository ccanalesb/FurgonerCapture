#!/usr/bin/env python
"""Released under the MIT License
Copyright 2015, 2016 MrTijn/Tijndagamer
"""

from mpu6050 import mpu6050
from time import sleep,clock
import os
from random import randint
import numpy as np #PARA SACAR VARIANZA
import threading
import datetime
import time
import json
import configparser
import pyrebase
from firebase import validate,add_bdd,db_data

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

ts = time.time()#timestamp
day = time.strftime('%A')#Dia actual a escribir en la bdd

sensor = mpu6050(0x68)

def setalert(): #Funcion ql para que no webieara la variable global
	global alert
	alert = 0 

def setdb_data_val():
	global db_data_val
	db_data = db.child("School_bus").child(user_ini).child("stadistic").get()
	db_data_val = db_data.val()

class FirstThread (threading.Thread):

	def run (self):
		cont = 0
		while True:
				print "Entre al hilo..."
				if alert == 0 or cont == 20: # Si no hay alerta, o si ya se grabo 20 veces en la bdd se escribe en la bdd
					if a == 0:
						print "No hay datos"
						sleep(10)
					else:	
						setdb_data_val()
						if "this_week" not in db_data_val:#En el caso de que no este creado el hijo "this_week por X motivo en la BDD"
							validate(a,b,c,ts,db_data)#Funcion que verifica que exista el child y luego lo agrega
							print "CREO THIS_WEEK Y AGREGO "
							cont = 0
							setalert()
							sleep(10)#Envia datos cada 2 segundos
						else:
							db_data = db.child("School_bus").child(user_ini).child("stadistic").child("this_week").get()
							if day in db_data.val(): 
								add_bdd(a,b,c,ts) #Funcion que agrega elemento a bdd
								print "TODO BIEN "
								cont = 0
								setalert()
								sleep(10)#Envia datos cada 10 segundos
							else:
								validate(a,b,c,ts,db_data)
								print "CREO DIA Y AGREGO"
								cont = 0
								setalert()
								sleep(10)#Envia datos cada 10 segundos
				else:	
					print "ALERTA ALERTA ALERTA " + str(cont+1)
					cont += 1
					add_bdd(x,y,z,ts)
					sleep(1)

f = FirstThread()
f.daemon = True # Daemon se usa para que el proceso muera cuando haga ^C
f.start()

config = configparser.ConfigParser()
config.read('config/FILE.INI', encoding='utf-8-sig')
user_ini = config['DEFAULT']['user']

config = {
  "apiKey": "AIzaSyAtLq-HbsgKKhJWD8HC2EaWV2FMQMeSfJc",
  "authDomain": "test-8c400.firebaseapp.com",
  "databaseURL": "https://test-8c400.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "config/serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

user = auth.sign_in_with_email_and_password("admin@admin.cl", "adminadmin")

db = firebase.database()
if user == None:
	print "No hay usuario"
else:
	
	data_old =""
	my_prom = [] 
	while True:
		accel_data = sensor.get_accel_data()
		# gyro_data = sensor.get_gyro_data()
		temp = sensor.get_temp()

		print("Accelerometer data")
		x=(int(accel_data['x']))
		y=(int(accel_data['y']))
		z=(int(accel_data['z']))

		print("x: " + str(int(accel_data['x'])))
		print("y: " + str(int(accel_data['y'])))
		print("z: " + str(int(accel_data['z'])))

		array_x.append(x)
		array_y.append(y)
		array_z.append(z)

		if len(array_x) == 10:
			test1 = sum(array_x)/len(array_x)
			test2 = sum(array_y)/len(array_y)
			test3 = sum(array_z)/len(array_z)

			print "Promedio X: " + str(sum(array_x)/len(array_x))
			a = str(sum(array_x)/len(array_x))

			print "Promedio Y: " + str(sum(array_y)/len(array_y))	
			b = str(sum(array_y)/len(array_y))		

			print "Promedio Z: " + str(sum(array_z)/len(array_z))
			c = str(sum(array_z)/len(array_z))

			print ("La varianza es: " + str(np.var(array_x)))

			if np.var(array_x) > 900: #Rango de alerta !
				print "ALARMAAAAAAAaaaaAAAAAAAAAAAAAAAAAAA" #para que se reinicie el contador de tiempo cada vez que haya una alarma	
				cont_1 = 0
				alert = 1
				
			array_x = []
			array_y = []	
			array_z = []
		# print("Gyroscope data")
		# print("x: " + str(int(gyro_data['x'])))
		# print("y: " + str(int(gyro_data['y'])))
		# print("z: " + str(int(gyro_data['z'])))

		print("Temp: " + str(temp) + " C")
		sleep(0.1)  
		# clear = lambda: os.system('clear')
		# clear()
