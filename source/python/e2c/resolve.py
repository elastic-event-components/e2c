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
    List, Callable

from .actor import Actor
from .event import Event


def resolve(actor: Actor, values: List, eventFactory: Callable[[object, object], object]) -> List[object]:
    """
    The function to find missing parameters.

    :type actor: Actor
    :param actor: The actor, at which the parameters are verified.

    :type values: List
    :param values: A list of values to add to the parameters on the first position.

    :rtype: eventFactory: Callable[[object, object], object]
    :return: The factory to create a event.
    """
    params: List = []
    for param_name, param_type in actor.specs.items():
        actors = actor.actors.get(param_name)
        input_actor = actors[0] if actors else None
        if not input_actor and values:
            params.append(values.pop(0))
        elif input_actor:
            # ignore first actor.
            event = eventFactory(input_actor, actors[1:])
            params.append(event)
        else:
            params.append(None)
    return params
