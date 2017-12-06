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
day = time.strftime('%A')  # Dia actual a escribir en la bdd

db_data = db.child("School_bus").child(user_ini).child("stadistic").get()

def toHours(timestamp):
    return datetime.datetime.fromtimestamp(
        int(timestamp)
    ).strftime('%H:%M')

def roundTime(dt=None, dateDelta=datetime.timedelta(minutes=1)):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    dateDelta : timedelta object, we round to a multiple of this, default 1 minute.
    Author: Thierry Husson 2012 - Use it as you want but don't blame me.
            Stijn Nevens 2014 - Changed to use only datetime objects as variables
    """
    roundTo = dateDelta.total_seconds()

    if dt == None : dt = datetime.datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo

    datetime_round = dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

    #return time.mktime(datetime.datetime.strptime(datetime_round, "%Y-%m-%d %H:%M:%S").timetuple())
    return time.mktime(datetime_round.timetuple())

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
        consolidate(user,day,stadistic)
    else:
        print "NO CONSOLIDO"

def consolidate(user,day,stadistic):
    stadistics_by_timestamp = db.sort(stadistic, "timestamp")

    reset = False
    time_finish = stadistics_by_timestamp.val()[0]['timestamp'] + 60*15

    acum_x = list()
    acum_y = list()
    acum_z = list()

    object_prom = list()
    acum_list = list()

    for idx, single_stadistic in enumerate(stadistics_by_timestamp.val()):
        if not reset and single_stadistic['timestamp'] > time_finish:
            # do stuff (acumular ultimo, que es el actual, y promediar)
            acum_x.append(int(single_stadistic['X']))
            acum_y.append(int(single_stadistic['Y']))
            acum_z.append(int(single_stadistic['Z']))

            prom_x = float(sum(acum_x)) / len(acum_x)
            prom_y = float(sum(acum_y)) / len(acum_y)
            prom_z = float(sum(acum_z)) / len(acum_z)
            timestamp = single_stadistic['timestamp']

            timestamp_rounded = roundTime(datetime.datetime.fromtimestamp(timestamp),datetime.timedelta(minutes=15))

            acum_list.append({"X": int(prom_x), "Y": int(prom_y), "Z": int(prom_z), "timestamp": timestamp_rounded})

            #print "X: " + str(prom_x)
            #print "Y: " + str(prom_y)
            #print "Z: " + str(prom_z)

            reset = True

        if reset and single_stadistic['timestamp'] > time_finish:
            time_finish = single_stadistic['timestamp'] + 60*15

            acum_x = list()
            acum_y = list()
            acum_z = list()

            object_prom = list()

            reset = False

        if not reset and single_stadistic['timestamp'] < time_finish:
            #do stuff (acumular)
            acum_x.append(int(single_stadistic['X']))
            acum_y.append(int(single_stadistic['Y']))
            acum_z.append(int(single_stadistic['Z']))

            if len(stadistics_by_timestamp.val()) -1 == idx:
                prom_x = float(sum(acum_x)) / len(acum_x)
                prom_y = float(sum(acum_y)) / len(acum_y)
                prom_z = float(sum(acum_z)) / len(acum_z)
                timestamp = single_stadistic['timestamp']

                timestamp_rounded = roundTime(datetime.datetime.fromtimestamp(timestamp),datetime.timedelta(minutes=15))

                if timestamp_rounded == acum_list[-1]["timestamp"]:
                    prom_x = ( (prom_x + acum_list[-1]['X']) / 2 )
                    prom_y = ( (prom_y + acum_list[-1]['Y']) / 2 )
                    prom_z = ( (prom_z + acum_list[-1]['Z']) / 2 )
                    acum_list.append({"X": int(prom_x), "Y": int(prom_y), "Z": int(prom_z), "timestamp": (timestamp_rounded + 60*15)})
                else:
                    acum_list.append({"X": int(prom_x), "Y": int(prom_y), "Z": int(prom_z), "timestamp": timestamp_rounded})

    historic_array = db.child("School_bus").child(user).child("stadistic").child("historic").child(str(day)).get()

    if historic_array.val() is None:
        db.child("School_bus").child(user).child("stadistic").child("historic").child(str(day)).set(acum_list)
    else:
        for single_acum in acum_list:
            find = False
            for idx, single_historic in enumerate(historic_array.val()):
                if toHours(single_historic["timestamp"]) == toHours(single_acum["timestamp"]):
                    prom_x = ( (single_acum['X'] + single_historic['X']) / 2 )
                    prom_y = ( (single_acum['Y'] + single_historic['Y']) / 2 )
                    prom_z = ( (single_acum['Z'] + single_historic['Z']) / 2 )
                    
                    object_historic = {"X": int(prom_x), "Y": int(prom_y), "Z": int(prom_z), "timestamp": single_historic["timestamp"]}                    

                    db.child("School_bus").child(user).child("stadistic").child("historic").child(str(day)).child(idx).set(object_historic)

                    find = True

            if find == False:
                object_historic = {"X": int(single_acum["X"]), "Y": int(single_acum["Y"]), "Z": int(single_acum["Z"]), "timestamp": single_acum["timestamp"]}                    
                historic = historic_array.val()
                historic.append(object_historic)
                db.child("School_bus").child(user).child("stadistic").child("historic").child(str(day)).set(historic)

    db.child("School_bus").child(user).child("stadistic").child("this_week").child(str(day)).remove()

def validate(a,b,c,ts,db_data):
    db_data_temp = db_data.val() # convierte el valor obtenido en tipo entendible de python
    #print db_data_temp
    data = {day: [{"X":a,"Y":b,"Z":c,"timestamp":ts}]}
    #print data
    new_data = dict(db_data_temp.items() + data.items())
    #print new_data
    db.child("School_bus").child(user_ini).child("stadistic").child("this_week").set(new_data)

def add_bdd(a,b,c,ts):
    db_data = db.child("School_bus").child(user_ini).child("stadistic").child("this_week").child(day).get()				
    db_data_temp = db_data.val() # convierte el valor obtenido en tipo entendible de python
    db_data_temp.append({"X":a,"Y":b,"Z":c,"timestamp":ts})
    School_bus = db.child("School_bus").child(user_ini).child("stadistic").child("this_week").child(day).set(db_data_temp)

