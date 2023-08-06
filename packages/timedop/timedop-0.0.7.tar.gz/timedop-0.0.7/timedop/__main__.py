""" TimedOp

    An example of basic TimedOp usage.
    -Christopher Welborn 10-4-16
"""
from __future__ import print_function, with_statement
import random

from .timedop import __version__, timed_call, TimedOp, TimedOut


def busy_work(x, increment=1):
    """ A dummy function, to simulate some work. """
    stop = x or random.choice((4000000, 5000000, 7000000))
    start = 0
    while start < stop:
        start += increment
    return start

if __name__ == '__main__':
    print('\n'.join((
        'TimedOp v. {ver}',
        'For example usage, look in: {path}\n',
    )).format(
        ver=__version__,
        path=__file__,
    ))

    # Basic example.
    t = TimedOp(label='Elapsed: ').set_format('{:0.2f}s').start()
    print('Simulating some long operation.')
    busy_work(0)
    print(t.stop())

    # Context manager example.
    print()
    with TimedOp(label='Elapsed: ') as t:
        for i in range(1, 4):
            busy_work(0)
            print('{}: {}'.format(i, t))

    # Nested example.
    print()
    with TimedOp('Total: ') as t:
        for i in range(1, 4):
            with TimedOp('Sub Operation {}: '.format(i)) as tsub:
                busy_work(0)
            print(tsub)
        print(t)

    # This 100 billion value will purposely cause a TimedOut, on my machine.
    for value in (5000000, 100000000000):
        try:
            # A timed/joined function call.
            print('\nA timed call returned: {}'.format(
                timed_call(
                    busy_work,
                    args=(value, ),
                    kwargs={'increment': 2},
                    timeout=2
                )
            ))
        except TimedOut as ex:
            print('\n{}'.format(ex))
