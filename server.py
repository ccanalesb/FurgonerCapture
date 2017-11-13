from flask import Flask
import json
import os
import configparser
import psutil

app = Flask(__name__)


@app.route('/user/<username>')
def show_user_profile(username):
    config = configparser.ConfigParser()
    config.read('config/FILE.INI', encoding='utf-8-sig')
    # print(config['DEFAULT']['path'])
    config['DEFAULT']['user'] = username  # create
    with open('config/FILE.INI', 'w+') as configfile:    # save
        config.write(configfile)
    return 'User added'

@app.route('/init')
def show_post():
    
    # show the post with the given id, the id is an integer
    return 'init process' 
