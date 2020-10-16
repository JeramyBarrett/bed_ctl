#!/usr/bin/python3

from bottle import route, run, static_file, template
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from enum import Enum

class buttonState(Enum):
    up = 1
    down = 2
    none = 3

headPosVal = 0
footPosVal = 0
headState = buttonState.none
footState = buttonState.none

@route('/')
def index():
    return static_file('index.htm', root='/home/pi/bed_ctl')

@route('/headUpOn')
def headUpOn():
    global headState
    if headState != buttonState.none:
        return
    
    headState = buttonState.up
    headUpGPIO_A.on()
    headUpGPIO_B.on()
    return

@route('/headUpOff')
def headUpOff():
    global headState
    if headState != buttonState.up:
        return

    headState = buttonState.none
    headUpGPIO_A.off()
    headUpGPIO_B.off()
    return

@route('/headDownOn')
def headDownOn():
    global headState
    if headState != buttonState.none:
        return

    headState = buttonState.down
    headDownGPIO_A.on()
    headDownGPIO_B.on()
    return

@route('/headDownOff')
def headDownOff():
    global headState
    if headState != buttonState.down:
        return

    headState = buttonState.none
    headDownGPIO_A.off()
    headDownGPIO_B.off()
    return

@route('/footUpOn')
def footUpOn():
    global footState
    if footState != buttonState.none:
        return

    footState = buttonState.up
    footUpGPIO_A.on()
    footUpGPIO_B.on()
    return

@route('/footUpOff')
def footUpOff():
    global footState
    if footState != buttonState.up:
        return

    footState = buttonState.none
    footUpGPIO_A.off()
    footUpGPIO_B.off()
    return

@route('/footDownOn')
def footDownOn():
    global footState
    if footState != buttonState.none:
        return

    footState = buttonState.down
    footDownGPIO_A.on()
    footDownGPIO_B.on()
    return

@route('/footDownOff')
def footDownOff():
    global footState
    if footState != buttonState.down:
        return

    footState = buttonState.none
    footDownGPIO_A.off()
    footDownGPIO_B.off()
    return

positionFormat = "<p style=\"text-align: center; font-size: xx-large\">{{val}}</p>"

@route('/headPos')
def headPos():
    global positionFormat
    return template(positionFormat, val=headPosVal)

@route('/footPos')
def footPos():
    global positionFormat
    return template(positionFormat, val=footPosVal)

def headPosChange(self):
    global headPosVal, headState

    if headState == buttonState.up:
        headPosVal += 1
    elif (headState == buttonState.down) & (headPosVal > 0):
        headPosVal -= 1

def footPosChange(self):
    global footPosVal, footState
    if footState == buttonState.up:
        footPosVal += 1
    elif (footState == buttonState.down) & (footPosVal > 0):
        footPosVal -= 1



headUpGPIO_A = DigitalOutputDevice(17)
headDownGPIO_A = DigitalOutputDevice(27)
footUpGPIO_A = DigitalOutputDevice(4)
footDownGPIO_A = DigitalOutputDevice(18)

headUpGPIO_B = DigitalOutputDevice(6)
headDownGPIO_B = DigitalOutputDevice(16)
footUpGPIO_B = DigitalOutputDevice(8)
footDownGPIO_B = DigitalOutputDevice(12)

headPosIn = DigitalInputDevice(14, pull_up=True)
footPosIn = DigitalInputDevice(15, pull_up=True)

headPosIn.when_activated = headPosChange
footPosIn.when_activated = footPosChange

run(host='0.0.0.0', port=80, debug=False)
