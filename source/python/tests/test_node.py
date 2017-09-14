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

from typing import cast, Any, List, Dict

import pytest
from e2c import errors
from e2c import node
from e2c import resolve
from e2c import session


def new_node(name: str, callable):
    sess = session.Session()
    return node.Node(sess, name, callable)


def test_on__error_on_empty_name():
    node = new_node('A', lambda: None)
    with pytest.raises(errors.E2CNodeError) as info:
        node.on('', new_node('test', lambda: None))
    assert str(info.value) == 'Channel name cannot be None or empty!'


def test_on__error_on_none_name():
    node = new_node('A', lambda: None)
    with pytest.raises(errors.E2CNodeError) as info:
        node.on(None, new_node('test', lambda: None))
    assert str(info.value) == 'Channel name cannot be None or empty!'


def test_name():
    node = new_node('A', lambda: None)
    assert node.name == 'A'


def test_on__double_name():
    node = new_node('A', lambda: None)
    child_node1 = new_node('B', lambda: None)
    child_node2 = new_node('C', lambda: None)
    node.on('B', child_node1)
    node.on('B', child_node2)
    assert len(node.nodes.keys()) == 1
    assert len(node.nodes['B']) == 2


def test_run__error_on_none_callable():
    node = new_node('A', None)
    with pytest.raises(errors.E2CNodeError) as info:
        node.run()
    assert str(info.value) == 'Node A has no callable function!'


def test_run__call_actor():
    result = []
    node = new_node('A', lambda x: result.append(x))

    assert node.run(1) == None
    assert result[0] == 1


def test_run__call_lambda_actor():
    result = []
    a = new_node('A', lambda x: result.append(x)).run(1)

    assert result[0] == 1


def test_run__call_function_actor():
    def actor(a):
        result.append(a)

    result = []
    new_node('A', actor).run(1)

    assert result[0] == 1


def test_run__inject_actor():
    def actor_a(a):
        result.append(a)

    def actor_b():
        pass

    result = []
    root = new_node('A', actor_a)
    root.on('a', new_node('a', actor_b))
    root.run()

    assert isinstance(result[0], resolve.Param)
    param = cast(resolve.Param, result[0])
    assert isinstance(param.node.callable, type(actor_b))


def test_run_with_params_inject_actor():
    def actor(a, b, c):
        result.append([a, b, c])

    result = []
    node = new_node('A', actor)
    params = [1, True, 'dat']
    node.run_with_params(*params)

    assert result[0] == [1, True, 'dat']


def test_spec():
    def actor(a, b: str, c: int, d: bool, e: float, f: List, g: Dict):
        pass

    params = new_node('A', actor).specs

    assert len(params) == 7
    assert params['a'] == Any
    assert params['b'] == str
    assert params['c'] == int
    assert params['d'] == bool
    assert params['e'] == float
    assert params['f'] == List
    assert params['g'] == Dict


def test_clone():
    def actor():
        pass

    cln = new_node('A', actor)
    cln.on('B', new_node('B', actor))
    cln.on('C', new_node('C', actor))
    clone = cln.clone()

    assert clone.name == 'A'
    assert clone.callable == actor
    assert len(clone.nodes) == 2

    assert len(clone.nodes['B']) == 1
    assert clone.nodes['B'][0].callable == actor
    assert clone.nodes['C'][0].callable == actor
