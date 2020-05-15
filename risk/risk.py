from collections import defaultdict
import logging
import time
from typing import Dict, Any, TYPE_CHECKING

import risk.board as board
import risk.agents as agents
import risk.rules as rules
import risk.cards as cards
from risk.battle_estimator import get_cached_probabilities

if TYPE_CHECKING:
    from typing import Optional
    from risk.cards import CardDeck

logging.getLogger().setLevel(logging.INFO)
logging.disable(logging.CRITICAL)

options = {
    'players': 3,
    'stocasticity': True,  # False does not roll dice
    'markov': False,  # If True replaces simulated dice roll with the probable outcomes
    'initial_placement': 'random',  # random|pick
    'deployment': 'blob',  # blob|free|spread
    'extra_start_deployment': False,
    'attack_limit': None,  # None for no limit
    'death_or_glory': True,  # Cannot withdraw after commiting
    'end_of_turn_slide': False,
    'bonus_cards': 'fixed',  # none|fixed|yes
    'plot_gameplay': True,  # if True generate graphviz plots in ./output for each turn
    'logging_level': logging.CRITICAL
}  # type: Dict[str, Any]


def risk(name: str, options: Dict[str, Any]):
    map = board.make_map()
    players = agents.make_players(options)
    if options['bonus_cards'] == 'yes':
        deck = cards.CardDeck(map)  # type: Optional[CardDeck]
    else:
        deck = None
    return rules.play_game(name, map, deck, players, options)


if __name__ == '__main__':
    logging.getLogger().setLevel(options['logging_level'])
    tournament_score = defaultdict(
        lambda: {'wins': 0, 'avg_turns': 0})  # type: Dict[str, Dict[str, int]]
    if options['markov']:
        get_cached_probabilities(50, 50)  # Build a large state cache to avoid many matrix cals
    start = time.time()
    for i in range(1):
        name = "game {}".format(i)
        logging.debug(name)
        winner, turns = risk(name, options)
        tournament_score[winner]['wins'] += 1
        tournament_score[winner]['avg_turns'] = (
            (tournament_score[winner]['wins'] - 1) *
            tournament_score[winner]['avg_turns'] + turns) /\
            tournament_score[winner]['wins']
    end = time.time()
    print(end - start)
    print(tournament_score)
