=======
calllib
=======

Overview
========

``calllib`` provides 3 functions, ``apply``, ``getargs``, and
``inspect_params``. These functions are used to inspect and call
Python functions whose parameters are not known in advance, but are
determined at runtime from a mapping of available objects.

This is particularly useful in plug-in frameworks, where you don't
want every callback function to be required to have identical
signatures. Instead, each function can take a subset of available
parameters.

For example::

    >>> from __future__ import print_function
    >>> import calllib

    >>> def callback1(time):
    ...    print('callback1 called at:', time)

    >>> def callback2(time, reason):
    ...    print('callback2 called at:', time, 'reason:', reason)

    # register the callbacks
    >>> callbacks = [callback1, callback2]

    # elsewhere: compute the total universe of possible
    #  callback arguments
    >>> args = {'time': 'noon', 'reason': 'abort'}
    >>> for callback in callbacks:
    ...    calllib.apply(callback, args)  # execute each callback
    callback1 called at: noon
    callback2 called at: noon reason: abort

The last line shows that you can call any callback routine without
knowing its exact arguments, as long as its arguments are a subset of
the available arguments.

apply()
-------

``apply(callable, args)``

  * `callable` - Any callable object that can be inspected with the
    `inspect` module.

  * `args` - A mapping object, typically a `dict`, that contains the
    available arguments that will be passed to `callable`.

  `callable` is inpsected with ``getargs`` and the its parameters are
  extracted by name. For each parameter the corresponding value is
  retrieved from `args` by name and passed to the callable.

  ``apply`` returns the result of executing `callable` with the
  computed arguments.


getargs()
---------

``getargs(callable, args)``

  * `callable` - Any callable object that can be inspected with the
    `inspect` module.

  * `args` - A mapping object, typically a `dict`, that contains the
    available arguments that could be passed to `callable`.

  `callable` is inspected to determine its parameters. For each
  parameter the corresponding value is retrieved from `args`. If a
  parameter is not found in args `callable` has a default value for
  that parameter, the default value is retrieved.

  ``getargs`` returns a list of actual argument values that would be
  passed to `callable`.


inspect_params()
----------------

``inspect_params(callable)``

  * `callable` - Any callable object that can be inspected with the
    `inspect` module.

  `callable` is inspected to deterine its parameters and default
  values, if any. ``inspect_params`` returns a tuple containing a
  list of parameter names and a dict with default values, if any.  For
  example::

    >>> def foo(x, y=0, z=6): pass
    ...
    >>> calllib.inspect_params(foo)
    (['x', 'y', 'z'], {'y': 0, 'z': 6})

    >>> class Baz(object):
    ...     def __init__(self, x, y='hello'): pass
    ...
    >>> calllib.inspect_params(Baz)
    (['x', 'y'], {'y': 'hello'})


Types of callables supported
============================

``calllib`` supports any callable written in Python. This includes
functions, bound and unbound methods, classes, and object instances
with `__call__` members.

Because they are not introspectable by the inspect module, built in
Python functions such as ``len`` cannot be used with ``apply``.

Default arguments
=================

Functions with default arguments are fully supported by
``calllib``. If an argument is not specified in the `args` parameter
to ``apply`` and it has a default, the default value will be used.

Testing
=======

To test, run 'python setup.py test'. On python >= 3.0, this also runs the doctests.

Change log
==========

1.8 2016-10-27 Eric V. Smith
----------------------------

* Remove hack for changing RPM name (issue #7).

* Always require setuptools (issue #6).

* No code changes.

1.7 2015-05-16 Eric V. Smith
----------------------------

* Removed 'test' package, so it won't get installed by bdist_*. It's still
  included in sdists.

* No code changes.

1.6 2015-05-15 Eric V. Smith
----------------------------

* Changed RPM name to python3-calllib if running with python 3.

* No code changes.

1.5 2014-12-07 Eric V. Smith
----------------------------

* Added inspect_params (issue #5).

1.4 2014-07-24 Eric V. Smith
----------------------------

* Release version 1.4. No code changes.

* Add a README.txt entry on running the test suite.

* Fix missing test/__init__.py in the sdist.

1.3 2014-03-14 Eric V. Smith
----------------------------

* Add MANIFEST.in to MANIFEST.in, so it will be included in sdists
  (issue #4).

1.2 2014-02-12 Eric V. Smith
----------------------------

* New release just to update development status classifier.

1.1 2014-02-12 Eric V. Smith
----------------------------

* Produce an RPM named python-calllib (issue #3).

* Support python3 (issue #2).

* Moved tests to a separate module (issue #1).

1.0 2011-11-10 Eric V. Smith
----------------------------

* Finalized API.

* Added tests for derived classes.

0.2 2011-11-10 Eric V. Smith
----------------------------

* Allow for classes with no __init__ method.

* Normalize test names.

0.1 2011-11-09 Eric V. Smith
----------------------------

* Initial release.


