import pytest
from risk.board import make_map
from risk.cards import CardDeck, Card

@pytest.fixture
def full_map():
    return make_map()


def test_card_deck(full_map):
    deck = CardDeck(full_map)
    assert len(deck.cards) == len(full_map.territories)

