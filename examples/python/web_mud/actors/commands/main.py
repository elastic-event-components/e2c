from typing import Callable

from examples.python.web_mud.contracts.token import FToken
from examples.python.web_mud.contracts.models import Room


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