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
    Generic, \
    TypeVar, \
    List

Response = TypeVar('Response')


class Param(Generic[Response]):
    """ A wrapper around a callable function.
    """

    def __init__(self, actor: 'Actor', continues: List['Actor']) -> None:
        """
        A wrapper around a callable function.

        :type actor: :class:`e2c.actor.Actor`
        :param actor: The actor.

         :type continues: :class:`List[e2c.actor.Actor]`
        :param continues: The related actors.
        """
        self.actor = actor
        self.continues = continues

    def __call__(self, *args, **kwargs):
        """
        The function to make :class:`Param` callable.

        :param args: The arguments.
        :param kwargs: The kwargs.
        :rtype: object
        :return: The result of the callable function.
        """
        params = resolve(self.actor, list(args))
        result = self.actor.run_with_params(*params)
        for continues_actor in self.continues:
            continues_actor.run(*args)
        return result


def resolve(actor: 'Actor', values: List) -> List[Param]:
    """
    The function to get a list of :class:`Param` for
    each parameter in callable function in specified actor.

    :type actor: Actor
    :param actor: The actor with the callable function to inspect the parameters.

    :type values: List
    :param values: A list of values to add to the result.

    :rtype: List[Param]
    :return: A list of parameters to call the function within class :class:`Actor`.
    """
    params: List = []
    for param_name in actor.specs:
        actors = actor.actors.get(param_name)
        input_actor = actors[0] if actors else None
        if not input_actor and values:
            params.append(values.pop(0))
        elif input_actor:
            param = Param(input_actor, actors[1:])
            params.append(param)
        else:
            params.append(None)
    return params
