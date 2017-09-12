import e2c

config = (
    '.run -- action',
    'action.out -- print')

sess = e2c.Session[str, str](config)
sess.actor('action', lambda data, out: out(data))
sess.actor('print', lambda data: print(data))

sess.visualize()
sess.run('hello')
