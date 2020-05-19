from risk.agents import Pacifist, Passive, Standard, Aggresive, Greedy, Human

from fixture_board import test_scenario, test_scenario_with_player, options


def test_pacifist(test_scenario_with_player):
    player = Pacifist(0, "Pacifist")
    map = test_scenario_with_player(player)
    assert len(player.attacks(map, {})) == 1


def test_passive(test_scenario_with_player):
    player = Passive(0, "Passive")
    map = test_scenario_with_player(player)
    assert player.attacks(map, {}) == []


def test_standard(test_scenario_with_player):
    player = Standard(0, "Standard")
    map = test_scenario_with_player(player)
    assert player.attacks(map, {})


def test_aggresive(test_scenario_with_player):
    player = Aggresive(0, "Aggresive")
    map = test_scenario_with_player(player)
    assert len(player.attacks(map, {})) == 2


def test_greedy(test_scenario_with_player, options):
    player = Greedy(0, "Greedy")
    map = test_scenario_with_player(player)
    assert player.attacks(map, options)


def test_human(test_scenario_with_player):
    assert Human(0, "Human")
