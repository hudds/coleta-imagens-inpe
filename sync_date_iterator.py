from threading import Lock, RLock
from threading_decorators import synchronized_with_attr
from datetime import datetime, timedelta

class SyncDateIterator:
    def __init__(self, d1, d2, delta):
        self.current = d1
        self.d2 = d2
        self.delta = delta
        self.lock = RLock()

    def __iter__(self):
        return self

    @synchronized_with_attr("lock")
    def __next__(self):
        self.current = self.current  + self.delta
        if self.current < self.d2:
            return self.current
        raise StopIteration