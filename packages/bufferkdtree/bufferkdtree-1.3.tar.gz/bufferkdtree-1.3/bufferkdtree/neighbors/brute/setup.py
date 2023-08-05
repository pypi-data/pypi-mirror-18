#
# Copyright (C) 2013-2016 Fabian Gieseke <fabian.gieseke@di.ku.dk>
# License: GPL v2
#

import os
import sys
import numpy

SOURCES_RELATIVE_PATH = "../../src/"

FILES_TO_BE_COMPILED = ["timing.c", "opencl.c", "util.c", "neighbors/brute/base.c", "neighbors/brute/util.c", "neighbors/brute/cpu.c", "neighbors/brute/gpu_opencl.c"]
DIRS_TO_BE_INCLUDED = ["neighbors/brute/include"]

# the absolute path to the sources
current_path = os.path.dirname(os.path.abspath(__file__))
sources_abs_path = os.path.abspath(os.path.join(current_path, SOURCES_RELATIVE_PATH))

# all source files
source_files = [os.path.abspath(os.path.join(sources_abs_path, x)) for x in FILES_TO_BE_COMPILED] 
include_paths = [os.path.abspath(os.path.join(sources_abs_path, x)) for x in DIRS_TO_BE_INCLUDED]

try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

if sys.version_info >= (3, 0):
    swig_opts = ['-modern', '-threads', '-py3']
else:
    swig_opts = ['-modern', '-threads']

def configuration(parent_package='', top_path=None):
    
    from numpy.distutils.misc_util import Configuration
    config = Configuration('neighbors/brute', parent_package, top_path)
        
    # CPU + FLOAT
    config.add_extension("_wrapper_cpu_float", \
                                    sources=["swig/cpu_float.i"] + source_files,
                                    swig_opts=swig_opts,
                                    include_dirs=[numpy_include] + [include_paths],
                                    define_macros=[
                                        ('SOURCE_PATH', os.path.join(SOURCES_RELATIVE_PATH, "neighbors/brute")),
                                        ('USE_GPU', 0),
                                        ('USE_DOUBLE', 0),
                                        ('TIMING', 1)
                                    ],
                                    libraries=['OpenCL', 'gomp'],
                                    extra_compile_args=["-fopenmp", '-O3', '-w'] + ['-I' + ipath for ipath in include_paths])

    # CPU + DOUBLE
    config.add_extension("_wrapper_cpu_double", \
                                    sources=["swig/cpu_double.i"] + source_files,
                                    swig_opts=swig_opts,
                                    include_dirs=[numpy_include] + [include_paths],
                                    define_macros=[
                                        ('SOURCE_PATH', os.path.join(SOURCES_RELATIVE_PATH, "neighbors/brute")),
                                        ('USE_GPU', 0),
                                        ('USE_DOUBLE', 1),
                                        ('TIMING', 1)
                                    ],
                                    libraries=['OpenCL', 'gomp'],
                                    extra_compile_args=["-fopenmp", '-O3', '-w'] + ['-I' + ipath for ipath in include_paths])
    
    # GPU + FLOAT
    config.add_extension("_wrapper_gpu_opencl_float", \
                                    sources=["swig/gpu_float.i"] + source_files,
                                    swig_opts=swig_opts,
                                    include_dirs=[numpy_include] + [include_paths],
                                    define_macros=[
                                        ('SOURCE_PATH', os.path.join(SOURCES_RELATIVE_PATH, "neighbors/brute")),
                                        ('USE_GPU', 1),
                                        ('USE_DOUBLE', 0),
                                        ('TIMING', 1),
                                        ('WORKGROUP_SIZE', 256)
                                    ],
                                    libraries=['OpenCL', 'gomp'],
                                    extra_compile_args=["-fopenmp", '-O3', '-w'] + ['-I' + ipath for ipath in include_paths])

    # GPU + DOUBLE
    config.add_extension("_wrapper_gpu_opencl_double", \
                                    sources=["swig/gpu_double.i"] + source_files,
                                    swig_opts=swig_opts,
                                    include_dirs=[numpy_include] + [include_paths],
                                    define_macros=[
                                        ('SOURCE_PATH', os.path.join(SOURCES_RELATIVE_PATH, "neighbors/brute")),
                                        ('USE_GPU', 1),
                                        ('USE_DOUBLE', 1),
                                        ('TIMING', 1),
                                        ('WORKGROUP_SIZE', 256)
                                    ],
                                    libraries=['OpenCL', 'gomp'],
                                    extra_compile_args=["-fopenmp", '-O3', '-w'] + ['-I' + ipath for ipath in include_paths])


    return config

if __name__ == '__main__':
    
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
