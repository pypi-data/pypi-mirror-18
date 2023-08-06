ExpBackoff
==========

An exponential backoff implementation as described in an `AWS architecture post`_. Uses full jitter.

Example
-------

.. code:: python

    from expbackoff import Backoff

    backoff = Backoff(base_seconds=0.5, max_seconds=120)

    while True:
        backoff.sleep() # Depending on previous failures, potentially delay before performing an action
        success = do_a_thing() # Perform an action, record whether it succeeded
        backoff.update(success) # Update the failure count

API
---

-  ``backoff = expbackoff.Backoff(...)``
-  Create a Backoff object. Arguments:

   -  ``base_seconds`` (required): Part of the backoff calculation, i.e
      ``base_seconds * 2 ^ (failures - 1)``
   -  ``max_seconds`` (required): Max seconds to delay, regardless of
      failure count.
   -  ``failures`` (optional): Number of current failures. Useful if
      another service is handling your retries. Defaults to ``0``.
   -  ``random`` (optional): A ``random`` object. Defaults to
      ``random.random``.

-  ``backoff.sleep()``: If failures have occurred, sleep for
   ``backoff.seconds``
-  ``backoff.update(success)``: Update the failure count by passing a
   boolean representing success.
-  ``backoff.seconds``: The current backoff time in seconds, with jitter
   applied. Zero if there are no recorded failures. Read-only.
-  ``backoff.failures``: The current number of failures. Read-only.

Alternatives
------------

Popular options are `retrying`_ and `backoff`_. These both use a
decorator API so aren’t suitable for all uses - hence ``expbackoff``.

.. _AWS architecture post: https://www.awsarchitectureblog.com/2015/03/backoff.html
.. _retrying: https://pypi.python.org/pypi/retrying
.. _backoff: https://pypi.python.org/pypi/backoff/1.3.1
