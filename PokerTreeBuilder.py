# Note: we did not implement all-in.

import TreeNode
import Util
import Constants

class PokerTreeBuilder(): 
    def __init__(self, rules): 
        self.rules = rules
               
    def build_tree(self, params): 
        root = TreeNode(params.root.street, ...)
        self._build_tree_dfs(root)
        
    def _build_tree_dfs(self, current_node): 
        
        children = self._get_children_nodes(current_node)
        current_node.children = children
        for i in range(len(children)): 
            children[i].parent = current_node
            current_node.actions[i] = ??? 
            self._build_tree_dfs(children[i]) 
            depth = max(depth, children[i].depth)
        current_node.depth = depth + 1
        
    def _get_children_nodes(self, current_node): 
        if current_node.terminal: 
            return [] 
        if current_node.current_player == Constants.players.Chance: 
            return self._get_children_of_chance_node(current_node)
        else: 
            return self._get_children_of_player_node(current_node)
        
    def _get_children_of_player_node(self, current_node): 
        children = []
        
        foldNode = TreeNode(current_node.street, Constants.players.Nobody, current_node.board, current_node.bets)
        foldNode.terminal = True
        children.append(foldNode)
        
        if possibleCheck()
            checkNode = TreeNode(current_node.street, 3 - current_node.current_player), current_node.board, current_node.bets)
            checkNode.terminal = False
            children.append(checkNode)
        
        # transition call 
        if possibleTransitionCall():

        
        # terminal call 
        if possibleTerminalCall(): 
            terminalCallNode = TreeNode(current_node.street, Constants.players.Nobody, current_node.board, Util.fill_bets(current_node.bets))
            terminalCallNode.terminal = True
            children.append(terminalCallNode)
        
        if possibleBet(): 
            for i in range(len(possibleBets)): 
                betNode = TreeNode()
                children.append(betNode)
                
        return children 
    
    