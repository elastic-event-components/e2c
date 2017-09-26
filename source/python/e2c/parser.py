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

from typing import \
    Dict, \
    List, \
    Callable

from . import const
from . import errors
from .actor import Actor


class Parser(object):
    """
    Represents a class to parse the graph and build relations between them.
    """

    def __init__(self, actors: Dict[str, Actor], create_actor: Callable[[str], Actor]):
        """
        Represents a class to parse the graph and build relations between them.

        :type actors: :class:`Dict[str, Actor]`
        :param actors: The list to add the handeled actors.

        :type create_actor: type: `Callable[[str], Actor]`
        :param create_actor: The function to build new actors.
        """
        self._actors = actors
        self._create_actor = create_actor

    def run(self, script: List[str], out_name: Callable[[str], None]):
        """
        Starts the parsing.

        :type script: List[str]
        :param script: The script to parse.

        :type out_name: Callable[[str], Actor]
        :param out_name: The function to receive the name of graph.

        :rtype: None
        """
        if not ''.join(script):
            raise errors.E2CParserError('No data to parse!')

        for index, line in enumerate(script, 1):
            line = line.replace('\n', '').replace(' ', '').strip()

            pos = line.find(const.COMMENT)
            if pos >= 0:
                line = line[:pos] if line else None
            if not line:
                continue

            if line.startswith('[') and line.endswith(']'):
                out_name(line[1:-1])
                continue

            if const.EDGE not in line:
                raise errors.E2CParserError(
                    'Missing {} in line {}!'.format(const.EDGE, index))

            left_actor_name_and_param, right_actor_name = line.split(const.EDGE)
            if not right_actor_name:
                raise errors.E2CParserError(
                    'Missing actor in line {}!'.format(index))

            left_actor_name, left_param = left_actor_name_and_param.split('.', 1)
            left_actor_name = left_actor_name or const.SELF

            if left_actor_name not in self._actors:
                self._actors[left_actor_name] = \
                    self._create_actor(left_actor_name)

            if right_actor_name not in self._actors:
                self._actors[right_actor_name] = \
                    self._create_actor(right_actor_name)

            self._actors[left_actor_name].on(
                left_param, self._actors[right_actor_name])
