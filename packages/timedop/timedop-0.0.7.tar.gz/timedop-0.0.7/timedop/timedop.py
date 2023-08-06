""" TimedOp

    A "timer" class to roughly time python operations, including a context
    manager for easy access.
    Also provides a "timed call" function, which will time out if a function
    call takes too long.
    -Christopher Welborn 10-4-16
"""

import multiprocessing
import time

__version__ = '0.0.7'

# Default timeout in seconds, for timed_call().
DEFAULT_TIMEOUT = 4


def _timed_call_helper(func, pipesend, args=None, kwargs=None):
    """ Calls a function, then sends the result through a pipe that
        timed_call is ready to receive.
    """
    pipesend.send(func(*(args or []), **(kwargs or {})))


def timed_call(func, args=None, kwargs=None, timeout=DEFAULT_TIMEOUT):
    """ Calls a function in a separate process, joins that process
        after 'timeout' seconds. If the process timed out, then
        TimedOut is raised. Otherwise the result of func() is returned.

        Example:
            def myfunc(x):
                return x * 5

            result = timed_call(myfunc, args=[5], timeout=4)
            # result is now 25 if it returns within 4 seconds.

        Arguments:
            func     : Function to call in a timed thread.
            args     : List of args for the function.
            kwargs   : Dict of keyword args for the function.
            timeout  : Seconds to wait before the function times out.
                       Default: 4
    """

    piperecv, pipesend = multiprocessing.Pipe()
    funcargs = args or []
    funckwargs = kwargs or {}
    execproc = multiprocessing.Process(
        target=_timed_call_helper,
        name='ExecutionProc',
        args=(func, pipesend),
        kwargs={'args': funcargs, 'kwargs': funckwargs}
    )
    execproc.start()
    execproc.join(timeout=timeout)
    if execproc.is_alive():
        execproc.terminate()
        raise TimedOut(
            'Operation timed out.',
            func=func,
            args=funcargs,
            kwargs=funckwargs,
            timeout=timeout,
        )
    # Return the functions result, which _timed_call_helper sent.
    return piperecv.recv()


class TimedOp(object):
    """ A class/context manager to time operations.
        The times are set in "seconds since epoch".
        The TimedOp can be used standalone, with it's `start` and`stop`
        methods, plus an `elapsed` property for calculating the elapsed time.
        It can also be used as a context manager:
            with TimedOp() as t:
                print('Doing some long operation...')
                print('Time so far: {:0.2f}'.format(t.elapsed()))
    """
    # Default format for elapsed time when using str(TimedOp()).
    default_format = '{:0.2f}'

    def __init__(self, label=None):
        self.label = label
        self.timestart = None
        self.timestop = None
        self.diff = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()

    def __str__(self):
        lbl = '' if self.label is None else str(self.label)
        if self.timestart is None:
            # Hasn't been started, there is no diff.
            return ''.join((lbl, '0'))
        return ''.join((lbl, self.default_format.format(self.elapsed)))

    @property
    def elapsed(self):
        """ Return the number of seconds since this TimedOp was started.
            If the TimedOp has not been stopped, or no previous difference
            was calculated, it will be calculated on the fly and returned.
        """
        if self.timestart is None:
            raise ValueError('TimedOp hasn\'t been started yet.')
        if (self.timestop is None):
            # Update the diff value if this timer hasn't been stopped.
            self.diff = time.time() - self.timestart
        return self.diff

    def set_format(self, fmt):
        """ Set the default format string for this TimedOp. """
        examplefmts = ('{}', '{:0.2f}', '{0}')
        msg = ''.join((
            'Invalid format, expecting simple float format ({fmts})',
            ', got: {gotfmt!r}'
        )).format(
            fmts=', '.join(repr(s) for s in examplefmts),
            gotfmt=fmt,
        )
        if not fmt:
            raise ValueError(msg)
        try:
            # Ensure the fmt string will actually work.
            fmt.format(1.0)
        except (AttributeError, IndexError, KeyError, ValueError):
            raise ValueError(msg)
        self.default_format = fmt
        return self

    @staticmethod
    def sleep(seconds):
        """ Convenience method. It calls time.sleep(seconds). """
        return time.sleep(seconds)

    def start(self):
        """ Reset the start/stop time and any previous difference set.
            Returns a freshly initialized TimedOp.
        """
        self.diff = None
        self.timestop = None
        self.timestart = time.time()
        return self

    def stop(self):
        """ Stop the TimedOp, calculate the elapsed time, and return the
            TimedOp instance for method chaining.
        """
        if self.timestart is None:
            raise ValueError('TimedOp hasn\'t been started yet.')
        if self.timestop is not None:
            raise ValueError('TimedOp was already stopped.')
        self.timestop = time.time()
        self.diff = self.timestop - self.timestart
        return self


class TimedOut(Exception):
    """ Raised when a timed_call() times out.
        Arguments:
            msg     : Message/reason for the exception.
            func    : The function that timed out.
            args    : The args that were used to call the function.
            kwargs  : The kwargs that were used to call the function.
            timeout : The timeout that was set for the function.
                      Default: timedop.DEFAULT_TIMEOUT
    """
    def __init__(
            self, msg=None, func=None, args=None, kwargs=None,
            timeout=DEFAULT_TIMEOUT):
        self.msg = msg or 'Operation timed out.'
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.timeout = timeout
        funcname = getattr(self.func, '__name__', None)
        if (self.func is None) or (funcname is None):
            self.formatted = '{} ({} seconds)'.format(
                self.msg,
                self.timeout
            )
        elif funcname:
            argstr = ', '.join(repr(a) for a in self.args)
            kwargstr = ', '.join(
                '{}={!r}'.format(k, v)
                for k, v in self.kwargs.items()
            )
            msgfmt = '{msg} ({name}({args}{argsep}{kwargs}), {secs} seconds)'
            self.formatted = msgfmt.format(
                msg=self.msg,
                name=funcname,
                args=argstr,
                argsep=', ' if argstr and kwargstr else '',
                kwargs=kwargstr,
                secs=self.timeout
            )
        else:
            # A function with no name?
            self.formatted = '{} ({}, {} seconds)'.format(
                self.msg,
                self.func,
                self.timeout
            )

    def __str__(self):
        return self.formatted
