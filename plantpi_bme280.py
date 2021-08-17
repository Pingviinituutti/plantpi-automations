#!/usr/bin/python
# -*- coding:UTF-8 -*-
import time
from datetime import datetime, timezone
from gpiozero import DigitalOutputDevice

# https://pypi.org/project/RPi.bme280/
import smbus2
import bme280


class BME280():
    def __init__(self, port=1, address=0x76, pin=24):
        self.port = port
        self.address = address
        self.bme280_pwr = DigitalOutputDevice(pin)
        self.bus = None
        self.data = None
        self.calibration_params = None

    def __enter__(self):
        # turn on the BME280 sensor only when its metrics should be read
        # And in this case, only when used with a `with` statement
        self.bme280_pwr.on()
        time.sleep(.1)
        return self

    def measure(self):
        self.bus = smbus2.SMBus(self.port)
        for i in range(5):
            try:
                self.calibration_params = bme280.load_calibration_params(
                    self.bus, self.address)
                self.data = bme280.sample(
                    self.bus, self.address, self.calibration_params)
            except OSError:
                print("Could not read bme280 through i2c. Trying soon again...")
                time.sleep(.2)
            else:
                break

        if (self.data is None):
            print("Could not read bme280 through i2c.")
        else:
            # Set the timestamp with python's datetime
            # Just so that we get consistent datetimes with  measurements with other devices
            now = datetime.now(timezone.utc)
            self.data.timestamp = now

    def __exit__(self, type, value, tb):
        self.bme280_pwr.off()
        return self


if __name__ == '__main__':
    print("Measuring environment temperature, pressure and humidity with a BME280.\n")
    data = None
    bme = BME280()
    with bme:
        bme.measure()
    data = bme.data
    if (data is None):
        print("Could not read bme280 through i2c.")
    else:
        print(f"BME280 timestamp: {data.timestamp}")
        print(f"BME280 temperature: {data.temperature}")
        print(f"BME280 pressure: {data.pressure}")
        print(f"BME280 humidity: {data.humidity}")
