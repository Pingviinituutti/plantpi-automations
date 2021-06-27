import unittest
from plantpi_waterer import Waterer
import time


class TestReadAmountString(unittest.TestCase):

    def test_waterer_ml(self):
        waterer = Waterer([5, 6])
        waterer.pump_amount(0, '10ml')

    def test_waterer_dl(self):
        waterer = Waterer([5, 6])
        waterer.pump_amount(0, '0.05 dl')
        time.sleep(.2)

    def test_with_waterer(self):
        with Waterer() as waterer:
            waterer.pump_amount(0, '5ml')
        time.sleep(.2)


if __name__ == '__main__':
    unittest.main()
