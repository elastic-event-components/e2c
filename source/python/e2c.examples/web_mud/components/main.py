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

from os import path
from typing import Callable

import e2c

from actors import commands
from actors import web
from components import room

folder = path.dirname(__file__)


def trace(actor: str):
    if actor == 'show_room':
        web.session.set_state('main', '')


def run(cmd: str, out: Callable[[str], None]) -> None:
    sess = e2c.Session[str, str]()
    sess.actor('trace', trace)
    sess.actor('main', commands.main.run)
    sess.actor('show_room', room.run_show)
    sess.actor('move_avatar', room.run_move)
    sess.load_graph(folder + '/config/main.e2c')
    start_actor = web.session.get_state('main')
    sess.run_continues(cmd, out, start_actor)
