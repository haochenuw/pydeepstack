import numpy as np

from GameSettings import game_settings


class TerminalEquity:
    def __init__(self):
        pass

    def set_board(self, board):
        self._set_call_matrix(board)
        self._set_fold_matrix(board)

    # Creates the matrix `B` such that for player ranges `x` and `y`, `x'By` is the equity
    # for the player who doesn't fold
    # @param board a possibly empty vector of board cards
    def _set_fold_matrix(self, board):
        # Create a fold_matrix with all elements initialized to 1
        self.fold_matrix = np.ones((game_settings.card_count, game_settings.card_count))

        # Setting cards that block each other to zero (similar to diagonal elements)
        self.fold_matrix -= np.eye(game_settings.card_count)

        # Assuming you have a function '_handle_blocking_cards' defined somewhere, call it with fold_matrix and board
        self._handle_blocking_cards(self.fold_matrix, board)

    def _handle_blocking_cards(self, board):
        pass

    # Computes (a batch of) counterfactual values that a player achieves at a terminal node
    # where no player has folded.
    #
    # `set_board` must be called before this function.
    #
    # @param ranges a batch of opponent ranges in an NxK tensor, where N is the batch size
    # and K is the range size
    # @param result a NxK tensor in which to save the cfvs
    def call_value(self, ranges, result):
        result = np.dot(ranges, self.equity_matrix)

    # Computes (a batch of) counterfactual values that a player achieves at a terminal node
    # where a player has folded.
    #
    # `set_board` must be called before this function.
    #
    # @param ranges: a batch of opponent ranges in an NxK tensor, where N is the batch size
    # and K is the range size
    # @param result: A NxK tensor in which to save the cfvs. Positive cfvs are returned, and
    # must be negated if the player in question folded.
    def fold_value(self, ranges, result):
        result = np.dot(ranges, self.fold_matrix)
