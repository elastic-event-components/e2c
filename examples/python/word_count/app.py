from os import walk
from typing import Callable

import e2c


def list_files(dir: str, load_file: Callable[[str], None]):
    for filename in next(walk(dir))[2]:
        load_file(dir + '/' + filename)


def open_file(file: str, out: Callable[[str], None]):
    with open(file) as f:
        content = "".join(f.readlines())
    out(content)


def word_count(content: str, out: Callable[[str], None]):
    count = len(content.split(' '))
    out(count)


sess = e2c.Session()
sess.configure_by_file('app.e2c')
sess.actor('list_files', list_files)
sess.actor('open_file', open_file)
sess.actor('word_count', word_count)
sess.actor('error', lambda x: print('error', x))
sess.actor('end', lambda x: print('end'))

sess.visualize('pdf')
sess.run_continues('data', lambda out: print(out))
