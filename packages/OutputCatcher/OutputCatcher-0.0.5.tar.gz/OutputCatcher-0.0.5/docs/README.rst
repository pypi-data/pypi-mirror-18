OutputCatcher
=============

A context manager that catches/suppresses output from ``sys.stderr`` and
``sys.stdout``.

API
---

StdOutCatcher / StdErrCatcher
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    StdOutCatcher(escaped=False, max_length=0)

Arguments
^^^^^^^^^

-  ``escaped``: If truthy, output is "encoded" using ``repr()``, but
   without quotes. Default: ``False``
-  ``max_length``: If non-zero, final output will not exceed
   ``max_length``. Once ``max_length`` is reached, further ``write()``
   calls will not write to the original stream. Default: ``0``

Usage
^^^^^

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

ProcessOutput
~~~~~~~~~~~~~

.. code:: python

    ProcessOutput(args, stdin_data=None, timeout=None, **popenkwargs)

After initializing a ``ProcessOutput`` object with a command to run, and
optional stdin input data, it can either be used as a context manager or
the ``run()`` method must be called. ``timeout`` is passed to
``self.proc.wait()`` before returning the output.

Arguments
^^^^^^^^^

-  ``args``: Command arguments, same as subprocess.Popen.
-  ``stdin_data``: str or bytes to send to command as stdin. Default:
   ``None``
-  ``timeout``: Time to wait for process after collecting data. Default:
   ``None``
-  ``**popenkwargs``: Any extra kwargs for Popen().

Usage
^^^^^

.. code:: python

    from outputcatcher import ProcessOutput

    # Basic usage:
    with ProcessOutput(['ls']) as p:
        print(p.stdout.decode())

    # Checking for stdout and stderr:
    with ProcessOutput(['ls', '/totally_nonexistent_dir']) as p:
        if p.stdout:
            print('Wow, it really does exist: {}'.format(p.stdout.decode()))
        else:
            print(p.stderr.decode())

    # Without a context manager:
    p = ProcessOutput(['ls'])
    stdout, stderr = p.run()

    # Sending stdin data to a process:
    stdin_data = 'Hello cat!'
    with ProcessOutput(['cat'], stdin_data=stdin_data) as p:
        assert p.stdout.decode() == stdin_data
        # cat received the data, and piped it back.
        print(p.stdout.decode())
