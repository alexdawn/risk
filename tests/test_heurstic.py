from risk.heuristic import border_threat, border_security_ratio, heuristic

from fixture_board import test_scenario

def test_border_threat(test_scenario):
    map, players = test_scenario
    assert border_threat(map, map.get_territory("Eastern Australia")) == 3

def test_border_security_ratio(test_scenario):
    map, players = test_scenario
    assert border_security_ratio(map, map.get_territory("Eastern Australia")) == 3 / 5


def test_heurstic(test_scenario):
    map, players = test_scenario
    assert heuristic(map, players[0]) == (3 / 5) + 2
