from flask import Flask
import json
import os
import configparser
import psutil
import firebase
app = Flask(__name__)
child_proc_id = None
command_route = None

@app.route('/user/<username>')
def setup_driver(username):
    config = configparser.ConfigParser()
    config.read('config/FILE.INI', encoding='utf-8-sig')
    # print(config['DEFAULT']['path'])
    config['DEFAULT']['user'] = username  # create
    with open('config/FILE.INI', 'w+') as configfile:    # save
        config.write(configfile)
    return 'User added'

@app.route('/init_journey')
def init_journey():
    p = psutil.Popen([os.getcwd()+"/furgoner/bin/python", os.getcwd() +
                      '/test.py'], shell=False)
    command_route = p.cmdline()
    child_proc_id = p.pid
    return 'init journey' 


@app.route('/terminate_journey')
def terminate_journey():
    for process in psutil.process_iter():
        if process.cmdline() == command_route:
            process.terminate()
            break
    return 'Stopping journey'


@app.route('/test')
def test():
    print firebase.check_date()
    return 'Stopping journey'
