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

from typing import Dict

from . import errors
from .actor import Actor


class Analyser(object):
    """
    The class to analyse actors and relations.
    """

    def __init__(self, actors: Dict[str, Actor]):
        """
        The class to analyse actors and relations.

        :type actors: :class:`Dict[str, Actor]`
        :param actors: The actors to analyse.
        """
        self._actors = actors

    def run(self, quiet=True):
        """
        Starts the analysing.

        :type quiet: bool
        :param quiet: False to print outputs on the command line.

        :rtype: None
        """
        for actor_name, output_actor in self._actors.items():
            if not quiet:
                print('\t', actor_name)

            if not output_actor.callable:
                raise errors.E2CAnalyserError(
                    'Actor {} has no callable function!'.format(actor_name))

            if not hasattr(output_actor.callable, '__call__'):
                raise errors.E2CAnalyserError(
                    'Actor {} is not a callable function!'.format(actor_name))

            for output_parameter, actors in output_actor.actors.items():
                for input_actor in actors:
                    if not quiet:
                        print('\t\t', (output_parameter, input_actor.name))
                    if not output_parameter in output_actor.specs:
                        raise errors.E2CAnalyserError(
                            '{} on actor {} is not a parameter in the callable function!'.format(
                                output_parameter, actor_name))