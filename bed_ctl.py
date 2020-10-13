#!/usr/bin/python3

#from flask import Flask
#app = Flask(__name__)


#@app.route('/')
#def hello_world():
#    return 'Hello World!'

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80)
#    print("Running")

from bottle import route, run, template, static_file
from gpiozero import LED



@route('/')
def index():
    return static_file('index.htm', root='/home/pi/bed_ctl')

@route('/headUpEn')
def headUpEn():
    headUp.on()

    return

@route('/headUpDis')
def headUpDis():
    headUp.off()

    return

headUp = LED(17)


run(host='0.0.0.0', port=80)
