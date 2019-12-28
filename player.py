class Player:
    def __init__(self, name):
        self.name = name
        self.in_game = True
        self.cards = []
        self.success = False
    def __repr__(self):
        return self.name

    def remove_first_match(self, type):
        raise NotImplementedError()

    def check_cards(self, map, armies):
        """Check cards and hand in some if desired"""
        raise NotImplementedError()
    
    def deploy(self, map, armies):
        """The player deployment logic"""
        raise NotImplementedError()

    def take_card(self, card):
        """Add card to the players hand"""
        raise NotImplementedError()

    def attacks(self, map):
        """Declare list of attacks"""
        raise NotImplementedError()

    def attack_continue(self, map, territory_from, territory_to):
        """Ask player if they wish to continue"""
        raise NotImplementedError()

    def attack_commit(self, map, territory_from, territory_to):
        """Ask player number of armies to commit to attack"""
        raise NotImplementedError()

    def attack_move(self, map, territory_from, territory_to):
        """Ask player how many armies to move into conquest"""
        raise NotImplementedError()
