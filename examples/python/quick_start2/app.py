from typing import Callable

import e2c

config = (
    '.run -- action',
    'action.render -- render',
    '   render.out -- .out',
    'action.log -- log',
    '   log.store -- .out',
)

def action(data: str, render, log):
    render(data)
    log('render done!')

sess = e2c.Session(config)
sess.actor('action', action)
sess.actor('render', lambda dat, out: out(dat))
sess.actor('log', lambda dat, store: store(dat))
sess.visualize()

sess.run_continues('Hello E2C', print)

