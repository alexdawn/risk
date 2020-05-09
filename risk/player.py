from typing import Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    from board import World, Territory
    from cards import Card


class Player:
    def __init__(self, index: int, name: str):
        self.index = index
        self.name = name
        self.in_game = True
        self.cards = []  # type: List[Card]
        self.success = False

    def __repr__(self) -> str:
        return self.name

    def remove_first_match(self, type):
        raise NotImplementedError()

    def check_cards(self, map: 'World', armies: int):
        """Check cards and hand in some if desired"""
        raise NotImplementedError()

    def deploy(self, map: 'World', armies: int):
        """The player deployment logic"""
        raise NotImplementedError()

    def take_card(self, card: 'Card'):
        """Add card to the players hand"""
        raise NotImplementedError()

    def attacks(self, map: 'World', options: Dict[str, Any]):
        """Declare list of attacks"""
        raise NotImplementedError()

    def attack_continue(self, map: 'World', territory_from: 'Territory', territory_to: 'Territory'):
        """Ask player if they wish to continue"""
        raise NotImplementedError()

    def attack_commit(self, map: 'World', territory_from: 'Territory', territory_to: 'Territory'):
        """Ask player number of armies to commit to attack"""
        raise NotImplementedError()

    def attack_move(self, map: 'World', territory_from: 'Territory', territory_to: 'Territory'):
        """Ask player how many armies to move into conquest"""
        raise NotImplementedError()
