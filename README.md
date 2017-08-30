<div align="center">
  <img src="https://github.com/enterstry/e2c/blob/master/images/e2c_logo_transp.png"><br><br>
</div>

# E2c - Elastic Event Components

**Elastic Event Components** is an open source software library to build flexible component using
function flow graphs. The graph nodes represent any operations, while
the graph edges represent the function parameters (event) that build
the flow between nodes. Elastic Event Components also includes flow visualization.


## Installation


#### *Try your first E2c program*
```shell
$ python
```python
>>> from e2c import E2c
>>> config = (
... '.run -- action',
... 'action.out -- print')
>>>
>>> e2c = E2c[str, str](config)
>>> e2c.actor('action', lambda data, out: out(data))
>>> e2c.actor('print', lambda data: print(data))
>>>
>>> e2c.run('hello')
hello
```

## License

[Apache License 2.0](LICENSE)
