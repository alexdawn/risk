import pytest

from risk.board import World, Territory, make_map
from risk.player import Player


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
