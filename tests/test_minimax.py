from risk.minimax import Minimax

# from wikipedia, this tree should have some alpha-beta pruning
tree = [
    [
        [
            [5, 6],
            [7, 4, 5]
        ],
        [
            [3]
        ]
    ],
    [
        [
            [6],
            [6, 9]
        ],
        [
            [7]
        ]
    ],
    [
        [
            [5]
        ],
        [
            [9, 8],
            [6]
        ]
    ]
]


class GameState():
    """Fake game state for testing"""
    def __init__(self, tree):
        self.tree = tree

    def next_state(self, move):
        return GameState(self.tree[move])

    def get_available_moves(self):
        return range(len(self.tree))

    def is_gameover(self):
        return type(self.tree) == int

    def evaluate(self):
        if type(self.tree) == int:
            return self.tree
        else:
            return float("inf")  # no heurstic for this


def test_minimax():
    game_state = GameState(tree)
    minimax = Minimax(100, 100)
    result = minimax.find_best(game_state)
    assert result == (0, (1, (0, (0, 3))))
