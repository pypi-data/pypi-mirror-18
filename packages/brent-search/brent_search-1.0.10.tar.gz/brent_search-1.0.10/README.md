# brent-search

Univariate function optimization based on Brent's method.

## Getting Started

```python
>>> from brent_search import brent
>>>
>>> def func(x, s):
...     return (x - s)**2 - 0.8
>>>
>>> brent(lambda x: func(x, 0), -10, 10)
(0.0, -0.8, 6)
```

### Installing

Via pip
```
pip install brent_search
```

or via [Conda](http://conda.pydata.org/docs/index.html)
```
conda install -c conda-forge brent_search
```

## Running the tests

After installation, you can test it
```
python -c "import brent_search; brent_search.test()"
```
if you have [pytest](http://pytest.org) installed.

## Authors

* **Danilo Horta** - [https://github.com/Horta](https://github.com/Horta)

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details
