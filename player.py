import rules

class Player:
    def __init__(self, name):
        self.name = name
        self.in_game = True
        self.cards = []
    
    def deploy(self, map, armies):
        """The player deployment logic"""
        for territory in map.territories:
            if territory.owner == self:
                map.add_armies(territory, armies)
                break

    def take_card(self, card):
        """Add card to the players hand"""
        self.cards.extend(card)

    def attacks(self, map):
        """Declare list of attacks"""
        attacks = []
        for territory in map.territories:
            if territory.owner == self:
                for neighbour in map.get_neighbours(territory):
                    if neighbour.owner != self:
                        attacks.extend(territory, neighbour)
                        break
        return attacks

    def attack_continue(self, map, territory_from, territory_to):
        """Ask player if they wish to continue"""
        return territory_from.armies > territory_to.armies and territory_from.armies > 1

    def attack_commit(self, map, territory_from, territory_to):
        """Ask player number of armies to commit to attack"""
        return min(territory_from.armies - 1, rules.MAX_ATTACK)

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