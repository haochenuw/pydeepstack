import numpy as np

from GameSettings import game_settings


def board_to_street(board):
    if len(board) == 0:
        return 1
    else:
        return 2


def get_boards():
    if game_settings["board_card_count"] == 1:
        boards_count = game_settings.card_count
        out = np.zeros((boards_count, 1), dtype=int)
        for card in range(1, game_settings["card_count"] + 1):
            out[card - 1, 0] = card
        return out
    elif game_settings["board_card_count"] == 2:
        boards_count = (game_settings.card_count * (game_settings.card_count - 1)) / 2
        out = np.zeros((boards_count, 2), dtype=int)
        board_idx = 0
        for card_1 in range(1, game_settings["card_count"] + 1):
            for card_2 in range(card_1 + 1, game_settings["card_count"] + 1):
                board_idx += 1
                out[board_idx - 1, 0] = card_1
                out[board_idx - 1, 1] = card_2
        assert board_idx == boards_count, "wrong boards count!"
        return out
    else:
        assert False, "unsupported board size"


# Gives the private hands which are valid with a given board.
# @param board a possibly empty vector of board cards
# @return a vector with an entry for every possible hand (private card), which
# is `1` if the hand shares no cards with the board and `0` otherwise
def get_possible_hand_indexes(board):
    out = np.zeros(game_settings.card_count, dtype=int)

    if board.size == 0:
        out.fill(1)
        return out

    whole_hand = np.zeros(board.size + 1, dtype=int)
    whole_hand[:-1] = board

    for card in range(1, game_settings.card_count + 1):
        whole_hand[-1] = card
        if hand_is_possible(whole_hand):
            out[card - 1] = 1

    return out


# Gives whether a set of cards is valid.
# @param hand a vector of cards
# @return `true` if the tensor contains valid cards and no card is repeated
def hand_is_possible(hand):
    assert all(
        card > 0 and card <= game_settings.card_count for card in hand
    ), "Illegal cards in hand"

    used_cards = np.zeros(game_settings.card_count, dtype=int)
    for card in hand:
        used_cards[card - 1] += 1

    return used_cards.max() < 2
