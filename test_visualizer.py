from TreeNode import TreeNode
from TreeVisualizer import TreeVisualizer

root = TreeNode(1, (1, 2), 1, "")

visualizer = TreeVisualizer()

visualizer.graphviz(root, "simple_tree")
