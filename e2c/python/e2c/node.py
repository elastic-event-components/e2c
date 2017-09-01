from inspect import getfullargspec
from typing import Callable, Any, Dict, List


class Node(object):
    def __init__(self, comp, name: str, callable: Callable) -> None:
        self.name = name
        self.comp = comp
        self.callable = callable
        self.nodes: Dict[str, List['Node']] = {}
        self._specs = []

    def on(self, channel: str, node: 'Node'):
        if channel not in self.nodes:
            self.nodes[channel] = []
        self.nodes[channel].append(node)

    def run(self, value=None):
        from .resolve import resolve
        params = resolve(self, [value])
        if self.comp.on_trace and self.comp.activate_trace:
            self.comp.on_trace(self.name)
        self.callable(*params)

    def run_with_params(self, *params):
        if self.comp.on_trace and self.comp.activate_trace:
            self.comp.on_trace(self.name)
        return self.callable(*params)

    def clone(self) -> 'Node':
        node = Node(self.comp, self.name, self.callable)
        for name, nodes in self.nodes.items():
            for n in nodes:
                node.on(name, n)
        return node

    @property
    def specs(self):
        if not self._specs and self.callable:
            result = getfullargspec(self.callable)
            self._specs = dict([(a, result.annotations.get(a, Any)) for a in result.args])
        return self._specs
