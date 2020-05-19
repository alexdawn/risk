import pytest
import logging
import random
import numpy as np

from risk.risk import risk, tournament

from fixture_board import options


def test_risk(options):
    random.seed(0)
    np.random.seed(0)
    assert risk("Test Game", options) == ('Standard 0', 20)


def test_tournament(options):
    random.seed(0)
    np.random.seed(0)
    r = tournament(3, options)
    assert dict(r) == {'Standard 0': {'wins': 2, 'avg_turns': 26.0}, 'Standard 1': {'wins': 1, 'avg_turns': 24.0}}

def test_risk_less_random(options):
    random.seed(0)
    np.random.seed(0)
    options['stocasticity'] = False
    assert risk("Test Game", options) == ('Standard 0', 19)


def test_risk_extra_start(options):
    random.seed(0)
    np.random.seed(0)
    options['extra_start_deployment'] = True
    assert risk("Test Game", options) == ('Standard 0', 15)


def test_risk_bonus_cards(options):
    random.seed(0)
    np.random.seed(0)
    options['bonus_cards'] = 'yes'
    assert risk("Test Game", options) == ('Standard 0', 24)


def test_risk_bonus_cards(options):
    random.seed(0)
    np.random.seed(0)
    options['players'] = 3
    assert risk("Test Game", options) == ('Standard 2', 24)
