import time
import logging

logging.getLogger().setLevel(logging.INFO)

# TODO handle multiple plays
# TODO MaxN and Paranoid algorithms variants
# TODO Natural Play (Dice)

class Minimax():
    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.max_time = max_time

    def elapsed_time(self):
        return time.time() - self.start_time

    def find_best(self, game_state):
        self.start_time = time.time()
        alpha, beta = float("-inf"), float("inf")
        return max(
            map(lambda move: (move, self.min_play(
                game_state.next_state(move), alpha, beta, 1)),
                game_state.get_available_moves()), key=lambda x: x[1])

    def min_play(self, game_state, alpha, beta, depth):
        logging.info("Min play at depth {}".format(depth))
        if (game_state.is_gameover() or
                depth > self.max_depth or
                self.elapsed_time() > self.max_time):
            return game_state.evaluate()
        branch_min = min(
            map(lambda move: (
                move, self.max_play(game_state.next_state(move), alpha, beta, depth+1)),
                game_state.get_available_moves()), key=lambda x: x[1])
        return branch_min
        # if branch_min < beta:
        #     beta = branch_min

    def max_play(self, game_state, alpha, beta, depth):
        logging.info("Max play at depth {}".format(depth))
        if (game_state.is_gameover() or
                depth > self.max_depth or
                self.elapsed_time() > self.max_time):
            return game_state.evaluate()
        branch_max = max(
            map(lambda move: (
                move, self.min_play(game_state.next_state(move), alpha, beta, depth+1)),
                game_state.get_available_moves()), key=lambda x: x[1])
        return branch_max
        # if branch_max > alpha:
        #     alpha = branch_max
