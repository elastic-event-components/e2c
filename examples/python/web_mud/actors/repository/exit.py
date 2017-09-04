from typing import Callable

from examples.python.web_mud.contracts.models import Exit
from examples.python.web_mud.contracts.models import Room


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
