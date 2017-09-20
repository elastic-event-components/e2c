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
    List

from .actor import Actor


class Callable(object):
    """ A wrapper around a callable function.
    """

    def __init__(self, actor: Actor, continues: List[Actor]) -> None:
        """
        A wrapper around a callable function.

        :type actor: :class:`e2c.actor.Actor`
        :param actor: The actor.

         :type continues: :class:`List[e2c.actor.Actor]`
        :param continues: The related actors.
        """
        self._actor = actor
        self._continues = continues

    def __call__(self, *args, **kwargs):
        """
        The function to make :class:`Callable` callable.

        :param args: The arguments.
        :param kwargs: The kwargs.
        :rtype: object
        :return: The result of the callable function.
        """
        return self.invoke(*args)

    def invoke(self, *args) -> object:
        """
        The function to call the actor.

       :param args: The arguments.
       :rtype: object
       :return: The result of the callable function.
       """
        from .resolve import resolve
        params = resolve(self._actor, list(args))
        result = self._actor.run_with_params(*params)
        for continues_actor in self._continues:
            continues_actor.run(*args)
        return result
