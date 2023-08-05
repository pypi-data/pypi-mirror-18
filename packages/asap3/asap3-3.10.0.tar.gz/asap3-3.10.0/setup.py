#!/usr/bin/env python

"""This is the setup and installation script for Asap.

To install, simply run
    python setup.py install --user

CUSTOMIZATION:
If you need to change compiler options or other stuff, 
do NOT EDIT THIS FILE.  Instead, you should edit 
customize.py or one of its friends.

Customization information is read from the first of
these files found:
    customize-local.py
    customize-hostname.domain.py
    customize.py
If setup.py is given the option --customize=myfile.py then
that file is used instead of the above.

Only one of these files is read.  See customize.py for further
instructions.  But remember: MOST USERS DO NOT NEED THIS!

"""

from __future__ import print_function
import distutils
import distutils.util
import distutils.spawn
import os
import os.path as op
import stat
import re
import sys
from distutils.command.build_ext import build_ext as _build_ext
from distutils.command.build_scripts import build_scripts as _build_scripts
#from distutils.command.sdist import sdist as _sdist
from distutils.core import setup, Extension
from distutils.sysconfig import get_config_vars
from glob import glob
import numpy
import platform

assert sys.version_info >= (2, 6)

description = "ASAP - classical potentials for MD with ASE."

long_description = """\
ASAP (Atomic SimulAtion Program or As Soon As Possible) is a
package for large-scale molecular dynamics within the Atomic
Simulation Environment (ASE).  It implements a number of 'classical'
potentials, most importantly the Effective Medium Theory, and also the
mechanisms for domain-decomposition of the atoms."""

folders = ['Basics', 'Interface', 'Brenner', 'Tools',
           'PTM', 'PTM/qcprot', 'PTM/voronoi']
#kim_folders = ['OpenKIMimport']
kim_folders = []  # Disabled
parallel_folders = ['Parallel', 'ParallelInterface']
exclude_files = ['Interface/AsapModule.cpp']
serial_only_files = ['Interface/AsapSerial.cpp']


libraries = ['m']
library_dirs = []
include_dirs = []
extra_link_args = []
extra_compile_args = ['-std=c++11']
runtime_library_dirs = []
extra_objects = []
define_macros = []  #('NPY_NO_DEPRECATED_API', 7)]
undef_macros = ['NDEBUG']

mpi_libraries = []
mpi_library_dirs = []
mpi_include_dirs = []
mpi_runtime_library_dirs = []
mpi_define_macros = []
mpi_undef_macros = []
mpi_compiler = ('mpicc', 'mpicxx')

systemname, hostname, dummy1, dummy2, machinename, processorname = platform.uname()

#platform_id = ''  # Not changable for Asap (see gpaw/setup.py)

# Get the version number from Python/asap3/version.py
# Get the current version number:
with open('Python/asap3/version.py') as fd:
    version = re.search('__version__ = "(.*)"', fd.read()).group(1)
print("Asap version number:", version)

# Look for --customize arg
for i, arg in enumerate(sys.argv):
    if arg.startswith('--customize'):
        customize = sys.argv.pop(i).split('=')[1]
        break
else:
    # No --customize arg.
    for c in ('customize-local.py', 
              'customize-{0}.py'.format(hostname),
              'customize.py'):
        if os.path.exists(c):
            customize = c
            break
        elif '-' in c:
            print(c, "not found - this is OK.")
    else:
        raise RuntimeError("customize.py not found - broken source distribution.")

print("Reading customization from", customize)
exec(open(customize).read())

# Check if the MPI compiler is present.

if mpi_compiler:
    for mpicomp in mpi_compiler:
        if not distutils.spawn.find_executable(mpicomp):
            print("WARNING: No MPI compiler '{}': Not building parallel version.".format(mpicomp))
            mpi_compiler = None
            break

def runcmd(cmd, verb=False):
    if verb:
        print(cmd)
    x = os.system(cmd)
    if x:
        raise RuntimeError("Command failed: "+cmd)

def build_interpreter(compiler, common_src, parallel_src,
                      libraries, library_dirs, include_dirs, 
                      extra_link_args, extra_compile_args,
                      runtime_library_dirs, extra_objects, define_macros,
                      undef_macros):
    """Build the asap-python executable."""
    print("\n\n*** Building the asap-python executable ***\n\n")
    # The compiler may be a single string, or a tuple for C, C++
    if isinstance(compiler, str):
        c_compiler = cpp_compiler = compiler
    else:
        (c_compiler, cpp_compiler) = compiler

    # Get configuration variable
    cfgDict = get_config_vars()
    plat = distutils.util.get_platform() + '-' + sys.version[0:3]

    # Split sources into C and C++, and find object names.
    c_sources = {}
    cpp_sources = {}
    common_sources = {} # Will not be compiled, don't care about C/C++
    for s in parallel_src:
        dir = 'build/temp.{0}/{1}'.format(plat, os.path.dirname(s))
        if not os.path.exists(dir):
            os.mkdir(dir)   # Create folder for object file.
        if s.endswith('.cpp'):
            objname = 'build/temp.{0}/{1}.o'.format(plat, s[:-4])
            cpp_sources[s] = objname
        elif s.endswith('.c'):
            objname = 'build/temp.{0}/{1}.o'.format(plat, s[:-2])
            c_sources[s] = objname
        else:
            raise RuntimeError("Source file {0} is neither C nor C++.".format(s))
    for s in common_src:
        if s.endswith('.cpp'):
            objname = 'build/temp.{0}/{1}.o'.format(plat, s[:-4])
            common_sources[s] = objname
        elif s.endswith('.c'):
            objname = 'build/temp.{0}/{1}.o'.format(plat, s[:-2])
            common_sources[s] = objname
        else:
            raise RuntimeError("Source file {0} is neither C nor C++.".format(s))        
    exefile = "build/bin.{0}/asap-python".format(plat)
    if not os.path.exists("build/bin.{0}".format(plat)):
        os.mkdir("build/bin.{0}".format(plat))
        
    # Now construct the compilation command lines
    macros = ' '.join(['-D%s=%s' % x for x in define_macros if x[0].strip()])
    macros += ' '.join(['-U%s' % (x,) for x in undef_macros if x.strip()])
    
    include_dirs = include_dirs + [cfgDict['INCLUDEPY'],
                                   cfgDict['CONFINCLUDEPY']]
    includes = ' '.join(['-I' + incdir for incdir in include_dirs])

    library_dirs = library_dirs + [cfgDict['LIBPL']]
    lib_dirs = ' '.join(['-L' + lib for lib in library_dirs])

    libs = ' '.join(['-l' + lib for lib in libraries if lib.strip()])
    libs += ' ' + cfgDict.get('BLDLIBRARY', '-lpython%s' % cfgDict['VERSION'])
    libs = ' '.join([libs, cfgDict['LIBS'], cfgDict['LIBM']])
    runtime_lib_option = '-Wl,-R'
    runtime_libs = ' '.join([runtime_lib_option + lib
                             for lib in runtime_library_dirs])
    extra_link_args = extra_link_args + [cfgDict['LDFLAGS'],
                                         cfgDict['LINKFORSHARED']]
    # Compile
    all_objects = []
    extra_compile_args_c = list(extra_compile_args)
    if '-std=c++11' in extra_compile_args_c:
        extra_compile_args_c.remove('-std=c++11')
    for compiler, sources, compargs in (\
                (c_compiler, c_sources, extra_compile_args_c),
                (cpp_compiler, cpp_sources, extra_compile_args)):
        print("*** COMPILING: ", list(sorted(sources.keys())))
        for src in sorted(sources.keys()):
            obj = sources[src]
            all_objects.append(obj)
            cmd = ('%s %s %s %s -o %s -c %s ') % \
                  (compiler,
                   macros,
                   ' '.join(compargs),
                   includes,
                   obj,
                   src)
            runcmd(cmd, True)
    # Link
    all_objects = list(common_sources.values()) + all_objects
    cmd = ('%s -o %s %s %s %s %s %s %s') % \
          (cpp_compiler,
           exefile,
           ' '.join(all_objects),
           ' '.join(extra_objects),
           lib_dirs,
           libs,
           runtime_libs,
           ' '.join(extra_link_args))
    runcmd(cmd, True)

# Create the version.cpp file
versiondir = "VersionInfo_autogen"
try:
    host = os.uname()[1]
except:
    host = 'unknown'
versioninfo_s = "{0}/version_{1}_s.cpp".format(versiondir, host)
versioninfo_p = "{0}/version_{1}_p.cpp".format(versiondir, host)
if not os.path.exists(versiondir):
    os.mkdir("VersionInfo_autogen")
t = os.stat("Python/asap3/version.py")[stat.ST_MTIME]
if not os.path.exists(versioninfo_s) or t > os.stat(versioninfo_s)[stat.ST_MTIME]:
    runcmd("python recordversion.py '"+version+"' 'serial' 'distutils' '' > "+versioninfo_s)
    runcmd("python recordversion.py '"+version+"' 'parallel' 'distutils' '' > "+versioninfo_p)

if kim_folders and 'ASAP_KIM_DIR' in os.environ:
    akd = os.environ['ASAP_KIM_DIR']
    include_dirs += [os.path.join(akd, 'src')]
    library_dirs += [os.path.join(akd, 'src')]
    libraries += ['kim-api-v1']
    define_macros += [('WITH_OPENKIM', '1')]
    folders.extend(kim_folders)
elif kim_folders and 'KIM_HOME' in os.environ:
    kh = os.environ['KIM_HOME']
    include_dirs += [os.path.join(kh, 'include', 'kim-api-v1')]
    library_dirs += [os.path.join(kh, 'lib')]
    libraries += ['kim-api-v1']
    define_macros += [('WITH_OPENKIM', '1')]
    folders.extend(kim_folders)
        
include_dirs += folders + kim_folders
include_dirs.append(numpy.get_include())
mpi_include_dirs += parallel_folders

print("Identifying source files")
# Find source files for serial compilation
common_src_files = []
for d in folders + kim_folders:
    for f in os.listdir(d):
        if f.endswith('.cpp'):
            fn = os.path.join(d,f)
            if fn not in (exclude_files + serial_only_files):
                common_src_files.append(fn)
                #print("  ", fn)
serial_src_files = common_src_files + serial_only_files
serial_src_files.append(versioninfo_s)
serial_src_files.sort()
parallel_src_files = []
for d in parallel_folders:
    for f in os.listdir(d):
        if f.endswith('.cpp') or f.endswith('.c'):
            fn = os.path.join(d,f)
            parallel_src_files.append(fn)
parallel_src_files.append(versioninfo_p)

print("Identifying Python submodules")
packages = []
for dirname, dirnames, filenames in os.walk('Python/asap3'):
    if '__init__.py' in filenames:
        dname = dirname.split('/')[1:]  # Remove leading Python/
        packages.append('.'.join(dname))

extensions = [Extension('_asap_p{0}'.format(sys.version_info[0]),
                        serial_src_files,
                        libraries=libraries,
                        library_dirs=library_dirs,
                        include_dirs=include_dirs,
                        define_macros=define_macros,
                        undef_macros=undef_macros,
                        extra_link_args=extra_link_args,
                        extra_compile_args=extra_compile_args,
                        runtime_library_dirs=runtime_library_dirs,
                        )]

# Scripts
scripts = ['scripts/asap-qsub']
if mpi_compiler:
    plat = distutils.util.get_platform() + '-' + sys.version[0:3]
    scripts.append("build/bin.{0}/asap-python".format(plat))
    
class build_ext(_build_ext):
    def run(self):
        _build_ext.run(self)
        if mpi_compiler:
            # Also build asap-python:
            build_interpreter(
                mpi_compiler,
                common_src_files,
                parallel_src_files,
                libraries=libraries+mpi_libraries,
                library_dirs=library_dirs+mpi_library_dirs,
                include_dirs=include_dirs+mpi_include_dirs,
                extra_link_args=extra_link_args,
                extra_compile_args=extra_compile_args,
                runtime_library_dirs=runtime_library_dirs,
                extra_objects=extra_objects,
                define_macros=define_macros+mpi_define_macros,
                undef_macros=undef_macros+mpi_undef_macros)

class build_scripts(_build_scripts):
    # Python 3 will try to read the asap-python executable, handle
    # that one specially.
    def copy_scripts(self):
        executables = []
        for i, s in enumerate(self.scripts):
            if 'asap-python' in s:
                print("Protecting", s, "from ajustment")
                executables.append(s)
        for s in executables:
            self.scripts.remove(s)
        assert len(executables) <= 1
        x =_build_scripts.copy_scripts(self)
        if x is None:
            # Python 2
            outfiles = []
            updated_files = []
        else:
            outfiles, updated_files = x
        for script in executables:
            outfile = op.join(self.build_dir, op.basename(script))
            outfiles.append(outfile)
            updated_files.append(outfile)
            self.copy_file(script, outfile)
        return outfiles, updated_files
            
setup(name="asap3",
      version=version,
      description=description,
      long_description=long_description,
      maintainer="Jakob Schiotz et. al.",
      maintainer_email="schiotz@fysik.dtu.dk",
      url="https://wiki.fysik.dtu.dk/asap",
      packages=packages,
      package_dir={'asap3': 'Python/asap3'},
      ext_modules=extensions,
      license='LGPLv3',
      platforms=['unix'],
      scripts=scripts,
      cmdclass={'build_ext': build_ext,
                'build_scripts': build_scripts},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
                    'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering :: Physics'
      ])

