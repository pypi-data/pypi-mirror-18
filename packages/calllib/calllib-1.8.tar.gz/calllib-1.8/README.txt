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
