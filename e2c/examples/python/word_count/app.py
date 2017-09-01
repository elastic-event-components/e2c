from os import walk
from typing import Callable

from e2c import E2c


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


e2c = E2c()
e2c.configure_by_file('app.e2c')
e2c.actor('list_files', list_files)
e2c.actor('open_file', open_file)
e2c.actor('word_count', word_count)
e2c.actor('error', lambda x: print('error', x))
e2c.actor('end', lambda x: print('end'))

e2c.visualize('pdf')
e2c.run_continues('data', lambda out: print(out))
