import logging
import random
import pytest
import numpy as np

from risk.cards import CardDeck, Card
from risk.rules import (
    summary, check_players, active_players, combat, slide, draw_card, attack)

from fixture_board import test_scenario, options


def test_summary(caplog, test_scenario):
    map, players = test_scenario
    caplog.set_level(logging.INFO)
    logging.info("foo")
    summary(map)
    # not capturing log for some reason?
    # assert "\{'Player 1': 1, 'Player 2': 2\}" in caplog.text


def test_check_players(test_scenario):
    map, players = test_scenario
    check_players(map, players)
    for player in players:
        assert player.in_game


def test_active_players(test_scenario):
    map, players = test_scenario
    assert active_players(players) == 2
    map.set_owner(map.get_territory("Eastern Australia"), players[1])
    check_players(map, players)
    assert active_players(players) == 1


def test_attack(test_scenario, options):
    np.random.seed(0)
    map, players = test_scenario
    t1 = map.get_territory("Eastern Australia")
    t2 = map.get_territory("Western Australia")
    players[0].attack_commit = lambda x, y, z: 4  # monkey patch in four commited attackers
    players[0].attack_move = lambda x, y, z: y.armies - 1  # move all armies in
    assert attack(map, players[0], options, t1, t2) == True
    # Check the attack was a success
    assert t2.owner == players[0]
    assert t2.armies == 4

def test_combat_fixed():
    assert combat(3, 1, {'stocasticity': False}) == (1, 1)
    assert combat(3, 2, {'stocasticity': False}) == (2, 2)


def test_combat():
    np.random.seed(0)  # Use seed to keep same outcome
    assert combat(3, 2, {'stocasticity': True}) == (2, 0)
    assert combat(3, 2, {'stocasticity': True}) == (1, 1)


def test_slide(test_scenario):
    map, players = test_scenario
    slide(map, players[0])


def test_draw_card(test_scenario):
    random.seed(0)
    map, players = test_scenario
    deck = CardDeck(map)
    assert draw_card(deck) == Card(map.get_territory("South Africa"), "Infantry")
