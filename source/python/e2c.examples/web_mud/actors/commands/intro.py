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


def run(cmd: str,
        out: Callable[[str], None],
        new: Callable[[str], None],
        load: Callable[[str], None]):
    if not cmd:
        text = (
            'Du stehst vor einer verschlossenen Tür.<br>'
            'Auf der rechten Seite vor der Tür steht eine Wache die grimmig guckt.<br>'
            '<br>'
            'Die Wache sagt:<br><br>'
            '''Willkommen in unserer Stadt.<br>'''
            '''Wenn du hier durch möchtest, dann verrate mir erst deinen Namen.<br>'''
            '<br>'
            'Wie heisst Du denn ("neu" für neuen Avatar)?<br>')
        out(text)
    elif cmd == 'neu':
        new('')
    else:
        load(cmd)
