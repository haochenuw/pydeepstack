import numpy as np

import card_tools
from GameSettings import game_settings


class TerminalEquity:
    def __init__(self):
        pass

    def set_board(self, board):
        self._set_call_matrix(board)
        self._set_fold_matrix(board)

    # @param board_cards: a vector of public cards 
    
    def get_last_round_call_matrix(self, board_cards, call_matrix):
        # Only support 1 or 2 board cards
        assert (
            board_cards.shape[0] == 1 or board_cards.shape[0] == 2
        ), "Only Leduc and extended Leduc are now supported"

        strength = evaluator.batch_eval(board_cards)

        # Handling hand strengths (winning probabilities)
        strength_view_1 = strength.reshape(game_settings.card_count, 1).repeat(
            1, call_matrix.shape[1]
        )
        strength_view_2 = strength.reshape(1, game_settings.card_count).repeat(
            call_matrix.shape[0], 1
        )

        call_matrix[:] = (strength_view_1 > strength_view_2).astype(
            call_matrix.dtype
        ) - (strength_view_1 < strength_view_2).astype(call_matrix.dtype)

        self._handle_blocking_cards(call_matrix, board_cards)

    def _set_call_matrix(self, board):
        street = card_tools.board_to_street(board)
        self.equity_matrix = np.zeros(
            (game_settings.card_count, game_settings.card_count), dtype=float
        )

        # only two possible streets: 1 or 2
        if street == 1:
            # Iterate through all possible next round streets
            next_round_boards = card_tools.get_boards()
            boards_count = next_round_boards.shape[0]
            next_round_equity_matrix = np.zeros(
                (game_settings.card_count, game_settings.card_count), dtype=float
            )

            for board_idx in range(boards_count):
                self.get_last_round_call_matrix(
                    next_round_boards[board_idx], next_round_equity_matrix
                )
                self.equity_matrix += next_round_equity_matrix

            # Averaging the values in the call matrix
            # seems this assumes there can be either 1 or 2 board cards?
            weight_constant = (
                1 / (game_settings.card_count - 2)
                if game_settings.board_card_count == 1
                else 2
                / ((game_settings.card_count - 2) * (game_settings.card_count - 3))
            )
            self.equity_matrix *= weight_constant

        elif street == 2:
            # For the last round, we just return the matrix
            self.get_last_round_call_matrix(board, self.equity_matrix)
        else:
            # Impossible street
            assert False, "impossible street"

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

    # Zeroes entries in an equity matrix that correspond to invalid hands.

    # A hand is invalid if it shares any cards with the board.
    # @param equity_matrix the matrix to modify
    # @param board a possibly empty vector of board cards
    # @local
    def _handle_blocking_cards(self, equity_matrix, board):
        possible_hand_indexes = card_tools.get_possible_hand_indexes(board)
        possible_hand_matrix = possible_hand_indexes.view(1, -1).expand_as(
            equity_matrix
        )
        equity_matrix.mul_(possible_hand_matrix)

        possible_hand_matrix = possible_hand_indexes.view(-1, 1).expand_as(
            equity_matrix
        )
        equity_matrix.mul_(possible_hand_matrix)

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
