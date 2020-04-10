from collections import defaultdict
import logging
from typing import Dict, Any

import board
import agents
import rules
import cards

logging.getLogger().setLevel(logging.INFO)

options = {
    'players': 9,
    'stocasticity': True,  # False does not roll dice
    'initial_placement': 'random',  # random|pick
    'deployment': 'blob',  # blob|free|spread
    'extra_start_deployment': False,
    'attack_limit': None,  # None for no limit
    'death_or_glory': True,  # Cannot withdraw after commiting
    'end_of_turn_slide': False,
    'bonus_cards': 'fixed'  # none|fixed|yes
}  # type: Dict[str, Any]

def risk(name: str, options: Dict[str, Any]):
    map = board.make_map()
    players = agents.make_players(options)
    if options['bonus_cards'] == 'yes':
        deck = cards.Card_Deck(map)
    else:
        deck = None
    return rules.play_game(name, map, deck, players, options)


if __name__ == '__main__':
    tournament_score = defaultdict(lambda: {'wins': 0, 'avg_turns': 0})
    for i in range(1):
        name = "game {}".format(i)
        logging.debug(name)
        winner, turns = risk(name, options)
        winner = winner if type(winner) == str else winner.name
        tournament_score[winner]['wins'] += 1
        tournament_score[winner]['avg_turns'] = (
            (tournament_score[winner]['wins'] - 1) *
            tournament_score[winner]['avg_turns'] + turns) /\
            tournament_score[winner]['wins']
    print(tournament_score)
