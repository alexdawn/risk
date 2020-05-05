import logging
import copy
import os
from graphviz import Graph
from collections import defaultdict


class Map:
    def __init__(self):
        self.territories = []
        self.territories_by_name = {}
        self.continents = {}
        self.players = set()
        self.player_territory_count = defaultdict(lambda: 0)

    def __repr__(self):
        return "\n".join("{}: {} armies owned by {}".format(
            territory.name, territory.armies, territory.owner.name if territory.owner else "N/A")
            for territory in self.territories)

    def make_copy(self):
        return copy.deepcopy(self)

    def make_graph(self, name: str, description: str) -> None:
        g = Graph('Map', filename='world.gv', engine='neato')
        # continent_graphs = {
        #     n: g.subgraph(name='cluster_{}'.format(n))
        #     for n in self.continents.keys()}
        g.attr(label=description)
        g.attr('node', colorscheme="pastel19", style="filled")
        for t in self.territories:
            # with continent_graphs[t.continent] as c:
            g.node(t.name, "{} ({:4d})".format(t.name, t.armies),
                   fillcolor=str(t.owner.index + 1), pos=t.get_coordinates())
            for i in t.connections:
                g.edge(t.name, self.territories[i - 1].name)
        g.format = 'svg'
        g.render('outputs/{}'.format(name), view=False)
        if os.path.exists('outputs/{}'.format(name)):
            os.remove('outputs/{}'.format(name))

    def make_terrority(self, id, name, continent, coordinates, connections):
        territory = Terrority(id, name, continent, coordinates, connections)
        self.territories.append(territory)
        self.territories_by_name[name] = territory

    def get_territory(self, name):
        return self.territories_by_name[name]

    def allocate_territories(self, players):
        territories_to_be_allocated = set(self.territories)
        self.players = set(players)
        while len(territories_to_be_allocated) > 0:
            for player in players:
                t = territories_to_be_allocated.pop()
                t.set_armies(1)
                t.set_owner(player)
                self.player_territory_count[player] += 1
                if len(territories_to_be_allocated) == 0:
                    break

    def get_neighbours(self, territory):
        return [self.territories[i - 1] for i in territory.connections]

    def set_continent_army_value(self, name, value):
        self.continents[name] = value

    def conquer(self, player, territory_from, territory_to, armies):
        logging.info("{} taken over by {}".format(territory_to.name, player.name))
        self.player_territory_count[territory_to.owner] -= 1
        territory_to.set_owner(player)
        self.player_territory_count[player] += 1
        self.move_armies(territory_from, territory_to, armies)

    def add_armies(self, territory, armies):
        logging.info("Add {} armies to {}".format(armies, territory.name))
        territory.set_armies(territory.armies + armies)

    def move_armies(self, territory_from, territory_to, armies):
        logging.info("{} armies moved from {} to {}".format(
            armies, territory_from.name, territory_to.name))
        territory_to.set_armies(territory_to.armies + armies)
        territory_from.set_armies(territory_from.armies - armies)

    def remove_armies(self, territory, armies):
        territory.set_armies(max(territory.armies - armies, 0))

    def count_territories(self, player):
        return self.player_territory_count[player]

    def count_continents(self, player):
        bonus = 0
        for continent_name in self.continents.keys():
            bonus += self.calculate_contienent(player, continent_name)
        return bonus

    def calculate_contienent(self, player, name):
        members = [territory for territory in self.territories if territory.continent == name]
        if all(m.owner.name == player.name for m in members):
            return self.continents[name]
        else:
            return 0


class Terrority:
    def __init__(self, id, name, continent, coordinates, connections):
        self.id = id
        self.name = name
        self.coordinates = coordinates
        self.continent = continent
        self.connections = connections
        self.owner = None
        self.armies = 0

    def get_coordinates(self):
        return "{},{}!".format(*self.coordinates)

    def __repr__(self):
        return self.name

    def set_owner(self, player):
        self.owner = player

    def set_armies(self, armies):
        assert armies >= 0
        self.armies = armies


def make_map():
    map = Map()
    map.set_continent_army_value('North America', 5)
    map.make_terrority(1, 'Alaska', 'North America', (0, 0), [2, 4, 30])
    map.make_terrority(2, 'North West Territory', 'North America', (2, 0), [1, 3, 4, 5])
    map.make_terrority(3, 'Greenland', 'North America', (5, 0), [2, 5, 6, 14])
    map.make_terrority(4, 'Alberta', 'North America', (1, -1), [1, 2, 5, 7])
    map.make_terrority(5, 'Ontario', 'North America', (3, -1), [2, 3, 4, 6, 7, 8])
    map.make_terrority(6, 'Quebec', 'North America', (5, -1), [3, 5, 8])
    map.make_terrority(7, 'Western United States', 'North America', (1, -2), [4, 5, 8, 9])
    map.make_terrority(8, 'Eastern United States', 'North America', (4, -2), [5, 6, 7, 9])
    map.make_terrority(9, 'Central America', 'North America', (2.5, -3), [7, 8, 10])

    map.set_continent_army_value('South America', 2)
    map.make_terrority(10, 'Venezuela', 'South America', (3, -4), [9, 11, 12])
    map.make_terrority(11, 'Peru', 'South America', (2.5, -5), [10, 12, 13])
    map.make_terrority(12, 'Brazil', 'South America', (3.5, -5), [10, 11, 13, 21])
    map.make_terrority(13, 'Argentina', 'South America', (3, -7), [11, 12])

    map.set_continent_army_value('Europe', 5)
    map.make_terrority(14, 'Iceland', 'Europe', (7, -0.5), [3, 15, 16])
    map.make_terrority(15, 'Great Britian', 'Europe', (7, -1), [14, 16, 17, 18])
    map.make_terrority(16, 'Scandinavia', 'Europe', (9, -1), [14, 15, 18, 20])
    map.make_terrority(17, 'Western Europe', 'Europe', (6, -2.5), [15, 18, 19, 21])
    map.make_terrority(18, 'Northern Europe', 'Europe', (8, -2), [15, 16, 17, 19, 20])
    map.make_terrority(19, 'Southern Europe', 'Europe', (7, -3), [17, 18, 20, 21, 22, 36])
    map.make_terrority(20, 'Ukraine', 'Europe', (10, -2), [16, 18, 19, 27, 34, 36])

    map.set_continent_army_value('Africa', 3)
    map.make_terrority(21, 'North Africa', 'Africa', (5, -4), [12, 17, 19, 22, 23, 24])
    map.make_terrority(22, 'Egypt', 'Africa', (8, -4), [19, 21, 24, 36])
    map.make_terrority(23, 'Congo', 'Africa', (6.5, -5), [21, 24, 25])
    map.make_terrority(24, 'East Africa', 'Africa', (8, -5), [21, 22, 23, 25, 26, 36])
    map.make_terrority(25, 'South Africa', 'Africa', (7, -7), [23, 24, 26])
    map.make_terrority(26, 'Madagascar', 'Africa', (9, -6), [24, 25])

    map.set_continent_army_value('Asia', 7)
    map.make_terrority(27, 'Ural', 'Asia', (11, -1.5), [20, 28, 34, 35])
    map.make_terrority(28, 'Siberia', 'Asia', (12, -1), [27, 29, 31, 32, 35])
    map.make_terrority(29, 'Yakutsk', 'Asia', (13, -0.5), [28, 30, 31])
    map.make_terrority(30, 'Kamchatka', 'Asia', (14, 0), [29, 31, 32, 33, 1])
    map.make_terrority(31, 'Irkutsk', 'Asia', (14, -2), [28, 29, 30, 32])
    map.make_terrority(32, 'Mongolia', 'Asia', (13, -2.5), [28, 30, 31, 33])
    map.make_terrority(33, 'Japan', 'Asia', (15, -3), [30, 32])
    map.make_terrority(34, 'Afghanistan', 'Asia', (11.2, -4), [20, 27, 35, 36, 37])
    map.make_terrority(35, 'China', 'Asia', (12, -3), [27, 28, 32, 34, 37, 38])
    map.make_terrority(36, 'Middle East', 'Asia', (9.4, -4), [19, 20, 22, 24, 34, 37])
    map.make_terrority(37, 'India', 'Asia', (12, -5), [34, 35, 36, 38])
    map.make_terrority(38, 'Siam', 'Asia', (13, -5), [35, 37, 39])

    map.set_continent_army_value('Oceania', 2)
    map.make_terrority(39, 'Indonesia', 'Oceania', (14, -6), [38, 40, 41])
    map.make_terrority(40, 'New Guinea', 'Oceania', (15, -7), [39, 41, 42])
    map.make_terrority(41, 'Western Australia', 'Oceania', (12.5, -8), [39, 40, 42])
    map.make_terrority(42, 'Eastern Australia', 'Oceania', (15, -8), [40, 41])
    return map
