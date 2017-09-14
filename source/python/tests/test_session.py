import os
import tempfile

import pytest
from e2c import errors
from e2c import session


def get_graph_file(file_name):
    graph_folder = os.path.join(
        os.path.dirname(__file__), 'graph')
    return os.path.join(graph_folder, file_name)


def get_temp_folder():
    dir = os.path.join(tempfile.gettempdir(), 'e2c')
    os.makedirs(dir, exist_ok=True)
    return dir


def test_analyse__error_on_no_actor():
    sess = session.Session()
    sess.actor('A', None)
    with pytest.raises(errors.E2CSessionError) as info:
        sess.analyse()
    assert str(info.value) == 'Actor A has no callable function!'


def test_analyse__error_on_actor_not_callable():
    sess = session.Session()
    sess.actor('A', "function")
    with pytest.raises(errors.E2CSessionError) as info:
        sess.analyse()
    assert str(info.value) == 'Actor A is not a callable function!'

def test_analyse__quite():
    sess = session.Session()
    sess.actor('A', lambda: None)
    sess.analyse(False)


def test_actor__error_on_double_name():
    sess = session.Session()
    sess.actor('A', lambda: None)
    with pytest.raises(errors.E2CSessionError) as info:
        sess.actor('A', lambda: None)
    assert str(info.value) == 'Actor A was already registered!'


def test_visualize__error_on_no_configuration():
    sess = session.Session()
    sess.actor('A', lambda: None)
    folder = get_temp_folder()
    with pytest.raises(errors.E2CVisualizeError) as info:
        sess.visualize(folder)
    assert str(info.value) == 'Graph is empty!'


def test_visualize__create():
    config = (
        '.trace -- trace',
        '.err -- error',
        '.run -- A',
        'A.a -- .out',
        'A.a -- B')

    sess = session.Session(config)
    sess.actor('A', lambda a: None)
    sess.actor('B', lambda: None)
    folder = get_temp_folder()
    sess.visualize(folder)

    assert os.path.exists(
        os.path.join(folder, 'default.pdf'))


def test_parse_graph__error_without_graph():
    with pytest.raises(errors.E2CParserError) as info:
        session.Session(['', ])
    assert str(info.value) == 'No data to parse!'


def test_parse_graph__error_missing_double_line():
    with pytest.raises(errors.E2CParserError) as info:
        session.Session(['.run', ''])
    assert str(info.value) == 'Missing -- in line 1!'


def test_parse_graph__error_missing_target():
    with pytest.raises(errors.E2CParserError) as info:
        session.Session(['.run --', ''])
    assert str(info.value) == 'Missing actor in line 1!'


def test_load_graph__error_invalid_filename():
    sess = session.Session()
    with pytest.raises(errors.E2CSessionError):
        sess.load_graph('graph/xx.e2c')


def test_run():
    sess = session.Session()
    sess.actor('A', lambda value, out: out(value + 5))
    sess.actor('B', lambda value, out: out(value * 2))
    sess.load_graph(get_graph_file('t1.e2c'))
    assert sess.run(3) == 16
    assert sess.run(3, actor="A") == 16
    assert sess.run(3, actor="B") == 6
    assert sess.run(2, actor="A") == 14


def test_run__invalid_start_actor():
    sess = session.Session()
    sess.actor('A', lambda value, out: None)
    sess.actor('B', lambda value, out: None)
    sess.load_graph(get_graph_file('t1.e2c'))
    with pytest.raises(errors.E2CSessionError) as info:
        sess.run(2, actor="X")
    assert str(info.value) == 'X is not a registered actor!'


def test_run__call_end():
    data = []
    sess = session.Session()
    sess.actor('A', lambda value, out: out(value))
    sess.actor('B', lambda value, out: out(value + 2))
    sess.actor('C', lambda value: data.append(value))
    sess.load_graph(get_graph_file('t2.e2c'))

    start_value = 1
    assert sess.run(start_value) == 3
    assert data[0] == start_value


def test_run__call_trace():
    data = []
    sess = session.Session()
    sess.actor('A', lambda value, out: out(value))
    sess.actor('B', lambda value, out: out(value))
    sess.actor('Trace', lambda value: data.append(value))
    sess.load_graph(get_graph_file('t3.e2c'))

    sess.run(None)
    assert data == ['A', 'B']

def test_run_continues():
    data = []
    sess = session.Session()
    sess.actor('A', lambda value, out: out(value+1))
    sess.actor('B', lambda value, out: out(value*3))
    sess.load_graph(get_graph_file('t4.e2c'))

    sess.run_continues(3, lambda value: data.append(value))
    assert data == [12, 12, 12]