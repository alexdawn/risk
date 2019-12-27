class Card_Deck:
    SUITS = set(["Infantry", "Calvary", "Cannon"])
    def __init__(self, map):
        self.cards = set()
        for t in map.territories:
            self.cards.add(Card(t, "Infantry"))

    def draw(self):
        return self.cards.pop()

    def returns(self, cards):
        self.cards.update(cards)


class Card:
    def __init__(self, territory, suit):
        self.suit = suit
        self.territory = territory