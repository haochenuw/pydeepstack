# Define a class named "Person"
class TreeNode:
    # Constructor method to initialize the object
    def __init__(self, street, bets, current_player, board, terminal = None, depth=None):
        self.street = street
        self.bets = bets
        self.current_player = current_player
        self.board = board
        self.terminal = terminal 
        self.depth = depth

    # Method to display information about the person
    def display_info(self):
        print(f"Street: {self.street}, bets: {self.bets}")

