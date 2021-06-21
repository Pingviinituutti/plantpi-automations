#!/usr/bin/python
# -*- coding:UTF-8 -*-

import RPi.GPIO as GPIO
import time

Relay = [5, 6, 13, 16, 19, 20, 21, 26]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(0,3):
    GPIO.setup(Relay[i], GPIO.OUT)
    GPIO.output(Relay[i], GPIO.HIGH)

GPIO.output(Relay[1], GPIO.LOW)
time.sleep(8)
GPIO.output(Relay[1], GPIO.HIGH)

GPIO.cleanup()


