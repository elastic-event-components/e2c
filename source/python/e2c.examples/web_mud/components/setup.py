#
# Copyright 2017 The E2C Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from os import path
from typing import Callable

import e2c

from actors import commands
from actors import repository
from actors import web

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

    sess.load_graph(folder + '/config/setup/avatar_name.e2c')
    # sess.visualize('components/graphviz/setup')
    sess.run_continues(cmd, out)


def run_avatar_password(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    sess = e2c.Session[str, str]()
    sess.actor('set_avatar_password', commands.avatar.set_avatar_password)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    sess.actor('store_avatar_password', repository.avatar.store_password)
    sess.actor('restart', lambda next: next(''))
    sess.actor('.next', next)

    sess.load_graph(folder + '/config/setup/avatar_password.e2c')
    # sess.visualize('components/graphviz/setup')
    sess.run_continues(cmd, out)


def run_avatar_race(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    sess = e2c.Session[str, str]()
    sess.actor('set_avatar_race', commands.avatar.set_avatar_race)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    sess.actor('store_avatar_race', repository.avatar.store_race)
    sess.actor('restart', lambda next: next(''))
    sess.actor('.next', next)

    sess.load_graph(folder + '/config/setup/avatar_race.e2c')
    # sess.visualize('components/graphviz/setup')
    sess.run_continues(cmd, out)


def run_avatar_sex(cmd, out: Callable[[str], None], next: Callable[[None], None]):
    sess = e2c.Session[str, str]()
    sess.actor('set_avatar_sex', commands.avatar.set_avatar_sex)
    sess.actor('get_avatar_id_from_session', web.session.get_avatar_id_from_session)
    sess.actor('store_avatar_sex', repository.avatar.store_sex)
    sess.actor('restart', lambda next: next(''))
    sess.actor('.next', next)

    sess.load_graph(folder + '/config/setup/avatar_sex.e2c')
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

    sess.load_graph(folder + '/config/setup.e2c')
    sess.visualize('components/graphviz/setup')

    start_actor = web.session.get_state('setup')
    sess.run_continues(cmd, out, start_actor)
