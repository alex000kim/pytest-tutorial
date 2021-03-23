from src.computer import Computer


class LaptopComputer(Computer):
  def __init__(self, price, width, length, height, year_manufactured, display_size, battery_capacity):
    super().__init__(price, width, length, height, year_manufactured)
    self.display_size = display_size
    self.battery_capacity = battery_capacity

  def is_portable(self):
    return True

  def get_hours_one_charge(self):
    return int(self.battery_capacity/(50*self.display_size))