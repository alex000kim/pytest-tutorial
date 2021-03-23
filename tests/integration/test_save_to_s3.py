import os
from random import randint

import boto3
import pytest

from src.computer import Computer


@pytest.fixture()
def setup_teardown():
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
    bucket_name = "alexkim-testbucket"
    session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
    s3 = session.client('s3')
    yield computer, fname, session, bucket_name
    s3.delete_object(Bucket=bucket_name, Key=f'computer_objects/{fname}')


def test_save_to_s3(setup_teardown):
    computer, fname, session, bucket_name = setup_teardown
    computer.save_to_s3(fname=fname, s3_dest=bucket_name, boto3_session=session)
    s3_client = session.client('s3')
    resp = s3_client.head_object(Bucket=bucket_name, Key=f'computer_objects/{fname}')
    assert resp['ResponseMetadata']['HTTPStatusCode'] == 200
