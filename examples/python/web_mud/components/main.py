from os import path
from typing import Callable

from e2c import E2c

from examples.python.web_mud.actors import commands
from examples.python.web_mud.actors import web
from examples.python.web_mud.components import room

folder = path.dirname(__file__)


def trace(actor: str):
    if actor == 'show_room':
        web.session.set_state('main', '')


def run(cmd: str, out: Callable[[str], None]) -> None:
    e2c = E2c[str, str]()
    e2c.actor('trace', trace)
    e2c.actor('main', commands.main.run)
    e2c.actor('show_room', room.run_show)
    e2c.actor('move_avatar', room.run_move)

    e2c.configure_by_file(folder + '/config/main.e2c')
    # e2c.visualize('components/graphviz/main')

    start_actor = web.session.get_state('main')
    e2c.run_continues(cmd, out, start_actor)
