# Default template for XBee MicroPython projects
import json

import xbee as xbee
import machine
from umachine import I2C
from xbee import atcmd
from time import sleep_ms

ON_OFF_CLUSTER = 0x0006
LEVEL_CONTROL_CLUSTER = 0x0008

pin = machine.Pin('D4', machine.Pin.OUT)


class Cluster:
    OnOffCluster = None
    LevelControlCluster = None

    def __init__(self, color):
        self.OnOffCluster = OnOffCluster(color)
        self.LevelControlCluster = LevelControlCluster(color)


class OnOffCluster:
    onOff = False
    color = ""

    def __init__(self, color):
        self.color = color

    def receive_command(self, msg):
        command = json.loads(msg['payload'])['commandIdentifier']

        if command == '0x00':
            # Off
            self.onOff = False
            self.set_led(self.onOff)
        elif command == '0x01':
            # On
            self.onOff = True
            self.set_led(self.onOff)
        elif command == '0x02':
            # Toggle
            self.onOff = not self.onOff
            self.set_led(self.onOff)

    def set_led(self, on):
        if self.color == 'user':
            if on:
                pin.value(0)
            else:
                pin.value(1)
        else:
            if on:
                sendToArduino(self.color + ":255")
            else:
                sendToArduino(self.color + ":1")


class LevelControlCluster:
    # A value of 0x00 shall not be used.
    # A value of 0x01 shall indicate the minimum light level that can be attained on a device.
    # A value of 0xfe shall indicate the maximum light level that can be attained on a device.
    # A value of 0xff shall represent an undefined value.
    currentLevel = 0x01
    remaining_time = 0
    color = ""
    stop = False

    def __init__(self, color):
        self.color = color

    def receive_command(self, msg):
        command_frame = json.loads(msg['payload'])
        command = command_frame['commandIdentifier']
        if command == '0x00':
            # Move to level
            level = command_frame['payload']['level']
            transition_time = command_frame['payload']['transitionTime']
            if self.currentLevel != 0x01:
                self.move_to_level(level, transition_time)
        if command == '0x01':
            # Move
            move_mode = command_frame['payload']['moveMode']
            rate = command_frame['payload']['rate']
            if self.currentLevel != 0x01:
                self.move(move_mode, rate)
        if command == '0x02':
            # Step
            step_mode = command_frame['payload']['stepMode']
            step_size = command_frame['payload']['stepSize']
            transition_time = command_frame['payload']['transitionTime']
            if self.currentLevel != 0x01:
                self.step(step_mode, step_size, transition_time)
        if command == '0x03':
            # Stop
            self.stop = True
        if command == '0x04':
            # Move to level (with on /off)
            level = command_frame['payload']['level']
            transition_time = command_frame['payload']['transitionTime']
            self.move_to_level(level, transition_time)
        if command == '0x05':
            # Move (with on / off)
            move_mode = command_frame['payload']['moveMode']
            rate = command_frame['payload']['rate']
            self.move(move_mode, rate)
        if command == '0x06':
            # Step (with on / off)
            step_mode = command_frame['payload']['stepMode']
            step_size = command_frame['payload']['stepSize']
            transition_time = command_frame['payload']['transitionTime']
            self.step(step_mode, step_size, transition_time)
        if command == '0x07':
            # Stop (with on/off)
            self.stop = True

    def move_to_level(self, level, transition_time):
        if transition_time == 0xffff or transition_time == 0:
            self.currentLevel = level
            self.set_led_to_level(level)
        else:
            each_step = (level - self.currentLevel) / transition_time / 10
            self.remaining_time = transition_time
            while abs(self.currentLevel - level) > 0.1 and not self.stop:
                self.currentLevel += each_step
                self.set_led_to_level(self.currentLevel)
                self.remaining_time -= 0.1
                sleep_ms(100)

            self.stop = False

    def set_led_to_level(self, level):
        sendToArduino(self.color + ":" + str(level))

    def move(self, move_mode, rate):
        UP = 0x00
        DOWN = 0x01
        level = 0

        if move_mode == UP:
            level = 0xfe
        elif move_mode == DOWN:
            level = 0x01

        difference = abs(self.currentLevel - level)
        transition_time = difference / rate

        self.move_to_level(level, transition_time)

    def step(self, step_mode, step_size, transition_time):
        UP = 0x00
        DOWN = 0x01
        level = 0

        if step_mode == UP:
            level = self.currentLevel + step_size
        elif step_mode == DOWN:
            level = self.currentLevel - step_size

        if level > 0xfe:
            level = 0xfe
        elif level < 0x01:
            level = 0x01

        self.move_to_level(level, transition_time)


redLight = Cluster("red")
greenLight = Cluster("green")
blueLight = Cluster("blue")
userLight = Cluster("user")

i2c = I2C(id=1, freq=400000)


def sendToArduino(command):
    try:
        i2c.writeto(8, bytearray(command))
    except:
        print("nö")


def getLightCluster(endpoint):
    if endpoint == 0xE8:
        return redLight
    if endpoint == 0xE9:
        return greenLight
    if endpoint == 0xEA:
        return blueLight
    if endpoint == 0xEB:
        return userLight


while True:
    msg = xbee.receive()
    if msg:
        cluster = getLightCluster(msg['dest_ep'])
        if msg['cluster'] == ON_OFF_CLUSTER:
            print(msg)
            cluster.OnOffCluster.receive_command(msg)
        if msg['cluster'] == LEVEL_CONTROL_CLUSTER:
            print(msg)
            cluster.LevelControlCluster.receive_command(msg)
