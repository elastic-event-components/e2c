from typing import Callable

import e2c

config = (
    '.run -- action',
    'action.output -- .out',
    'action.output -- .out')


def action(cmd: str, output: Callable[[str], None]):
    output(cmd)


sess = e2c.Session(config)
sess.actor('action', action)
sess.visualize()

data = []
sess.run_continues(
    'Hello E2C', lambda result: data.append(result))

print(data)
