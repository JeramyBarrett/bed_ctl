#!/usr/bin/python3

from bottle import route, run, static_file, template
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from enum import Enum
from threading import Thread
from time import sleep

class motorCtl:
    class state(Enum):
        movingUp = 1
        movingDown = 2
        idle = 3

    def __init__(self, pinUp, pinDown, pinPosition):
        self._moveUp = DigitalOutputDevice(pinUp)
        self._moveDown = DigitalOutputDevice(pinDown)
        positionInput = DigitalInputDevice(pinPosition, pull_up=True)
        positionInput.when_activated = self._positionEdge

        self._moveUp.off()
        self._moveDown.off()

        self._inMotion = False
        self._edgeDetected = False
        self._position = 0
        self._state = self.state.idle

        self._motionDetectThread = Thread(target=self._motionDetect, args=())
        self._motionDetectThread.daemon = True
        self._motionDetectThread.start()

    def __del__(self):
        pass

    def upStart(self):
        if self._state != self.state.idle:
            return
        
        self._state = self.state.movingUp
        self._moveUp.on()

    def upStop(self):
        if self._state != self.state.movingUp:
            return

        self._state = self.state.idle
        self._moveUp.off()

    def downStart(self):
        if self._state != self.state.idle:
            return
        
        self._state = self.state.movingDown
        self._moveDown.on()

    def downStop(self):
        if self._state != self.state.movingDown:
            return

        self._state = self.state.idle
        self._moveDown.off()

    def getPosition(self):
        return self._position

    def _motionDetect(self):
        while True:
            # Still in motion
            if self._inMotion == True & self._edgeDetected == True:
                self._edgeDetected = False

            # Just started moving
            elif self._inMotion == False & self._edgeDetected == True:
                self._inMotion = True
                self._edgeDetected = False

            # Stopped moving
            elif self._inMotion == True & self._edgeDetected == False:
                self._inMotion = False

            sleep(0.5)

    def _positionEdge(self):
        print("Edge Detected")
        if self._state == self.state.movingUp:
            self._position += 1
        elif self._state == self.state.movingDown & self._position > 0:
            self._position -= 1

        self._edgeDetected = True
        self._inMotion = True

    def inMotion(self):
        return self._inMotion


@route('/')
def index():
    return static_file('index.htm', root='/home/pi/bed_ctl')

@route('/headUpStart')
def headUpStart():
    rightHead.upStart()
    leftHead.upStart()
    return

@route('/headUpStop')
def headUpStop():
    rightHead.upStop()
    leftHead.upStop()
    return

@route('/headDownStart')
def headDownStart():
    rightHead.downStart()
    leftHead.downStart()
    return

@route('/headDownStop')
def headDownStop():
    rightHead.downStop()
    leftHead.downStop()
    return

@route('/footUpStart')
def footUpStart():
    rightFoot.upStart()
    leftFoot.upStart()
    return

@route('/footUpStop')
def footUpStop():
    rightFoot.upStop()
    leftFoot.upStop()
    return

@route('/footDownStart')
def footDownStart():
    rightFoot.downStart()
    leftFoot.downStart()
    return

@route('/footDownStop')
def footDownStop():
    rightFoot.downStop()
    leftFoot.downStop()
    return

positionFormat = "<p style=\"text-align: center; font-size: xx-large\">{{val}}</p>"

@route('/headPos')
def headPos():
    return template(positionFormat, val=rightHead.getPosition())

@route('/footPos')
def footPos():
    return template(positionFormat, val=rightFoot.getPosition())

leftHead = motorCtl(17, 27, 14)
leftFoot = motorCtl(4, 18, 15)
rightHead = motorCtl(6, 16, 7)
rightFoot = motorCtl(8, 12, 5)

run(host='0.0.0.0', port=80, debug=False)

del leftHead
del leftFoot
del rightHead
del rightFoot