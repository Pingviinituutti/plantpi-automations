import datetime
import unittest
from plantpi_bme280 import BME280


class TestBME280(unittest.TestCase):

    def test_with(self):
        bme280 = BME280()
        with bme280:
            pass
        self.assertIsNone(bme280.data)

    def test_measure(self):
        bme280 = BME280()
        with bme280:
            bme280.measure()

        self.assertIsInstance(bme280.data.timestamp, datetime.datetime)
        self.assertIsInstance(bme280.data.temperature, float)
        self.assertIsInstance(bme280.data.humidity, float)
        self.assertIsInstance(bme280.data.pressure, float)


if __name__ == '__main__':
    unittest.main()
