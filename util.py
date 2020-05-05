from collections import defaultdict
import rules


def test_combat(attack, defend, times):
    outcomes = defaultdict(int)
    for i in range(times):
        res = rules.combat(attack, defend)
        outcomes[res] += 1
    for k, v in outcomes.items():
        outcomes[k] = '{}%'.format(100 * v / times)
    print(outcomes)
