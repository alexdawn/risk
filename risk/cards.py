from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from risk.board import World, Territory


class CardDeck:
    SUITS = ["Infantry", "Calvary", "Cannon"]

    def __init__(self, map: 'World') -> None:
        self.cards = set()
        for i, t in enumerate(map.territories):
            self.cards.add(Card(t, CardDeck.SUITS[i % len(CardDeck.SUITS)]))
        for i in range(0):
            self.cards.add(Card(None, "Wildcard"))

    def draw(self) -> 'Card':
        return self.cards.pop()

    def returns(self, cards) -> None:
        self.cards.update(cards)


class Card:
    def __init__(self, territory: 'Territory', suit: str) -> None:
        self.suit = suit
        self.territory = territory
