===============
 flufl.testing
===============

This is a small collection of test helpers that I use in almost all my
packages.  Specifically, plugins for the following test tools are provided:

* nose2
* flake8

Python 3.5 is the minimum supported version.


Using test helpers
==================

You can use each of the plugins independently.  For example, if you use flake8
but you don't use nose2, just enable the flake8 plugin and ignore the rest.


flake8 import order plugin
--------------------------

This flake8_ plugin enables import order checks as are used in the `GNU
Mailman`_ project.  Specifically, it enforces the following rules:

* Non-``from`` imports must precede ``from``-imports.
* Exactly one line must separate the block of non-``from`` imports from the
  block of ``from`` imports.
* Import exactly one module per non-``from`` import line.
* Lines in the non-``from`` import block are sorted by length first, then
  alphabetically.  Dotted imports count toward both restrictions.
* Lines in the ``from`` import block are sorted alphabetically.
* Multiple names can be imported in a ``from`` import line, but those names
  must be sorted alphabetically.
* Names imported from the same module in a ``from`` import must appear in the
  same import statement.

It's so much easier to see an example::

    import copy
    import socket
    import logging
    import smtplib

    from mailman import public
    from mailman.config import config
    from mailman.interfaces.mta import IMailTransportAgentDelivery
    from mailman.mta.connection import Connection
    from zope.interface import implementer

To enable this plugin, add the following to your ``tox.ini`` or any other
`flake8 recognized configuration file`_::

    [flake8]
    enable-extensions = U4


nose2 plugin
------------

The `nose2`_ plugin enables a few helpful things for folks who use that test
runner:

* Implements better support for doctests, including supporting layers.
* Enables sophisticated test pattern matching.
* Provides test tracing.
* A *log to stderr* flag that you can check [1]_
* Pluggable doctest setup/teardowns.

To enable this plugin, add the following to your ``unittest.cfg`` file::

    plugins = flufl.testing.nose

Now when you run your tests, you can include one or more ``-P`` options, which
provide patterns to match your tests against.  If given, only tests matching
the given pattern are run.  This is especially helpful if your test suite is
huge.  These patterns can match a test name, class, module, or filename, and
follow Python's regexp syntax.


Author
======

``flufl.testing`` is Copyright (C) 2013-2016 Barry Warsaw <barry@python.org>

Licensed under the terms of the Apache License, Version 2.0.


Project details
===============

 * Project home: https://gitlab.com/warsaw/flufl.testing
 * Report bugs at: https://gitlab.com/warsaw/flufl.testing/issues
 * Code hosting: https://gitlab.com/warsaw/flufl.testing.git
 * Documentation: https://gitlab.com/warsaw/flufl.testing/tree/master


Footnotes
=========

.. [1] It's up to your application to do something with this flag.


.. _flake8: http://flake8.pycqa.org/en/latest/index.html
.. _`GNU Mailman`: http://www.list.org
.. _`flake8 recognized configuration file`: http://flake8.pycqa.org/en/latest/user/configuration.html
.. _nose2: http://nose2.readthedocs.io/en/latest/index.html
