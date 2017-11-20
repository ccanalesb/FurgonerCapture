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

def consolidate(user,day)
    print "hola"