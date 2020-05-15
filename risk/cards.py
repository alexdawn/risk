import random
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing import List, Optional
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
        c = random.choice(sorted(list(self.cards)))
        self.cards.remove(c)
        return c

    def returns(self, cards: 'List[Card]') -> None:
        self.cards.update(cards)


class Card:
    def __init__(self, territory: 'Optional[Territory]', suit: str) -> None:
        self.suit = suit
        self.territory = territory

    def __lt__(self, other: 'Card') -> Any:
        # WIldcards ranked least
        return self.territory < other.territory if self.territory else True

    def __repr__(self) -> str:
        return str((self.suit, self.territory))

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other: Any) -> bool:
        return self.suit == other.suit and self.territory == self.territory
