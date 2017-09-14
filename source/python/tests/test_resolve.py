from e2c import node
from e2c import resolve
from e2c import session


def new_node(name: str, callable):
    sess = session.Session()
    return node.Node(sess, name, callable)


def test_param__call():
    data = []
    node = new_node('A', lambda: data.append('1'))
    param = resolve.Param(node, [])
    param()
    assert data[0] == '1'


def test_resolve_value():
    data = []

    def actor(a, b, c, func_a, func_b):
        data.append([a, b, c, func_a, func_b])

    node = new_node('A', actor)
    params1 = resolve.resolve(node, [1, 'data', True])
    params2 = resolve.resolve(node, [])

    assert len(params1) == 5
    assert params1 == [1, 'data', True, None, None]
    assert params2 == [None, None, None, None, None]
