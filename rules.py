import math
from collections import defaultdict
import dice

TERRITORIES_PER_ARMY = 3
MIN_DEPLOYMENT = 3
MAX_ATTACK = 3
MAX_DEFENSE = 2

def summary(map):
    ownership = defaultdict(lambda :0)
    for t in map.territories:
        ownership[t.owner] += 1
    print(dict(ownership))


def play_game(map, cards, players):
    map.allocate_territories(players)
    turn = 1
    while len([p for p in players if p.in_game]) > 1:
        print("TURN {}".format(turn))
        play_round(map, cards, players)
        print("End of TURN {}".format(turn))
        summary(map)
        _ = input("Press Enter for next round")
        turn += 1
    winner = [p for p in players if p.in_game][0]
    print("Winner is {}".format(winner.name))

def play_round(map, cards, players):
    for player in players:
        if map.count_territories(player):
            print("{}'s turn".format(player.name))
            play_turn(map, cards, player)
        else:
            player.in_game = False

def play_turn(map, cards, player):
    armies =  calculate_troop_deployment(map, player)
    returns, bonus = player.check_cards(map, armies)
    if returns:
        cards.returns(returns)
    deploy(map, player, armies + bonus)
    success = attacks(map, player)
    if success:
        player.take_card(draw_card(cards))
    slide(map, player)


def deploy(map, player, armies):
    player.deploy(map, armies)

def contienent_bonus(map, player):
    bonuses = 0
    for name, bonus in map.continents.items():
        members = [territory for territory in map.territories if territory.continent == name]
        if all(m.owner == player for m in members):
            print("Bonus of {} for owning {}".format(bonus, name))
            bonuses += bonus
    return bonuses

def calculate_troop_deployment(map, player):
    base_count = max(math.floor(map.count_territories(player) / TERRITORIES_PER_ARMY), MIN_DEPLOYMENT)
    return base_count + contienent_bonus(map, player)

def attacks(map, player):
    at_least_one_victory = False
    for territory_from, territory_to in player.attacks(map):
        if (territory_from.owner == player and
           territory_to.owner != player and
           territory_from.armies > 1):
            result = attack(map, player, territory_from, territory_to)
            if result:
                at_least_one_victory = True
    return at_least_one_victory

def attack(map, player, territory_from, territory_to):
    while player.attack_continue(map, territory_from, territory_to) and territory_from.armies > 1:
        commited_attackers = player.attack_commit(map, territory_from, territory_to)
        a, d = combat(commited_attackers, territory_to.armies)
        print("Combat in {} attacker loses {} and defender loses {}".format(territory_to, d, a))
        map.remove_armies(territory_from, d)
        map.remove_armies(territory_to, a)
        if territory_to.armies == 0:
            map.conquer(player, territory_from, territory_to, max(player.attack_move(map, territory_from, territory_to), commited_attackers))
            return True
    return False


def combat(attackers, defenders):
    attack = dice.roll_dice(min(attackers, MAX_ATTACK))
    defend = dice.roll_dice(min(defenders, MAX_DEFENSE))
    attacker_kills, defender_kills = 0, 0
    for a, d in zip(sorted(attack, reverse=True), sorted(defend, reverse=True)):
        if a > d:
            attacker_kills += 1
        else:
            defender_kills += 1
    return attacker_kills, defender_kills


def slide(map, player):
    pass

def draw_card(cards):
    return cards.draw()