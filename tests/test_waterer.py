import unittest
from plantpi_waterer import Waterer
import time


class TestPump(unittest.TestCase):

    def test_waterer_pump(self):
        with Waterer() as waterer:
            waterer.pump(0, '5ml')
            time.sleep(.2)
            waterer.pump(0, .1)

    def test_waterer_ml(self):
        with Waterer() as waterer:
            waterer.pump_amount(0, '10ml')

    def test_waterer_dl(self):
        with Waterer([5, 6]) as waterer:
            waterer.pump_amount(0, '0.05 dl')
        time.sleep(.2)

    def test_with_waterer(self):
        with Waterer() as waterer:
            waterer.pump_amount(0, '5ml')
        time.sleep(.2)


if __name__ == '__main__':
    unittest.main()
