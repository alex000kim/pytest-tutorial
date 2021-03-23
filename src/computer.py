import os
from datetime import datetime

import joblib


class Computer:
    def __init__(self, price, width, length, height, year_manufactured):
        self.price = price
        self.width = width
        self.length = length
        self.height = height
        self.year_manufactured = year_manufactured

    def __repr__(self):
        return f"Computer(price={self.price}, width={self.width}, length={self.length}, height={self.height}, year_manufactured={self.year_manufactured})"

    def __str__(self):
        return f"Price: ${self.price}. Dimensions: {self.width}x{self.length}x{self.height}"

    def get_years_since_manufactured(self):
        time_now = datetime.now()
        years_since_manufactured = time_now.year - self.year_manufactured
        return years_since_manufactured

    def is_portable(self):
        raise NotImplementedError('is_portable() not implemented. Computer is a parent class')

    def apply_discount(self, amount=None, percentage=None):
        if (amount is not None) and (percentage is not None):
            raise ValueError('To apply discount provide either `amount` or `percentage` values, but not both')
        elif amount is not None:
            if amount >= self.price:
                raise ValueError(
                    f"Can't apply discount of ${amount} because it's great than the current price of ${self.price}")
            self.price = self.price - amount
        elif percentage is not None:
            if (percentage >= 1) or (percentage <= 0):
                raise ValueError(f"Discount percentage must be between 0 and 1. {percentage} provided")
            self.price = self.price * (1 - percentage)

    def save_to_disk(self, fname):
        joblib.dump(self, fname)

    def save_to_s3(self, fname, s3_dest, boto3_session):
        s3_client = boto3_session.client('s3')
        self.save_to_disk(fname)
        s3_client.upload_file(fname, s3_dest, f"computer_objects/{fname}")
        os.remove(fname)

# if __name__ == "__main__":
#     my_comp = Computer(price=1000, width=10, length=10, height=10, year_manufactured=2020)
#     session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
#     my_comp.save_to_s3('my_comp2', 'alexkim-bucket', session)
