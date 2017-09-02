from typing import Callable, List

from examples.python.web_mud.contracts.models import Avatar
from examples.python.web_mud.contracts.models import Exit
from examples.python.web_mud.contracts.models import Room
from examples.python.web_mud.contracts.token import FToken


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

