import pytest
import random
from risk.board import make_map
from risk.cards import CardDeck, Card

@pytest.fixture
def full_map():
    return make_map()


def test_card_deck(full_map):
    random.seed(0)
    deck = CardDeck(full_map)
    assert len(deck.cards) == len(full_map.territories)
    assert deck.draw() == Card(full_map.get_territory("Congo"), "Infantry")
