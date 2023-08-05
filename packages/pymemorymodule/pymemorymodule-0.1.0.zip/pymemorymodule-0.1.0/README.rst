PyMemoryModule
==============

PyMemoryModule is a Python binding for
`MemoryModule <https://github.com/fancycode/MemoryModule>`__.

|Build status|

By this module, you can load DLL completely from memory - without
storing on the disk first - all thanks to
`MemoryModule <https://github.com/fancycode/MemoryModule>`__ written by
Joachim Bauch.

How to install
==============

::

    pip install pymemorymodule

Packages are available at
`PyPI <https://pypi.python.org/pypi/pymemorymodule>`__ and `PyPI
test <https://testpypi.python.org/pypi/pymemorymodule>`__.

How to use
==========

::

    import pymemorymodule as pymm
    from ctypes import cast, c_int, CFUNCTYPE

    with open("path/to/library.dll", "rb") as fp:
        # Load DLL from bytes object
        handle = pymm.MemoryLoadLibrary(fp.read())

        # __declspec(dllexport) int add(int a, int b)
        add = cast(
            pymm.MemoryGetProcAddress(handle, "add"),
            CFUNCTYPE(c_int, c_int, c_int)
        )

        # Use function exported from DLL
        assert add(1, 2) == 3

        # Free loaded DLL
        pymm.MemoryFreeLibrary(handle)

How to build and test
=====================

::

    python setup.py build_ext -i test

How to run code check
=====================

::

    python -m pip install flake8
    python -m flake8 --show-source setup.py test.py

How to prepare README.rst
=========================

::

    python setup.py md2rst

MemoryModule
============

https://github.com/fancycode/MemoryModule

License
=======

Mozilla Public License Version 2.0 (MPL2.0)

See also `license of
MemoryModule <https://github.com/fancycode/MemoryModule/blob/master/LICENSE.txt>`__.

Note: PyMemoryModule also distributes a few lines of MIT licensed codes
taken from `py3c project <https://github.com/encukou/py3c>`__.

.. |Build status| image:: https://img.shields.io/appveyor/ci/sakurai_youhei/pymemorymodule/master.svg?label=Python%202.6%20to%202.7%2C%203.3%20to%203.5%20%2F%20win32%20%26%20win_amd64
   :target: https://ci.appveyor.com/project/sakurai_youhei/pymemorymodule/branch/master
