from Arguments import params
from GameSettings import game_settings
from TreeNode import TreeNode


class TreeCFR:
    def __init__(self):
        self.regret_epsilon = 1 / 1000000000
        self._cached_terminal_equities = {}

    def _get_terminal_equity(self, node: TreeNode):
        cached = self._cached_terminal_equities.get(node.board, None)
        if cached is None:
            cached = TerminalEquity()
            cached.set_board(node.board)
            self._cached_terminal_equities[node.board] = cached

        return cached

    def cfrs_iter_dfs(self, node: TreeNode, iteration: int):
        # if
        assert (
            node.current_player == constants.players.P1
            or node.current_player == constants.players.P2
            or node.current_player == constants.players.chance
        )

        opponent_index = 3 - node.current_player

        # Dimensions in tensor
        action_dimension = 1
        card_dimension = 2

        # Compute values using terminal_equity in terminal nodes
        # Compute CF values using the TerminalEquity object, also need the ranges_absolute to be populated.
        if node.terminal:
            terminal_equity = self._get_terminal_equity(node)

            values = node.ranges_absolute.clone().fill_(0)

            if node.type == constants.node_types.terminal_fold:
                terminal_equity.tree_node_fold_value(
                    node.ranges_absolute, values, opponent_index
                )
            else:
                terminal_equity.tree_node_call_value(node.ranges_absolute, values)

            # Multiply by the pot
            values *= node.pot
            node.cf_values = values.view_as(node.ranges_absolute)

        else:
            actions_count = len(node.children)
            current_strategy = None

            if node.current_player == constants.players.chance:
                current_strategy = node.strategy
            else:
                # We have to compute the current strategy at the beginning of each iteration

                # Initialize regrets in the first iteration
                if not hasattr(node, "regrets"):
                    node.regrets = params.Tensor(
                        actions_count, game_settings.card_count
                    ).fill_(
                        self.regret_epsilon
                    )  # actions_count x card_count
                if not hasattr(node, "possitive_regrets"):
                    node.possitive_regrets = params.Tensor(
                        actions_count, game_settings.card_count
                    ).fill_(self.regret_epsilon)

                # Compute positive regrets so that we can compute the current strategy from them
                node.possitive_regrets.copy_(node.regrets)
                node.possitive_regrets[
                    node.possitive_regrets.le(self.regret_epsilon)
                ] = self.regret_epsilon

                # Compute the current strategy
                regrets_sum = node.possitive_regrets.sum(action_dimension)
                current_strategy = node.possitive_regrets.clone()
                current_strategy.cdiv_(regrets_sum.expand_as(current_strategy))

    def run_cfr(self, root, starting_ranges=None, iter_count=None):
        if starting_ranges is None:
            raise ValueError("Starting ranges must be provided")

        iter_count = iter_count or params.cfr_iters

        root.ranges_absolute = starting_ranges

        for iter in range(1, iter_count + 1):
            self.cfrs_iter_dfs(root, iter)
