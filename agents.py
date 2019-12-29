import random
import logging

import rules
from board import Terrority
from player import Player

class Human(Player):
    def __init__(self, name):
        super().__init__(name)
    def __repr__(self):
        return super().__repr__()

    def check_cards(self, map, armies):
        """Check cards and hand in some if desired"""
        raise NotImplementedError()
    
    def deploy(self, map, armies):
        """The player deployment logic"""
        id = None
        while not id or map.territories[id].owner not in (self, None):
            if id:
                logging.info("You don't own that territory")
            id = input("You get {} armies, where do you wish to deploy?".format(armies))
            id = int(id)
        map.add_armies(map.territories[id], armies)

    def take_card(self, card):
        """Add card to the players hand"""
        input("Take Card {}".format(card))
        self.cards.append(card)

    def attacks(self, map):
        """Declare list of attacks"""
        base, to = None, None
        while ((not base or map.territories[base].owner != self) or
               (not to or map.territories[to].owner in (self, None))):
            if base and to:
                logging.info("Invalid base and/or target")
            result = input("Input your attack both base and target (x, x)")
            if result:
                base, to = [int(x) for x in result.split(',')]
            else:
                return []
        return [(map.territories[base], map.territories[to])]

    def attack_continue(self, map, territory_from, territory_to):
        """Ask player if they wish to continue"""
        answer = input("Do you wish to continue? yes/no")
        return True if answer in ('yes', 'Yes', 'y', 'Y') else False

    def attack_commit(self, map, territory_from, territory_to):
        """Ask player number of armies to commit to attack"""
        armies = input("How many armies do you wish to commit of {} avaiable?".format(territory_from.armies - 1))
        return int(armies)

    def attack_move(self, map, territory_from, territory_to):
        """Ask player how many armies to move into conquest"""
        armies = input("How many armies do you wish to move in of {} avaiable?".format(territory_from.armies - 1))
        return int(armies)

class Passive(Player):
    def __init__(self, name):
        super().__init__(name)
    def __repr__(self):
        return super().__repr__()

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
        """passive deployts to the first territory with the least troops"""
        own = sorted((
            territory for territory in map.territories if territory.owner == self),
            key=lambda t: t.id + len(map.territories) * t.armies)
        map.add_armies(own[0], armies)

    def take_card(self, card):
        """Add card to the players hand"""
        self.cards.append(card)

    def attacks(self, map):
        """Passive does not attack"""
        return []

    def attack_continue(self, map, territory_from, territory_to):
        """Ask player if they wish to continue"""
        raise NotImplementedError()

    def attack_commit(self, map, territory_from, territory_to):
        """Ask player number of armies to commit to attack"""
        raise NotImplementedError()

    def attack_move(self, map, territory_from, territory_to):
        raise NotImplementedError()

class Standard(Player):
    def __init__(self, name):
        super().__init__(name)
    def __repr__(self):
        return super().__repr__()

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
        return territory_from.armies - 1

    def attack_move(self, map, territory_from, territory_to):
        return territory_from.armies - 1


class Aggresive(Player):
    def __init__(self, name):
        super().__init__(name)
    def __repr__(self):
        return super().__repr__()

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
        """Aggressive blobs as much as possible"""
        own = sorted((
            territory for territory in map.territories if territory.owner == self and any(n.owner != self for n in map.get_neighbours(territory))),
            key=lambda t: t.id + len(map.territories) * t.armies, reverse=True)
        map.add_armies(own[0], armies)

    def take_card(self, card):
        """Add card to the players hand"""
        self.cards.append(card)

    def attacks(self, map):
        """Declare list of attacks"""
        options = [(territory, neighbour) for territory in map.territories if territory.owner is self and territory.armies > 1
            for neighbour in map.get_neighbours(territory) if neighbour.owner is not self and territory.armies - 1 > neighbour.armies]
        attacks = sorted(options, key=lambda path: map.calculate_contienent(path[1].owner, path[1].continent), reverse=True)
        return attacks

    def attack_continue(self, map, territory_from, territory_to):
        """Ask player if they wish to continue"""
        return territory_from.armies > 1

    def attack_commit(self, map, territory_from, territory_to):
        """Ask player number of armies to commit to attack"""
        return territory_from.armies - 1

    def attack_move(self, map, territory_from, territory_to):
        return territory_from.armies - 1

def make_players(options):
    assert options['players'] >= 2
    players = []
    # for i in range(options['players']):
    players.append(Standard("ai {}".format(1)))
    players.append(Aggresive("ai {}".format(2)))
    return players