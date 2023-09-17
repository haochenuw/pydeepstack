from enum import Enum, auto


class Constants:
    params = {
        "max_street": 2, 
        "stack":4, 
    }

    # board_choices = ["As", "Ah", "Ks", "Kh", "Qs", "Qh"]

    board_choices = ["A", "K", "Q"]

    players = {
        "Chance": 0, 
        "P1": 1, 
        "P2":  2, 
        "Nobody": -1,
    }

    node_types = {
        "terminal_fold": -2,
        "terminal_call": -1,
        "check": 0,  # Note: 'check' has the same value as 'terminal_call' in the original code.
        "chance_node": 1,
        "inner_node": 2,
    }
