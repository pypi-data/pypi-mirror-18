Librato BG
==========

|Build Status| |Coverage Status|

Enables submitting of Librato events in a background thread. Heavily
inspired by segment.io's python library which does the same.

Usage
-----

.. code:: python

    from librato_bg import Client

    # initialize with Librato API tokens
    client = Client(username, token)

    # track as your normally would, params are event, value and source.
    # This is non-blocking, submission will take place in other thread
    client.gauge('user_clicked', 1, 'prod')

    # when exiting, flush to join threads and make sure everything is sent
    client.join()

.. |Build Status| image:: https://travis-ci.org/nyaruka/python-librato-bg.svg?branch=master
   :target: https://travis-ci.org/nyaruka/python-librato-bg
.. |Coverage Status| image:: https://coveralls.io/repos/github/nyaruka/python-librato-bg/badge.svg?branch=master
   :target: https://coveralls.io/github/nyaruka/python-librato-bg


