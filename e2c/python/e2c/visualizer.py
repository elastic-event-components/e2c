import os
from typing import Dict

from graphviz import Digraph

from .node import Node


def visualize(folder: str, name, nodes: Dict[str, Node]):
    graph_attr = {'label': name, 'labeljust': 'r'}  # {'rankdir': 'LR', } #'splines': 'ortho',}# 'nodesep':'1'}
    edge_attr = {'color': 'blue', 'labelheadcolor': 'blue', 'fontcolor': 'blue'}
    dot = Digraph(comment=name, graph_attr=graph_attr, edge_attr=edge_attr)

    for output_name, output_node in nodes.items():
        for output_channel, inputs in output_node.nodes.items():
            if output_name == '•':
                dot.node(output_name, None, {'color': 'green'})
            for input_node in inputs:
                if input_node.name == '.end':
                    dot.node(input_node.name, None, {'color': 'green'})

                edge_attr = {}
                if output_channel == 'err':
                    edge_attr = {'color': 'red', 'fontcolor': 'red'}
                elif output_channel == 'trace':
                    edge_attr = {'color': 'darkorchid1', 'fontcolor': 'darkorchid1'}

                dot.edge(output_name, input_node.name, label=output_channel, _attributes=edge_attr)

    dot.render(name, folder, cleanup=True)
    dot.save(name, directory=os.path.join(folder or '', 'dot'))
