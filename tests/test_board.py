import pytest

from risk.board import World, Territory, make_map
from risk.player import Player

from fixture_board import test_scenario


@pytest.fixture
def full_map():
    return make_map()


@pytest.fixture
def two_players():
    return [Player(i, str(i)) for i in range(2)]


def test_make_map(full_map):
    assert type(full_map) == World


def test_world(full_map, two_players):
    clone = full_map.make_copy()
    assert type(clone) == World
    assert str(clone.territories) == str(full_map.territories)
    alaska = full_map.get_territory("Alaska")
    kamchatka = full_map.get_territory("Kamchatka")
    assert alaska.name == "Alaska"
    neighbours = full_map.get_neighbours(alaska)
    assert len(neighbours) == 3
    assert kamchatka in neighbours
    full_map.add_armies(alaska, 5)
    assert alaska.armies == 5
    full_map.move_armies(alaska, kamchatka, 3)
    assert alaska.armies == 2
    full_map.remove_armies(alaska, 2)
    full_map.remove_armies(kamchatka, 1000) #far too high
    assert alaska.armies == 0
    assert kamchatka.armies == 0
    assert all(t.owner == None for t in full_map.territories)
    full_map.allocate_territories(two_players)
    assert all(t.owner in two_players for t in full_map.territories)
    # both players should have some number of territories
    assert (full_map.count_territories(two_players[1]) - full_map.count_territories(two_players[0])) == 0
    for t in full_map.territories:
        if t.continent == 'Oceania':
            t.set_owner(two_players[0])
    assert full_map.calculate_contienent(two_players[0], 'Oceania') == 2
    assert full_map.calculate_contienent(two_players[1], 'Oceania') == 0
    assert full_map.count_continents(two_players[0]) >= 2


def test_count_territories(test_scenario):
    map, players = test_scenario
    assert map.count_territories(players[0]) == 1
    assert map.count_territories(players[1]) == 2

def test_territory():
    test_territory = Territory(0, "Fooland", "Baz", (0, 0), [])
    assert str(test_territory) == "Fooland"
    assert test_territory.get_coordinates() == "0,0!"
    test_territory.set_armies(5)
    assert test_territory.armies == 5
    with pytest.raises(AssertionError):
        test_territory.set_armies(-5)
