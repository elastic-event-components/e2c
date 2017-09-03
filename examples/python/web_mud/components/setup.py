from os import path
from typing import Callable

from e2c import E2c

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
    e2c = E2c[str, str]()
    e2c.actor('set_avatar_name', commands.avatar.set_avatar_name)
    e2c.actor('set_avatar_to_session', web.session.set_avatar_to_session)
    e2c.actor('store_avatar_name', repository.avatar.store_name)
    e2c.actor('restart', lambda next: next(''))
    e2c.actor('.next', next)

    e2c.configure_by_file(folder + '/config/setup/avatar_name.e2c')
    # e2c.visualize('components/graphviz/setup')
    e2c.run_continues(cmd, out)


def run_avatar_password(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    e2c = E2c[str, str]()
    e2c.actor('set_avatar_password', commands.avatar.set_avatar_password)
    e2c.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    e2c.actor('store_avatar_password', repository.avatar.store_password)
    e2c.actor('restart', lambda next: next(''))
    e2c.actor('.next', next)

    e2c.configure_by_file(folder + '/config/setup/avatar_password.e2c')
    # e2c.visualize('components/graphviz/setup')
    e2c.run_continues(cmd, out)


def run_avatar_race(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    e2c = E2c[str, str]()
    e2c.actor('set_avatar_race', commands.avatar.set_avatar_race)
    e2c.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    e2c.actor('store_avatar_race', repository.avatar.store_race)
    e2c.actor('restart', lambda next: next(''))
    e2c.actor('.next', next)

    e2c.configure_by_file(folder + '/config/setup/avatar_race.e2c')
    # e2c.visualize('components/graphviz/setup')
    e2c.run_continues(cmd, out)


def run_avatar_sex(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    e2c = E2c[str, str]()
    e2c.actor('set_avatar_sex', commands.avatar.set_avatar_sex)
    e2c.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    e2c.actor('store_avatar_sex', repository.avatar.store_sex)
    e2c.actor('restart', lambda next: next(''))
    e2c.actor('.next', next)

    e2c.configure_by_file(folder + '/config/setup/avatar_sex.e2c')
    # e2c.visualize('components/graphviz/setup')
    e2c.run_continues(cmd, out)


def run(cmd: str, out: Callable[[str], None]):
    e2c = E2c[str, str]()
    e2c.actor('trace', trace)
    e2c.actor('run_avatar_name', run_avatar_name)
    e2c.actor('run_avatar_password', run_avatar_password)
    e2c.actor('run_avatar_race', run_avatar_race)
    e2c.actor('run_avatar_sex', run_avatar_sex)

    e2c.actor('show_welcome', commands.welcome.run)

    e2c.configure_by_file(folder + '/config/setup.e2c')
    # e2c.visualize('components/graphviz/setup')

    start_actor = web.session.get_state('setup')
    e2c.run_continues(cmd, out, start_actor)
