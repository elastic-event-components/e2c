from os import path
from typing import Callable

from e2c import E2c

from examples.python.web_mud.actors import commands
from examples.python.web_mud.actors import repository
from examples.python.web_mud.actors import web

folder = path.dirname(__file__)


def run_show(cmd: str, out: Callable[[str], None]) -> None:
    e2c = E2c[str, str]()

    e2c.actor('show_room', commands.room.show_room)

    e2c.actor('get_avatar[id]', repository.avatar.get_by_id)
    e2c.actor('get_current_avatar', commands.avatar.get_current_avatar)
    e2c.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)

    e2c.actor('get_room[id]', repository.room.get_or_create_by_id)
    e2c.actor('get_exits[id]', repository.exit.get_list)

    e2c.configure_by_file(folder + '/config/room/show_room.e2c')
    # e2c.visualize('components/graphviz/room')

    e2c.run_continues(cmd, out)


def run_move(cmd: str, out: Callable[[str], None]) -> None:
    e2c = E2c[str, str]()

    e2c.actor('move_to_room', commands.room.move_to_room)
    e2c.actor('show_room', run_show)
    e2c.actor('get_avatar[id]', repository.avatar.get_by_id)
    e2c.actor('get_current_avatar', commands.avatar.get_current_avatar)
    e2c.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)

    e2c.actor('get_next_position', repository.exit.get_next_position)
    e2c.actor('update_avatar', repository.avatar.update)

    e2c.configure_by_file(folder + '/config/room/move_to_room.e2c')
    # e2c.visualize('components/graphviz/room')

    e2c.run_continues(cmd, out)
