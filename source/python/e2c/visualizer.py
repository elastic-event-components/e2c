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

from . import const
from . import errors
from .actor import Actor


class Visualizer(object):
    """
    The class to visualize actors and relations.
    """

    def __init__(self, actors: Dict[str, Actor]):
        """
        The class to visualize actors and relations.

        :type actors: :class:`Dict[str, Actor]`
        :param actors: The actors to analyse.
        """
        self._actors = actors

    def run(self, folder: str, name: str):
        """
        Starts the visualizing.

        :type folder: str
        :param folder: The folder to store the output.

        :type name: str
        :param name: The name of the graph.

        :rtype: None
        """
        graph_attr = {'label': name, 'labeljust': 'r'}  # {'rankdir': 'LR', } #'splines': 'ortho',}# 'actorsep':'1'}
        edge_attr = {'color': 'orange', 'fontcolor': 'orange'}
        actor_attr = {'color': 'black', 'fontcolor': 'black'}

        dot = Digraph(comment=name, graph_attr=graph_attr, node_attr=actor_attr, edge_attr=edge_attr)
        dot.format = "png"
        any_actor = False
        for left_actor_name, left_actor in self._actors.items():
            for left_param, right_actors in left_actor.actors.items():

                any_actor = True
                if left_actor_name == const.SELF:
                    dot.node(left_actor_name, None, {'color': 'orange'})
               
                for relation_actor in right_actors:
                    if relation_actor.name == const.OUT:
                        dot.node(relation_actor.name, None, {'color': 'orange'})

                    edge_attr = {}
                    if left_param == const.ERR:
                        edge_attr = {'color': 'red', 'fontcolor': 'red'}
                    elif left_param ==  const.TRC:
                        edge_attr = {'color': 'darkorchid1', 'fontcolor': 'darkorchid1'}

                    dot.edge(left_actor_name, relation_actor.name, label=left_param, _attributes=edge_attr)

        if not any_actor:
            raise errors.E2CVisualizeError('Graph is empty!')

        dot.render(name, folder, cleanup=True)
        #dot.save(name, directory=os.path.join(folder or '', 'dot'))
