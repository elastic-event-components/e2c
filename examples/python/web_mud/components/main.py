from os import path
from typing import Callable

import e2c

from examples.python.web_mud.actors import commands
from examples.python.web_mud.actors import web
from examples.python.web_mud.components import room

folder = path.dirname(__file__)


def trace(actor: str):
    if actor == 'show_room':
        web.session.set_state('main', '')


def run(cmd: str, out: Callable[[str], None]) -> None:
    sess = e2c.Session[str, str]()
    sess.actor('trace', trace)
    sess.actor('main', commands.main.run)
    sess.actor('show_room', room.run_show)
    sess.actor('move_avatar', room.run_move)
    sess.configure_by_file(folder + '/config/main.e2c')
    start_actor = web.session.get_state('main')
    sess.run_continues(cmd, out, start_actor)
