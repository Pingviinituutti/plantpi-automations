import unittest
from plantpi_waterer import read_amount_string


class TestReadAmountString(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(ValueError):
            read_amount_string('')

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            read_amount_string(2)
        with self.assertRaises(TypeError):
            read_amount_string([2])
        with self.assertRaises(TypeError):
            read_amount_string(2.0)

    def test_invalid_strings(self):
        with self.assertRaises(ValueError):
            read_amount_string('')
        with self.assertRaises(ValueError):
            read_amount_string('50')
        with self.assertRaises(ValueError):
            read_amount_string('invalid string')

    def test_ml(self):
        self.assertEqual(read_amount_string('50ml'), 50)
        self.assertEqual(read_amount_string('350.2 ml'), 350.2)

    def test_dl(self):
        self.assertEqual(read_amount_string('2dl'), 200)
        self.assertEqual(read_amount_string('1.5 dl'), 150)
        self.assertEqual(read_amount_string('0.22 dl'), 22)
        self.assertEqual(read_amount_string('.1342 dl'), 13.42)

    def test_l(self):
        self.assertEqual(read_amount_string('0.2l'), 200)
        self.assertEqual(read_amount_string('1.5 l'), 1500)
        self.assertEqual(read_amount_string('.25 l'), 250)


if __name__ == '__main__':
    unittest.main()
