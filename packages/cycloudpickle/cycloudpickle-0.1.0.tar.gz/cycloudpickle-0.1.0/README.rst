=====================================
Cycloudpickle - Cloudpickle on Cython
=====================================

This module is a cythonized version of `<https://github.com/cloudpipe/cloudpickle>`_ and
``pickle._Pickler`` and is meant to be a drop in replacement which is about twice as fast.

The cloudpickle license is included in ``cycloudpickle.cycloudpickle``. The Python software
foundation license applies to the adaptation of ``pickle._Pickler``.

While cloudpickle is compatible with python 2, cycloudpickle is *not* due the adaptation of the
``pickle._Pickler`` from python 3. Python 2 support should be 'doable', but a bit difficult
because of the use of cdef classes and the inheritance between ``CloudPickler`` and ``Pickler``.
