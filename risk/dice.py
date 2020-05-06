import numpy as np


def roll_dice(number):
    return np.random.randint(1, 7, size=number)
