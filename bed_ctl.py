#!/usr/bin/python3

from bottle import route, run, template, static_file
from gpiozero import LED



@route('/')
def index():
    return static_file('index.htm', root='/home/pi/bed_ctl')

@route('/headUpOn')
def headUpOn():
    headUpGPIO_A.on()
    headUpGPIO_B.on()
    return

@route('/headUpOff')
def headUpOff():
    headUpGPIO_A.off()
    headUpGPIO_B.off()
    return

@route('/headDownOn')
def headDownOn():
    headDownGPIO_A.on()
    headDownGPIO_B.on()
    return

@route('/headDownOff')
def headDownOff():
    headDownGPIO_A.off()
    headDownGPIO_B.off()
    return

@route('/footUpOn')
def footUpOn():
    footUpGPIO_A.on()
    footUpGPIO_B.on()
    return

@route('/footUpOff')
def footUpOff():
    footUpGPIO_A.off()
    footUpGPIO_B.off()
    return

@route('/footDownOn')
def headUpfootDownOnDis():
    footDownGPIO_A.on()
    footDownGPIO_B.on()
    return

@route('/footDownOff')
def footDownOff():
    footDownGPIO_A.off()
    footDownGPIO_B.off()
    return


headUpGPIO_A = LED(17)
headDownGPIO_A = LED(27)
footUpGPIO_A = LED(4)
footDownGPIO_A = LED(18)

headUpGPIO_B = LED(6)
headDownGPIO_B = LED(16)
footUpGPIO_B = LED(8)
footDownGPIO_B = LED(12)


run(host='0.0.0.0', port=80)
