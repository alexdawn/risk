import logging

class Map:
    def __init__(self):
        self.territories = []
        self.continents = {}

    def __repr__(self):
        return "\n".join("{}: {} armies owned by {}".format(
            territory.name, territory.armies, territory.owner.name if territory.owner else "N/A") for territory in self.territories)

    def make_terrority(self, id, name, continent, connections):
        self.territories.append(Terrority(id, name, continent, connections))

    def allocate_territories(self, players):
        territories_to_be_allocated = set(self.territories)
        while len(territories_to_be_allocated) > 0:
            for player in players:
                t = territories_to_be_allocated.pop()
                t.set_armies(1)
                t.owner = player
                if len(territories_to_be_allocated) == 0:
                    break

    def get_neighbours(self, territory):
        return [self.territories[i - 1] for i in territory.connections]

    def set_continent_army_value(self, name, value):
        self.continents[name] = value

    def conquer(self, player, territory_from, territory_to, armies):
        logging.info("{} taken over by {}".format(territory_to.name, player.name))
        territory_to.set_owner(player)
        self.move_armies(territory_from, territory_to, armies)

    def add_armies(self, territory, armies):
        logging.info("Add {} armies to {}".format(armies, territory.name))
        territory.set_armies(territory.armies + armies)

    def move_armies(self, territory_from, territory_to, armies):
        logging.info("{} armies moved from {} to {}".format(armies, territory_from.name, territory_to.name))
        territory_to.set_armies(territory_to.armies + armies)
        territory_from.set_armies(territory_from.armies - armies)        

    def remove_armies(self, territory, armies):
        territory.set_armies(max(territory.armies - armies, 0))

    def count_territories(self, player):
        return sum(1 for t in self.territories if t.owner == player)

    def count_continents(self, player):
        bonus = 0
        for continent_name in self.continents.keys():
            bonus += self.calculate_contienent(player, continent_name)
        return bonus

    def calculate_contienent(self, player, name):
        members = [territory for territory in self.territories if territory.continent == name]
        if all(m.owner == player for m in members):
            return self.continents[name]
        else:
            return 0

class Terrority:
    def __init__(self, id, name, continent, connections):
        self.id = id
        self.name = name
        self.continent = continent
        self.connections = connections
        self.owner = None
        self.armies = 0
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
    map.make_terrority(1, 'Alaska', 'North America', [2, 4, 30])
    map.make_terrority(2, 'North West Territory', 'North America', [1, 3, 4, 5])
    map.make_terrority(3, 'Greenland', 'North America', [2, 5, 6, 14])
    map.make_terrority(4, 'Alberta', 'North America', [1, 2, 5, 7])
    map.make_terrority(5, 'Ontario', 'North America', [2, 3, 4, 6, 7, 8])
    map.make_terrority(6, 'Quebec', 'North America', [3, 5, 8])
    map.make_terrority(7, 'Western United States', 'North America', [4, 5, 8, 9])
    map.make_terrority(8, 'Eastern United States', 'North America', [5, 6, 7, 9])
    map.make_terrority(9, 'Central America', 'North America', [7, 8, 10])

    map.set_continent_army_value('South America', 2)
    map.make_terrority(10, 'Venezuela', 'South America', [9, 11, 12])
    map.make_terrority(11, 'Peru', 'South America', [10, 12, 13])
    map.make_terrority(12, 'Brazil', 'South America', [10, 11, 13, 21])
    map.make_terrority(13, 'Argentina', 'South America', [11, 12])
    
    map.set_continent_army_value('Europe', 5)
    map.make_terrority(14, 'Iceland', 'Europe', [3, 15, 16])
    map.make_terrority(15, 'Great Britian', 'Europe', [14, 16, 17, 18])
    map.make_terrority(16, 'Scandinavia', 'Europe', [14, 15, 18, 20])
    map.make_terrority(17, 'Western Europe', 'Europe', [15, 18, 19, 21])
    map.make_terrority(18, 'Northern Europe', 'Europe', [15, 16, 17, 19, 20])
    map.make_terrority(19, 'Southern Europe', 'Europe', [17, 18, 20, 21, 22, 36])
    map.make_terrority(20, 'Ukraine', 'Europe', [16, 18, 19, 27, 34, 36])

    map.set_continent_army_value('Africa', 3)
    map.make_terrority(21, 'North Africa', 'Africa', [12, 17, 19, 22, 23, 24])
    map.make_terrority(22, 'Egypt', 'Africa', [19, 21, 24, 36])
    map.make_terrority(23, 'Congo', 'Africa', [21, 24, 25])
    map.make_terrority(24, 'East Africa', 'Africa', [21, 22, 23, 25, 26, 36])
    map.make_terrority(25, 'South Africa', 'Africa', [23, 24, 26])
    map.make_terrority(26, 'Madagascar', 'Africa', [24, 25])

    map.set_continent_army_value('Asia', 7)
    map.make_terrority(27, 'Ural', 'Asia', [20, 28, 34, 35])
    map.make_terrority(28, 'Siberia', 'Asia', [27, 29, 31, 32, 35])
    map.make_terrority(29, 'Yakutsk', 'Asia', [28, 30, 31])
    map.make_terrority(30, 'Kamchatka', 'Asia', [29, 31, 32, 33, 1])
    map.make_terrority(31, 'Irkutsk', 'Asia', [28, 29, 30, 32])
    map.make_terrority(32, 'Mongolia', 'Asia', [28, 30, 31, 33])
    map.make_terrority(33, 'Japan', 'Asia', [30, 32])
    map.make_terrority(34, 'Afghanistan', 'Asia', [20, 27, 35, 36, 37])
    map.make_terrority(35, 'China', 'Asia', [27, 28, 32, 34, 37, 38])
    map.make_terrority(36, 'Middle East', 'Asia', [19, 20, 22, 24, 34, 37])
    map.make_terrority(37, 'India', 'Asia', [34, 35, 36, 38])
    map.make_terrority(38, 'Siam', 'Asia', [35, 37, 39])

    map.set_continent_army_value('Oceania', 2)
    map.make_terrority(39, 'Indonesia', 'Oceania', [38, 40, 41])
    map.make_terrority(40, 'New Guinea', 'Oceania', [39, 41, 42])
    map.make_terrority(41, 'Western Australia', 'Oceania', [39, 40, 42])
    map.make_terrority(42, 'Eastern Australia', 'Oceania', [40, 41])
    return map