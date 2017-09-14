from os import path
from typing import Callable

import e2c

from examples.python.web_mud.actors import commands
from examples.python.web_mud.actors import repository
from examples.python.web_mud.actors import web

folder = path.dirname(__file__)


def run_show(cmd: str, out: Callable[[str], None]) -> None:
    sess = e2c.Session[str, str]()

    sess.actor('show_room', commands.room.show_room)

    sess.actor('get_avatar[id]', repository.avatar.get_by_id)
    sess.actor('get_current_avatar', commands.avatar.get_current_avatar)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)

    sess.actor('get_room[id]', repository.room.get_or_create_by_id)
    sess.actor('get_exits[id]', repository.exit.get_list)

    sess.load_graph(folder + '/config/room/show_room.e2c')
    # sess.visualize('components/graphviz/room')

    sess.run_continues(cmd, out)


def run_move(cmd: str, out: Callable[[str], None]) -> None:
    sess = e2c.Session[str, str]()

    sess.actor('move_to_room', commands.room.move_to_room)
    sess.actor('show_room', run_show)
    sess.actor('get_avatar[id]', repository.avatar.get_by_id)
    sess.actor('get_current_avatar', commands.avatar.get_current_avatar)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)

    sess.actor('get_next_position', repository.exit.get_next_position)
    sess.actor('update_avatar', repository.avatar.update)

    sess.load_graph(folder + '/config/room/move_to_room.e2c')
    # sess.visualize('components/graphviz/room')

    sess.run_continues(cmd, out)
