import os
import pytest
from datetime import datetime
from random import randint
from glob import glob
from src.computer import Computer

@pytest.fixture()
def setup_teardown():
	price = randint(500, 5000)
	width = randint(2, 20)
	length = randint(2, 20)
	height = randint(2, 20)
	year_manufactured = randint(2000, 2020)
	object_id = randint(0, 1000)
	computer = Computer(price=price,
		width=width,
		length=length,
		height=height,
		year_manufactured=year_manufactured)
	yield computer, price, width, length, height, year_manufactured, object_id
	for f in glob("save_computer*"):
		os.remove(f)

def test_repr(setup_teardown):
	computer, price, width, length, height, year_manufactured, _ = setup_teardown
	assert repr(computer) == f"Computer(price={price}, width={width}, length={length}, height={height}, year_manufactured={year_manufactured})"

def test_str(setup_teardown):
	computer, price, width, length, height, year_manufactured, _ = setup_teardown
	assert str(computer) == f"Price: ${price}. Dimensions: {width}x{length}x{height}"

def test_get_years_since_manufactured(setup_teardown):
	computer, price, width, length, height, year_manufactured, _ = setup_teardown
	assert computer.get_years_since_manufactured() == (datetime.now().year - year_manufactured)

def test_is_portable(setup_teardown):
	computer, *_ = setup_teardown
	with pytest.raises(NotImplementedError):
		computer.is_portable()

def test_apply_discount_amount(setup_teardown):
	computer, price, *_ = setup_teardown
	discount_amount = 100
	computer.apply_discount(amount=discount_amount)
	assert computer.price == price - discount_amount

def test_apply_discount_amount(setup_teardown):
	computer, price, *_ = setup_teardown
	discount_percentage = 0.3
	computer.apply_discount(percentage=discount_percentage)
	assert computer.price == price*(1-discount_percentage)

def test_apply_discount_exception(setup_teardown):
	computer, *_ = setup_teardown
	discount_amount = 10000
	discount_percentage = 1.3

	with pytest.raises(ValueError):
		computer.apply_discount(amount=discount_amount, percentage=discount_percentage)

	with pytest.raises(ValueError):
		computer.apply_discount(amount=discount_amount)

	with pytest.raises(ValueError):
		computer.apply_discount(percentage=discount_percentage)

def test_save_to_disk(setup_teardown):
	computer, *_,  object_id= setup_teardown
	computer.save_to_disk(str(f"save_computer_{object_id}"))
	assert os.path.isfile(str(f"save_computer_{object_id}"))