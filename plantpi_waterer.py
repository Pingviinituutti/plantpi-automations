#!/usr/bin/python
# -*- coding:UTF-8 -*-

import RPi.GPIO as GPIO
import time
import signal
import sys


def cleanup(sig, frame):
    print('Exit signal caught!')
    GPIO.cleanup()
    sys.exit(0)


def read_amount_string(amount: str):
    """
        Allowed input units: 'ml' 'dl' 'l'
        Returns the amount in milli litres.
    """
    if not isinstance(amount, str):
        raise TypeError(
            f"Invalid type '{type(amount)}' given to read_amount_string. Type must be 'str'.")
    elif len(amount) < 2:
        raise ValueError(
            f"Invalid string '{amount}' given to read_amount_string.")
    elif 'ml' == amount.lower()[-2:]:
        return round(float(amount.lower().replace('ml', '').replace(',', '.').strip()), 2)
    elif 'dl' == amount.lower()[-2:]:
        return round(float(amount.lower().replace('dl', '').replace(',', '.').strip()) * 100, 2)
    elif 'l' == amount.lower()[-1]:
        return round(float(amount.lower().replace('l', '').replace(',', '.').strip()) * 1000, 2)
    raise ValueError(f"Could not read input string '{amount}'.")


class Waterer():
    relays = []
    flow_speed = 25.5  # millilitres per second

    def __init__(self, relays=None):
        signal.signal(signal.SIGINT, cleanup)
        signal.signal(signal.SIGTERM, cleanup)
        if relays == None:
            # Default gpio pins used in Waveshare's RPi 8 relay board with DIN-mount.
            self.relays = [5, 6, 13, 16, 19, 20, 21, 26]
        else:
            self.relays = relays

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for i in self.relays:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)

    def __enter__(self, relays=None):
        return self

    def pump_duration(self, relay: int, duration: float):
        if relay >= 0 and relay < len(self.relays):
            GPIO.output(self.relays[relay], GPIO.LOW)
            time.sleep(duration)
            GPIO.output(self.relays[relay], GPIO.HIGH)
        else:
            print(self.relays)
            raise IndexError(f"Invalid relay index {relay}")

    def pump_amount(self, relay: int, amount: str):
        duration = read_amount_string(amount) / self.flow_speed
        self.pump_duration(relay, duration)

    def __del__(self):
        GPIO.cleanup()

    def __exit__(self, type, value, tb):
        GPIO.cleanup()
