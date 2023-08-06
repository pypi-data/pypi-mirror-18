OutputCatcher
=============

A context manager that catches/suppresses output from ``sys.stderr`` and
``sys.stdout``.

Usage
-----

.. code:: python

    from outputcatcher import StdErrCatcher, StdOutCatcher

    # Catching stdout
    with StdOutCatcher() as fakeout:
        print('This is a test. you shouldn\'t see it right away.')
    print('Captured stdout: {}'.format(fakeout.output))

    # Catching stderr
    with StdErrCatcher() as fakeerr:
        print('Testing stderr output.', file=sys.stderr)
    print('Captured stderr: {}'.format(fakeerr.output))

API
---

.. code:: python

    StdOutCatcher(escaped=False, max_length=0)

Arguments
~~~~~~~~~

-  ``escaped``: If truthy, output is "encoded" using ``repr()``, but
   without quotes. Default: ``False``
-  ``max_length``: If non-zero, final output will not exceed
   ``max_length``. Once ``max_length`` is reached, further ``write()``
   calls will not write to the original stream. Default: ``0``
