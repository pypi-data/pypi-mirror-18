#! /usr/bin/env python
#
# Copyright (C) 2013-2016 Fabian Gieseke <fabian.gieseke@di.ku.dk>
# License: GPL v2
#
#   Inspired by https://github.com/scikit-learn/scikit-learn/blob/master/setup.py
#   Copyright (C) 2007-2009 Cournapeau David <cournape@gmail.com>
#                 2010 Fabian Pedregosa <fabian.pedregosa@inria.fr>
#   License: 3-clause BSD
#

import os
import sys
import shutil
from distutils.command.clean import clean

# set flag to indicate that package
# is installed (similar to scikit-learn
# installation routine)
if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins
builtins.__BUFFERKDTREE_SETUP__ = True
 
DISTNAME = 'bufferkdtree'
DESCRIPTION = 'A Python library for large-scale exact nearest neighbor search using Buffer k-d Trees (bufferkdtree).'
LONG_DESCRIPTION = open('README.rst').read()
MAINTAINER = 'Fabian Gieseke'
MAINTAINER_EMAIL = 'fabian.gieseke@di.ku.dk'
URL = 'https://github.com/gieseke/bufferkdtree'
LICENSE = 'GNU GENERAL PUBLIC LICENSE Version 2'
DOWNLOAD_URL = 'https://github.com/gieseke/bufferkdtree'

# adapted from scikit-learn
if len(set(('develop', 'release')).intersection(sys.argv)) > 0:
    import setuptools
    extra_setuptools_args = dict(zip_safe=False)
else:
    extra_setuptools_args = dict()
            
def configuration(parent_package='', top_path=None):

    from numpy.distutils.misc_util import Configuration
    config = Configuration(None, parent_package, top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True,
                       )
    config.add_subpackage('bufferkdtree')

    return config

class CleanCommand(clean):
    
    description = "Cleaning up code ..."

    def run(self):

        clean.run(self)

        # remove hidden '~' files
        for dirpath, dirnames, filenames in os.walk('.'):
            for filename in filenames:
                if filename.endswith('~'):
                    os.unlink(os.path.join(dirpath, filename))

        # build related files and directories
        if os.path.exists('build'):
            shutil.rmtree('build')
        if os.path.exists('bufferkdtree.egg-info'):
            shutil.rmtree('bufferkdtree.egg-info')
        if os.path.exists('docs/_build'):
            shutil.rmtree('docs/_build')

        # remaining files and directories in bufferkdtree dir (recursively)
        for dirpath, dirnames, filenames in os.walk('bufferkdtree'):
            
            for filename in filenames:
                if (filename.endswith('.so') or \
                    filename.endswith('.pyd') or \
                    filename.endswith('.dll') or \
                    filename.endswith('.pyc') or \
                    filename.endswith('_wrap.c') or \
                    filename.startswith('wrapper_') or \
                    filename.endswith('~')):
                        os.unlink(os.path.join(dirpath, filename))

            for dirname in dirnames:
                if dirname == '__pycache__' or dirname == 'build' or dirname == '_build':
                    shutil.rmtree(os.path.join(dirpath, dirname))
        try:
            shutil.rmtree("dist")
        except:
            pass

            
def setup_package():
    
    import bufferkdtree
    VERSION = bufferkdtree.__version__

    metadata = dict(name=DISTNAME,
                    maintainer=MAINTAINER,
                    maintainer_email=MAINTAINER_EMAIL,
                    description=DESCRIPTION,
                    license=LICENSE,
                    url=URL,
                    version=VERSION,
                    download_url=DOWNLOAD_URL,
                    long_description=LONG_DESCRIPTION,
                    classifiers=[
                                 'Intended Audience :: Science/Research',
                                 'Intended Audience :: Developers',
                                 'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
                                 'Programming Language :: C',
                                 'Programming Language :: Python',
                                 'Programming Language :: Python :: 2',
                                 'Programming Language :: Python :: 2.6',
                                 'Programming Language :: Python :: 2.7',
                                 ],
                    cmdclass={'clean': CleanCommand},
                    setup_requires=["numpy>=1.11.0"],
                    install_requires=["numpy>=1.11.0"],
                    include_package_data=True,
                    package_data={'bufferkdtree': ['src/neighbors/brute/kernels/opencl/*.cl',
                                                   'src/neighbors/buffer_kdtree/kernels/*.cl'
                                                  ]},
                    **extra_setuptools_args)

    if (len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or sys.argv[1] in ('--version', 'clean'))):
 
        try:
            from setuptools import setup
        except ImportError:
            from distutils.core import setup
        metadata['version'] = VERSION
        setup(**metadata)
        
    else:

        # if pip is installed, make sure that numpy
        # is installed (pip is not a requirement
        # for the bufferkdtree package) 
        try:
            import pip
            pip.main(["install", "numpy>=1.11.0"])
        except:
            pass
                    
        try:
            from numpy.distutils.core import setup as numpy_setup
            metadata['configuration'] = configuration
            numpy_setup(**metadata)
        except Exception as e:
            print("Could not install package: %s" % str(e))
            sys.exit(0)

if __name__ == "__main__":

    setup_package()
