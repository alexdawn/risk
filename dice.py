import random

def roll_die():
    return random.randrange(1, 6)

def roll_dice(number):
    return [roll_die() for i in range(number)]