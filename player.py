import random
import rules

class Player:
    def __init__(self, name):
        self.name = name
        self.in_game = True
        self.cards = []
    def __repr__(self):
        return self.name

    def remove_first_match(self, type):
        for i in range(len(self.cards)):
            card = self.cards[i]
            if card.suit == type:
                self.cards.remove(card)
                return card

    def check_cards(self, map, armies):
        if (any(card.suit == "Infantry" for card in self.cards) and
            any(card.suit == "Cavalry" for card in self.cards) and
            any(card.suit == "Cannon" for card in self.cards)):
            return [self.remove_first_match("Infantry"), self.remove_first_match("Cavalry"), self.remove_first_match("Cannon")], 12
        elif sum(1 for card in self.cards if card.suit == "Infantry") >= 3:
            return [self.remove_first_match("Infantry"), self.remove_first_match("Infantry"), self.remove_first_match("Infantry")], 6
        elif sum(1 for card in self.cards if card.suit == "Cavalry") >= 3:
            return [self.remove_first_match("Cavalry"), self.remove_first_match("Cavalry"), self.remove_first_match("Cavalry")], 8
        elif sum(1 for card in self.cards if card.suit == "Cannon") >= 3:
            return [self.remove_first_match("Cannon"), self.remove_first_match("Cannon"), self.remove_first_match("Cannon")], 10
        else:
            return None, 0
    def deploy(self, map, armies):
        """The player deployment logic"""
        own = [territory for territory in map.territories if territory.owner == self and any(n for n in map.get_neighbours(territory) if n.owner != self)]
        map.add_armies(own[random.randint(0, len(own)) - 1], armies)

    def take_card(self, card):
        """Add card to the players hand"""
        self.cards.append(card)

    def attacks(self, map):
        """Declare list of attacks"""
        attacks = []
        for territory in map.territories:
            if territory.owner is self and territory.armies > 1:
                for neighbour in map.get_neighbours(territory):
                    if neighbour.owner is not self:
                        attacks.append((territory, neighbour))
        return attacks

    def attack_continue(self, map, territory_from, territory_to):
        """Ask player if they wish to continue"""
        return territory_from.armies > 1

    def attack_commit(self, map, territory_from, territory_to):
        """Ask player number of armies to commit to attack"""
        return min(territory_from.armies - 1, rules.MAX_ATTACK)

    def attack_move(self, map, territory_from, territory_to):
        return territory_from.armies - 1

    def attack_success(self, map, territory_from, territory_to):
        """Allow player to adapt plan"""
        pass

    def attack_fail(self, map,territory_from, territory_to):
        """Allow player to adapt plan"""
        pass

def make_players(count):
    assert count > 2
    players = []
    for i in range(count):
        players.append(Player("Player {}".format(i + 1)))
    return players