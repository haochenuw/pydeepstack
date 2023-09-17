# Note: we did not implement all-in.

from typing import List, Tuple

import Util
from Constants import Constants
from TreeNode import TreeNode


class PokerTreeBuilder(): 
    def __init__(self, rules = None): 
        self.rules = rules
               
    def build_tree(self, root: TreeNode): 
        self._build_tree_dfs(root)
        
    def _build_tree_dfs(self, current_node: TreeNode): 
        
        children = self._get_children_nodes(current_node)
        print(f'found {len(children)} children nodes')
        current_node.children = children
        depth = 0
        for i in range(len(children)): 
            children[i].parent = current_node
            # current_node.actions[i] = "TBD" 
            self._build_tree_dfs(children[i]) 
            depth = max(depth, children[i].depth)
        current_node.depth = depth + 1
        
    def _get_children_nodes(self, current_node: TreeNode): 
        if current_node.terminal: 
            return [] 
        if current_node.current_player == Constants.players["Chance"]: 
            return self._get_children_of_chance_node(current_node)
        else: 
            return self._get_children_of_player_node(current_node)
        
    def _possibleCheck(self, parent: TreeNode): 
        # a player can check only if the bettings are the same 
        return parent.bets[0] == parent.bets[1]
    
    def _possibleBet(self, parent): 
        # same, you can bet whenever you can check 
        return parent.bets[0] == parent.bets[1]
    
    def _possibleCall(self, parent: TreeNode): 
        # you can call when you have uneven bets  
        return parent.bets[0] != parent.bets[1]
    
    def _get_children_of_chance_node(self, current_node):
        # todo 
        return [] 

    def _get_children_of_player_node(self, current_node: TreeNode): 
        children = []

        if current_node.terminal: 
            return [] 
        
        foldNode = TreeNode(current_node.street, current_node.bets, Constants.players["Nobody"], current_node.board)
        foldNode.terminal = True
        children.append(foldNode)

        if self._possibleCheck(current_node): 
            checkNode = TreeNode(current_node.street, current_node.bets, 3 - current_node.current_player, current_node.board)
            if current_node.street == Constants.params["max_street"]:
                checkNode.terminal = True
            children.append(checkNode)
        
        if self._possibleBet(current_node):
            potSize = current_node.bets[0] + current_node.bets[1]
            possibleBets = [potSize]
            for i in range(len(possibleBets)): 
                newBets = Util.makeBets(possibleBets[i], current_node.bets, current_node.current_player)
                if max(newBets[0], newBets[1]) <= Constants.params["stack"]:
                    betNode = TreeNode(current_node.street, newBets, 3 - current_node.current_player, current_node.board)
                    children.append(betNode)

        if self._possibleCall(current_node): 
            callNode = TreeNode(current_node.street, Util.fill_bets(current_node.bets), Constants.players["Nobody"], current_node.board)
            if current_node.street == Constants.params["max_street"]:
                callNode.terminal = True
            children.append(callNode)
        
        # todo: implement terminal call. 
                
        return children 
    
    