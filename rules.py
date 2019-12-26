import math
import dice

TERRITORIES_PER_ARMY = 3
MIN_DEPLOYMENT = 3
MAX_ATTACK = 3
MAX_DEFENSE = 2

def play_game(map, cards, players):
    while len(p for p in players if p.in_game) > 1:
        play_round(map, players)
    winner = [p for p in plyers if p.in_game][0]
    print("Winner is {}".format(winner.name))

def play_round(map, cards, players):
    for player in players:
        if map.count_terrorities(player):
            play_turn(map, player)
        else:
            player.in_game = False

def play_turn(map, cards, player):
    armies =  calculate_troop_deployment(map, player)
    deploy(map, player, armies)
    success = attacks(map, player)
    if success:
        player.take_card(draw_card(cards))
    slide(map, player)


def deploy(map, player, armies):
    player.deploy(map, armies)

def calculate_troop_deployment(map, player):
    return max(math.floor(map.count_terrorities(player) / TERRITORIES_PER_ARMY), MIN_DEPLOYMENT)

def attacks(map, player):
    at_least_one_victory = False
    for territory_from, territory_to in player.attacks(map):
        assert territory_from.owner == player
        assert territory_to.owner != player
        if territory_from.armies > 1:
            result = attack(map, player, territory_to, territory_to)
            if result:
                at_least_one_victory = True
    return at_least_one_victory

def attack(map, player, territory_from, territory_to):
    while player.attack_continue(map, e) and territory_from.armies > 1:
        commited_attackers = player.attack_commit(map, territory_from, territory_to)
        a, d = combat(commited_attackers, territory_to.armies)
        print("Combat in {} attacker loses {} and defender loses {}".format(territory_to, d, a))
        map.remove_armies(territory_from, d)
        map.remove_armies(territory_to, a)
        if territory_to.armies == 0:
            map.conquer(player, territory_from, territory_to, commited_attackers)
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
    pass