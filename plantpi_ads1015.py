#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
#  From https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15/blob/main/examples/ads1x15_simpletest.py
# But slightly modified to be used as a class

# The ADS1015 and ADS1115 both have the same gain options.
#
#       GAIN    RANGE (V)
#       ----    ---------
#        2/3    +/- 6.144
#          1    +/- 4.096
#          2    +/- 2.048
#          4    +/- 1.024
#          8    +/- 0.512
#         16    +/- 0.256

import time
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS1015():
    def __init__(self, gain):
        if gain in [2/3, 1, 2, 4, 8, 16]:
            self.gain = gain
        else:
            print("Invalid gain received.")
            print("Valid values are 2/3, 1, 2, 4 and 8. Defaulting to 1.")
        self.chan0 = None
        self.chan1 = None
        self.chan2 = None
        self.chan3 = None

    def __enter__(self):
        # Create the I2C bus
        self.i2c = busio.I2C(board.SCL, board.SDA)

        # Create the ADC object using the I2C bus
        self.ads = ADS.ADS1015(self.i2c)

        self.ads.gain = self.gain

        # Create single-ended input on channel 0
        self.chan0 = AnalogIn(self.ads, ADS.P0)
        self.chan1 = AnalogIn(self.ads, ADS.P1)
        self.chan2 = AnalogIn(self.ads, ADS.P2)
        self.chan3 = AnalogIn(self.ads, ADS.P3)
        return self

    def __exit__(self, type, value, tb):
        pass


if __name__ == '__main__':
    ads1015 = ADS1015(gain=2/3)

    print("Sampling all analog channels with an ADS1015.")
    print(f"Gain: {'2/3' if ads1015.gain < 1 else ads1015.gain}\n")

    print(f"{'chan':>5}\t{'A0':<5}\t{'chan':>5}\t"
          + f"{'A1':<5}\t{'chan':>5}\t"
          + f"{'A2':<5}\t{'chan':>5}\t"
          + f"{'A3':<5}"
          )
    print("{:>5}\t{:>5}\t".format('raw', 'v') * 4)
    with ads1015 as s:
        while True:
            print(f"{s.chan0.value:>5}\t{s.chan0.voltage:>5.3f}\t"
                  + f"{s.chan1.value:>5}\t{s.chan1.voltage:>5.3f}\t"
                  + f"{s.chan2.value:>5}\t{s.chan2.voltage:>5.3f}\t"
                  + f"{s.chan3.value:>5}\t{s.chan3.voltage:>5.3f}\t"
                  )
            time.sleep(0.5)
