from os import path
from typing import Callable

import e2c

from examples.python.web_mud.actors import commands
from examples.python.web_mud.actors import repository
from examples.python.web_mud.actors import web

folder = path.dirname(__file__)


def trace(actor: str):
    if actor in ['run_avatar_name', 'run_avatar_password', 'run_avatar_race', 'run_avatar_sex']:
        web.session.set_state('setup', actor)
    if actor == 'show_welcome':
        web.session.set_state('main', '')
        web.session.set_state('app', 'main')


def run_avatar_name(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    sess = e2c.Session[str, str]()
    sess.actor('set_avatar_name', commands.avatar.set_avatar_name)
    sess.actor('set_avatar_to_session', web.session.set_avatar_to_session)
    sess.actor('store_avatar_name', repository.avatar.store_name)
    sess.actor('restart', lambda next: next(''))
    sess.actor('.next', next)

    sess.configure_by_file(folder + '/config/setup/avatar_name.e2c')
    # sess.visualize('components/graphviz/setup')
    sess.run_continues(cmd, out)


def run_avatar_password(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    sess = e2c.Session[str, str]()
    sess.actor('set_avatar_password', commands.avatar.set_avatar_password)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    sess.actor('store_avatar_password', repository.avatar.store_password)
    sess.actor('restart', lambda next: next(''))
    sess.actor('.next', next)

    sess.configure_by_file(folder + '/config/setup/avatar_password.e2c')
    # sess.visualize('components/graphviz/setup')
    sess.run_continues(cmd, out)


def run_avatar_race(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    sess = e2c.Session[str, str]()
    sess.actor('set_avatar_race', commands.avatar.set_avatar_race)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    sess.actor('store_avatar_race', repository.avatar.store_race)
    sess.actor('restart', lambda next: next(''))
    sess.actor('.next', next)

    sess.configure_by_file(folder + '/config/setup/avatar_race.e2c')
    # sess.visualize('components/graphviz/setup')
    sess.run_continues(cmd, out)


def run_avatar_sex(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    sess = e2c.Session[str, str]()
    sess.actor('set_avatar_sex', commands.avatar.set_avatar_sex)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    sess.actor('store_avatar_sex', repository.avatar.store_sex)
    sess.actor('restart', lambda next: next(''))
    sess.actor('.next', next)

    sess.configure_by_file(folder + '/config/setup/avatar_sex.e2c')
    # sess.visualize('components/graphviz/setup')
    sess.run_continues(cmd, out)


def run(cmd: str, out: Callable[[str], None]):
    sess = e2c.Session[str, str]()
    sess.actor('trace', trace)
    sess.actor('run_avatar_name', run_avatar_name)
    sess.actor('run_avatar_password', run_avatar_password)
    sess.actor('run_avatar_race', run_avatar_race)
    sess.actor('run_avatar_sex', run_avatar_sex)

    sess.actor('show_welcome', commands.welcome.run)

    sess.configure_by_file(folder + '/config/setup.e2c')
    #sess.visualize('components/graphviz/setup')

    start_actor = web.session.get_state('setup')
    sess.run_continues(cmd, out, start_actor)
