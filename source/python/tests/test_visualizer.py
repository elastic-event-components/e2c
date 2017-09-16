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

import os
import tempfile
from typing import Dict

import pytest
from e2c import const
from e2c import errors
from e2c.actor import Actor
from e2c.session import Session
from e2c.visualizer import Visualizer


def get_graph_file(file_name):
    graph_folder = os.path.join(
        os.path.dirname(__file__), 'graph')
    return os.path.join(graph_folder, file_name)


def get_temp_folder():
    dir = os.path.join(tempfile.gettempdir(), 'e2c')
    os.makedirs(dir, exist_ok=True)
    return dir


def test_run__error_on_no_configuration():
    session = Session()
    root = Actor(session, const.SELF, None)

    folder = get_temp_folder()
    vis = Visualizer({const.SELF: root})
    with pytest.raises(errors.E2CVisualizeError) as info:
        vis.run(folder, "my_name")
    assert str(info.value) == 'Graph is empty!'


def test_run__create():
    session = Session()
    actors: Dict[str, Actor] = {}

    b_actor = Actor(session, 'B', None)
    actors['B'] = b_actor

    a_actor = Actor(session, 'A', None)
    a_actor.on('write', Actor(session, const.OUT, None))
    a_actor.on('write', b_actor)
    actors['A'] = a_actor

    root = Actor(session, const.SELF, None)
    root.on(const.RUN, a_actor)
    root.on(const.ERR, Actor(session, 'E', None))
    root.on(const.TRC, Actor(session, 'T', None))
    actors[const.SELF] = root

    folder = get_temp_folder()
    vis = Visualizer(actors)
    vis.run(folder, "my_name")

    assert os.path.exists(
        os.path.join(folder, 'my_name.pdf'))
