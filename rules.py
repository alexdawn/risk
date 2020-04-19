import math
import logging
import io
from collections import defaultdict
from typing import List, Dict, Any

import dice

# Create the logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

TERRITORIES_PER_ARMY = 3
MIN_DEPLOYMENT = 3
MAX_ATTACK = 3
MAX_DEFENSE = 2

def summary(map):
    """Log how many territories each player has"""
    ownership = defaultdict(lambda: 0)
    for t in map.territories:
        ownership[t.owner] += 1
    logging.info(dict(ownership))


def play_game(
        name: str,
        map,
        cards, players: List[Any], options: Dict[str, Any]):
    map.allocate_territories(players)
    turn = 1
    first = options['extra_start_deployment']
    while len([p for p in players if p.in_game]) > 1 and turn < 1000:
        logging.info("TURN {}".format(turn))
        play_round(map, cards, players, first, name, turn, options)
        logging.info("End of TURN {}".format(turn))
        summary(map)
        turn += 1
        first = False
    if turn < 1000:  # stop game going on forever
        winner = [p for p in players if p.in_game][0]
        logging.info("Winner is {}".format(winner.name))
    else:
        winner = 'Draw'
        turn = 1000
    return winner, turn

def check_players(map, players):
    """Check which players still have territory"""
    for check_player in players:
        check_player.in_game = bool(map.count_territories(check_player))

def active_players(players):
    """Count of players still in game"""
    len([p for p in players if p.in_game])

def play_round(
        map, cards, players, first, name: str, turn, options):
    for player in players:
        if player.in_game:
            # Setup the console handler with a StringIO object
            log_capture_string = io.StringIO()
            ch = logging.StreamHandler(log_capture_string)

            # Add the console handler to the logger
            logger.addHandler(ch)
            logging.info("{}'s turn".format(player.name))
            play_turn(map, cards, player, first, options)
            log_contents = log_capture_string.getvalue()
            logging.RemoveHandler(ch)
            log_capture_string.close()
            map.make_graph("map-{}-{}-{}".format(name, turn, player.index), log_contents.lower())
            check_players(map, players)
        if active_players(players) == 1:
            break

def play_turn(map, cards, player, first_turn, options):
    base_armies = calculate_troop_deployment(map, player)
    contienent_bonus = calculate_contienent_bonus(map, player)
    if options['bonus_cards'] == 'yes':
        returns, card_bonus = player.check_cards(map, base_armies)
        if returns:
            cards.returns(returns)
    elif options['bonus_cards'] == 'fixed':
        card_bonus = 2 if player.success else 0
    elif options['bonus_cards'] == 'none':
        card_bonus = 0
    else:
        raise ValueError("Invalid setting")
    armies = base_armies + contienent_bonus + card_bonus
    logging.info("{} gets {} (+{}+{} bonus) armies this turn"
                 .format(player.name, base_armies, contienent_bonus, card_bonus))
    deploy(map, player, armies)
    if not first_turn:
        player.success = attacks(map, player, options)
        if player.success and options['bonus_cards'] == 'yes':
            player.take_card(draw_card(cards))
        if options['end_of_turn_slide']:
            slide(map, player)


def deploy(map, player, armies):
    player.deploy(map, armies)

def calculate_contienent_bonus(map, player):
    return map.count_continents(player)

def calculate_troop_deployment(map, player):
    return max(math.floor(map.count_territories(player) / TERRITORIES_PER_ARMY), MIN_DEPLOYMENT)

def attacks(map, player, options):
    at_least_one_victory = False
    attack_plan = player.attacks(map, options)[:options['attack_limit']]
    if len(attack_plan) == 0:
        logging.info("No attacks made by {}".format(player))
    for territory_from, territory_to in attack_plan:
        if (territory_from.owner == player and
           territory_to.owner != player and
           territory_from.armies > 1):
            result = attack(map, player, options, territory_from, territory_to)
            if result:
                at_least_one_victory = True
        else:
            logging.debug("Invalid target {}->{}!".format(territory_from, territory_to))
    return at_least_one_victory

def battle_results(ac, dc, attacker_wins, name):
    prefix = "Attacker wins" if attacker_wins else "Defender holds"
    logging.info("{} {}, losses Attacker: {} Defender {}".format(prefix, name, dc, ac))


def attack(map, player, options, territory_from, territory_to):
    ac, dc = 0, 0
    commited_attackers = player.attack_commit(map, territory_from, territory_to)
    assert commited_attackers < territory_from.armies
    while ((True if options['death_or_glory']
           else player.attack_continue(map, territory_from, territory_to))
           and territory_from.armies > 1
           and territory_to.armies > 0):
        a, d = combat(commited_attackers, territory_to.armies, options)
        ac += a
        dc += d
        # logging.info("Combat in {} attacker loses {} and defender loses {}"
        #              .format(territory_to, d, a))
        map.remove_armies(territory_from, d)
        map.remove_armies(territory_to, a)
    battle_results(ac, dc, territory_to.armies == 0, territory_to.name)
    if territory_to.armies == 0:
        invaders = min(commited_attackers, territory_from.armies - 1)
        map.conquer(player, territory_from, territory_to,
                    max(player.attack_move(map, territory_from, territory_to), invaders))
        return True
    else:
        return False


def combat(attackers, defenders, options):
    assert attackers > 0
    assert defenders > 0
    if options['stocasticity']:
        attack = dice.roll_dice(min(attackers, MAX_ATTACK))
        defend = dice.roll_dice(min(defenders, MAX_DEFENSE))
        attacker_kills, defender_kills = 0, 0
        for a, d in zip(sorted(attack, reverse=True), sorted(defend, reverse=True)):
            if a > d:
                attacker_kills += 1
            else:
                defender_kills += 1
    else:
        attacker_kills, defender_kills = min(defenders, attackers), min(defenders, attackers)
    return attacker_kills, defender_kills


def slide(map, player):
    pass

def draw_card(cards):
    return cards.draw()
