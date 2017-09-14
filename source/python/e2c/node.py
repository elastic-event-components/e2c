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


from inspect import getfullargspec, ismethod
from typing import Callable, Any, Dict, List

from . import errors



class Node(object):
    def __init__(self, session, name: str, callable: Callable or None) -> None:
        self.name = name
        self.session = session
        self.callable = callable
        self.nodes: Dict[str, List['Node']] = {}
        self._specs = []

    def on(self, channel: str, node: 'Node'):
        if not channel:
            raise errors.E2CNodeError(
                'Channel name cannot be None or empty!')
        if not channel in self.nodes:
            self.nodes[channel] = []
        self.nodes[channel].append(node)

    def run(self, *args):
        from .resolve import resolve
        params = resolve(self, [*args])
        if self.session.on_trace and self.session.activate_trace:
            self.session.on_trace(self.name)
        if not self.callable:
            raise errors.E2CNodeError(
                'Node {0} has no callable function!'.format(self.name))
        self.callable(*params)

    def run_with_params(self, *params):
        if self.session.on_trace and self.session.activate_trace:
            self.session.on_trace(self.name)
        return self.callable(*params)

    def clone(self) -> 'Node':
        node = Node(self.session, self.name, self.callable)
        for name, nodes in self.nodes.items():
            for n in nodes:
                node.on(name, n)
        return node

    @property
    def specs(self):
        if not self._specs and self.callable:
            result = getfullargspec(self.callable)
            args = result.args
            if ismethod(self.callable):
                args = args[1:]  # skip self
            self._specs = dict([(a, result.annotations.get(a, Any)) for a in args])
        return self._specs
