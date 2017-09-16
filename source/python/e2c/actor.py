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


from inspect import \
    getfullargspec, \
    ismethod

from typing import \
    Callable, \
    Any,\
    Dict,\
    List

from . import errors


class Actor(object):
    """
    A wrapper around a callable function.
    """

    def __init__(self, session, name: str, callable: Callable or None) -> None:
        """
        A wrapper around a callable function.

        :type session: :class:`e2c.session.Session`
        :param session: The Session to which the Actor belong.

        :type name: str
        :param name: The name of the actor to register on the session.

        :type callable: Callable
        :param callable: Any callable function.
        """
        self.name = name
        self.session = session
        self.callable = callable
        self.actors: Dict[str, List['Actor']] = {}
        self._specs = []

    def on(self, channel: str, actor: 'Actor') -> None:
        """
        Method to register the given actor under specified channel.

        :type channel: str
        :param channel: The name to register the actor in this actor.

        :type actor: Actor
        :param actor: An instance of the actor to register.

        :rtype: None
        """
        if not channel:
            raise errors.E2CActorError(
                'Channel name cannot be None or empty!')
        if not channel in self.actors:
            self.actors[channel] = []
        self.actors[channel].append(actor)

    def run(self, *args) -> object:
        """
        Run the callable function with specified arguments.

        :type args: List[object]
        :param args: A list of arguments.

        :rtype: object
        :return: The result of the callable function.
        """
        from .resolve import resolve
        params = resolve(self, [*args])
        if self.session.on_trace and self.session.activate_trace:
            self.session.on_trace(self.name)
        if not self.callable:
            raise errors.E2CActorError(
                'Actor {0} has no callable function!'.format(self.name))
        return self.callable(*params)

    def run_with_params(self, *params) -> object:
        """
        Run the callable function with specified parameters.

        :type params: List[Param]
        :param params: A list of parameters

        :rtype: object
        :return: The result of the callable function.
        """
        if self.session.on_trace and self.session.activate_trace:
            self.session.on_trace(self.name)
        return self.callable(*params)

    def clone(self) -> 'Actor':
        """
        Get a new instance of type `Actor`

        :rtype: `Actor`
        :return: The flat clone of that actor.
        """
        actor = Actor(self.session, self.name, self.callable)
        for name, actors in self.actors.items():
            for n in actors:
                actor.on(name, n)
        return actor

    @property
    def specs(self) -> Dict[str, str]:
        """
        Getter property to get the introspection parameter
        of the internal callable function.

        :rtype: Dict[str, type]
        :return: A dictionary of name and type of any parameter.
        """
        if not self._specs and self.callable:
            result = getfullargspec(self.callable)
            args = result.args
            if ismethod(self.callable):
                args = args[1:]  # skip self
            self._specs = dict([(a, result.annotations.get(a, Any)) for a in args])
        return self._specs
