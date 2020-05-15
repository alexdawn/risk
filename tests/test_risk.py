import pytest
import logging
import random
import numpy as np

from risk.risk import risk

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

def test_risk(options):
    random.seed(0)
    np.random.seed(0)
    assert risk("Test Game", options) == ('Standard 0', 20)
