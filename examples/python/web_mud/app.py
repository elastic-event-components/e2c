import e2c
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
    sess = e2c.Session[str, str]()
    sess.configure_by_file('app.e2c')

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
