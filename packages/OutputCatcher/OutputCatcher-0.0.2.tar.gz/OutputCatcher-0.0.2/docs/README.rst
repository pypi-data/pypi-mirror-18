OutputCatcher
=============

A context manager that catches/suppresses output from ``sys.stderr`` and
``sys.stdout``.

Usage
-----

.. code:: python

    from outputcatcher import StdErrCatcher, StdOutCatcher

    # Catching stdout
    with StdOutCatcher(safe=False, maxlength=0) as fakeout:
        print('This is a test. you shouldn\'t see it right away.')
    print('Captured stdout: {}'.format(fakeout.output))

    # Catching stderr
    with StdErrCatcher(safe=False, maxlength=0) as fakeerr:
        print('Testing stderr output.', file=sys.stderr)
    print('Captured stderr: {}'.format(fakeerr.output))

API
---

.. code:: python

    StdOutCatcher(safe=False, maxlength=0)

Arguments
~~~~~~~~~

-  ``safe``: If truthy, output is "encoded" using ``repr()``. Default:
   ``False``
-  ``maxlength``: If non-zero, trim each ``write()`` call to
   ``maxlength``. Default: ``0``
