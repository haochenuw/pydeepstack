from enum import Enum, auto


class Players(Enum):
    Nobody = auto()
    P1 = auto()
    P2 = auto()
    Chance = auto()


class Constants:
    node_types = {
        "terminal_fold": -2,
        "terminal_call": -1,
        "check": 0,  # Note: 'check' has the same value as 'terminal_call' in the original code.
        "chance_node": 1,
        "inner_node": 2,
    }
