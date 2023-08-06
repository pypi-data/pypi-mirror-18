import random
import time

class Backoff(object):
    """
    Exponential backoff with full jitter
    <https://www.awsarchitectureblog.com/2015/03/backoff.html>

    e.g:
        backoff.sleep()
        success = do_a_thing()
        backoff.update(success)
    """

    def __init__(self, base_seconds, max_seconds, failures=0, random=random):
        self.base_seconds = base_seconds
        self.max_seconds = max_seconds
        self.failures = failures
        self.random = random

    def sleep(self):
        time.sleep(self.seconds)

    def update(self, success):
        if success:
            self.failures = max(0, self.failures - 1)
        else:
            self.failures += 1

    @property
    def seconds(self):
        return self._apply_full_jitter(self._get_raw_seconds())

    @property
    def failures(self):
        return self._failures

    @failures.setter
    def failures(self, failures):
        if not isinstance(failures, int) or failures < 0:
            raise ValueError("Expected positive integer, received {!r}".format(failures))
        self._failures = failures

    def _get_raw_seconds(self):
        if self._failures == 0:
            return 0
        else:
            return min(self.max_seconds, self.base_seconds * 2 ** (self._failures - 1))

    def _apply_full_jitter(self, seconds):
        return self.random.uniform(0, seconds)
