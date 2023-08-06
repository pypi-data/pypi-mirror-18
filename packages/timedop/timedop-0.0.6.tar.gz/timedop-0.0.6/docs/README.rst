TimedOp
=======

A module to roughly measure the amount of time Python operations take.
There is also a ``timed_call`` function that will enforce a time limit
on function calls.

Examples
--------

Basic
~~~~~

.. code:: python

    from timedop import TimedOp

    with TimedOp(label='Elapsed: ') as t:
        # Some long operation?
        busy_work()
    print(t)

Output:

::

    Elapsed: 0.24

Timed Call
~~~~~~~~~~

.. code:: python

    from timedop import timed_call, TimedOut

    def busy_work(stop, increment=1):
        """ A dummy function, to simulate some work. """
        start = 0
        while start < stop:
            start += increment
        return start

    # Allow 2 seconds for busy_work() to return:
    try:
        result = timed_call(
            busy_work,
            args=(100000000000, ),
            kwargs={'increment': 2},
            timeout=2
        )
    except TimedOut as ex:
        print('Uh oh.')
        print(ex)
    else:
        # Doesn't happen on my machine.
        print(result)

Output:

::

    Uh oh.
    Operation timed out. (busy_work(100000000000, increment=2), 2 seconds)

API
---

TimedOp
~~~~~~~

A ``TimedOp`` is just a timer that you can ``start`` and ``stop``. You
can initialise a ``TimedOp`` with an optional ``label``, which will be
used for ``str()`` or ``repr()``.

.. code:: python

    t = TimedOp(label='Time elapsed: ').start()
    something()
    print(t.stop())

A ``TimedOp`` can also be used as a context manager. The ``start``
method is called on ``__enter__``, and ``stop`` is called on
``__exit__``.

.. code:: python

    with TimedOp(label='Elapsed: ') as t:
        something()
    # Prints the time elapsed while inside the `with` block.
    print(t)

TimedOp Methods:
^^^^^^^^^^^^^^^^

-  ``elapsed``: Return the number of seconds since the ``TimedOp``
   started.

-  ``set_format(fmt)``: Set the default format string for the elapsed
   seconds and returns ``self``. Default: ``'{:0.2f}'``

-  ``sleep(seconds)``: Shortcut for ``time.sleep(seconds)``

-  ``start``: Starts the timer, and returns ``self``.

-  ``stop``: Stops the timer, and returns ``self``.

TimedOut
~~~~~~~~

An exception that is raised from ``timed_call``, containing information
about the timed function call such as:

-  ``self.func``: The function object.
-  ``self.args``: The arguments provided to the function.
-  ``self.kwargs``: The keyword arguments provided to the function.
-  ``self.timeout``: The timeout that was set for the timed call.
-  ``self.formatted``: A string representing all of the above
   information. Used for ``str(TimedOut)``.

timed\_call
~~~~~~~~~~~

.. code:: python

    timed_call(func, args=None, kwargs=None, timeout=DEFAULT_TIMEOUT)

Calls a function (``func``), and raises ``TimedOut`` if the function
call takes more than ``timeout`` seconds. The default timeout is set to
``timedop.DEFAULT_TIMEOUT`` (4 seconds).

Returns the result from calling ``func(*args, **kwargs)`` unless it
times out.

timed\_call Arguments
^^^^^^^^^^^^^^^^^^^^^

-  ``func``: The function to call.

-  ``args``: A ``list``/``tuple`` of arguments to use when calling the
   function (``func``).

-  ``kwargs``: A ``dict`` of keyword arguments to use when calling the
   function (``func``).

-  ``timeout``: The number of seconds to wait before raising a
   ``TimedOut`` exception. This is set to ``timedop.DEFAULT_SECONDS`` by
   default (4 seconds).
