from PokerTreeBuilder import PokerTreeBuilder
from TreeNode import TreeNode
from TreeVisualizer import TreeVisualizer

root = TreeNode(2, (2, 2), 1, "K")

pokerTreeBuilder = PokerTreeBuilder()

pokerTreeBuilder.build_tree(root)

visualizer = TreeVisualizer()

visualizer.graphviz(root, "tree")
