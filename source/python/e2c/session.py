from typing import Callable, Generic, Dict, List, TypeVar

from .node import Node
from .visualizer import visualize

Request = TypeVar('Request')
Response = TypeVar('Response')
Value = TypeVar('Value')

T = TypeVar('T', bound='Flow')

SELF = '•'
EDGE = '--'
COMMENT = '//'
DEFAULT = 'default'
OUT = '.out'


class Result(object):
    def __init__(self):
        self.value = None
        self.value_callback = None

    def run(self, data: object) -> None:
        if self.value_callback:
            self.value_callback(data)
        else:
            self.value = data

    def sync(self):
        return self.value


class Session(Generic[Request, Response]):
    def __init__(self, config_list: List[str] = None):
        self.name = DEFAULT
        self._result = Result()
        self._tracer = None
        self._end = None
        self._actors: Dict[str, Node] = {}
        self.actor(SELF, self._process)
        self.actor(OUT, self._result.run)
        self.activate_trace = True
        if config_list:
            self.configure_by_list(config_list)

    def _process(self, request, run, end=None, err=None, trace=None):
        try:
            self._tracer = trace
            self._end = end
            run(request)
        except Exception as exc:
            if not err: raise exc
            err(exc)

    def on_trace(self, name):
        if self._tracer:
            try:
                # deactivate trace in tracing process
                # to avoid recursion
                self.activate_trace = False
                self._tracer(name)
            finally:
                self.activate_trace = True

    def actor(self, name: str, callable: Callable):
        if name not in self._actors:
            self._actors[name] = Node(self, name, None)
        self._actors[name].callable = callable

    def analyse(self, quiet=True):
        if not quiet:
            print('===', self.name.upper(), '===')
        for actor_name, output_node in self._actors.items():
            if not quiet:
                print('\t', actor_name)
            if not output_node.callable:
                raise Exception('Actor %s has no function' % output_node.name)
            if not hasattr(output_node.callable, '__call__'):
                raise Exception('Actor %s is not callable' % output_node.name)

            for output_channel, nodes in output_node.nodes.items():
                for input_node in nodes:
                    if not quiet:
                        print('\t\t', (output_channel, input_node.name))
                    if not output_channel in output_node.specs:
                        raise Exception(
                            'Event {} in actor {} is not a parameter in function.'.format(
                                output_channel, actor_name))

    def visualize(self, folder: str = None):
        visualize(folder, self.name, self._actors)

    def configure_by_file(self, file_name: str):
        with open(file_name, 'r') as f:
            self.configure_by_list(f.readlines())

    def configure_by_list(self, lines: List[str]):
        for line in lines:
            line = line.replace('\n', '').replace(' ', '').strip()

            pos = line.find(COMMENT)
            if pos >= 0:
                line = line[:pos] if line else None
            if not line:
                continue

            if line.startswith('[') and line.endswith(']'):
                self.name = line[1:-1]
                continue

            output, input_name = line.split(EDGE)
            output_name, output_channel = output.split('.', 1)
            output_name = output_name or SELF

            if output_name not in self._actors:
                self._actors[output_name] = Node(self, output_name, None)
            if input_name not in self._actors:
                self._actors[input_name] = Node(self, input_name, None)

            self._actors[output_name].on(
                output_channel, self._actors[input_name])

    def run(self, request: Request = None, operation: str = None) -> Response:
        self.analyse(True)
        if not operation:
            self._actors[SELF].run(request)
        else:
            runner = self._actors[SELF].clone()
            runner.nodes['run'].clear()
            runner.on('run', self._actors[operation])
            runner.run(request)
        if self._end and self._end.node:
            self._end.node.run(request)
        return self._result.value

    def run_continues(self, request: Request = None,
                      result: Callable[[Response], None] = None, operation: str = None):
        self._result.value_callback = result
        self.run(request, operation)
