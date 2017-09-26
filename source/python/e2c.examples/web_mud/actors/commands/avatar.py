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

from typing import Callable

from contracts.models import Avatar
from contracts.models import Race
from contracts.token import FToken

def set_avatar_name(cmd: str, ask: Callable[[str], None], store: Callable[[str], None]):
    if not cmd:
        text = (
            'Denk Dir jetzt bitte einen Namen für Deinen neuen Charakter aus.<br>'
            '<br>'
            'Der Name sollte mindestens drei und höchstens 15 Buchstaben lang sein.<br>'
            'Bedenke: Nachträglich kann Dein Name nicht mehr geändert werden!<br>'
            'Wie möchtest Du in diesem Spiel heissen?<br>'
            'Name:')
        ask(text)
    elif cmd in ['neu', 'admin']:
        raise Exception(FToken.wrap('Dieser Name ist nicht zulässig.<br><br>', FToken.error))
    elif len(cmd) < 3:
        raise Exception(FToken.wrap('%s ist zu kurz.<br>' % cmd, FToken.error))
    else:
        store(cmd)


def set_avatar_password(cmd: str, ask: Callable[[str], None], store: Callable[[str], None]):
    if not cmd:
        text = (
            'Wähle ein Passwort:<br>'
            'Dein Passwort muss wenigstens 6 Zeichen lang sein.<br>'
            'Bitte gib jetzt ein Passwort an:<br>')
        ask(text)
    elif len(cmd) < 6:
        raise Exception(FToken.wrap('Dein Passwort ist zu kurz.<br><br>', FToken.error))
    else:
        store(cmd)


def set_avatar_race(cmd: str, ask: Callable[[str], None], store: Callable[[str], None]):
    if not cmd:

        def races_to_text():
            return "<br>".join([str(a[0]) + ". " + a[1] for a in Race.races])

        text = (
            'Welcher Rasse möchtest du in dieser Welt angehören?<br>'
            'Eine Rasse kann jederzeit gewechselt werden.<br>'
            'Derzeit stehen folgende Rassen zur Auswahl:<br><br>'
            '%s<br><br>'
            'Durch Eingabe einer Ziffer wählst Du die Rasse aus.<br>' % races_to_text())
        ask(text)
    elif cmd not in [a[0] for a in Race.races]:
        raise Exception(FToken.wrap('Die Eingabe war ungültig.<br><br>', FToken.error))
    else:
        store(Race.races[int(cmd) - 1][1])


def set_avatar_sex(cmd: str, ask: Callable[[str], None], store: Callable[[str], None]):
    if not cmd:
        text = 'Bist du männlich oder weiblich?<br>'
        ask(text)
    elif cmd not in ['m', 'w', 'männlich', 'weiblich']:
        raise Exception(FToken.wrap('Die Eingabe war ungültig.<br><br>', FToken.error))
    else:
        if cmd == 'm':
            cmd = 'männlich'
        if cmd == 'w':
            cmd = 'weiblich'
        store(cmd)


def load_avatar_by_name(
        name: str, get_avatar: Callable[[str], Avatar],
        set_avatar_to_session: Callable[[int], None],
        load_world: Callable[[None], None]):
    avatar = get_avatar(name)
    if avatar:
        set_avatar_to_session(avatar.id)
        load_world('')


def get_current_avatar(
        get_avatar_id: Callable[[None], None],
        get_avatar: Callable[[int], Avatar]) -> Avatar:
    avatar_id = get_avatar_id()
    return get_avatar(avatar_id)

