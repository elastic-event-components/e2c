from typing import Generic, TypeVar, List

Response = TypeVar('Response')


class Param(Generic[Response]):
    def __init__(self, node: 'Node', continues: List['Node']) -> None:
        self.node = node
        self.continues = continues

    def __call__(self, *args, **kwargs):
        params = resolve(self.node, list(args))
        result = self.node.run_with_params(*params)
        for continues_node in self.continues:
            continues_node.run(*args)
        return result


def resolve(node: 'Node', values=[]):
    params: List = []
    for param_name in node.specs:
        nodes = node.nodes.get(param_name)
        input_node = nodes[0] if nodes else None
        if not input_node and values:
            params.append(values.pop(0))
        elif input_node:
            param = Param(input_node, nodes[1:])
            params.append(param)
    return params
