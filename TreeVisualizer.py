import os
import subprocess

from Constants import Constants
from Util import cards_to_string


class TreeVisualizer:
    def __init__(self):
        pass

    def node_to_graphviz(self, node):
        out = {}
        out["label"] = f"<f0>{node.current_player}"

        if node["terminal"]:
            if node["type"] == Constants.node_types["terminal_fold"]:
                out["label"] += "| TERMINAL FOLD"
            elif node["type"] == Constants.node_types["terminal_call"]:
                out["label"] += "| TERMINAL CALL"
            else:
                raise ValueError("unknown terminal node type")
        else:
            out["label"] += f"| bet1: {node['bets'][0]} | bet2: {node['bets'][1]}"

        if node["street"]:
            out[
                "label"
            ] += f"| street: {node['street']} | board: {cards_to_string(node['board'])} | depth: {node['depth']}"

        return out

    def graphviz_dfs(self, root, nodes, edges):
        gv_node = self.node_to_graphviz(root)
        nodes.append(gv_node)

    def graphviz(self, root, filename):
        data_directory = "./"

        filename = filename or "tree.dot"

        out = 'digraph g {  graph [ rankdir = "LR"];node [fontsize = "16" shape = "ellipse"]; edge [];'

        nodes = []
        edges = []
        self.graphviz_dfs(root, nodes, edges)

        for node in nodes:
            node_text = f"{node.name}[label={node.label} shape={node.shape}];"
            out += node_text

        for edge in edges:
            edge_text = f'{edge.id_from}:f0 -> {edge.id_to}:f0 [id = {edge.id} label = "{edge.strategy}"];'
            out += edge_text

        # write into dot file
        file_path = os.path.join(data_directory, "Dot", filename)
        with open(file_path, "w") as file:
            file.write(out)

        command = f"dot {data_directory}Dot/{filename} -Tpng -O"

        try:
            completed_process = subprocess.run(
                command,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Check for any errors
            if completed_process.returncode == 0:
                # Print the standard output
                print("Output:")
                print(completed_process.stdout)
            else:
                # Print the error output
                print("Error:")
                print(completed_process.stderr)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
