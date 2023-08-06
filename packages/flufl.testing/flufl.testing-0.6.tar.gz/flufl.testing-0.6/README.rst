===============
 flufl.testing
===============

This is a small collection of test helpers that I use in almost all my
packages.  Specifically, plugins for the following test tools are provided:

* nose2_
* flake8_

Python 3.4 is the minimum supported version.


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

To enable this plugin [#]_, add the following to your ``tox.ini`` or any other
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
* A *log to stderr* flag that you can check. [#]_
* Pluggable doctest setup/teardowns.

To enable this plugin, add the following to your ``unittest.cfg`` file, in the
``[unittest]`` section::

    plugins = flufl.testing.nose

You also need to add this section to ``unittest.cfg``, where *<package>* names
the top-level package you want to test::

    [flufl.testing]
    always-on = True
    package = <package>

Now when you run your tests, you can include one or more ``-P`` options, which
provide patterns to match your tests against.  If given, only tests matching
the given pattern are run.  This is especially helpful if your test suite is
huge.  These patterns can match a test name, class, module, or filename, and
follow Python's regexp syntax.

The following options are also available by setting configuration variables in
your ``unittest.cfg`` file, under the ``[flufl.testing]`` section.


Doctests
~~~~~~~~

The plugin also provides some useful features for doctests.  If you make a
directory a package in your source tree (i.e. by adding an `__init__.py`), you
can optionally also add specify a `nose2 layer`_ to use for the doctest.  Bind
the layer object you want to the ``layer`` attribute in the ``__init__.py``
and it will be automatically assigned to the doctest's ``layer`` attribute for
nose2 to find.

Also for doctests, you can specify the ``setUp()`` and ``tearDown()`` methods
you want by adding the following::

    setup = my.package.namespace.setup
    teardown = my.package.other.namespace.teardown

The named packages will be imported, with the last path component naming an
attribute in the module.  This attribute should be a function taking a single
argument, in the style used by the stdlib ``doctest.DocFileTest`` class [#]_.

You can also name a default layer by setting::

    default_layer = my.package.layers.DefaultLayer.

This has the same format as the ``setup`` and ``teardown settings, except that
it should name a class.


Pre-test initialization
~~~~~~~~~~~~~~~~~~~~~~~

If you need to do anything before the tests starts, such as initialize
database connections or acquire resources, set this::

    start_run = my.package.initializer

This has the same format as the ``setup`` and ``teardown`` settings, except
that it takes a single argument which is the plugin instance.  You can use
this plugin instance for example to check if the ``-E`` option was given on
the command line.  This flag sets the ``stderr`` attribute to True on the
plugin instance.


Tracing
~~~~~~~

If you add this the plugin will also print some additional tracers to stderr
for ever test as it starts and stops::

    trace = True



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

.. [#] Note that flake8 3.1 or newer is required.
.. [#] It's up to your application to do something with this flag.
.. [#] This class is undocumented, so use the doctest_ module source to grok
       the details.


.. _flake8: http://flake8.pycqa.org/en/latest/index.html
.. _`GNU Mailman`: http://www.list.org
.. _`flake8 recognized configuration file`: http://flake8.pycqa.org/en/latest/user/configuration.html
.. _nose2: http://nose2.readthedocs.io/en/latest/index.html
.. _`nose2 layer`: http://nose2.readthedocs.io/en/latest/plugins/layers.html
.. _doctest: https://docs.python.org/3/library/doctest.html
