from typing import Dict, Callable
from examples.python.web_mud.contracts.models import Room

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
