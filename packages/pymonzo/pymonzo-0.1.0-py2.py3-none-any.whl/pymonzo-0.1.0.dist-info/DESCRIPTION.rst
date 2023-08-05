pymonzo
=======

|Build Status| |PyPI Version| |Python Versions| |License|

Python library that nicely wraps `Monzo <https://monzo.com/>`__ public
API and allows you to use it directly from your Python project.

To use the library you have to provide it with you Monzo access token.
You can either do that by exporting it as an environment variable
(``$ export MONZO_ACCESS_TOKEN="YOUR_ACTUAL_ACCESS_TOKEN"``) or by
passing it explicitly to ``MonzoAPI()``.

The library currently does not implement feed items, webhooks and
attachments endpoints - I plan to add them in the future, but they
were't essential to my current needs and they could be completely
different in the future - per
`docs <https://monzo.com/docs/#introduction>`__: > The Monzo API is
under active development. Breaking changes should be expected.

The major addition I do want to add is better authentication support -
currently access tokens can be taken directly from the developer
playground and only last a couple of hours which is really annoying.

Installation
------------

>From PyPI:

.. code:: shell

    $ pip install pymonzo

API
---

There's no documentation as of now, but the code is commented and
*should* be pretty straightforward to use.

But feel free to ask me via `mail <mailto:pawel.adamczak@sidnet.info>`__
or `GitHub issues <https://github.com/pawelad/pymonzo>`__ if anything is
unclear.

Tests
-----

Package was tested with ``pytest`` and ``tox`` on Python 2.7, 3.4 and
3.5 (see ``tox.ini``).

To run tests yourself you need to set environment variables with access
token before running ``tox`` inside the repository:

.. code:: shell

    $ export MONZO_ACCESS_TOKEN="YOUR_ACTUAL_ACCESS_TOKEN"
    $ tox

Contributions
-------------

Package source code is available at
`GitHub <https://github.com/pawelad/pymonzo>`__.

Feel free to use, ask, fork, star, report bugs, fix them, suggest
enhancements and point out any mistakes.

Authors
-------

Developed and maintained by `Paweł
Adamczak <https://github.com/pawelad>`__.

Released under [MIT
License][`license <https://github.com/pawelad/pymonzo/blob/master/LICENSE>`__].

.. |Build Status| image:: https://img.shields.io/travis/pawelad/pymonzo.svg
   :target: https://travis-ci.org/pawelad/pymonzo
.. |PyPI Version| image:: https://img.shields.io/pypi/v/pymonzo.svg
   :target: https://pypi.python.org/pypi/pymonzo
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/pymonzo.svg
   :target: https://pypi.python.org/pypi/pymonzo
.. |License| image:: https://img.shields.io/github/license/pawelad/pymonzo.svg
   :target: https://github.com/pawelad/pymonzo/blob/master/LICENSE


