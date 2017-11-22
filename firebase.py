import pyrebase
import configparser
import datetime
import time
import json
config = {
    "apiKey": "AIzaSyAtLq-HbsgKKhJWD8HC2EaWV2FMQMeSfJc",
    "authDomain": "test-8c400.firebaseapp.com",
    "databaseURL": "https://test-8c400.firebaseio.com",
    "storageBucket": "projectId.appspot.com",
    "serviceAccount": "config/serviceAccountKey.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

config = configparser.ConfigParser()
config.read('config/FILE.INI', encoding='utf-8-sig')
user_ini = config['DEFAULT']['user']
day = time.strftime('%A')#Dia actual a escribir en la bdd

def check_date():
    config = configparser.ConfigParser()
    config.read('config/FILE.INI', encoding='utf-8-sig')
    user = config['DEFAULT']['user']
    ts = int(time.time())
    day = time.strftime("%A", time.localtime(ts))
    stadistic = db.child("School_bus").child(user).child("stadistic").child("this_week").child(str(day)).get()
    data = stadistic.val()[0]
    if data is None:
        return None
    delta = datetime.date.fromtimestamp(
        ts) - datetime.date.fromtimestamp(data['timestamp'])
    if delta.days > 7:
        print "CONSOLIDOOOOOOO"
    else:
        print "NO CONSOLIDO"

def consolidate(user,day):
    print "hola"

def validate(a,b,c,ts,db_data):
    db_data_temp = db_data.val() # convierte el valor obtenido en tipo entendible de python
    print db_data_temp
    data = {day: [{"X":a,"Y":b,"Z":c,"timestamp":ts}]}
    print data
    new_data = dict(db_data_temp.items() + data.items())
    print new_data
    db.child("School_bus").child(user_ini).child("stadistic").child("this_week").set(new_data)

def add_bdd(a,b,c,ts):
    db_data = db.child("School_bus").child(user_ini).child("stadistic").child("this_week").child(day).get()				
    db_data_temp = db_data.val() # convierte el valor obtenido en tipo entendible de python
    db_data_temp.append({"X":a,"Y":b,"Z":c,"timestamp":ts})
    School_bus = db.child("School_bus").child(user_ini).child("stadistic").child("this_week").child(day).set(db_data_temp)
    
    