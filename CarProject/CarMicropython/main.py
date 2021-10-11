# Default template for XBee MicroPython projects
import json

import xbee as xbee
import machine
from machine import Pin, PWM
from time import sleep_ms

LEVEL_CONTROL_CLUSTER = 0x0008

pin = machine.Pin('D4', machine.Pin.OUT)

car_enabled = False


def get_car_enbaled_val():
    return car_enabled


def set_car_enabled_val(car_local):
    car_enabled = car_local


class LevelControlClusterSteering:
    p30 = machine.Pin('D3', Pin.OUT)
    p31 = machine.Pin('D6', Pin.OUT)
    pwm7 = machine.PWM(Pin('P0'))

    currentLevel = 0x01
    remaining_time = 0

    def receive_command(self, msg):
        command_frame = json.loads(msg['payload'])
        command = command_frame['commandIdentifier']
        if command == '0x00':
            # Move to level
            level = command_frame['payload']['level']
            transition_time = command_frame['payload']['transitionTime']
            if get_car_enbaled_val():
                self.move_to_level(level, transition_time)
        if command == '0x01':
            # Move
            move_mode = command_frame['payload']['moveMode']
            rate = command_frame['payload']['rate']
            if get_car_enbaled_val():
                self.move(move_mode, rate)
        if command == '0x02':
            # Step
            step_mode = command_frame['payload']['stepMode']
            step_size = command_frame['payload']['stepSize']
            transition_time = command_frame['payload']['transitionTime']
            if get_car_enbaled_val():
                self.step(step_mode, step_size, transition_time)
        if command == '0x03':
            # Stop
            set_car_enabled_val(False)
        """
            ############### With ON/OFF ######################
        """
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
            set_car_enabled_val(False)

    def move_to_level(self, level, transition_time):

        if transition_time == 0xffff or transition_time == 0:
            self.currentLevel = level
            self.set_motor_to_level(level)
        else:
            each_step = (level - self.currentLevel) / transition_time / 10
            self.remaining_time = transition_time
            while abs(self.currentLevel - level) > 0.1:
                self.currentLevel += each_step
                self.set_motor_to_level(self.currentLevel)
                self.remaining_time -= 0.1
                sleep_ms(100)

    def move(self, move_mode, rate):
        UP = 0x00
        DOWN = 0x01
        level = 0

        if move_mode == UP:
            level = 1
        elif move_mode == DOWN:
            level = -1

        difference = abs(self.currentLevel - level)
        transition_time = difference / rate

        self.move_to_level(level, transition_time)

    def set_motor_to_level(self, level):

        if level == 1:
            self.p30.value(0)
            self.p31.value(1)
        elif level == -1:
            self.p30.value(1)
            self.p31.value(0)
        else:
            self.p30.value(0)
            self.p31.value(0)

        self.pwm7.duty(100)

    def step(self, step_mode, step_size, transition_time):
        UP = 0x00
        DOWN = 0x01
        level = 0

        if step_mode == UP:
            level = self.currentLevel + step_size
        elif step_mode == DOWN:
            level = self.currentLevel - step_size

        if level > 1:
            level = 1
        elif level < -1:
            level = -1

        self.move_to_level(level, transition_time)


class LevelControlClusterDriving:
    p32 = machine.Pin('D0', Pin.OUT)
    p33 = machine.Pin('D1', Pin.OUT)
    pwm8 = machine.PWM(Pin('P1'))

    currentLevel = 0
    remaining_time = 0

    def receive_command(self, msg):
        command_frame = json.loads(msg['payload'])
        command = command_frame['commandIdentifier']
        if command == '0x00':
            # Move to level
            level = command_frame['payload']['level']
            transition_time = command_frame['payload']['transitionTime']
            if get_car_enbaled_val():
                self.move_to_level(level, transition_time)
        if command == '0x01':
            # Move
            move_mode = command_frame['payload']['moveMode']
            rate = command_frame['payload']['rate']
            if get_car_enbaled_val():
                self.move(move_mode, rate)
        if command == '0x02':
            # Step
            step_mode = command_frame['payload']['stepMode']
            step_size = command_frame['payload']['stepSize']
            transition_time = command_frame['payload']['transitionTime']
            if get_car_enbaled_val():
                self.step(step_mode, step_size, transition_time)
        if command == '0x03':
            # Stop
            set_car_enabled_val(False)

        """
            ############### With ON/OFF ######################
        """
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
            set_car_enabled_val(False)

    def move_to_level(self, level, transition_time):
        if transition_time == 0:
            self.currentLevel = level
            self.set_motor_to_level(level)
        else:
            each_step = (level - self.currentLevel) / transition_time / 10
            self.remaining_time = transition_time
            while abs(self.currentLevel - level) > 0.1:
                self.currentLevel += each_step
                self.set_motor_to_level(self.currentLevel)
                self.remaining_time -= 0.1
                sleep_ms(100)

    def set_motor_to_level(self, level):
        if level > 0:
            self.p32.value(0)
            self.p33.value(1)
        else:
            self.p32.value(1)
            self.p33.value(0)

        speed = abs((1023 / 100) * level)
        self.pwm8.duty(speed)

    def move(self, move_mode, rate):
        UP = 0x00
        DOWN = 0x01
        level = 0

        if move_mode == UP:
            level = 100
        elif move_mode == DOWN:
            level = -100

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

        if level > 100:
            level = 100
        elif level < -100:
            level = -100

        self.move_to_level(level, transition_time)


levelControlClusterSteering = LevelControlClusterSteering()
levelControlClusterDriving = LevelControlClusterDriving()


def getLevelControlCluster(endpoint):
    if endpoint == 0xE8:
        return levelControlClusterSteering
    if endpoint == 0xE9:
        return levelControlClusterDriving



while True:
    msg = xbee.receive()
    if msg:
        if msg['cluster'] == LEVEL_CONTROL_CLUSTER:
            print(msg)
            getLevelControlCluster(msg['dest_ep']).receive_command(msg)

