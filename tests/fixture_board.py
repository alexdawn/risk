import pytest

from risk.board import World, Territory, make_map
from risk.player import Player


@pytest.fixture
def test_scenario():
    p1, p2 = (Player(i, str(i)) for i in range(2))
    map = make_map()
    map.get_territory("Eastern Australia").set_owner(p1).set_armies(5)
    map.get_territory("Western Australia").set_owner(p2).set_armies(1)
    map.get_territory("New Guinea").set_owner(p2).set_armies(2)
    return map, (p1, p2)
