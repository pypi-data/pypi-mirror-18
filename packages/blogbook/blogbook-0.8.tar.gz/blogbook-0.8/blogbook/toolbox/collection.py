# -*- coding: utf-8 -*-

import queue
from time import monotonic as time


class SetQueue(queue.Queue):
    def __init__(self):
        queue.Queue.__init__(self)

    def _put(self, item):
        if item not in self.queue:
            queue.Queue._put(self, item)

    def peek(self, block=True, timeout=None):
        """Return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        with self.not_empty:
            if not block:
                if not self._qsize():
                    raise queue.Empty
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = time() + timeout
                while not self._qsize():
                    remaining = endtime - time()
                    if remaining <= 0.0:
                        raise queue.Empty
                    self.not_empty.wait(remaining)
            return self._peek()

    def _peek(self):
        return next(iter(self.queue))
