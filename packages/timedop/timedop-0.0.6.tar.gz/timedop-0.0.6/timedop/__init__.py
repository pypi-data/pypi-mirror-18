""" TimedOp

    A "timer" class to roughly time python operations, including a context
    manager for easy access.
    Also provides a "timed call" function, which will time out if a function
    call takes too long.
    -Christopher Welborn 10-4-16
"""

from .timedop import (
    __version__,
    timed_call,
    TimedOp,
    TimedOut,
    DEFAULT_TIMEOUT,
)

__all__ = [
    '__version__',
    'timed_call',
    'TimedOp',
    'TimedOut',
    'DEFAULT_TIMEOUT',
]
