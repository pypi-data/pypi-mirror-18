from __future__ import unicode_literals

from setuptools.command.build_ext import build_ext
import os

def error(msg):
    from distutils.errors import DistutilsSetupError
    raise DistutilsSetupError(msg)

class CApiLib(object):

    def __init__(self, name, sources,
                 include_dirs=None,
                 define_macros=None,
                 undef_macros=None,
                 library_dirs=None,
                 libraries=None,
                 runtime_library_dirs=None,
                 extra_objects=None,
                 extra_compile_args=None,
                 extra_link_args=None,
                 export_symbols=None,
                 depends=None):

        self.name = name
        self.sources = sources
        self.include_dirs = include_dirs or []
        self.define_macros = define_macros or []
        self.undef_macros = undef_macros or []
        self.library_dirs = library_dirs or []
        self.libraries = libraries or []
        self.runtime_library_dirs = runtime_library_dirs or []
        self.extra_objects = extra_objects or []
        self.extra_compile_args = extra_compile_args or []
        self.extra_link_args = extra_link_args or []
        self.export_symbols = export_symbols or []
        self.depends = depends or []


def capi_libs(dist, attr, value):
    assert attr == 'capi_libs'
    if isinstance(value, CApiLib) or callable(value):
        value = [value]

    for capi_lib in value:
        _check_capi_lib(capi_lib)

    cmdclass = dist.cmdclass
    _build_ext = _process_build_ext(cmdclass.pop('build_ext', build_ext))
    cmdclass['build_ext'] = _build_ext
    dist.cmdclass = cmdclass


def _check_capi_lib(capi_lib):
    if not isinstance(capi_lib, CApiLib) and not callable(capi_lib):
        error("argument to 'capi_libs=...' must be either a CApiLib or a" +
              " callable object or a list those," +
              " not %r" % (type(capi_lib).__name__,))


def _process_build_ext(klass):
    def run(self):
        self.reinitialize_command('build_capi', inplace=self.inplace,
                                  build_clib=self.build_lib)
        self.run_command("build_capi")
        return klass.old_run(self)
    klass.old_run = klass.run
    klass.run = run
    return klass
