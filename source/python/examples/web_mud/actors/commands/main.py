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

from typing import Callable

from contracts.token import FToken
from contracts.models import Room


def run(cmd: str,
        show_room: Callable[[str], None],
        move_avatar: Callable[[str], None],
        out: Callable[[str], None]):
    cmd = cmd.lower()
    if cmd in Room.DIRECTIONS:
        move_avatar(cmd)
    elif not cmd or cmd == 'schau':
        show_room(cmd)
    else:
        show_room('')
        out(FToken.wrap('<br>Das kenne ich nicht!', FToken.error))