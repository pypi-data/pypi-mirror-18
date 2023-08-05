While |python-subprocess|_ is great, it may not be the easiest library to use. This is the reason I created ``nicecall``: it allows to do simple tasks with processes very easily.

.. |python-subprocess| replace:: Python's ``subprocess`` library
.. _python-subprocess: https://docs.python.org/3/library/subprocess.html

Note that ``nicecall`` is not a substitute to ``subprocess``, because much of ``subprocess`` functionality doesn't exist. For instance, one can't use ``stdin`` or pipes with ``nicecall``. The goal is not to replace ``subprocess``, but only to provide an easy way to do the most common tasks.

How to use the library
----------------------

Note: make sure you also check `the tests <http://source.pelicandd.com/codebase/nicecall/tests/>`_ which
give a few examples of how to use the library. Most pieces of code below are in ``tests/smoke/test_docs.py``.

Fluent interface
~~~~~~~~~~~~~~~~

The library uses method chaining, which allows to add logic on the fly before actually launching the process. Methods such as ``on_stdout``, ``ignore``, etc. create a copy of the object, modify this copy, and return it to the caller. This makes it possible to reuse base objects in multiple locations in your code, reducing code duplication.

Exit code
~~~~~~~~~

Let's start by executing a task::

    result = nicecall.Process().execute(["touch", "/tmp/hello"])

The ``result`` contains the exit code, which makes it possible to determine whether the process terminated successfully. Below, the value of ``result`` is expected to be zero. You may also make it fail::

    result = nicecall.Process().execute(["touch", "/tmp/a/b/c/d"])

The ``result`` should now be ``1``, assuming you don't have ``/tmp/a/b/c`` directory.

Sometimes, one may prefer raising an exception if the process fails, instead of checking for the exit code manually. The ``raise_if_error()`` method can be used for that. When called, exit code different from zero will lead to ``subprocess.CalledProcessError`` being raised.

``stdout`` and ``stderr``
~~~~~~~~~~~~~~~~~~~~~~~~~

One can also perform a bunch of actions on ``stdout`` and ``stderr``. Let's display ``stdout`` in terminal::

    nicecall.Process().on_stdout(print).execute(["echo", "a\nb\nc"])

The output should be::

    a
    b
    c

If you just want to read ``stdout`` output, then instead of ``execute``, you can use ``read_stdout``. The following piece of code produces the same output::

    lines = nicecall.Process().read_stdout(["echo", "a\nb\nc"])
    print("\n".join(lines))

Note that when using ``read_stdout``, a non-zero exit code *will* lead to ``subprocess.CalledProcessError`` being raised, independently of the presence of ``raise_if_error()`` in the chain. The reason for this choice is that with ``read_stdout``, there is no way to check for the actual exit code, and plainly ignoring it would lead to difficult to debug situations.

Also note that ``read_stdout`` stores ``stdout`` in a list and is *not* lazy. This means that:

 * The method is appropriate only for commands which output a small quantity of lines.

 * Looping through the lines and stopping in the middle wouldn't affect neither the processing of the exit code, nor the other actions such as logging which may have been specified earlier in the chain through ``on_stdout``.

 * The lines from ``stderr`` are not returned. The ``on_stderr`` method can still be used, exactly in the same way it is with ``execute``.

 * All the actions defined through ``on_stdout`` will be performed *before* the list is returned.

 * Filters added through ``keep`` and ``ignore`` apply to the lines in the result as well.

Logging
~~~~~~~

A common thing, at least in my case, is to log ``stdout`` or ``stderr`` to syslog. With ``nicecall``, it's easy::

    # Initialize logging.
    log_handler = logging.handlers.SysLogHandler(address="/dev/log")
    formatter = logging.Formatter("demo: [%(levelname)s] %(message)s")
    log_handler.setFormatter(formatter)
    log_handler.setLevel(logging.DEBUG)

    demo_logger = logging.getLogger("demo")
    demo_logger.setLevel(logging.DEBUG)
    demo_logger.addHandler(log_handler)

    ...

    # Log stdout.
    logger = nicecall.StdoutLogger("test")
    nicecall.Process().on_stdout(logger.log).execute(["echo", "a\nb"])

Note that ``nicecall.StdoutLogger`` can be initialized with either the name of the logger, or the instance of the logger itself.

The library itself logs calls (``INFO`` level) and call failures (``WARNING`` level) through the logger named ``nicecall.process``. For instance, executing ``touch /tmp/a/b/c/d`` will produce two log messages::

    INFO:nicecall.process:Called “touch /tmp/a/b/c/d”.
    WARNING:nicecall.process:“touch /tmp/a/b/c/d” failed with exit code 1.

Filtering
~~~~~~~~~

Sometimes, you don't want to process specific content such as empty lines or whitespace. This is what filters are about::

    nicecall \
        .Process() \
        .ignore(nicecall.filters.whitespace) \
        .on_stdout(print) \
        .execute(["echo", "a\n\nb"])

Here, ``a`` and ``b`` will be displayed in terminal; however, the empty line will be ignored. The reverse is called ``keep``. Both ``keep`` and ``ignore`` accept any function which takes a string as a parameter and returns a boolean. For instance, this will print only ``stdout`` content longer than fifteen characters::

    nicecall \
        .Process() \
        .keep(lambda line: len(line) > 15) \
        .on_stdout(print) \
        .execute(["echo", "Hello World!\nWhat a lovely day!"])

Multiple ``keep`` and ``ignore`` methods can be combined. The output will keep the lines which match *all* predicates from ``keep`` methods and *none* from ``ignore`` ones.

Filters apply to both ``stdout`` and ``stderr``; there is no way to apply them to only one of the streams.

Testing
-------

In order to be able to test your code, the library provides a ``NullProcess`` class, a stub and a mock.

``NullProcess``
~~~~~~~~~~~~~~~

This class creates an object which will *not* launch any process when ``execute`` is called. The purpose of this class is to replace the actual ``Process`` class during testing.

Stub
~~~~

The stub makes it possible to emulate ``Process`` without actually doing the system calls. The difference with ``NullProcess`` is that the stub makes it possible to define the exit codes and ``stdout``/``stderr`` output for specific commands.

The stub allows to define associations between the arguments and the expected response. For instance, imagine a situation where the tested code is expected to perform two calls: one to create a directory, another one to create a file in it. We want to test how the code under testing will perform if the second command fails: are the developers handling this edge case? For this purpose, one can use the stub like this::

    stub = nicecall.tests.ProcessStub()
    stub.add_match(["mkdir", "/tmp/a"], 0)
    stub.add_match(
        ["touch", "/tmp/a/b"],
        1,
        stderr=["touch: cannot touch '/tmp/a/b': No such file or directory"])

The ``stub`` can now be passed to the code under tests instead of ``nicecall.Process()``. The tested code will run, perform a ``mkdir``, and, when executing the ``touch`` command, will get back the exit code ``1`` and a call to the actions, if any, set through ``on_stderr``.

Mock
~~~~

The mock performs in a similar way to a stub, but also records the activity of the code under tests, i.e. the parameters which were passed to different methods of the mock. Usually, the mock is used this way::

    with nicecall.tests.ProcessMockContext() as context:
        # Code under tests goes here.
        # The mock is `context.mock`.
        ...

        # Follows the assertions. In this example, I'm just ensuring that the
        # code under tests added `print` to the `stdout` actions, i.e. ran the
        # `...on_stdout(print)...` command.
        actual = context.on_stdout_actions
        expected = [print]
        self.assertCountEqual(expected, actual)

The mock makes it possible to check the following elements:

 * ``executed_args``: the ``args`` which were used when calling ``execute()`` method.

 * ``ignore_predicates``: the list of predicates added by the tested code using the ``ignore`` method.

 * ``keep_predicates``: same as previous, but for ``keep``.

 * ``on_stdout_actions``: the list of actions added by the tested code using the ``on_stdout`` method.

 * ``on_stderr_actions``: same as previous, but for ``on_stderr``.

Classes
-------

``process.py``
~~~~~~~~~~~~~~

The class is the entry point of the library. It makes it possible to specify different options before actually starting the process.

 * ``execute``: actually executes the process and blocks until the process finishes.

   *Parameters:*

   ``args`` is an array which indicates the process to start, and its parameters. Example: ``["touch", "/tmp/hello"]``.

   *Returns:*

   Returns the exit code.

 * ``keep``: specifies a filter to apply to determine if the line of ``stdout`` or ``stderr`` should be processed by the actions specified through ``on_stdout`` and ``on_stderr``.

   The method can be called multiple times and mixed with ``ignore`` to aggregate multiple filters.

   *Parameters:*

   ``predicate`` is a function which takes a string as a parameter and returns a boolean value: ``true`` if the line should be processed, or ``false`` otherwise.

   *Returns:*

   Returns a new instance of the ``Process`` class with the new filter.

 * ``ignore``: see ``keep``. Here, the predicate is reverted.

 * ``on_stdout``: adds an action to perform when a line from ``stdout`` is received.

   The method can be called multiple times if multiple actions should be performed for every line of ``stdout``.

   *Parameters:*

   ``action``: a function which takes a string as a parameter and doesn't return anything.

   *Returns:*

   Returns a new instance of the ``Process`` class with the new action.

 * ``on_stderr``: see ``on_stdout``. Here, it deals with ``stderr`` instead.

``filters.py``
~~~~~~~~~~~~~~

The file contains a bunch of filters which can be used in ``Process.keep`` and ``Process.ignore``.

``logger.py``
~~~~~~~~~~~~~

This class is used to log output from ``stdout`` or ``stderr``.

Compatibility
-------------

The library was written for Python 3 under Linux. I haven't tested it neither with Python 2, nor under Windows.

Reliability
-----------

While I used Test Driven Development when creating this library and naturally have a 100% branch coverage, I don't know neither Python, nor ``subprocess`` well enough to be sure that the library can be used reliably in production. Use at own risk.

Contributing
------------

If you want to contribute, contact me at `arseni.mourzenko@pelicandd.com <mailto:arseni.mourzenko@pelicandd.com>`_. You'll be able to contribute to the project using the `official SVN repository <http://source.pelicandd.com/codebase/nicecall/>`_. If you find it more convinient to clone the source to GitHub, you can do that too.

The source code of the library and the corresponding documentation are covered by the `MIT License <https://opensource.org/licenses/MIT>`_.
