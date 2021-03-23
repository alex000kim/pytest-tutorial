import os
from datetime import datetime
from glob import glob
from random import randint

import boto3
import pytest
from botocore.exceptions import ClientError
from moto import mock_s3

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
    for f in glob("test_computer_*"):
        os.remove(f)


def test_repr(setup_teardown):
    computer, price, width, length, height, year_manufactured, _ = setup_teardown
    assert repr(
        computer) == f"Computer(price={price}, width={width}, length={length}, height={height}, year_manufactured={year_manufactured})"


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

@pytest.mark.parametrize("discount_percentage", [0.1, 0.5, 0.9])
def test_apply_discount_percentage(setup_teardown, discount_percentage):
    computer, price, *_ = setup_teardown
    computer.apply_discount(percentage=discount_percentage)
    assert computer.price == price * (1 - discount_percentage)


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
    computer, *_, object_id = setup_teardown
    computer.save_to_disk(str(f"test_computer_{object_id}"))
    assert os.path.isfile(str(f"test_computer_{object_id}"))


@pytest.fixture()
def setup_teardown_s3_mock():
    price = randint(500, 5000)
    width = randint(2, 20)
    length = randint(2, 20)
    height = randint(2, 20)
    year_manufactured = randint(2000, 2020)
    computer = Computer(price=price,
                        width=width,
                        length=length,
                        height=height,
                        year_manufactured=year_manufactured)
    fname = "test_computer"
    bucket_name = "test-bucket"
    with mock_s3():
        session = boto3.Session(region_name='us-east-1')
        s3client = session.client('s3')
        s3client.create_bucket(Bucket=bucket_name)
        yield computer, fname, session, bucket_name


def test_save_to_s3_mock(setup_teardown_s3_mock):
    computer, fname, session, bucket_name = setup_teardown_s3_mock
    computer.save_to_s3(fname=fname, s3_dest=bucket_name, boto3_session=session)
    s3_client = session.client('s3')
    resp = s3_client.head_object(Bucket=bucket_name, Key=f'computer_objects/{fname}')
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200


def test_save_to_s3_raises_mock(setup_teardown_s3_mock):
    computer, fname, session, bucket_name = setup_teardown_s3_mock
    computer.save_to_s3(fname=fname, s3_dest=bucket_name, boto3_session=session)
    s3_client = session.client('s3')
    with pytest.raises(ClientError):
        s3_client.head_object(Bucket=bucket_name, Key=f'INVALID/{fname}')
