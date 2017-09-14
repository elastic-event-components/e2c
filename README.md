<div align="center">
  <img src="https://github.com/enterstry/e2c/blob/master/images/e2c-logo.png"><br><br>
</div>

# E2C - Elastic Event Components

**Elastic Event Components** is an open source software library to build flexible component using
function flow graphs. The graph nodes represent any operations, while
the graph edges represent the function parameters that build
the flow between nodes. Elastic Event Components also includes flow visualization.

## Installation
*See [Installing E2C](https://github.com/enterstry/e2c/blob/master/INSTALL.md) for instructions 
on how to build from source.*

#### *Try your first E2C program*
```shell
$ python
```

```python
>>> import e2c

>>> config = (
... '.run -- action',
... 'action.render -- render',
... '   render.out -- .out',
... 'action.log -- log',
... '   log.store -- .out')

>>> def action(data: str, render, log):
...    render(data)
...    log('Render done!')

>>> sess = e2c.Session[str, str](config)
>>> sess.actor('action', action)
>>> sess.actor('render', lambda dat, out: out(dat))
>>> sess.actor('log', lambda dat, store: store(dat))

>>> sess.run_continues('Hello E2C!', print)
Hello e2c!
Render done!
```

<div align="center">
  <img src="https://github.com/enterstry/e2c/blob/master/images/quickstart.png"><br><br>
</div>


## For more information
* [E2C website](http://www.elastic-event-components.org)

## License
[Apache 2.0 License](LICENSE)
