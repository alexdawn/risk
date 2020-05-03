import time
import logging

logging.getLogger().setLevel(logging.INFO)

# TODO handle multiple plays
# TODO MaxN and Paranoid algorithms variants
# TODO Natural Play (Dice)
# TODO Killer heuristic
# TODO negamax scout

class Minimax():
    def __init__(self, max_depth, max_time):
        self.max_depth = max_depth
        self.max_time = max_time

    def elapsed_time(self):
        """keep Track of run time"""
        return time.time() - self.start_time

    def find_best(self, game_state):
        """Method to intitate a search from game_state"""
        self.start_time = time.time()
        alpha, beta = float("-inf"), float("inf")
        depth = 1
        best = max(
            map(lambda move: self.search(move, self.min_play, game_state, alpha, beta, depth),
                game_state.get_available_moves()), key=lambda x: x[1])
        logging.info("Found Best {}, Time taken {}".format(best, self.elapsed_time()))
        return best

    def is_search_termination(self, game_state, depth):
        """Evalulate if to end the search"""
        return (game_state.is_gameover() or
                depth > self.max_depth or
                self.elapsed_time() > self.max_time)

    def search(self, move, function, game_state, alpha, beta, depth):
        """Function to search onward from a move, function can be either max or min"""
        return (
            move, function(game_state.next_state(move), alpha, beta, depth + 1))

    def min_play(self, game_state, alpha, beta, depth):
        logging.info("Min play at depth {}".format(depth))
        if self.is_search_termination(game_state, depth):
            return game_state.evaluate()
        branch_min = min(
            map(lambda move: self.search(move, self.max_play, game_state, alpha, beta, depth),
                game_state.get_available_moves()), key=lambda x: x[1])
        return branch_min

    def max_play(self, game_state, alpha, beta, depth):
        logging.info("Max play at depth {}".format(depth))
        if (game_state.is_gameover() or
                depth > self.max_depth or
                self.elapsed_time() > self.max_time):
            return game_state.evaluate()
        branch_max = max(
            map(lambda move: self.search(move, self.min_play, game_state, alpha, beta, depth),
                game_state.get_available_moves()), key=lambda x: x[1])
        return branch_max
