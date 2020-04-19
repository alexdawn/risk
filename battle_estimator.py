from typing import Callable, Any
from itertools import product


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


def probable_outcome(
        attackers: int, defenders: int, defender_loses: int) -> float:
    """Probability P(i,j,k) of Defender losing k given i attackers and j defenders"""
    assert attackers >= 1 and attackers <= 4
    assert defenders >= 1 and defenders <= 2
    assert defender_loses >= 0 and defender_loses <= 2
    Attacker = dice(attackers)
    Defender = dice(defenders)
    die = range(1, 7)
    prob = 0
    if attackers == 1 and defenders == 1:
        for y1, z1 in product(*([die] * 2)):
            if y1 > z1 and defender_loses == 1:
                prob += Attacker(y1, None) * Defender(z1, None)
            elif y1 <= z1 and defender_loses == 0:
                prob += Attacker(y1, None) * Defender(z1, None)
    elif attackers == 1:
        for y1, z1, z2 in product(*([die] * 3)):
            if y1 > z1 and defender_loses == 1:
                prob += Attacker(y1, None) * Defender(z1, z2)
            elif y1 <= z1 and defender_loses == 0:
                prob += Attacker(y1, None) * Defender(z1, z2)
    elif defenders == 1:
        for y1, y2, z1 in product(*([die] * 3)):
            if y1 > z1 and defender_loses == 1:
                prob += Attacker(y1, y2) * Defender(z1, None)
            elif y1 <= z1 and defender_loses == 0:
                prob += Attacker(y1, y2) * Defender(z1, None)
    else:
        for y1, y2, z1, z2 in product(*([die] * 4)):
            if y1 > z1 and y2 > z2 and defender_loses == 2:
                prob += Attacker(y1, y2) * Defender(z1, z2)
            elif ((y1 > z1 and y2 <= z2) or (y1 <= z1 and y2 > z2)) and defender_loses == 1:
                x = Attacker(y1, y2) * Defender(z1, z2)
                prob += x
            elif y1 <= z1 and y2 <= z2 and defender_loses == 0:
                prob += Attacker(y1, y2) * Defender(z1, z2)
    return prob


if __name__ == '__main__':
    for i, j, k in product(range(1, 4), range(1, 3), range(0, 3)):
        if k <= i and k <= j:
            print(i, j, k, round(probable_outcome(i, j, k), 3))
