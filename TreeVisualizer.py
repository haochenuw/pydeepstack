
import os
import subprocess

from Constants import Constants
from Util import cards_to_string


class TreeVisualizer:
    def __init__(self):
        self.node_to_graphviz_counter = 0 
        self.edge_to_graphviz_counter = 0 

    def node_to_graphviz(self, node):
        out = {}
        out['name'] = f"node {self.node_to_graphviz_counter}"
        out["label"] = f"<f0>{node.current_player}"

        if node.terminal:
            if node.isCall:
                out["label"] += "| TERMINAL CALL"
            elif node.isFold: 
                out["label"] += "| TERMINAL FOLD"
            else: 
                out["label"] += "| TERMINAL CHECK"

        out["label"] += f"| bet1: {node.bets[0]} | bet2: {node.bets[1]}"

        if node.street:
            out[
                "label"
            ] += f"| street: {node.street} | board: {node.board} | depth: {node.depth}"
        
        out['shape'] = 'record'
        self.node_to_graphviz_counter += 1 

        return out

    def graphviz_dfs(self, root, nodes, edges):
        gv_node = self.node_to_graphviz(root)
        nodes.append(gv_node)

        for i in range(len(root.children)):
            child = root.children[i]
            gv_child = self.graphviz_dfs(child, nodes, edges)
            edge = self.compute_gv_edge(gv_node["name"], gv_child["name"], i)
            edges.append(edge)
        return gv_node
    
    def compute_gv_edge(self, node_name, child_name, child_index): 
        out = {}
        
        out["id_from"] = node_name
        out["id_to"] = child_name
        out["id"] = self.edge_to_graphviz_counter
        
        # out["strategy"] = self.add_tensor(node["strategy"][child_id], None, "%.2f", card_to_string.card_to_string_table)
        
        self.edge_to_graphviz_counter = self.edge_to_graphviz_counter + 1
        return out

    def graphviz(self, root, filename):
        data_directory = "./"

        filename = filename or "tree.dot"

        out = 'digraph g {  graph [ rankdir = "LR"];node [fontsize = "16" shape = "ellipse"]; edge [];'

        nodes = []
        edges = []
        self.graphviz_dfs(root, nodes, edges)

        for node in nodes:
            node_text = f"\"{node['name']}\"[label=\"{node['label']}\" shape=\"{node['shape']}\"];"
            out += node_text + "\n"; 

        for edge in edges:
            edge_text = f'\"{edge["id_from"]}\":f0 -> \"{edge["id_to"]}\":f0 [id = {edge["id"]} label = "strategy placeholder"];'
            out += edge_text + "\n"; 

        out += "}"

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
