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

from actors import commands
from actors import repository
from actors import web
from components import main
from components import setup
from flask import Flask, render_template, request

import e2c

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


def trace(actor: str):
    if actor in ['setup', 'main']:
        web.session.set_state('app', actor)


@app.route('/', methods=['GET', 'POST'])
def root():
    output = []
    sess = e2c.Session[str, str]()
    sess.load_graph('app.e2c')

    sess.actor('trace', trace)
    sess.actor('intro', commands.intro.run)
    sess.actor('setup', setup.run)
    sess.actor('main', main.run)

    sess.actor('get_avatar_by_name', repository.avatar.get_by_name)
    sess.actor('load_avatar_by_name', commands.avatar.load_avatar_by_name)
    sess.actor('set_avatar_to_session', web.session.set_avatar_to_session)

    # sess.visualize('components/graphviz')

    def collect_data(result: str):
        output.append(str(result))

    input_data = request.form.get('input', '')
    start_actor = web.session.get_state('app')
    sess.run_continues(input_data, collect_data, start_actor)

    return render_template(
        'form.html', input=input_data, output="".join(output))


if __name__ == "__main__":
    app.run(port=3000)
