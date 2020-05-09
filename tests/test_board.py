from risk.board import World, Territory, make_map


def test_make_map():
    result = make_map()
    assert type(result) == World
