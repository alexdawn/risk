import numpy as np
from risk.dice import roll_dice


def test_roll_dice():
    for i in range(10):
        results = roll_dice(i)
        assert len(results) == i
        assert all([r > 0 and r < 7 for r in results])


def test_seed():
    np.random.seed(0)
    assert list(roll_dice(3)) == [5, 6, 1]
