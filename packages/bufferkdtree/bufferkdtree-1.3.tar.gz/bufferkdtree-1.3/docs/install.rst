.. -*- rst -*-

Installation
============

.. warning::

    The authors are not responsible for any implications that stem from the use of this software.

Quick Installation
------------------

The package is available on `PyPI <https://pypi.python.org/pypi>`_, but can also be installed from the sources. We recommend to use `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ to install the package and all dependencies (see below). The installation process has been tested on various Linux-based machines: To install the package via `PyPI <https://pypi.python.org/pypi>`_ on Linux systems, type::

  $ sudo pip install bufferkdtree

To install the package from the sources, first get the current stable release via::

  $ git clone https://github.com/gieseke/bufferkdtree.git

Subsequently, install the package locally via::

  $ cd bufferkdtree
  $ python setup.py install --user

or, globally for all users, via::

  $ sudo python setup.py build
  $ sudo python setup.py install

Dependencies
------------

The bufferkdtree package has been tested under various Linux-based systems such as Ubuntu and OpenSUSE and requires Python 2.6/2.7/3.*. Below, some installation instructions are given for Linux-based systems; similar steps have to be conducted on other systems.

To install the package, a working C/C++ compiler, `OpenCL <https://www.khronos.org/opencl>`_ (version 1.2 or higher), `Swig <http://www.swig.org/>`_, and the Python development files (headers) along with `setuptools <https://pypi.python.org/pypi/setuptools>`_ need to be available. Further, the `NumPy <http://www.numpy.org>`_ package (>=1.11.0) is needed.

On Ubuntu 12.04/14.04/16.04, for instance, the following command can be used to install most dependencies (except for OpenCL)::

   $ sudo apt-get install python2.7 python-dev swig build-essential python-numpy python-setuptools

On an OpenSUSE system, the corresponding command is::

   $ sudo zypper install python python-devel swig python-numpy python-setuptools

.. admonition:: Compatibility

   The implementation is based on the efficient use of implicit hardware caches. Thus, to obtain good speed-ups, the system's GPU has to support this feature! Current architectures such as Nvidia's Kepler architecture exhibit such caches, see, e.g., the `Kepler GK110 Whitepaper <http://www.nvidia.com/content/PDF/kepler/NVIDIA-Kepler-GK110-Architecture-Whitepaper.pdf>`_. 

OpenCL
------

`OpenCL <https://www.khronos.org/opencl>`_ (version 1.2 or higher) needs to be installed correctly on the system. The installation of OpenCL depends on the particular host system and the devices used, see, e.g.,

- `Intel <https://software.intel.com/en-us/intel-opencl/download>`_
- `Nvidia <https://developer.nvidia.com/opencl>`_
- `AMD <http://developer.amd.com/tools-and-sdks/opencl-zone/opencl-resources/getting-started-with-opencl/>`_

We refer to Andreas Klöckner's `wiki <https://wiki.tiker.net/OpenCLHowTo>`_ page for an excellent description of the OpenCL installation process on Linux-based systems. OpenCL is installed on `macOS <https://developer.apple.com/opencl/>`_. For Windows, we refer to this `blog post <https://streamcomputing.eu/blog/2015-03-16/how-to-install-opencl-on-windows/>`_.

Please make sure that the the OpenCL header files are available as well and accessible during the installation process, e.g., by setting the C_INCLUDE_PATH environment variable in the .bashrc file on Linux-based systems. For instance, given a Nvidia device alogn with CUDA and OpenCL being installed, the header files are probably located in ``/usr/local/cuda/include``. Hence, the following command would update the environment variable accordingly (if needed)::

   export C_INCLUDE_PATH=$C_INCLUDE_PATH:/usr/local/cuda/include

Sometimes, one also needs to set the path to the OpenCL libraries (e.g., linking errors such as /usr/bin/ld: cannot find -lOpenCL). On Linux-based systems, adapting the library path usually fixes such problems::

   export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/cuda/lib64

.. admonition:: No OpenCL Support?

   In case OpenCL is not supported on the system, one can still compile **standard k-d tree implementation** by setting the global variable `BUFFERKDTREE_KDTREE_ONLY` to `True`. On Linux-based systems, this can be achieved via 

   export BUFFERKDTREE_KDTREE_ONLY=True
   

Virtualenv & Pip
----------------

As for most Python packages, we recommend to make use of `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ to install the package. To install virtualenv on recent Debian/Ubuntu-based systems, the following commands can be used to install virtualenv and pip::

   $ sudo apt-get install python-virtualenv python-pip

Afterwards, a new virtual environment can be created to install the Numpy and the bufferkdtree package::

   $ mkdir ~/.virtualenvs
   $ cd ~/.virtualenvs
   $ virtualenv bufferkdtree
   $ source bufferkdtree/bin/activate
   $ pip install numpy==1.6.1
   $ pip install bufferkdtree

