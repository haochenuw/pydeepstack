from PokerTreeBuilder import PokerTreeBuilder
from TreeNode import TreeNode
from TreeVisualizer import TreeVisualizer

root = TreeNode(1, (1, 2), 1, "")

pokerTreeBuilder = PokerTreeBuilder()

pokerTreeBuilder.build_tree(root)

visualizer = TreeVisualizer()

visualizer.graphviz(root, "tree")
