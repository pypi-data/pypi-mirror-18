# build-capi

[![PyPIl](https://img.shields.io/pypi/l/build-capi.svg?style=flat-square)](https://pypi.python.org/pypi/build-capi/)
[![PyPIv](https://img.shields.io/pypi/v/build-capi.svg?style=flat-square)](https://pypi.python.org/pypi/build-capi/)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/build-capi/badges/version.svg)](https://anaconda.org/conda-forge/build-capi)

Build and distribute C/C++ static libraries via Python packages.

## Getting Started

You can have a ``setup.py`` similar to

```python
from os.path import join
from setuptools import setup

def get_lib():
  from build_capi import CApiLib

  mylib = CApiLib('pkg_name.lib.nmylib',
                  sources=[join('pkg_name', 'sources', 'example.c')],
                  include_dirs=[join('pkg_name', 'include')])

setup(
      name='pkg_name',
      # ...
      setup_requires=['build_capi'],
      capi_libs=[get_lib],
      include_package_data=True,
      data_files=[(join('pkg_name', 'include'), join('pkg_name', 'include',
                                                     'example.h'))],
      package_data={'': [join('pkg_name', 'lib', '*.*')]})
```

and then have a ``pkg_name/__init__.py``

```python
def get_include():
  import pkg_name
  from os.path import join, dirname
  return join(dirname(pkg_name.__file__), 'include')

def get_lib():
  import pkg_name
  from os.path import join, dirname
  return join(dirname(pkg_name.__file__), 'lib')
```

Please, refer to [build_capi/example/prj_name](build_capi/example/prj_name)
for a minimal example of project using ``build_capi``.

## Install

The recommended way of installing it is via
[conda](http://conda.pydata.org/docs/index.html)
```bash
conda install -c conda-forge build-capi
```

An alternative way would be via pip
```bash
pip install build-capi
```

## Authors

* **Danilo Horta** - [https://github.com/Horta](https://github.com/Horta)

## License

This project is licensed under the MIT License - see the
[LICENSE](LICENSE) file for details
