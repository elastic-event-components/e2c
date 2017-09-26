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

from contracts.models import Exit
from contracts.models import Room


def get_list(avatar_id: int, room_id: int, get_room: Callable[[int, int], Room]) -> list:
    from ..repository import ExitModel

    exits = []
    for entity in ExitModel.select().where(ExitModel.room_id == room_id):
        if not entity.name:
            entity.name = get_room(avatar_id, entity.target_id).name
        exits.append(Exit(entity))
    return sorted(exits, key=lambda x: x.direction)


def get_next_position(position: int, direction: str) -> None:
    from ..repository import ExitModel

    for entity in ExitModel.select().where(
                    ExitModel.room_id == position,
                    ExitModel.direct == direction):
        return entity.target_id
    return None
