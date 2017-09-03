from e2c import E2c
from flask import Flask, render_template, request

from examples.python.web_mud.actors import commands
from examples.python.web_mud.actors import repository
from examples.python.web_mud.actors import web
from examples.python.web_mud.components import main
from examples.python.web_mud.components import setup

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


def trace(actor: str):
    if actor in ['setup', 'main']:
        web.session.set_state('app', actor)


@app.route('/', methods=['GET', 'POST'])
def root():
    output = []
    e2c = E2c[str, str]()
    e2c.configure_by_file('app.e2c')

    e2c.actor('trace', trace)
    e2c.actor('intro', commands.intro.run)
    e2c.actor('setup', setup.run)
    e2c.actor('main', main.run)

    e2c.actor('get_avatar_by_name', repository.avatar.get_by_name)
    e2c.actor('load_avatar_by_name', commands.avatar.load_avatar_by_name)
    e2c.actor('set_avatar_to_session', web.session.set_avatar_to_session)

    # e2c.visualize('components/graphviz')

    def collect_data(result: str):
        output.append(str(result))

    input_data = request.form.get('input', '')
    start_actor = web.session.get_state('app')
    e2c.run_continues(input_data, collect_data, start_actor)

    return render_template(
        'form.html', input=input_data, output="".join(output))


if __name__ == "__main__":
    app.run(port=3000)
