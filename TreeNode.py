# Define a class named "Person"
from typing import List, Optional, Tuple


class TreeNode:
    # Constructor method to initialize the object
    def __init__(self, street: int, bets: Tuple[int, int], current_player: int, board: str, isCall:  bool = False, terminal: Optional[bool]= None, depth: Optional[int] = None):
        self.street = street
        self.bets = bets
        self.current_player = current_player
        self.board = board
        self.terminal = terminal 
        self.depth = depth
        self.isCall = isCall
        self.children = None

    # Method to display information about the person
    def display_info(self):
        print(f"Street: {self.street}, bets: {self.bets}")

