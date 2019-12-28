class Card_Deck:
    SUITS = ["Infantry", "Calvary", "Cannon"]
    def __init__(self, map):
        self.cards = set()
        for i, t in enumerate(map.territories):
            self.cards.add(Card(t, Card_Deck.SUITS[i % len(Card_Deck.SUITS)]))
        for i in range(0):
            self.cards.add(Card(None, "Wildcard"))

    def draw(self):
        return self.cards.pop()

    def returns(self, cards):
        self.cards.update(cards)


class Card:
    def __init__(self, territory, suit):
        self.suit = suit
        self.territory = territory