# ndarray-listener

[![PyPIl](https://img.shields.io/pypi/l/ndarray-listener.svg?style=flat-square)](https://pypi.python.org/pypi/ndarray-listener/)
[![PyPIv](https://img.shields.io/pypi/v/ndarray-listener.svg?style=flat-square)](https://pypi.python.org/pypi/ndarray-listener/)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/ndarray-listener/badges/version.svg)](https://anaconda.org/conda-forge/ndarray-listener)

Implementation of the [Observer pattern](https://en.wikipedia.org/wiki/Observer_pattern)
for [NumPy](http://www.numpy.org) arrays.

## Example

```python
from numpy import array
from ndarray_listener import ndarray_listener as ndl

a = ndl(array([-0.5, 0.1, 1.1]))

class Observer(object):
  def __init__(self):
    self.called_me = False

  def __call__(self, _):
    self.called_me = True

o = Observer()
a.talk_to(o)
print(o.called_me)
a[0] = 1.2
print(o.called_me)
```
The output should be
```
False
True
```

## Installing

The recommended way of installing it is via
[conda](http://conda.pydata.org/docs/index.html)
```bash
conda install -c conda-forge ndarray-listener
```

An alternative way would be via pip
```bash
pip install ndarray-listener
```


## Running the tests

After installation, you can test it
```bash
python -c "import ndarray_listener; ndarray_listener.test()"
```
as long as you have [pytest](http://docs.pytest.org/en/latest/).

## Authors

* **Danilo Horta** - [https://github.com/Horta](https://github.com/Horta)

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details
