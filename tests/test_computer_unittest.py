import os
import unittest
from datetime import datetime
from random import randint
from glob import glob
from src.computer import Computer


# In terminal (from project directory): export PYTHONPATH="$(pwd)"
class TestComputer(unittest.TestCase):
    def setUp(self):
        self.price = randint(500, 5000)
        self.width = randint(2, 20)
        self.length = randint(2, 20)
        self.height = randint(2, 20)
        self.year_manufactured = randint(2000, 2020)
        self.object_id = 1 #randint(0, 1000)
        self.computer = Computer(price=self.price,
                                 width=self.width,
                                 length=self.length,
                                 height=self.height,
                                 year_manufactured=self.year_manufactured)

    def tearDown(self):
        for f in glob("save_computer*"):
            os.remove(f)

    def test_repr(self):
        self.assertEqual(repr(self.computer),
                         f"Computer(price={self.price}, width={self.width}, length={self.length}, "
                         f"height={self.height}, year_manufactured={self.year_manufactured})")

    def test_str(self):
        self.assertEqual(str(self.computer),
                         f"Price: ${self.price}. Dimensions: {self.width}x{self.length}x{self.height}")

    def test_get_years_since_manufactured(self):
        self.assertEqual(self.computer.get_years_since_manufactured(), datetime.now().year - self.year_manufactured)

    def test_is_portable(self):
        with self.assertRaises(NotImplementedError):
            self.computer.is_portable()

    def test_save_to_disk(self):
        self.computer.save_to_disk(str(f"save_computer_{self.object_id}"))
        self.assertTrue(os.path.isfile(str(f"save_computer_{self.object_id}")))


if __name__ == '__main__':
    unittest.main()