#
# Copyright 2017 The E2C Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


import os
from typing import Dict

from graphviz import Digraph

from .node import Node
from . import errors

def visualize(folder: str, name, nodes: Dict[str, Node]):
    graph_attr = {'label': name, 'labeljust': 'r'}  # {'rankdir': 'LR', } #'splines': 'ortho',}# 'nodesep':'1'}
    edge_attr = {'color': 'orange', 'fontcolor': 'orange'}
    node_attr = {'color': 'black', 'fontcolor': 'black'}

    dot = Digraph(comment=name, graph_attr=graph_attr, node_attr=node_attr, edge_attr=edge_attr)
    any_node = False
    for output_name, output_node in nodes.items():
        for output_channel, inputs in output_node.nodes.items():

            any_node = True
            if output_name == '•':
                dot.node(output_name, None, {'color': 'orange'})
            for input_node in inputs:
                if input_node.name == '.out':
                    dot.node(input_node.name, None, {'color': 'orange'})

                edge_attr = {}
                if output_channel == 'err':
                    edge_attr = {'color': 'red', 'fontcolor': 'red'}
                elif output_channel == 'trace':
                    edge_attr = {'color': 'darkorchid1', 'fontcolor': 'darkorchid1'}

                dot.edge(output_name, input_node.name, label=output_channel, _attributes=edge_attr)

    if not any_node:
        raise errors.E2CVisualizeError('Graph is empty!')

    dot.render(name, folder, cleanup=True)
    dot.save(name, directory=os.path.join(folder or '', 'dot'))
