import numpy as np
from typing import Callable, Any
from itertools import product, chain
from functools import lru_cache

from scipy.sparse import csr_matrix
from scipy.sparse.linalg import inv


def probY(y1: int, y2: int = None) -> float:
    """Probability top two of 3 ordered dice Y1=y1 and Y2=y2"""
    assert y1 > 0 and y1 <= 7
    assert y2 > 0 and y2 <= 7
    if y2:
        if y1 == y2:
            return (3 * y1 - 2) / 216
        elif y1 > y2:
            return (6 * y2 - 3) / 216
        else:
            return 0
    else:
        return 1 - 3 * y1 + 3 * pow(y1, 2) / 216


def probZ(z1: int, z2: int = None) -> float:
    """Probability of two ordered dice Z1=z1 and Z2=2z"""
    assert z1 > 0 and z1 <= 7
    assert z2 > 0 and z2 <= 7
    if z2:
        if z1 == z2:
            return 1 / 36
        elif z1 > z2:
            return 2 / 36
        else:
            return 0
    else:
        return (2 * z1 - 1) / 36


def probSingle(x: int, _: None) -> float:
    """Probability of Dice X=x"""
    return 1 / 6


def dice(dice: int) -> Callable[[Any, Any], float]:
    functions = {
        1: probSingle,
        2: probZ,
        3: probY
    }
    return functions[dice]


@lru_cache()
def probable_outcome(
        attackers: int, defenders: int, defender_loses: int) -> float:
    """Probability P(i,j,k) of Defender losing k given i attackers and j defenders"""
    assert attackers >= 1 and attackers <= 4, "Invalid attackers {}".format(attackers)
    assert defenders >= 1 and defenders <= 2, "Invalid defenders {}".format(defenders)
    assert defender_loses >= 0 and defender_loses <= 2, "Invalid losers {}".format(defender_loses)
    Attacker = dice(attackers)
    Defender = dice(defenders)
    die = range(1, 7)
    prob = 0
    if attackers == 1 and defenders == 1:
        for y1, z1 in product(*([die] * 2)):
            if (y1 > z1 and defender_loses == 1) or (y1 <= z1 and defender_loses == 0):
                prob += Attacker(y1, None) * Defender(z1, None)
    elif attackers == 1:
        for y1, z1, z2 in product(*([die] * 3)):
            if (y1 > z1 and defender_loses == 1) or (y1 <= z1 and defender_loses == 0):
                prob += Attacker(y1, None) * Defender(z1, z2)
    elif defenders == 1:
        for y1, y2, z1 in product(*([die] * 3)):
            if (y1 > z1 and defender_loses == 1) or (y1 <= z1 and defender_loses == 0):
                prob += Attacker(y1, y2) * Defender(z1, None)
    else:
        for y1, y2, z1, z2 in product(*([die] * 4)):
            if ((y1 > z1 and y2 > z2 and defender_loses == 2) or
                    (((y1 > z1 and y2 <= z2) or (y1 <= z1 and y2 > z2)) and defender_loses == 1) or
                    (y1 <= z1 and y2 <= z2 and defender_loses == 0)):
                prob += Attacker(y1, y2) * Defender(z1, z2)
    return prob


def probability_win(A, D):
    # Generate possible states
    transient_state = [
        (a, d) for a, d in product(range(1, A + 1), range(1, D + 1))
    ]
    absorbing_state = [
        (a, d) for a, d in chain(zip([0] * D, range(1, D + 1)), zip(range(1, A + 1), [0] * A))
    ]
    states = transient_state + absorbing_state
    state_lookup = {s: i for i, s in enumerate(states)}
    state_size = len(states)

    # Add probability to transition elements
    row = []
    col = []
    data = []
    for i, (a, d) in enumerate(states):
        if a > 0 and d > 0:
            max_deaths = 2 if a > 1 and d > 1 else 1
            for dl in range(0, max_deaths + 1):
                al = max_deaths - dl
                row.append(i)
                col.append(state_lookup[(a - al, d - dl)])
                data.append(probable_outcome(min(a, 3), min(d, 2), dl))
        else:
            row.append(i)
            col.append(i)
            data.append(1)
    A = csr_matrix((data, (row, col)), shape=(state_size, state_size))
    print(A)


probability_win(30, 30)
