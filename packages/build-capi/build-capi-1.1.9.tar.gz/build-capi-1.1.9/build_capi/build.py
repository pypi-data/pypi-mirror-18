from __future__ import unicode_literals

import os
import sys
PY3 = sys.version_info > (3,)
from setuptools import Command

from ._unicode import unicode_airlock
from ._unicode import ascii_airlock

def _show_compilers():
    from distutils.ccompiler import show_compilers as sc
    sc()

class build_capi(Command, object):

    description = "build C/C++ libraries"

    user_options = [
        ('build-clib', 'b',
         "directory to build C/C++ libraries to"),
        ('build-temp', 't',
         "directory to put temporary build by-products"),
        ('debug', 'g',
         "compile with debugging information"),
        ('force', 'f',
         "forcibly build everything (ignore file timestamps)"),
        ('compiler=', 'c',
         "specify the compiler type"),
        ('inplace', 'i',
         "ignore build-lib and put compiled extensions into the source " +
         "directory alongside your pure Python modules"),
    ]

    boolean_options = ['inplace', 'debug', 'force']

    help_options = [
        ('help-compiler', None,
         "list available compilers", _show_compilers),
    ]

    def __init__(self, *args, **kwargs):
        self.build_clib = None
        self.build_temp = None

        # List of libraries to build
        self.capi_libs = None

        # Compilation options for all libraries
        self.include_dirs = None
        self.define = []
        self.undef = []
        self.debug = None
        self.force = 0
        self.inplace = 0
        self.compiler = None
        super(build_capi, self).__init__(*args, **kwargs)

    def initialize_options(self):

        self.build_clib = None
        self.build_temp = None
        self.capi_libs = []

        # Compilation options for all libraries
        self.include_dirs = None
        self.define = []
        self.undef = []
        self.debug = None
        self.force = 0
        self.inplace = 0
        self.compiler = None

    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_lib', 'build_clib'),
                                   ('build_temp', 'build_temp'),
                                   ('compiler', 'compiler'),
                                   ('debug', 'debug'),
                                   ('force', 'force'))
        self.set_undefined_options('build_ext',
                                   ('inplace', 'inplace'))

        self.capi_libs = self.distribution.capi_libs

        if self.include_dirs is None:
            self.include_dirs = self.distribution.include_dirs or []

        if isinstance(self.include_dirs, str):
            self.include_dirs = self.include_dirs.split(os.pathsep)

    def run(self):
        if not self.capi_libs:
            return

        from distutils.sysconfig import customize_compiler
        from distutils.ccompiler import new_compiler
        self.compiler = new_compiler(compiler=self.compiler,
                                     dry_run=self.dry_run,
                                     force=self.force)
        customize_compiler(self.compiler)

        if self.include_dirs is not None:
            self.compiler.set_include_dirs(self.include_dirs)
        if self.define is not None:
            # 'define' option is a list of (name,value) tuples
            for (name, value) in self.define:
                self.compiler.define_macro(name, value)
        if self.undef is not None:
            for macro in self.undef:
                self.compiler.undefine_macro(macro)

        self.build_libraries(self.capi_libs)

    def get_library_names(self):
        # Assume the library list is valid -- 'check_library_list()' is
        # called from 'finalize_options()', so it should be!
        if not self.capi_libs:
            return None

        lib_names = []
        for lib in self.capi_libs:
            if callable(lib):
                lib = lib()
            lib_names.append(lib.name)
        return lib_names

    def build_libraries(self, capi_libs):
        from distutils.errors import DistutilsSetupError
        for lib in capi_libs:
            if callable(lib):
                lib = lib()
            sources = lib.sources
            if sources is None or not isinstance(sources, (list, tuple)):
                raise DistutilsSetupError(
                    ("in 'libraries' option (library '%s'), " +
                     "'sources' must be present and must be " +
                     "a list of source filenames") % lib.name)
            sources = [unicode_airlock(s) for s in sources]

            from distutils import log
            log.info("building '%s' library", lib.name)

            macros = lib.define_macros
            include_dirs = lib.include_dirs
            eca = lib.extra_compile_args
            if PY3:
                sources = [unicode_airlock(s) for s in sources]
                output_dir = unicode_airlock(self.build_temp)
                include_dirs = [unicode_airlock(incd) for incd in include_dirs]
                macros = [unicode_airlock(m) for m in macros]
            else:
                sources = [ascii_airlock(s) for s in sources]
                output_dir = ascii_airlock(self.build_temp)
                include_dirs = [ascii_airlock(incd) for incd in include_dirs]
                macros = [ascii_airlock(m) for m in macros]
            objects = self.compiler.compile(sources,
                                            output_dir=output_dir,
                                            macros=macros,
                                            include_dirs=include_dirs,
                                            debug=self.debug,
                                            extra_preargs=eca)

            if PY3:
                lib_name = unicode_airlock(self.get_ext_fullpath(lib.name))
                objects = [unicode_airlock(o) for o in objects]
                output_dir = u'./'
            else:
                lib_name = ascii_airlock(self.get_ext_fullpath(lib.name))
                objects = [ascii_airlock(o) for o in objects]
                output_dir = b'./'
            self.compiler.create_static_lib(objects, lib_name,
                                            output_dir=output_dir,
                                            debug=self.debug)

    def get_ext_fullpath(self, ext_name):
        """Returns the path of the filename for a given extension.

        The file is located in `build_lib` or directly in the package
        (inplace option).
        """
        ext_name = unicode_airlock(ext_name)
        fullname = self.get_ext_fullname(ext_name)
        modpath = fullname.split('.')
        filename = self.get_ext_filename(ext_name)
        filename = os.path.split(filename)[-1]

        if not self.inplace:
            # no further work needed
            # returning :
            #   build_dir/package/path/filename
            filename = os.path.join(*modpath[:-1] + [filename])
            return os.path.join(self.build_clib, filename)

        # the inplace option requires to find the package directory
        # using the build_py command for that
        package = '.'.join(modpath[0:-1])
        build_py = self.get_finalized_command('build_py')
        package_dir = os.path.abspath(build_py.get_package_dir(package))

        # returning
        #   package_dir/filename
        return os.path.join(package_dir, filename)

    def get_ext_fullname(self, ext_name):
        """Returns the fullname of a given extension name.

        Adds the `package.` prefix"""
        if not hasattr(self, 'package') or self.package is None:
            return ext_name
        else:
            return self.package + '.' + ext_name

    def get_ext_filename(self, ext_name):
        r"""Convert the name of an extension (eg. "foo.bar") into the name
        of the file from which it will be loaded (eg. "foo/bar.so", or
        "foo\bar.pyd").
        """
        # from distutils.sysconfig import get_config_var
        ext_path = ext_name.split('.')
        # OS/2 has an 8 character module (extension) limit :-(
        if os.name == "os2":
            ext_path[len(ext_path) - 1] = ext_path[len(ext_path) - 1][:8]
        # extensions in debug_mode are named 'module_d.pyd' under windows
        # so_ext = get_config_var('SO')
        so_ext = ''
        if os.name == 'nt' and self.debug:
            return os.path.join(*ext_path) + '_d' + so_ext
        return os.path.join(*ext_path) + so_ext
