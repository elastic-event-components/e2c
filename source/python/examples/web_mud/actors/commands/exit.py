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

from typing import Callable, List

from contracts.models import Avatar
from contracts.models import Exit
from contracts.models import Room
from contracts.token import FToken


def create_exit(cmd: str,
                get_avatar: Callable[[None], Avatar],
                show_room: Callable[[None], None],
                get_room: Callable[[int, int], Room],
                get_exists: Callable[[int, int], List[Exit]],
                store: Callable[[int, int], None],
                out: Callable[[str], None]):
    avatar = get_avatar()
    room = get_room(avatar.id, avatar.position)
    exist_list = get_exists(avatar.id, room.id)

    def show_visible_exists():
        show_room(None)
        out(FToken.wrap('<br>Mögliche Werte für einen neue Ausgang:', FToken.text))
        occ_dirs = [a.direction for a in exist_list]
        directions = [
            (" - ".join([FToken.wrap("{0}".format(a[0]), FToken.enum), a[1]]))
            for a in Room.DIRECTION_NAMES.items() if a[0] not in occ_dirs]
        out(FToken.wrap('<br>{}<br>'.format("<br>".join(directions)), FToken.text))

    if not cmd:
        show_visible_exists()
    else:
        if not cmd in Room.DIRECTIONS:
            show_visible_exists()
            out(FToken.wrap('<br>Unbekannter Ausgang', FToken.error))
            return

        directions = [a.direction for a in exist_list]
        if cmd in directions:
            show_visible_exists()
            out(FToken.wrap('<br>Ausgang "{0}" existiert bereits'.format(cmd), FToken.error))
            return

        store(avatar.id, room.id, cmd)

