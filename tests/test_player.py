import pytest

from risk.player import Player


def test_player():
    player = Player(0, "Test")
    assert str(player)
    with pytest.raises(NotImplementedError):
        player.remove_first_match("Infantry")
    with pytest.raises(NotImplementedError):
        player.check_cards(None, 0)
    with pytest.raises(NotImplementedError):
        player.deploy(None, 0)
    with pytest.raises(NotImplementedError):
        player.take_card(None)
    with pytest.raises(NotImplementedError):
        player.attacks(None, {})
    with pytest.raises(NotImplementedError):
        player.attack_continue(None, None, None)
    with pytest.raises(NotImplementedError):
        player.attack_commit(None, None, None)
    with pytest.raises(NotImplementedError):
        player.attack_move(None, None, None)
