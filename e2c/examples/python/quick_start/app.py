from e2c import E2c

config = (
    '.run -- action',
    'action.out -- print')

e2c = E2c[str, str](config)
e2c.actor('action', lambda data, out: out(data))
e2c.actor('print', lambda data: print(data))

e2c.visualize()
