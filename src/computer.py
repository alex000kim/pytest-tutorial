import joblib
from datetime import datetime


class Computer:
    # initilizer or constructor
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
                raise ValueError(f"Can't apply discount of ${amount} because it's great than the current price of ${self.price}")
            self.price = self.price - amount
        elif percentage is not None:
            if (percentage >= 1) or (percentage <= 0) :
                raise ValueError(f"Discount percentage must be between 0 and 1. {percentage} provided")
            self.price = self.price*(1-percentage)

    def save_to_disk(self, fname):
        joblib.dump(self, fname)