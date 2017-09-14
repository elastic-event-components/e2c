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
        else:
            params.append(None)
    return params
