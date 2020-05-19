import pytest
import logging

from risk.board import World, Territory, make_map
from risk.player import Player


@pytest.fixture
def options():
    return {
    'players': 2,
    'stocasticity': True,  # False does not roll dice
    'markov': False,  # If True replaces simulated dice roll with the probable outcomes
    'initial_placement': 'random',  # random|pick
    'deployment': 'blob',  # blob|free|spread
    'extra_start_deployment': False,
    'attack_limit': None,  # None for no limit
    'death_or_glory': True,  # Cannot withdraw after commiting
    'end_of_turn_slide': False,
    'bonus_cards': 'none',  # none|fixed|yes
    'plot_gameplay': False,  # if True generate graphviz plots in ./output for each turn
    'logging_level': logging.CRITICAL
    }


@pytest.fixture
def test_scenario():
    p1, p2 = (Player(i, "Player {}".format(i)) for i in range(2))
    map = make_map()
    t1 = map.get_territory("Eastern Australia")
    t2 = map.get_territory("Western Australia")
    t3 = map.get_territory("New Guinea")
    map.set_owner(t1, p1).add_armies(t1, 5)
    map.set_owner(t2, p2).set_armies(t2, 1)
    map.set_owner(t3, p2).set_armies(t3, 2)
    return map, [p1, p2]


@pytest.fixture
def test_scenario_with_player():
    def add_player(p1: 'Player'):
        p2 = Player(1, "Player 2")
        map = make_map()
        t1 = map.get_territory("Eastern Australia")
        t2 = map.get_territory("Western Australia")
        t3 = map.get_territory("New Guinea")
        map.set_owner(t1, p1).add_armies(t1, 5)
        map.set_owner(t2, p2).set_armies(t2, 1)
        map.set_owner(t3, p2).set_armies(t3, 2)
        return map
    return add_player
