from typing import Callable, Any, Tuple, Dict, List
from itertools import product, chain
from functools import lru_cache
import warnings
import numpy as np

from scipy.sparse import csc_matrix
from scipy.sparse import identity
from scipy.sparse.linalg import inv

warnings.filterwarnings('ignore')  # scipy generates tons of errors

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
    """Use the approriate probability distribution for number of dice"""
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


def generate_states(A: int, D: int)\
        -> Tuple[Dict[Tuple[int, int], int], Dict[Tuple[int, int], int]]:
    """"Generate all the possible transient and outcome states from the initial state"""
    transient_state = [
        (a, d) for a, d in product(range(1, A + 1), range(1, D + 1))
    ]
    absorbing_state = [
        (a, d) for a, d in chain(zip([0] * D, range(1, D + 1)), zip(range(1, A + 1), [0] * A))
    ]
    return transient_state, absorbing_state


def generate_prob_matrix(A: int, D: int)\
        -> Tuple[Dict[Tuple[int, int], int], Dict[Tuple[int, int], int], np.ndarray]:
    """Generate the probability outcome matrix"""
    transient_state, absorbing_state = generate_states(A, D)
    transient_state_lookup = {s: i for i, s in enumerate(transient_state)}
    absorbing_state_lookup = {s: i for i, s in enumerate(absorbing_state)}
    transient_length, absorbing_length = len(transient_state), len(absorbing_state)
    # Add probability to transition elements
    Qrow = []
    Qcol = []
    Qdata = []
    Rrow = []
    Rcol = []
    Rdata = []
    for i, (a, d) in enumerate(transient_state):
        max_deaths = 2 if a > 1 and d > 1 else 1
        for dl in range(0, max_deaths + 1):
            al = max_deaths - dl
            na, nd = a - al, d - dl
            if a - al > 0 and d - dl > 0:
                Qrow.append(i)
                Qcol.append(transient_state_lookup[(na, nd)])
                Qdata.append(probable_outcome(min(a, 3), min(d, 2), dl))
            else:
                Rrow.append(i)
                Rcol.append(absorbing_state_lookup[(na, nd)])
                Rdata.append(probable_outcome(min(a, 3), min(d, 2), dl))
    Q = csc_matrix((Qdata, (Qrow, Qcol)), shape=(transient_length, transient_length))
    R = csc_matrix((Rdata, (Rrow, Rcol)), shape=(transient_length, absorbing_length))
    iden = identity(transient_length)
    F = inv(iden - Q) * R
    return transient_state_lookup, absorbing_state_lookup, F


def filter_states(states, probs):
    """Filter invalid states"""
    reverse_states = {y: x for x, y in states.items()}
    new_states, new_probs = tuple(
        zip(*list((reverse_states[i], prob) for i, prob in enumerate(probs) if prob > 0)))
    return new_states, new_probs


def get_matrix_row(F, row: int):
    if len(F.shape) > 1:
        return F[row][:].toarray()[0]
    else:
        return F


def wrap_probabilities()\
        -> Callable[[int, int], Tuple[Dict[Tuple[int, int], int], np.ndarray]]:
    """Avoids generating probability matrix if a larger one already exists"""
    F = []  # type: List[List[int]]
    transient_state_lookup = {}  # type: Dict[Tuple[int, int], int]
    absorbing_state_lookup = {}  # type: Dict[Tuple[int, int], int]

    def get_prob(a: int, d: int) -> Tuple[Dict[Tuple[int, int], int], np.ndarray]:
        nonlocal F, transient_state_lookup, absorbing_state_lookup
        if (a, d) in transient_state_lookup.keys():
            return filter_states(
                absorbing_state_lookup, get_matrix_row(F, transient_state_lookup[(a, d)]))
        else:
            transient_state_lookup, absorbing_state_lookup, F = generate_prob_matrix(a, d)
            return filter_states(absorbing_state_lookup, get_matrix_row(F, -1))
    return get_prob


# Need a smarter way of doing this?
get_cached_probabilities = wrap_probabilities()


@lru_cache()
def calculate_win_prob(a: int, d: int) -> float:
    _, probs = get_cached_probabilities(a, d)
    return sum(probs[d:])


@lru_cache()
def calculate_expected_remainder(a: int, d: int) -> Tuple[float, float, float, float]:
    """Calculated Expectations and Standard Deviations from a Battle"""
    states, probs = get_cached_probabilities(a, d)
    ea = sum(a * p for (a, d), p in zip(states, probs))
    ed = sum(d * p for (a, d), p in zip(states, probs))
    va = sum(p * pow(a - ea, 2) for (a, d), p in zip(states, probs))
    vd = sum(p * pow(d - ed, 2) for (a, d), p in zip(states, probs))
    return ea, va, ed, vd


def generate_outcome(a: int, d: int, repeats: int = 1) -> List[Tuple[int, int]]:
    """Run a battle using the matrix instead of simulated dice"""
    states, probs = get_cached_probabilities(a, d)
    return [states[x] for x in np.random.choice(range(len(states)), repeats, p=probs)]
