from e2c import E2c

config = (
    '.run -- action',
    'action.out -- print',
    'action.out -- print')

def print_data(x: int, data):
    print(x, data)



e2c = E2c[str, str](config)
e2c.actor('action', lambda data, out: out(data, {'a': 1}))
e2c.actor('print', print_data)

e2c.visualize()
e2c.run('hello')
