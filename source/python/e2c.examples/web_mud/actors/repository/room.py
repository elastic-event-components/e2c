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

from typing import Dict, Callable
from contracts.models import Room

create_title = 'Nichts'
create_text = (
    'Du stehst in der unendlichen Weite. Es ist überhaupt nichts zu sehen.<br>'
    'Scheinbar wartet dieser Ort darauf mit Leben gefüllt zu werden.'
)


def get_or_create_by_id(avatar_id: int, room_id: int) -> Room:
    from ..repository import RoomModel
    try:
        return Room(RoomModel.get(RoomModel.id == room_id))
    except RoomModel.DoesNotExist:
        return Room(RoomModel.create(
            id=room_id, avatar=avatar_id, name=create_title, desc=create_text, zone=''))


def create(avatar_id: int) -> Room:
    from ..repository import RoomModel
    return Room(RoomModel.create(
        avatar=avatar_id, name=create_title, desc=create_text, zone=''))


def update(avatar: Room, data: Dict, out:Callable[[str], None]) -> None:
    from ..repository import RoomModel
    entity = RoomModel.update(**data).where(RoomModel.id == avatar.id)
    entity.execute()
    out('')
