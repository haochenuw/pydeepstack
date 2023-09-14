def fill_bets(bets):
    m = max(bets[0], bets[1])
    return (m, m)


card_to_string_table = {}
card_to_string_table[1] = "As"
card_to_string_table[2] = "Ah"
card_to_string_table[3] = "Ks"
card_to_string_table[4] = "Kh"
card_to_string_table[5] = "Qs"
card_to_string_table[6] = "Qh"


def card_to_string(card):
    return card_to_string_table[card]


def cards_to_string(board):
    return ".".join(card_to_string(card) for card in board)
