#!/usr/bin/python3

from bottle import route, run, static_file, template
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from enum import Enum
from threading import Thread
from time import sleep

class motorCtl:
    class buttonState(Enum):
        up = 1
        down = 2
        idle = 3

    class motorState(Enum):
        idle = 1
        buttonInput = 2
        awatingEdge = 3
        edge = 4

    def __init__(self, pinUp, pinDown, pinEncoder):
        self._encoderPosition = 0
        self._buttonState = self.buttonState.idle
        self._motorState = self.motorState.idle

        # __io = DigitalInputDevice(pinEncoder, pull_up=True)
        # __io.when_activated = self._encoderEdge
        self._moveUp = DigitalOutputDevice(pinUp)
        self._moveDown = DigitalOutputDevice(pinDown)

        self._moveUp.off()
        self._moveDown.off()

        self._motionDetectThread = Thread(target=self._motionDetect, args=())
        self._motionDetectThread.daemon = True
        self._motionDetectThread.start()

    def __del__(self):
        pass

    def upStart(self):
        if self._buttonState != self.buttonState.idle:
            return
        
        self._buttonState = self.buttonState.up
        self._moveUp.on()
        self._motorState = self.motorState.buttonInput

    def upStop(self):
        if self._buttonState != self.buttonState.up:
            return

        self._buttonState = self.buttonState.idle
        self._moveUp.off()

    def downStart(self):
        if self._buttonState != self.buttonState.idle:
            return
        
        self._buttonState = self.buttonState.down
        self._moveDown.on()
        self._motorState = self.motorState.buttonInput

    def downStop(self):
        if self._buttonState != self.buttonState.down:
            return

        self._buttonState = self.buttonState.idle
        self._moveDown.off()

    def getPosition(self):
        return self._encoderPosition

    def _motionDetect(self):
        while True:
            if self._motorState == self.motorState.idle:
                continue

            elif self._motorState == self.motorState.buttonInput:
                self._motorState = self.motorState.awatingEdge

            elif self._motorState == self.motorState.awatingEdge:
                if self._buttonState == self.buttonState.down:
                    print("Down Stopped")
                    self.downStop()

                if self._buttonState == self.buttonState.up:
                    print("Up Stopped")
                    self.upStop()

                self._motorState = self.motorState.idle

            elif self._motorState == self.motorState.edge:
                self._motorState = self.motorState.awatingEdge

            sleep(1)

    def _encoderEdge(self):
        if self._buttonState == self.buttonState.up:
            self._encoderPosition += 1
        elif (self._buttonState == self.buttonState.down) & (self._encoderPosition > 0):
            self._encoderPosition -= 1

        self._motorState = self.motorState.edge

    def inMotion(self):
        return False

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

@route('/allDownRun')
def allDownRun():
    rightHead.downStart()
    rightFoot.downStart()
    leftHead.downStart()
    leftFoot.downStart()
    return

positionFormat = "<p style=\"text-align: center; font-size: xx-large\">{{val}}</p>"

@route('/headPos')
def headPos():
    return template(positionFormat, val=leftHead.getPosition())

@route('/footPos')
def footPos():
    return template(positionFormat, val=leftFoot.getPosition())

def _leftHeadEdge():
    # print("Left Head Edge")
    leftHead._encoderEdge()

def _leftFootEdge():
    # print("Left Foot Edge")
    leftFoot._encoderEdge()

def _rightHeadEdge():
    # print("Right Head Edge")
    rightHead._encoderEdge()

def _rightFootEdge():
    # print("Right Foot Edge")
    rightFoot._encoderEdge()

lh = DigitalInputDevice(14, pull_up=True)
lh.when_activated = _leftHeadEdge
lf = DigitalInputDevice(15, pull_up=True)
lf.when_activated = _leftFootEdge
rh = DigitalInputDevice(7, pull_up=True)
rh.when_activated = _rightHeadEdge
rf = DigitalInputDevice(5, pull_up=True)
rf.when_activated = _rightFootEdge

leftHead = motorCtl(17, 27, 14)
leftFoot = motorCtl(4, 18, 15)
rightHead = motorCtl(6, 16, 7)
rightFoot = motorCtl(8, 12, 5)

run(host='0.0.0.0', port=80, debug=False)

del leftHead
del leftFoot
del rightHead
del rightFoot