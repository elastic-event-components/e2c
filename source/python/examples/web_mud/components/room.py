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
from actors import repository
from actors import web

folder = path.dirname(__file__)


def run_show(cmd: str, out: Callable[[str], None]) -> None:
    sess = e2c.Session[str, str]()

    sess.actor('show_room', commands.room.show_room)

    sess.actor('get_avatar[id]', repository.avatar.get_by_id)
    sess.actor('get_current_avatar', commands.avatar.get_current_avatar)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)

    sess.actor('get_room[id]', repository.room.get_or_create_by_id)
    sess.actor('get_exits[id]', repository.exit.get_list)

    sess.load_graph(folder + '/config/room/show_room.e2c')
    # sess.visualize('components/graphviz/room')

    sess.run_continues(cmd, out)


def run_move(cmd: str, out: Callable[[str], None]) -> None:
    sess = e2c.Session[str, str]()

    sess.actor('move_to_room', commands.room.move_to_room)
    sess.actor('show_room', run_show)
    sess.actor('get_avatar[id]', repository.avatar.get_by_id)
    sess.actor('get_current_avatar', commands.avatar.get_current_avatar)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)

    sess.actor('get_next_position', repository.exit.get_next_position)
    sess.actor('update_avatar', repository.avatar.update)

    sess.load_graph(folder + '/config/room/move_to_room.e2c')
    # sess.visualize('components/graphviz/room')

    sess.run_continues(cmd, out)
