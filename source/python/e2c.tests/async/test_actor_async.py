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
from e2c.async import actor_async as actor
from e2c.async import event_async as event
from e2c.async import session_async as session


def new_actor(name: str, callable_obj):
    sess = session.Session()
    return actor.Actor(sess, name, callable_obj)


@pytest.mark.asyncio
async def test_on__error_on_empty_name():
    actor = new_actor('A', lambda: None)
    with pytest.raises(errors.E2CActorError) as info:
        await actor.on('', new_actor('test', lambda: None))

    assert str(info.value) == 'Name cannot be None or empty!'


@pytest.mark.asyncio
async def test_on__error_on_none_name():
    actor = new_actor('A', lambda: None)
    with pytest.raises(errors.E2CActorError) as info:
        await actor.on(None, new_actor('test', lambda: None))

    assert str(info.value) == 'Name cannot be None or empty!'


@pytest.mark.asyncio
async def test_name():
    actor = new_actor('A', lambda: None)

    assert actor.name == 'A'


@pytest.mark.asyncio
async def test_on__double_name():
    actor = new_actor('A', lambda: None)
    child_actor1 = new_actor('B', lambda: None)
    child_actor2 = new_actor('C', lambda: None)
    actor.on('B', child_actor1)
    actor.on('B', child_actor2)

    assert len(actor.actors.keys()) == 1
    assert len(actor.actors['B']) == 2


@pytest.mark.asyncio
async def test_run__error_on_none_callable():
    actor = new_actor('A', None)
    with pytest.raises(errors.E2CActorError) as info:
        await actor.run()
    assert str(info.value) == 'Actor A has no callable function!'


@pytest.mark.asyncio
async def test_run__call_actor():
    result = []

    async def action(x):
        result.append(x)

    actor = new_actor('A', action)

    assert await actor.run(1) == None
    assert result[0] == 1

@pytest.mark.asyncio
async def test_run__call_function_actor():
    async def actor(a):
        result.append(a)

    result = []
    await new_actor('A', actor).run(1)

    assert result[0] == 1

@pytest.mark.asyncio
async def test_run__inject_actor():
    async def actor_a(a):
        result.append(a)

    async def actor_b():
        pass

    result = []
    root = new_actor('A', actor_a)
    root.on('a', new_actor('a', actor_b))
    await root.run()

    assert isinstance(result[0], event.Event)
    evt = cast(event.Event, result[0])
    assert isinstance(evt._actor.callable, type(actor_b))


@pytest.mark.asyncio
async def test_run_with_params_inject_actor():
    async def actor(a, b, c):
        result.append([a, b, c])

    result = []
    actor = new_actor('A', actor)
    params = [1, True, 'dat']
    await actor.run_with_params(*params)

    assert result[0] == [1, True, 'dat']


@pytest.mark.asyncio
async def test_spec():
    async def actor(a, b: str, c: int, d: bool, e: float, f: List, g: Dict):
        pass

    params = new_actor('A', actor).specs

    assert len(params) == 7
    assert params['a'] == Any
    assert params['b'] == str
    assert params['c'] == int
    assert params['d'] == bool
    assert params['e'] == float
    assert params['f'] == List
    assert params['g'] == Dict


@pytest.mark.asyncio
async def test_clone():
    def actor():
        pass

    cln = new_actor('A', actor)
    cln.on('B', new_actor('B', actor))
    cln.on('C', new_actor('C', actor))
    clone = cln.clone()

    assert clone.name == 'A'
    assert clone.callable == actor
    assert len(clone.actors) == 2

    assert len(clone.actors['B']) == 1
    assert clone.actors['B'][0].callable == actor
    assert clone.actors['C'][0].callable == actor
