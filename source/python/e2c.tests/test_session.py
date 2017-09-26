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

import os
import tempfile

import pytest
from e2c import errors
from e2c import session


def get_graph_file(file_name):
    graph_folder = os.path.join(
        os.path.dirname(__file__), 'graph')
    return os.path.join(graph_folder, file_name)


def test_analyse():
    class MockAnalyser(object):
        def run(self, quiet=True):
            self.quiet = quiet

    mockup = MockAnalyser()
    sess = session.BaseSession({}, mockup, None, None, None)
    sess.analyse(quiet=True)
    assert mockup.quiet == True


def test_visualize():
    class MockVisualizer(object):
        def run(self, folder: str, name: str):
            self.folder = folder
            self.name = name

    mockup = MockVisualizer()
    sess = session.BaseSession({}, None, None, mockup, None)
    sess.name = "test"
    sess.visualize('test_folder')
    assert mockup.folder == 'test_folder'
    assert mockup.name == sess.name


def test_actor__error_on_double_name():
    sess = session.Session()
    sess.actor('A', lambda: None)
    with pytest.raises(errors.E2CSessionError) as info:
        sess.actor('A', lambda: None)
    assert str(info.value) == 'Actor A was already registered!'


def test_parse_graph__error_on_empty_graph():
    with pytest.raises(errors.E2CParserError) as info:
        session.Session(['', ])
    assert str(info.value) == 'No data to parse!'


def test_parse_graph__error_on_missing_double_line():
    with pytest.raises(errors.E2CParserError) as info:
        session.Session(['.run', ''])
    assert str(info.value) == 'Missing -- in line 1!'


def test_parse_graph__error_on_missing_target():
    with pytest.raises(errors.E2CParserError) as info:
        session.Session(['.run --', ''])
    assert str(info.value) == 'Missing actor in line 1!'


def test_load_graph__error_on_invalid_filename():
    sess = session.Session()
    with pytest.raises(errors.E2CSessionError):
        sess.load_graph('graph/xx.e2c')


def test_run__raise_custom_exception():
    config = (
        '.run -- A',)

    def raise_error():
        raise Exception('Invalid operation')

    sess = session.Session(config)
    sess.actor('A', raise_error)
    with pytest.raises(Exception) as info:
        sess.run()
    assert str(info.value) == 'Invalid operation'


def test_run__raise_exception_missing_run():
    config = (
        '.trace -- trace',)

    def trace(name: str):
        pass

    sess = session.Session(config)
    sess.actor('trace', trace)
    with pytest.raises(errors.E2CSessionError) as info:
        sess.run()
    assert str(info.value) == 'Missing .run -- ? in graph!'


def test_run__raise_exception_catch_actor():
    config = (
        '.err -- error',
        '.run -- A')

    def raise_error():
        raise Exception('Invalid operation')

    def error_handler():
        error['error'] = 1

    error = {}
    sess = session.Session(config)
    sess.actor('A', raise_error)
    sess.actor('error', error_handler)
    sess.run()

    assert error


def test_run__assign_before_define():
    config = (
        'A.out -- B',
        '.run -- A')

    data = []
    sess = session.Session(config)
    sess.actor('A', lambda data, out: out(data))
    sess.actor('B', lambda d: data.append(d))
    sess.run(1)

    assert data[0] == 1


def test_run():
    # class method as actor
    class Dummy():
        def operation(self, value, out):
            out(value + 5)

    # function as actor
    def operation(value, out):
        out(value * 2)

    sess = session.Session()
    sess.actor('A', Dummy().operation)
    sess.actor('B', operation)
    sess.load_graph(get_graph_file('t1.e2c'))
    assert sess.run(3) == 16
    assert sess.run(3, actor="A") == 16
    assert sess.run(3, actor="B") == 6
    assert sess.run(2, actor="A") == 14


def test_run__error_on_invalid_start_actor():
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
    sess.actor('A', lambda value, out: out(value + 1))
    sess.actor('B', lambda value, out: out(value * 3))
    sess.load_graph(get_graph_file('t4.e2c'))

    sess.run_continues(3, lambda value: data.append(value))
    assert data == [12, 12, 12]
