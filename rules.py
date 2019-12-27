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
    first = True
    while len([p for p in players if p.in_game]) > 1:
        print("TURN {}".format(turn))
        play_round(map, cards, players, first)
        print("End of TURN {}".format(turn))
        summary(map)
        #_ = input("Press Enter for next round")
        turn += 1
        first = False
    winner = [p for p in players if p.in_game][0]
    print("Winner is {}".format(winner.name))

def play_round(map, cards, players, first):
    for player in players:
        if player.in_game:
            print("{}'s turn".format(player.name))
            play_turn(map, cards, player, first)
            for check_player in players:
                if not map.count_territories(check_player):
                    check_player.in_game = False
        if len([p for p in players if p.in_game]) == 1:
            break

def play_turn(map, cards, player, first_turn):
    armies =  calculate_troop_deployment(map, player)
    returns, bonus = player.check_cards(map, armies)
    if returns:
        cards.returns(returns)
    deploy(map, player, armies + bonus)
    if not first_turn:
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

def battle_results(ac, dc, attacker_wins, name):
    prefix = "Attacker wins" if attacker_wins else "Defender holds"
    print("{} {}, losses Attacker: {} Defender {}".format(prefix, name, dc, ac))


def attack(map, player, territory_from, territory_to):
    ac, dc = 0, 0
    while player.attack_continue(map, territory_from, territory_to) and territory_from.armies > 1 and territory_to.armies > 0:
        commited_attackers = player.attack_commit(map, territory_from, territory_to)
        a, d = combat(commited_attackers, territory_to.armies)
        ac += a
        dc += d
        # print("Combat in {} attacker loses {} and defender loses {}".format(territory_to, d, a))
        map.remove_armies(territory_from, d)
        map.remove_armies(territory_to, a)
    battle_results(ac, dc, territory_to.armies == 0, territory_to.name)
    if territory_to.armies == 0:
        map.conquer(player, territory_from, territory_to, max(player.attack_move(map, territory_from, territory_to), commited_attackers))
        return True
    else:
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