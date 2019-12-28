import board
import agents
import rules
import cards

options = {
    'players': 2,
    'stocasticity': True,  # False does not roll dice
    'initial_placement': 'random', # random|pick
    'deployment': 'blob', # blob|free|spread
    'extra_start_deployment': True,
    'attack_limit': 1,  # None for no limit
    'death_or_glory': False, # Cannot withdraw after commiting
    'end_of_turn_slide': False,
    'bonus_cards': 'fixed'  # none|fixed|yes
}

def risk(options):
    map = board.make_map()
    players = agents.make_players(options)
    if options['bonus_cards'] == 'yes':
        deck = cards.Card_Deck(map)
    else:
        deck = None
    rules.play_game(map, deck, players, options)

if __name__ == '__main__':
    for i in range(1):
        risk(options)
