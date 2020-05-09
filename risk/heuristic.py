from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import World, Territory
    from player import Player

BORDER_SECURITY_FACTOR = 1
FOREIGN_TERRITORY_FACTOR = 1
OWN_CONTINENT_FACTOR = 0
FOREIGN_CONTINENT_FACTOR = 0


def border_threat(map: 'World', territory: 'Territory') -> int:
    """Sum of armies that threaten the province"""
    return sum(
        n.armies for n in map.get_neighbours(territory)
        if territory.owner.name != n.owner.name)


def border_security_ratio(map: 'World', territory: 'Territory') -> float:
    """Ratio of threatening armies to armies in territory"""
    if not territory.armies:
        raise RuntimeError("Zero armies on {}".format(territory.name))
    return float(border_threat(map, territory) / territory.armies)


def heuristic(map: 'World', player: 'Player') -> float:
    """Sum of BSR and number of foreign territories"""
    return float(sum(BORDER_SECURITY_FACTOR * border_security_ratio(map, t)
                if t.owner.name == player.name else FOREIGN_TERRITORY_FACTOR
                for t in map.territories) -
            OWN_CONTINENT_FACTOR * map.count_continents(player) + FOREIGN_CONTINENT_FACTOR *
            sum(map.count_continents(p) for p in map.players if p.name != player.name))
