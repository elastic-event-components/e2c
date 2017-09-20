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

from e2c import actor
from e2c import callable
from e2c import session
from e2c import resolve


def new_actor(name: str, callable):
    sess = session.Session()
    return actor.Actor(sess, name, callable)


def test_param__call():
    data = []
    actor = new_actor('A', lambda: data.append('1'))
    param = callable.Callable(actor, [])
    param()
    assert data[0] == '1'


def test_resolve__value():
    data = []

    def actor(a, b, c, func_a, func_b):
        data.append([a, b, c, func_a, func_b])

    actor = new_actor('A', actor)
    params1 = resolve.resolve(actor, [1, 'data', True])
    params2 = resolve.resolve(actor, [])

    assert len(params1) == 5
    assert params1 == [1, 'data', True, None, None]
    assert params2 == [None, None, None, None, None]
