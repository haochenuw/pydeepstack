import numpy as np

from card_tools import card_tools
from GameSettings import game_settings


# Gives strength representations for all private hands on the given board.
# @param board a possibly empty vector of board cards
# @param impossible_hand_value the value to assign to hands which are invalid
# on the board
# @return a vector containing a strength value or `impossible_hand_value` for
# every private hand
def batch_eval(board, impossible_hand_value):
    hand_values = np.full(game_settings.card_count, -1, dtype=float)

    if board.shape[0] == 0:
        for hand in range(1, game_settings.card_count + 1):
            hand_values[hand - 1] = int((hand - 1) / game_settings.suit_count) + 1
    else:
        board_size = board.shape[0]
        assert board_size == 1 or board_size == 2, "Incorrect board size for Leduc"
        whole_hand = np.zeros(board_size + 1, dtype=int)
        whole_hand[:-1] = board

        for card in range(1, game_settings.card_count + 1):
            whole_hand[-1] = card
            hand_values[card - 1] = evaluate(whole_hand, impossible_hand_value)

    return hand_values


# Gives a strength representation for a two or three card hand.
# @param hand a vector of two or three cards
# @param[opt] impossible_hand_value the value to return if the hand is invalid
# @return the strength value of the hand, or `impossible_hand_value` if the
# hand is invalid
def evaluate(whole_hand, impossible_hand_value=None):
    assert (
        np.max(whole_hand) <= game_settings["card_count"] and np.min(whole_hand) > 0
    ), "hand does not correspond to any cards"
    impossible_hand_value = (
        impossible_hand_value if impossible_hand_value is not None else -1
    )

    if not card_tools.hand_is_possible(whole_hand):
        return impossible_hand_value

    # We are not interested in the hand suit; we will use ranks instead of cards
    hand_ranks = np.copy(whole_hand)
    for i in range(hand_ranks.size):
        hand_ranks[i] = card_to_string.card_to_rank(hand_ranks[i])

    hand_ranks.sort()

    if whole_hand.size == 2:
        return evaluate_two_card_hand(hand_ranks)
    elif whole_hand.size == 3:
        return evaluate_three_card_hand(hand_ranks)
    else:
        assert False, "unsupported size of hand!"
