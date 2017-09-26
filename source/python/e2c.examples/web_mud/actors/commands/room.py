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

from typing import Callable, List, Dict

from contracts.models import Avatar
from contracts.models import Exit
from contracts.models import Room
from contracts.token import FToken


def show_room(cmd: str,
              get_avatar: Callable[[None], Avatar],
              get_room: Callable[[int, int], Room],
              get_exists: Callable[[int, int], List[Exit]],
              out: Callable[[str], None]):
    avatar = get_avatar()
    room = get_room(avatar.id, avatar.position)
    name = room.name if not room.zone else room.name + ' - ' + room.zone

    out(FToken.wrap('{} ({})'.format(name, room.id), FToken.room_name) + '<br>')
    out(FToken.line)
    out(FToken.wrap('{}<br>'.format(room.description), FToken.room_desc))

    exists = [a.title for a in get_exists(avatar.id, room.id)]
    if exists:
        out(FToken.wrap('<br>Sichtbare Ausgänge:<br>', FToken.exit_title))
        for ex in exists:
            out(FToken.wrap('  {}<br>'.format(ex), FToken.exit_object))


def move_to_room(cmd: str,
                 get_avatar: Callable[[None], Avatar],
                 get_next_position: Callable[[int, int], Room],
                 update_avatar: Callable[[Avatar, Dict], None],
                 out: Callable[[str], None]):
    avatar = get_avatar()
    next_room_id = get_next_position(avatar.position, cmd)
    if next_room_id:
        avatar.position = next_room_id
        update_avatar(avatar, {'position': next_room_id})
    out('')
