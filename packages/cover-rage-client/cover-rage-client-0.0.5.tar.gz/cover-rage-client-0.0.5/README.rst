===================
Cover Rage - server
===================
.. image:: https://badge.fury.io/py/cover-rage-client.svg
    :target: https://badge.fury.io/py/cover-rage-client
.. image:: https://circleci.com/gh/alexryabtsev/cover_rage_client/tree/master.svg?style=shield
    :target: https://circleci.com/gh/alexryabtsev/cover_rage_client/tree/master

Run **rage_client** on CI after running tests.

It will check test coverage for new lines of code and send this data to `cover rage server`_.

-----
Usage
-----

.. code-block:: shell

    rage_client <cover_rage_server_url> <cover_rage_app_token> </path/to/git/root> </path/to/coverage.xml>

.. _cover rage server: https://github.com/alexryabtsev/cover_rage_server
