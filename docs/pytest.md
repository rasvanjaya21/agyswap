# pytest documentation

- Version: **9.1.1**
- Source: https://github.com/pytest-dev/pytest/tree/9.1.1 (doc/en; commit `cf470ec`)
- Mirrored: 2026-10-06

Pages follow the Sphinx toctree from `doc/en/index.rst`, kept as reStructuredText. Changelog, announcements, project/governance pages and the generated plugin list are left out.

Complete official documentation for this exact version, mirrored for offline use. Not written by hand; regenerate it with `uv run python scripts/docs.py` instead of editing it.

---

# pytest: helps you write better programs
Source: https://docs.pytest.org/en/stable/index.html

.. _features:

.. sidebar:: **Next Open Trainings and Events**

    - `pytest development sprint <https://github.com/pytest-dev/sprint>`_, **July 20th -- 24th**, Klaus (AT), sign-up open until June 15th
    - `Professional Testing with Python <https://python-academy.com/courses/python_course_testing.html>`_, via `Python Academy <https://www.python-academy.com/>`_ (3 day in-depth training), **March 9th -- 11th 2027**, Leipzig (DE) / Remote

    Also see :doc:`previous talks and blogposts <talks>`

pytest: helps you write better programs
=======================================

.. toctree::
    :hidden:

    getting-started
    how-to/index
    reference/index
    explanation/index
    example/index

.. toctree::
    :caption: About the project
    :hidden:

    changelog
    contributing
    backwards-compatibility
    sponsor
    tidelift
    license
    contact

.. toctree::
    :caption: Useful links
    :hidden:

    pytest @ PyPI <https://pypi.org/project/pytest/>
    pytest @ GitHub <https://github.com/pytest-dev/pytest/>
    Issue Tracker <https://github.com/pytest-dev/pytest/issues>
    PDF Documentation <https://media.readthedocs.org/pdf/pytest/latest/pytest.pdf>

.. module:: pytest

The ``pytest`` framework makes it easy to write small, readable tests, and can
scale to support complex functional testing for applications and libraries.


**PyPI package name**: :pypi:`pytest`

A quick example
---------------

.. code-block:: python

    # content of test_sample.py
    def inc(x):
        return x + 1


    def test_answer():
        assert inc(3) == 5


To execute it:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_sample.py F                                                     [100%]

    ================================= FAILURES =================================
    _______________________________ test_answer ________________________________

        def test_answer():
    >       assert inc(3) == 5
    E       assert 4 == 5
    E        +  where 4 = inc(3)

    test_sample.py:6: AssertionError
    ========================= short test summary info ==========================
    FAILED test_sample.py::test_answer - assert 4 == 5
    ============================ 1 failed in 0.12s =============================

Due to ``pytest``'s detailed assertion introspection, only plain ``assert`` statements are used.
See :ref:`Get started <getstarted>` for a basic introduction to using pytest.


Features
--------

- Detailed info on failing :ref:`assert statements <assert>` (no need to remember ``self.assert*`` names)

- :ref:`Auto-discovery <test discovery>` of test modules and functions

- :ref:`Modular fixtures <fixture>` for managing small or parametrized long-lived test resources

- Can run :ref:`unittest <unittest>` (including trial) test suites out of the box

- Python 3.10+ or PyPy 3

- Rich plugin architecture, with over 1300+ :ref:`external plugins <plugin-list>` and thriving community


Documentation
-------------

* :ref:`Get started <get-started>` - install pytest and grasp its basics in just twenty minutes
* :ref:`How-to guides <how-to>` - step-by-step guides, covering a vast range of use-cases and needs
* :ref:`Reference guides <reference>` - includes the complete pytest API reference, lists of plugins and more
* :ref:`Explanation <explanation>` - background, discussion of key topics, answers to higher-level questions


Bugs/Requests
-------------

Please use the `GitHub issue tracker <https://github.com/pytest-dev/pytest/issues>`_ to submit bugs or request features.


Support pytest
--------------

`Open Collective`_ is an online funding platform for open and transparent communities.
It provides tools to raise money and share your finances in full transparency.

It is the platform of choice for individuals and companies that want to make one-time or
monthly donations directly to the project.

See more details in the `pytest collective`_.

.. _Open Collective: https://opencollective.com
.. _pytest collective: https://opencollective.com/pytest


pytest for enterprise
---------------------

Available as part of the Tidelift Subscription.

The maintainers of pytest and thousands of other packages are working with Tidelift to deliver commercial support and
maintenance for the open source dependencies you use to build your applications.
Save time, reduce risk, and improve code health, while paying the maintainers of the exact dependencies you use.

`Learn more. <https://tidelift.com/subscription/pkg/pypi-pytest?utm_source=pypi-pytest&utm_medium=referral&utm_campaign=enterprise&utm_term=repo>`_

Security
~~~~~~~~

If you have found an issue that you believe is a security vulnerability, please do not create an issue -- instead, report it via a `new security advisory <https://github.com/pytest-dev/pytest/security/advisories/new>`__.

# Get Started
Source: https://docs.pytest.org/en/stable/getting-started.html

.. _get-started:

Get Started
===================================

.. _`getstarted`:
.. _`installation`:

Install ``pytest``
----------------------------------------

1. Run the following command in your command line:

.. code-block:: bash

    pip install -U pytest

2. Check that you installed the correct version:

.. code-block:: bash

    $ pytest --version
    pytest 9.1.1

.. _`simpletest`:

Create your first test
----------------------------------------------------------

Create a new file called ``test_sample.py``, containing a function, and a test:

.. code-block:: python

    # content of test_sample.py
    def func(x):
        return x + 1


    def test_answer():
        assert func(3) == 5

The test

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_sample.py F                                                     [100%]

    ================================= FAILURES =================================
    _______________________________ test_answer ________________________________

        def test_answer():
    >       assert func(3) == 5
    E       assert 4 == 5
    E        +  where 4 = func(3)

    test_sample.py:6: AssertionError
    ========================= short test summary info ==========================
    FAILED test_sample.py::test_answer - assert 4 == 5
    ============================ 1 failed in 0.12s =============================

The ``[100%]`` refers to the overall progress of running all test cases. After it finishes, pytest then shows a failure report because ``func(3)`` does not return ``5``.

.. note::

    You can use the ``assert`` statement to verify test expectations. pytest’s :ref:`Advanced assertion introspection <python:assert>` will intelligently report intermediate values of the assert expression so you can avoid the many names :ref:`of JUnit legacy methods <testcase-objects>`.

Run multiple tests
----------------------------------------------------------

``pytest`` will run all files of the form ``test_*.py`` or ``*_test.py`` in the current directory and its subdirectories. More generally, it follows :ref:`standard test discovery rules <test discovery>`.


Assert that a certain exception is raised
--------------------------------------------------------------

Use the :ref:`raises <assertraises>` helper to assert that some code raises an exception:

.. code-block:: python

    # content of test_sysexit.py
    import pytest


    def f():
        raise SystemExit(1)


    def test_mytest():
        with pytest.raises(SystemExit):
            f()

Execute the test function with “quiet” reporting mode:

.. code-block:: pytest

    $ pytest -q test_sysexit.py
    .                                                                    [100%]
    1 passed in 0.12s

.. note::

    The ``-q/--quiet`` flag keeps the output brief in this and following examples.

See :ref:`assertraises` for specifying more details about the expected exception.

Group multiple tests in a class
--------------------------------------------------------------

.. regendoc:wipe

Once you develop multiple tests, you may want to group them into a class. pytest makes it easy to create a class containing more than one test:

.. code-block:: python

    # content of test_class.py
    class TestClass:
        def test_one(self):
            x = "this"
            assert "h" in x

        def test_two(self):
            x = "hello"
            assert hasattr(x, "check")

``pytest`` discovers all tests following its :ref:`Conventions for Python test discovery <test discovery>`, so it finds both ``test_`` prefixed functions. There is no need to subclass anything, but make sure to prefix your class with ``Test`` otherwise the class will be skipped. We can simply run the module by passing its filename:

.. code-block:: pytest

    $ pytest -q test_class.py
    .F                                                                   [100%]
    ================================= FAILURES =================================
    ____________________________ TestClass.test_two ____________________________

    self = <test_class.TestClass object at 0xdeadbeef0001>

        def test_two(self):
            x = "hello"
    >       assert hasattr(x, "check")
    E       AssertionError: assert False
    E        +  where False = hasattr('hello', 'check')

    test_class.py:8: AssertionError
    ========================= short test summary info ==========================
    FAILED test_class.py::TestClass::test_two - AssertionError: assert False
    1 failed, 1 passed in 0.12s

The first test passed and the second failed. You can easily see the intermediate values in the assertion to help you understand the reason for the failure.

Grouping tests in classes can be beneficial for the following reasons:

 * Test organization
 * Sharing fixtures for tests only in that particular class
 * Applying marks at the class level and having them implicitly apply to all tests

Something to be aware of when grouping tests inside classes is that each test has a unique instance of the class.
Having each test share the same class instance would be very detrimental to test isolation and would promote poor test practices.
This is outlined below:

.. regendoc:wipe

.. code-block:: python

    # content of test_class_demo.py
    class TestClassDemoInstance:
        value = 0

        def test_one(self):
            self.value = 1
            assert self.value == 1

        def test_two(self):
            assert self.value == 1


.. code-block:: pytest

    $ pytest -k TestClassDemoInstance -q
    .F                                                                   [100%]
    ================================= FAILURES =================================
    ______________________ TestClassDemoInstance.test_two ______________________

    self = <test_class_demo.TestClassDemoInstance object at 0xdeadbeef0002>

        def test_two(self):
    >       assert self.value == 1
    E       assert 0 == 1
    E        +  where 0 = <test_class_demo.TestClassDemoInstance object at 0xdeadbeef0002>.value

    test_class_demo.py:9: AssertionError
    ========================= short test summary info ==========================
    FAILED test_class_demo.py::TestClassDemoInstance::test_two - assert 0 == 1
    1 failed, 1 passed in 0.12s

Note that attributes added at class level are *class attributes*, so they will be shared between tests.

Compare floating-point values with pytest.approx
--------------------------------------------------------------

``pytest`` also provides a number of utilities to make writing tests easier.
For example, you can use :func:`pytest.approx` to compare floating-point
values that may have small rounding errors:

.. code-block:: python

    # content of test_approx.py
    import pytest


    def test_sum():
        assert (0.1 + 0.2) == pytest.approx(0.3)

This avoids the need for manual tolerance checks or using
``math.isclose`` and works with scalars, lists, and NumPy arrays.


Request a unique temporary directory for functional tests
--------------------------------------------------------------

``pytest`` provides :std:doc:`Builtin fixtures/function arguments <builtin>` to request arbitrary resources, like a unique temporary directory:

.. code-block:: python

    # content of test_tmp_path.py
    def test_needsfiles(tmp_path):
        print(tmp_path)
        assert 0

List the name ``tmp_path`` in the test function signature and ``pytest`` will lookup and call a fixture factory to create the resource before performing the test function call. Before the test runs, ``pytest`` creates a unique-per-test-invocation temporary directory:

.. code-block:: pytest

    $ pytest -q test_tmp_path.py
    F                                                                    [100%]
    ================================= FAILURES =================================
    _____________________________ test_needsfiles ______________________________

    tmp_path = PosixPath('PYTEST_TMPDIR/test_needsfiles0')

        def test_needsfiles(tmp_path):
            print(tmp_path)
    >       assert 0
    E       assert 0

    test_tmp_path.py:3: AssertionError
    --------------------------- Captured stdout call ---------------------------
    PYTEST_TMPDIR/test_needsfiles0
    ========================= short test summary info ==========================
    FAILED test_tmp_path.py::test_needsfiles - assert 0
    1 failed in 0.12s

More info on temporary directory handling is available at :ref:`Temporary directories and files <tmp_path handling>`.

Find out what kind of builtin :ref:`pytest fixtures <fixtures>` exist with the command:

.. code-block:: bash

    pytest --fixtures   # shows builtin and custom fixtures

Note that this command omits fixtures with leading ``_`` unless the :option:`-v` option is added.

Continue reading
-------------------------------------

Check out additional pytest resources to help you customize tests for your unique workflow:

* ":ref:`usage`" for command line invocation examples
* ":ref:`existingtestsuite`" for working with preexisting tests
* ":ref:`mark`" for information on the ``pytest.mark`` mechanism
* ":ref:`fixtures`" for providing a functional baseline to your tests
* ":ref:`plugins`" for managing and writing plugins
* ":ref:`goodpractices`" for virtualenv and test layouts

# How-to guides
Source: https://docs.pytest.org/en/stable/how-to/index.html

:orphan:

.. _how-to:

How-to guides
================

Core pytest functionality
-------------------------

.. toctree::
   :maxdepth: 1

   usage
   assert
   fixtures
   mark
   parametrize
   subtests
   tmp_path
   monkeypatch
   doctest
   cache

Test output and outcomes
----------------------------

.. toctree::
   :maxdepth: 1

   failures
   output
   logging
   capture-stdout-stderr
   capture-warnings
   skipping

Plugins
----------------------------

.. toctree::
   :maxdepth: 1

   plugins
   writing_plugins
   writing_hook_functions

pytest and other test systems
-----------------------------

.. toctree::
   :maxdepth: 1

   existingtestsuite
   unittest
   xunit_setup

pytest development environment
------------------------------

.. toctree::
   :maxdepth: 1

   bash-completion

# How to invoke pytest
Source: https://docs.pytest.org/en/stable/how-to/usage.html

.. _usage:

How to invoke pytest
==========================================

..  seealso:: :ref:`Complete pytest command-line flags reference <command-line-flags>`

In general, pytest is invoked with the command ``pytest`` (see below for :ref:`other ways to invoke pytest
<invoke-other>`). This will execute all tests in all files whose names follow the form ``test_*.py`` or ``*_test.py``
in the current directory and its subdirectories. More generally, pytest follows :ref:`standard test discovery rules
<test discovery>`.


.. _select-tests:

Specifying which tests to run
------------------------------

Pytest supports several ways to run and select tests from the command-line or from a file
(see below for :ref:`reading arguments from file <args-from-file>`).

**Run tests in a module**

.. code-block:: bash

    pytest test_mod.py

**Run tests in a directory**

.. code-block:: bash

    pytest testing/

**Run tests by keyword expressions**

.. code-block:: bash

    pytest -k 'MyClass and not method'

This will run tests which contain names that match the given *string expression* (case-insensitive),
which can include Python operators that use filenames, class names and function names as variables.
The example above will run ``TestMyClass.test_something``  but not ``TestMyClass.test_method_simple``.
Use ``""`` instead of ``''`` in expression when running this on Windows

.. _nodeids:

**Run tests by collection arguments**

Pass the module filename relative to the working directory, followed by specifiers like the class name and function name
separated by ``::`` characters, and parameters from parameterization enclosed in ``[]``.

To run a specific test within a module:

.. code-block:: bash

    pytest tests/test_mod.py::test_func

To run all tests in a class:

.. code-block:: bash

    pytest tests/test_mod.py::TestClass

Specifying a specific test method:

.. code-block:: bash

    pytest tests/test_mod.py::TestClass::test_method

Specifying a specific parametrization of a test:

.. code-block:: bash

    pytest tests/test_mod.py::test_func[x1,y2]

**Run tests by marker expressions**

To run all tests which are decorated with the ``@pytest.mark.slow`` decorator:

.. code-block:: bash

    pytest -m slow


To run all tests which are decorated with the annotated ``@pytest.mark.slow(phase=1)`` decorator,
with the ``phase`` keyword argument set to ``1``:

.. code-block:: bash

    pytest -m "slow(phase=1)"

For more information see :ref:`marks <mark>`.

**Run tests from packages**

.. code-block:: bash

    pytest --pyargs pkg.testing

This will import ``pkg.testing`` and use its filesystem location to find and run tests from.

.. _args-from-file:

**Read arguments from file**

.. versionadded:: 8.2

All of the above can be read from a file using the ``@`` prefix:

.. code-block:: bash

    pytest @tests_to_run.txt

where ``tests_to_run.txt`` contains an entry per line, e.g.:

.. code-block:: text

    tests/test_file.py
    tests/test_mod.py::test_func[x1,y2]
    tests/test_mod.py::TestClass
    -m slow

This file can also be generated using ``pytest --collect-only -q`` and modified as needed.

Getting help on version, option names, environment variables
--------------------------------------------------------------

.. code-block:: bash

    pytest --version   # shows where pytest was imported from
    pytest --fixtures  # show available builtin function arguments
    pytest -h | --help # show help on command line and config file options


.. _durations:

Profiling test execution duration
-------------------------------------

.. versionchanged:: 6.0

To get a list of the slowest 10 test durations over 1.0s long:

.. code-block:: bash

    pytest --durations=10 --durations-min=1.0

By default, pytest will not show test durations that are too small (<0.005s) unless ``-vv`` is passed on the command-line.


Managing loading of plugins
-------------------------------

Early loading plugins
~~~~~~~~~~~~~~~~~~~~~~~

You can early-load plugins (internal and external) explicitly in the command-line with the :option:`-p` option::

    pytest -p mypluginmodule

The option receives a ``name`` parameter, which can be:

* A full module dotted name, for example ``myproject.plugins``. This dotted name must be importable.
* The entry-point name of a plugin. This is the name passed to ``importlib`` when the plugin is
  registered. For example to early-load the :pypi:`pytest-cov` plugin you can use::

    pytest -p pytest_cov


Disabling plugins
~~~~~~~~~~~~~~~~~~

To disable loading specific plugins at invocation time, use the :option:`-p` option
together with the prefix ``no:``.

Example: to disable loading the plugin ``doctest``, which is responsible for
executing doctest tests from text files, invoke pytest like this:

.. code-block:: bash

    pytest -p no:doctest


.. _invoke-other:

Other ways of calling pytest
-----------------------------------------------------

.. _invoke-python:

Calling pytest through ``python -m pytest``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can invoke testing through the Python interpreter from the command line:

.. code-block:: text

    python -m pytest [...]

This is almost equivalent to invoking the command line script ``pytest [...]``
directly, except that calling via ``python`` will also add the current directory to ``sys.path``.


.. _`pytest.main-usage`:

Calling pytest from Python code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can invoke ``pytest`` from Python code directly:

.. code-block:: python

    retcode = pytest.main()

this acts as if you would call "pytest" from the command line.
It will not raise :class:`SystemExit` but return the :ref:`exit code <exit-codes>` instead.
If you don't pass it any arguments, ``main`` reads the arguments from the command line arguments of the process (:data:`sys.argv`), which may be undesirable.
You can pass in options and arguments explicitly:

.. code-block:: python

    retcode = pytest.main(["-x", "mytestdir"])

You can specify additional plugins to ``pytest.main``:

.. code-block:: python

    # content of myinvoke.py
    import sys

    import pytest


    class MyPlugin:
        def pytest_sessionfinish(self):
            print("*** test run reporting finishing")


    if __name__ == "__main__":
        sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))

Running it will show that ``MyPlugin`` was added and its
hook was invoked:

.. code-block:: pytest

    $ python myinvoke.py
    *** test run reporting finishing


.. note::

    Calling ``pytest.main()`` will result in importing your tests and any modules
    that they import. Due to the caching mechanism of python's import system,
    making subsequent calls to ``pytest.main()`` from the same process will not
    reflect changes to those files between the calls. For this reason, making
    multiple calls to ``pytest.main()`` from the same process (in order to re-run
    tests, for example) is not recommended.

# How to write and report assertions in tests
Source: https://docs.pytest.org/en/stable/how-to/assert.html

.. _`assert`:

How to write and report assertions in tests
==================================================

.. _`assert with the assert statement`:

Asserting with the ``assert`` statement
---------------------------------------------------------

``pytest`` allows you to use the standard Python ``assert`` for verifying
expectations and values in Python tests.  For example, you can write the
following:

.. code-block:: python

    # content of test_assert1.py
    def f():
        return 3


    def test_function():
        assert f() == 4

to assert that your function returns a certain value. If this assertion fails
you will see the return value of the function call:

.. code-block:: pytest

    $ pytest test_assert1.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_assert1.py F                                                    [100%]

    ================================= FAILURES =================================
    ______________________________ test_function _______________________________

        def test_function():
    >       assert f() == 4
    E       assert 3 == 4
    E        +  where 3 = f()

    test_assert1.py:6: AssertionError
    ========================= short test summary info ==========================
    FAILED test_assert1.py::test_function - assert 3 == 4
    ============================ 1 failed in 0.12s =============================

``pytest`` has support for showing the values of the most common subexpressions
including calls, attributes, comparisons, and binary and unary
operators. (See :ref:`tbreportdemo`).  This allows you to use the
idiomatic python constructs without boilerplate code while not losing
introspection information.

If a message is specified with the assertion like this:

.. code-block:: python

    assert a % 2 == 0, "value was odd, should be even"

it is printed alongside the assertion introspection in the traceback.

See :ref:`assert-details` for more information on assertion introspection.

Assertions about approximate equality
-------------------------------------

When comparing floating point values (or arrays of floats), small rounding
errors are common. Instead of using ``assert abs(a - b) < tol`` or
``numpy.isclose``, you can use :func:`pytest.approx`:

.. code-block:: python

    import pytest
    import numpy as np


    def test_floats():
        assert (0.1 + 0.2) == pytest.approx(0.3)


    def test_arrays():
        a = np.array([1.0, 2.0, 3.0])
        b = np.array([0.9999, 2.0001, 3.0])
        assert a == pytest.approx(b)

``pytest.approx`` works with scalars, lists, dictionaries, and NumPy arrays.
It also supports comparisons involving NaNs.

See :func:`pytest.approx` for details.

.. _`assertraises`:

Assertions about expected exceptions
------------------------------------------

In order to write assertions about raised exceptions, you can use
:func:`pytest.raises` as a context manager like this:

.. code-block:: python

    import pytest


    def test_zero_division():
        with pytest.raises(ZeroDivisionError):
            1 / 0

and if you need to have access to the actual exception info you may use:

.. code-block:: python

    def test_recursion_depth():
        with pytest.raises(RuntimeError) as excinfo:

            def f():
                f()

            f()
        assert "maximum recursion" in str(excinfo.value)

``excinfo`` is an :class:`~pytest.ExceptionInfo` instance, which is a wrapper around
the actual exception raised.  The main attributes of interest are
``.type``, ``.value`` and ``.traceback``.

Note that ``pytest.raises`` will match the exception type or any subclasses (like the standard ``except`` statement).
If you want to check if a block of code is raising an exact exception type, you need to check that explicitly:


.. code-block:: python

    def test_foo_not_implemented():
        def foo():
            raise NotImplementedError

        with pytest.raises(RuntimeError) as excinfo:
            foo()
        assert excinfo.type is RuntimeError

The :func:`pytest.raises` call will succeed, even though the function raises :class:`NotImplementedError`, because
:class:`NotImplementedError` is a subclass of :class:`RuntimeError`; however the following `assert` statement will
catch the problem.

Matching exception messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can pass a ``match`` keyword parameter to the context-manager to test
that a regular expression matches on the string representation of an exception
(similar to the ``TestCase.assertRaisesRegex`` method from ``unittest``):

.. code-block:: python

    import pytest


    def myfunc():
        raise ValueError("Exception 123 raised")


    def test_match():
        with pytest.raises(ValueError, match=r".* 123 .*"):
            myfunc()

Notes:

* The ``match`` parameter is matched with the :func:`re.search`
  function, so in the above example ``match='123'`` would have worked as well.
* The ``match`` parameter also matches against `PEP-678 <https://peps.python.org/pep-0678/>`__ ``__notes__``.


.. _`assert-matching-exception-groups`:

Assertions about expected exception groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When expecting a :exc:`BaseExceptionGroup` or :exc:`ExceptionGroup` you can use :class:`pytest.RaisesGroup`:

.. code-block:: python

    def test_exception_in_group():
        with pytest.RaisesGroup(ValueError):
            raise ExceptionGroup("group msg", [ValueError("value msg")])
        with pytest.RaisesGroup(ValueError, TypeError):
            raise ExceptionGroup("msg", [ValueError("foo"), TypeError("bar")])


It accepts a ``match`` parameter, that checks against the group message, and a ``check`` parameter that takes an arbitrary callable which it passes the group to, and only succeeds if the callable returns ``True``.

.. code-block:: python

    def test_raisesgroup_match_and_check():
        with pytest.RaisesGroup(BaseException, match="my group msg"):
            raise BaseExceptionGroup("my group msg", [KeyboardInterrupt()])
        with pytest.RaisesGroup(
            Exception, check=lambda eg: isinstance(eg.__cause__, ValueError)
        ):
            raise ExceptionGroup("", [TypeError()]) from ValueError()

It is strict about structure and unwrapped exceptions, unlike :ref:`except* <except_star>`, so you might want to set the ``flatten_subgroups`` and/or ``allow_unwrapped`` parameters.

.. code-block:: python

    def test_structure():
        with pytest.RaisesGroup(pytest.RaisesGroup(ValueError)):
            raise ExceptionGroup("", (ExceptionGroup("", (ValueError(),)),))
        with pytest.RaisesGroup(ValueError, flatten_subgroups=True):
            raise ExceptionGroup("1st group", [ExceptionGroup("2nd group", [ValueError()])])
        with pytest.RaisesGroup(ValueError, allow_unwrapped=True):
            raise ValueError

To specify more details about the contained exception you can use :class:`pytest.RaisesExc`

.. code-block:: python

    def test_raises_exc():
        with pytest.RaisesGroup(pytest.RaisesExc(ValueError, match="foo")):
            raise ExceptionGroup("", (ValueError("foo")))

They both supply a method :meth:`pytest.RaisesGroup.matches` :meth:`pytest.RaisesExc.matches` if you want to do matching outside of using it as a :external+python:std:ref:`context manager <context-managers>`. This can be helpful when checking ``.__context__`` or ``.__cause__``.

.. code-block:: python

    def test_matches():
        exc = ValueError()
        exc_group = ExceptionGroup("", [exc])
        if RaisesGroup(ValueError).matches(exc_group):
            ...
        # helpful error is available in `.fail_reason` if it fails to match
        r = RaisesExc(ValueError)
        assert r.matches(e), r.fail_reason

Check the documentation on :class:`pytest.RaisesGroup` and :class:`pytest.RaisesExc` for more details and examples.

``ExceptionInfo.group_contains()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   This helper makes it easy to check for the presence of specific exceptions, but it is very bad for checking that the group does *not* contain *any other exceptions*. So this will pass:

    .. code-block:: python

       class EXTREMELYBADERROR(BaseException):
           """This is a very bad error to miss"""


       def test_for_value_error():
           with pytest.raises(ExceptionGroup) as excinfo:
               excs = [ValueError()]
               if very_unlucky():
                   excs.append(EXTREMELYBADERROR())
               raise ExceptionGroup("", excs)
           # This passes regardless of if there's other exceptions.
           assert excinfo.group_contains(ValueError)
           # You can't simply list all exceptions you *don't* want to get here.


   There is no good way of using :func:`excinfo.group_contains() <pytest.ExceptionInfo.group_contains>` to ensure you're not getting *any* other exceptions than the one you expected.
   You should instead use :class:`pytest.RaisesGroup`, see :ref:`assert-matching-exception-groups`.

You can also use the :func:`excinfo.group_contains() <pytest.ExceptionInfo.group_contains>`
method to test for exceptions returned as part of an :class:`ExceptionGroup`:

.. code-block:: python

    def test_exception_in_group():
        with pytest.raises(ExceptionGroup) as excinfo:
            raise ExceptionGroup(
                "Group message",
                [
                    RuntimeError("Exception 123 raised"),
                ],
            )
        assert excinfo.group_contains(RuntimeError, match=r".* 123 .*")
        assert not excinfo.group_contains(TypeError)

The optional ``match`` keyword parameter works the same way as for
:func:`pytest.raises`.

By default ``group_contains()`` will recursively search for a matching
exception at any level of nested ``ExceptionGroup`` instances. You can
specify a ``depth`` keyword parameter if you only want to match an
exception at a specific level; exceptions contained directly in the top
``ExceptionGroup`` would match ``depth=1``.

.. code-block:: python

    def test_exception_in_group_at_given_depth():
        with pytest.raises(ExceptionGroup) as excinfo:
            raise ExceptionGroup(
                "Group message",
                [
                    RuntimeError(),
                    ExceptionGroup(
                        "Nested group",
                        [
                            TypeError(),
                        ],
                    ),
                ],
            )
        assert excinfo.group_contains(RuntimeError, depth=1)
        assert excinfo.group_contains(TypeError, depth=2)
        assert not excinfo.group_contains(RuntimeError, depth=2)
        assert not excinfo.group_contains(TypeError, depth=1)

Alternate `pytest.raises` form (legacy)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is an alternate form of :func:`pytest.raises` where you pass
a function that will be executed, along with ``*args`` and ``**kwargs``. :func:`pytest.raises`
will then execute the function with those arguments and assert that the given exception is raised:

.. code-block:: python

    def func(x):
        if x <= 0:
            raise ValueError("x needs to be larger than zero")


    pytest.raises(ValueError, func, x=-1)

This form was the original :func:`pytest.raises` API, developed before the ``with`` statement was
added to the Python language. Nowadays, this form is rarely used, with the context-manager form (using ``with``)
being considered more readable.

xfail mark and pytest.raises
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is also possible to specify a ``raises`` argument to
:ref:`pytest.mark.xfail <pytest.mark.xfail ref>`, which checks that the test is failing in a more
specific way than just having any exception raised:

.. code-block:: python

    def f():
        raise IndexError()


    @pytest.mark.xfail(raises=IndexError)
    def test_f():
        f()


This will only "xfail" if the test fails by raising ``IndexError`` or subclasses.

* Using :ref:`pytest.mark.xfail <pytest.mark.xfail ref>` with the ``raises`` parameter is probably better for something
  like documenting unfixed bugs (where the test describes what "should" happen) or bugs in dependencies.

* Using :func:`pytest.raises` is likely to be better for cases where you are
  testing exceptions your own code is deliberately raising, which is the majority of cases.

You can also use :class:`pytest.RaisesGroup`:

.. code-block:: python

    def f():
        raise ExceptionGroup("", [IndexError()])


    @pytest.mark.xfail(raises=RaisesGroup(IndexError))
    def test_f():
        f()


.. _`assertwarns`:

Assertions about expected warnings
-----------------------------------------



You can check that code raises a particular warning using
:ref:`pytest.warns <warns>`.


.. _newreport:

Making use of context-sensitive comparisons
-------------------------------------------------



``pytest`` has rich support for providing context-sensitive information
when it encounters comparisons.  For example:

.. code-block:: python

    # content of test_assert2.py
    def test_set_comparison():
        set1 = set("1308")
        set2 = set("8035")
        assert set1 == set2

if you run this module:

.. code-block:: pytest

    $ pytest test_assert2.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_assert2.py F                                                    [100%]

    ================================= FAILURES =================================
    ___________________________ test_set_comparison ____________________________

        def test_set_comparison():
            set1 = set("1308")
            set2 = set("8035")
    >       assert set1 == set2
    E       AssertionError: assert {'0', '1', '3', '8'} == {'0', '3', '5', '8'}
    E
    E         Extra items in the left set:
    E         '1'
    E         Extra items in the right set:
    E         '5'
    E         Use -v to get more diff

    test_assert2.py:4: AssertionError
    ========================= short test summary info ==========================
    FAILED test_assert2.py::test_set_comparison - AssertionError: assert {'0'...
    ============================ 1 failed in 0.12s =============================

Special comparisons are done for a number of cases:

* comparing long strings: a context diff is shown
* comparing long sequences: first failing indices
* comparing dicts: different entries

In string context diffs, lines prefixed with ``-`` come from the left-hand side
of ``assert left == right``, while lines prefixed with ``+`` come from the
right-hand side.

See the :ref:`reporting demo <tbreportdemo>` for many more examples.

Defining your own explanation for failed assertions
---------------------------------------------------

It is possible to add your own detailed explanations by implementing
the ``pytest_assertrepr_compare`` hook.

.. autofunction:: _pytest.hookspec.pytest_assertrepr_compare
   :noindex:

As an example consider adding the following hook in a :ref:`conftest.py <conftest.py>`
file which provides an alternative explanation for ``Foo`` objects:

.. code-block:: python

   # content of conftest.py
   from test_foocompare import Foo


   def pytest_assertrepr_compare(op, left, right):
       if isinstance(left, Foo) and isinstance(right, Foo) and op == "==":
           return [
               "Comparing Foo instances:",
               f"   vals: {left.val} != {right.val}",
           ]

now, given this test module:

.. code-block:: python

   # content of test_foocompare.py
   class Foo:
       def __init__(self, val):
           self.val = val

       def __eq__(self, other):
           return self.val == other.val


   def test_compare():
       f1 = Foo(1)
       f2 = Foo(2)
       assert f1 == f2

you can run the test module and get the custom output defined in
the conftest file:

.. code-block:: pytest

   $ pytest -q test_foocompare.py
   F                                                                    [100%]
   ================================= FAILURES =================================
   _______________________________ test_compare _______________________________

       def test_compare():
           f1 = Foo(1)
           f2 = Foo(2)
   >       assert f1 == f2
   E       assert Comparing Foo instances:
   E            vals: 1 != 2

   test_foocompare.py:12: AssertionError
   ========================= short test summary info ==========================
   FAILED test_foocompare.py::test_compare - assert Comparing Foo instances:
   1 failed in 0.12s

.. _`return-not-none`:

Returning non-None value in test functions
------------------------------------------

A :class:`pytest.PytestReturnNotNoneWarning` is emitted when a test function returns a value other than ``None``.

This helps prevent a common mistake made by beginners who assume that returning a ``bool`` (e.g., ``True`` or ``False``) will determine whether a test passes or fails.

Example:

.. code-block:: python

    @pytest.mark.parametrize(
        ["a", "b", "result"],
        [
            [1, 2, 5],
            [2, 3, 8],
            [5, 3, 18],
        ],
    )
    def test_foo(a, b, result):
        return foo(a, b) == result  # Incorrect usage, do not do this.

Since pytest ignores return values, it might be surprising that the test will never fail based on the returned value.

The correct fix is to replace the ``return`` statement with an ``assert``:

.. code-block:: python

    @pytest.mark.parametrize(
        ["a", "b", "result"],
        [
            [1, 2, 5],
            [2, 3, 8],
            [5, 3, 18],
        ],
    )
    def test_foo(a, b, result):
        assert foo(a, b) == result




.. _assert-details:
.. _`assert introspection`:

Assertion introspection details
-------------------------------


Reporting details about a failing assertion is achieved by rewriting assert
statements before they are run.  Rewritten assert statements put introspection
information into the assertion failure message.  ``pytest`` only rewrites test
modules directly discovered by its test collection process, so **asserts in
supporting modules which are not themselves test modules will not be rewritten**.

You can manually enable assertion rewriting for an imported module by calling
:ref:`register_assert_rewrite <assertion-rewriting>`
before you import it (a good place to do that is in your root ``conftest.py``).

For further information, Benjamin Peterson wrote up `Behind the scenes of pytest's new assertion rewriting <http://pybites.blogspot.com/2011/07/behind-scenes-of-pytests-new-assertion.html>`_.

Assertion rewriting caches files on disk
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pytest`` will write back the rewritten modules to disk for caching. You can disable
this behavior (for example to avoid leaving stale ``.pyc`` files around in projects that
move files around a lot) by adding this to the top of your ``conftest.py`` file:

.. code-block:: python

   import sys

   sys.dont_write_bytecode = True

Note that you still get the benefits of assertion introspection, the only change is that
the ``.pyc`` files won't be cached on disk.

Additionally, rewriting will silently skip caching if it cannot write new ``.pyc`` files,
e.g. in a read-only filesystem or a zipfile.


Disabling assert rewriting
~~~~~~~~~~~~~~~~~~~~~~~~~~

``pytest`` rewrites test modules on import by using an import
hook to write new ``pyc`` files. Most of the time this works transparently.
However, if you are working with the import machinery yourself, the import hook may
interfere.

If this is the case you have two options:

* Disable rewriting for a specific module by adding the string
  ``PYTEST_DONT_REWRITE`` to its docstring.

* Disable rewriting for all modules by using :option:`--assert=plain`.

# How to use fixtures
Source: https://docs.pytest.org/en/stable/how-to/fixtures.html

.. _how-to-fixtures:

How to use fixtures
====================

.. seealso:: :ref:`about-fixtures`
.. seealso:: :ref:`Fixtures reference <reference-fixtures>`


"Requesting" fixtures
---------------------

At a basic level, test functions request fixtures they require by declaring
them as arguments.

When pytest goes to run a test, it looks at the parameters in that test
function's signature, and then searches for fixtures that have the same names as
those parameters. Once pytest finds them, it runs those fixtures, captures what
they returned (if anything), and passes those objects into the test function as
arguments.


Quick example
^^^^^^^^^^^^^

.. code-block:: python

    import pytest


    class Fruit:
        def __init__(self, name):
            self.name = name
            self.cubed = False

        def cube(self):
            self.cubed = True


    class FruitSalad:
        def __init__(self, *fruit_bowl):
            self.fruit = fruit_bowl
            self._cube_fruit()

        def _cube_fruit(self):
            for fruit in self.fruit:
                fruit.cube()


    # Arrange
    @pytest.fixture
    def fruit_bowl():
        return [Fruit("apple"), Fruit("banana")]


    def test_fruit_salad(fruit_bowl):
        # Act
        fruit_salad = FruitSalad(*fruit_bowl)

        # Assert
        assert all(fruit.cubed for fruit in fruit_salad.fruit)

In this example, ``test_fruit_salad`` "**requests**" ``fruit_bowl`` (i.e.
``def test_fruit_salad(fruit_bowl):``), and when pytest sees this, it will
execute the ``fruit_bowl`` fixture function and pass the object it returns into
``test_fruit_salad`` as the ``fruit_bowl`` argument.

Here's roughly
what's happening if we were to do it by hand:

.. code-block:: python

    def fruit_bowl():
        return [Fruit("apple"), Fruit("banana")]


    def test_fruit_salad(fruit_bowl):
        # Act
        fruit_salad = FruitSalad(*fruit_bowl)

        # Assert
        assert all(fruit.cubed for fruit in fruit_salad.fruit)


    # Arrange
    bowl = fruit_bowl()
    test_fruit_salad(fruit_bowl=bowl)


Fixtures can **request** other fixtures
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

One of pytest's greatest strengths is its extremely flexible fixture system. It
allows us to boil down complex requirements for tests into more simple and
organized functions, where we only need to have each one describe the things
they are dependent on. We'll get more into this further down, but for now,
here's a quick example to demonstrate how fixtures can use other fixtures:

.. code-block:: python

    # contents of test_append.py
    import pytest


    # Arrange
    @pytest.fixture
    def first_entry():
        return "a"


    # Arrange
    @pytest.fixture
    def order(first_entry):
        return [first_entry]


    def test_string(order):
        # Act
        order.append("b")

        # Assert
        assert order == ["a", "b"]


Notice that this is the same example from above, but very little changed. The
fixtures in pytest **request** fixtures just like tests. All the same
**requesting** rules apply to fixtures that do for tests. Here's how this
example would work if we did it by hand:

.. code-block:: python

    def first_entry():
        return "a"


    def order(first_entry):
        return [first_entry]


    def test_string(order):
        # Act
        order.append("b")

        # Assert
        assert order == ["a", "b"]


    entry = first_entry()
    the_list = order(first_entry=entry)
    test_string(order=the_list)

Fixtures are reusable
^^^^^^^^^^^^^^^^^^^^^

One of the things that makes pytest's fixture system so powerful, is that it
gives us the ability to define a generic setup step that can be reused over and
over, just like a normal function would be used. Two different tests can request
the same fixture and have pytest give each test their own result from that
fixture.

This is extremely useful for making sure tests aren't affected by each other. We
can use this system to make sure each test gets its own fresh batch of data and
is starting from a clean state so it can provide consistent, repeatable results.

Here's an example of how this can come in handy:

.. code-block:: python

    # contents of test_append.py
    import pytest


    # Arrange
    @pytest.fixture
    def first_entry():
        return "a"


    # Arrange
    @pytest.fixture
    def order(first_entry):
        return [first_entry]


    def test_string(order):
        # Act
        order.append("b")

        # Assert
        assert order == ["a", "b"]


    def test_int(order):
        # Act
        order.append(2)

        # Assert
        assert order == ["a", 2]


Each test here is being given its own copy of that ``list`` object,
which means the ``order`` fixture is getting executed twice (the same
is true for the ``first_entry`` fixture). If we were to do this by hand as
well, it would look something like this:

.. code-block:: python

    def first_entry():
        return "a"


    def order(first_entry):
        return [first_entry]


    def test_string(order):
        # Act
        order.append("b")

        # Assert
        assert order == ["a", "b"]


    def test_int(order):
        # Act
        order.append(2)

        # Assert
        assert order == ["a", 2]


    entry = first_entry()
    the_list = order(first_entry=entry)
    test_string(order=the_list)

    entry = first_entry()
    the_list = order(first_entry=entry)
    test_int(order=the_list)

A test/fixture can **request** more than one fixture at a time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tests and fixtures aren't limited to **requesting** a single fixture at a time.
They can request as many as they like. Here's another quick example to
demonstrate:

.. code-block:: python

    # contents of test_append.py
    import pytest


    # Arrange
    @pytest.fixture
    def first_entry():
        return "a"


    # Arrange
    @pytest.fixture
    def second_entry():
        return 2


    # Arrange
    @pytest.fixture
    def order(first_entry, second_entry):
        return [first_entry, second_entry]


    # Arrange
    @pytest.fixture
    def expected_list():
        return ["a", 2, 3.0]


    def test_string(order, expected_list):
        # Act
        order.append(3.0)

        # Assert
        assert order == expected_list

Fixtures can be **requested** more than once per test (return values are cached)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fixtures can also be **requested** more than once during the same test, and
pytest won't execute them again for that test. This means we can **request**
fixtures in multiple fixtures that are dependent on them (and even again in the
test itself) without those fixtures being executed more than once.

.. code-block:: python

    # contents of test_append.py
    import pytest


    # Arrange
    @pytest.fixture
    def first_entry():
        return "a"


    # Arrange
    @pytest.fixture
    def order():
        return []


    # Act
    @pytest.fixture
    def append_first(order, first_entry):
        return order.append(first_entry)


    def test_string_only(append_first, order, first_entry):
        # Assert
        assert order == [first_entry]

If a **requested** fixture was executed once for every time it was **requested**
during a test, then this test would fail because both ``append_first`` and
``test_string_only`` would see ``order`` as an empty list (i.e. ``[]``), but
since the return value of ``order`` was cached (along with any side effects
executing it may have had) after the first time it was called, both the test and
``append_first`` were referencing the same object, and the test saw the effect
``append_first`` had on that object.

.. _`autouse`:
.. _`autouse fixtures`:

Autouse fixtures (fixtures you don't have to request)
-----------------------------------------------------

Sometimes you may want to have a fixture (or even several) that you know all
your tests will depend on. "Autouse" fixtures are a convenient way to make all
tests automatically **request** them. This can cut out a
lot of redundant **requests**, and can even provide more advanced fixture usage
(more on that further down).

We can make a fixture an autouse fixture by passing in ``autouse=True`` to the
fixture's decorator. Here's a simple example for how they can be used:

.. code-block:: python

    # contents of test_append.py
    import pytest


    @pytest.fixture
    def first_entry():
        return "a"


    @pytest.fixture
    def order(first_entry):
        return []


    @pytest.fixture(autouse=True)
    def append_first(order, first_entry):
        return order.append(first_entry)


    def test_string_only(order, first_entry):
        assert order == [first_entry]


    def test_string_and_int(order, first_entry):
        order.append(2)
        assert order == [first_entry, 2]

In this example, the ``append_first`` fixture is an autouse fixture. Because it
happens automatically, both tests are affected by it, even though neither test
**requested** it. That doesn't mean they *can't* be **requested** though; just
that it isn't *necessary*.

.. _smtpshared:

Scope: sharing fixtures across classes, modules, packages or session
--------------------------------------------------------------------

.. regendoc:wipe

Fixtures requiring network access depend on connectivity and are
usually time-expensive to create.  Extending the previous example, we
can add a ``scope="module"`` parameter to the
:py:func:`@pytest.fixture <pytest.fixture>` invocation
to cause a ``smtp_connection`` fixture function, responsible to create a connection to a preexisting SMTP server, to only be invoked
once per test *module* (the default is to invoke once per test *function*).
Multiple test functions in a test module will thus
each receive the same ``smtp_connection`` fixture instance, thus saving time.
Possible values for ``scope`` are: ``function``, ``class``, ``module``, ``package`` or ``session``.

The next example puts the fixture function into a separate ``conftest.py`` file
so that tests from multiple test modules in the directory can
access the fixture function:

.. code-block:: python

    # content of conftest.py
    import smtplib

    import pytest


    @pytest.fixture(scope="module")
    def smtp_connection():
        return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)


.. code-block:: python

    # content of test_module.py


    def test_ehlo(smtp_connection):
        response, msg = smtp_connection.ehlo()
        assert response == 250
        assert b"smtp.gmail.com" in msg
        assert 0  # for demo purposes


    def test_noop(smtp_connection):
        response, msg = smtp_connection.noop()
        assert response == 250
        assert 0  # for demo purposes

Here, the ``test_ehlo`` needs the ``smtp_connection`` fixture value.  pytest
will discover and call the :py:func:`@pytest.fixture <pytest.fixture>`
marked ``smtp_connection`` fixture function.  Running the test looks like this:

.. code-block:: pytest

    $ pytest test_module.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    test_module.py FF                                                    [100%]

    ================================= FAILURES =================================
    ________________________________ test_ehlo _________________________________

    smtp_connection = <smtplib.SMTP object at 0xdeadbeef0001>

        def test_ehlo(smtp_connection):
            response, msg = smtp_connection.ehlo()
            assert response == 250
            assert b"smtp.gmail.com" in msg
    >       assert 0  # for demo purposes
            ^^^^^^^^
    E       assert 0

    test_module.py:7: AssertionError
    ________________________________ test_noop _________________________________

    smtp_connection = <smtplib.SMTP object at 0xdeadbeef0001>

        def test_noop(smtp_connection):
            response, msg = smtp_connection.noop()
            assert response == 250
    >       assert 0  # for demo purposes
            ^^^^^^^^
    E       assert 0

    test_module.py:13: AssertionError
    ========================= short test summary info ==========================
    FAILED test_module.py::test_ehlo - assert 0
    FAILED test_module.py::test_noop - assert 0
    ============================ 2 failed in 0.12s =============================

You see the two ``assert 0`` failing and more importantly you can also see
that the **exact same** ``smtp_connection`` object was passed into the
two test functions because pytest shows the incoming argument values in the
traceback.  As a result, the two test functions using ``smtp_connection`` run
as quick as a single one because they reuse the same instance.

If you decide that you rather want to have a session-scoped ``smtp_connection``
instance, you can simply declare it:

.. code-block:: python

    @pytest.fixture(scope="session")
    def smtp_connection():
        # the returned fixture value will be shared for
        # all tests requesting it
        ...


Fixture scopes
^^^^^^^^^^^^^^

Fixtures are created when first requested by a test, and are destroyed based on their ``scope``:

* ``function``: the default scope, the fixture is destroyed at the end of the test.
* ``class``: the fixture is destroyed during teardown of the last test in the class.
* ``module``: the fixture is destroyed during teardown of the last test in the module.
* ``package``: the fixture is destroyed during teardown of the last test in the package where the fixture is defined, including sub-packages and sub-directories within it.
* ``session``: the fixture is destroyed at the end of the test session.

.. note::

    Pytest only caches one instance of a fixture at a time, which
    means that when using a parametrized fixture, pytest may invoke a fixture more than once in
    the given scope.

.. _dynamic scope:

Dynamic scope
^^^^^^^^^^^^^

.. versionadded:: 5.2

In some cases, you might want to change the scope of the fixture without changing the code.
To do that, pass a callable to ``scope``. The callable must return a string with a valid scope
and will be executed only once - during the fixture definition. It will be called with two
keyword arguments - ``fixture_name`` as a string and ``config`` with a configuration object.

This can be especially useful when dealing with fixtures that need time for setup, like spawning
a docker container. You can use the command-line argument to control the scope of the spawned
containers for different environments. See the example below.

.. code-block:: python

    def determine_scope(fixture_name, config):
        if config.getoption("--keep-containers", None):
            return "session"
        return "function"


    @pytest.fixture(scope=determine_scope)
    def docker_container():
        yield spawn_container()



.. _`finalization`:

Teardown/Cleanup (AKA Fixture finalization)
-------------------------------------------

When we run our tests, we'll want to make sure they clean up after themselves so
they don't mess with any other tests (and also so that we don't leave behind a
mountain of test data to bloat the system). Fixtures in pytest offer a very
useful teardown system, which allows us to define the specific steps necessary
for each fixture to clean up after itself.

This system can be leveraged in two ways.

.. _`yield fixtures`:

1. ``yield`` fixtures (recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. regendoc: wipe

"Yield" fixtures ``yield`` instead of ``return``. With these
fixtures, we can run some code and pass an object back to the requesting
fixture/test, just like with the other fixtures. The only differences are:

1. ``return`` is swapped out for ``yield``.
2. Any teardown code for that fixture is placed *after* the ``yield``.

Once pytest figures out a linear order for the fixtures, it will run each one up
until it returns or yields, and then move on to the next fixture in the list to
do the same thing.

Once the test is finished, pytest will go back down the list of fixtures, but in
the *reverse order*, taking each one that yielded, and running the code inside
it that was *after* the ``yield`` statement.

As a simple example, consider this basic email module:

.. code-block:: python

    # content of emaillib.py
    class MailAdminClient:
        def create_user(self):
            return MailUser()

        def delete_user(self, user):
            # do some cleanup
            pass


    class MailUser:
        def __init__(self):
            self.inbox = []

        def send_email(self, email, other):
            other.inbox.append(email)

        def clear_mailbox(self):
            self.inbox.clear()


    class Email:
        def __init__(self, subject, body):
            self.subject = subject
            self.body = body

Let's say we want to test sending email from one user to another. We'll have to
first make each user, then send the email from one user to the other, and
finally assert that the other user received that message in their inbox. If we
want to clean up after the test runs, we'll likely have to make sure the other
user's mailbox is emptied before deleting that user, otherwise the system may
complain.

Here's what that might look like:

.. code-block:: python

    # content of test_emaillib.py
    from emaillib import Email, MailAdminClient

    import pytest


    @pytest.fixture
    def mail_admin():
        return MailAdminClient()


    @pytest.fixture
    def sending_user(mail_admin):
        user = mail_admin.create_user()
        yield user
        mail_admin.delete_user(user)


    @pytest.fixture
    def receiving_user(mail_admin):
        user = mail_admin.create_user()
        yield user
        user.clear_mailbox()
        mail_admin.delete_user(user)


    def test_email_received(sending_user, receiving_user):
        email = Email(subject="Hey!", body="How's it going?")
        sending_user.send_email(email, receiving_user)
        assert email in receiving_user.inbox

Because ``receiving_user`` is the last fixture to run during setup, it's the first to run
during teardown.

There is a risk that even having the order right on the teardown side of things
doesn't guarantee a safe cleanup. That's covered in a bit more detail in
:ref:`safe teardowns`.

.. code-block:: pytest

   $ pytest -q test_emaillib.py
   .                                                                    [100%]
   1 passed in 0.12s

Handling errors for yield fixture
"""""""""""""""""""""""""""""""""

If a yield fixture raises an exception before yielding, pytest won't try to run
the teardown code after that yield fixture's ``yield`` statement. But, for every
fixture that has already run successfully for that test, pytest will still
attempt to tear them down as it normally would.

2. Adding finalizers directly
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While yield fixtures are considered to be the cleaner and more straightforward
option, there is another choice, and that is to add "finalizer" functions
directly to the test's `request-context`_ object. It brings a similar result as
yield fixtures, but requires a bit more verbosity.

In order to use this approach, we have to request the `request-context`_ object
(just like we would request another fixture) in the fixture we need to add
teardown code for, and then pass a callable, containing that teardown code, to
its ``addfinalizer`` method.

We have to be careful though, because pytest will run that finalizer once it's
been added, even if that fixture raises an exception after adding the finalizer.
So to make sure we don't run the finalizer code when we wouldn't need to, we
would only add the finalizer once the fixture would have done something that
we'd need to teardown.

Here's how the previous example would look using the ``addfinalizer`` method:

.. code-block:: python

    # content of test_emaillib.py
    from emaillib import Email, MailAdminClient

    import pytest


    @pytest.fixture
    def mail_admin():
        return MailAdminClient()


    @pytest.fixture
    def sending_user(mail_admin):
        user = mail_admin.create_user()
        yield user
        mail_admin.delete_user(user)


    @pytest.fixture
    def receiving_user(mail_admin, request):
        user = mail_admin.create_user()

        def delete_user():
            mail_admin.delete_user(user)

        request.addfinalizer(delete_user)
        return user


    @pytest.fixture
    def email(sending_user, receiving_user, request):
        _email = Email(subject="Hey!", body="How's it going?")
        sending_user.send_email(_email, receiving_user)

        def empty_mailbox():
            receiving_user.clear_mailbox()

        request.addfinalizer(empty_mailbox)
        return _email


    def test_email_received(receiving_user, email):
        assert email in receiving_user.inbox


It's a bit longer than yield fixtures and a bit more complex, but it
does offer some nuances for when you're in a pinch.

.. code-block:: pytest

   $ pytest -q test_emaillib.py
   .                                                                    [100%]
   1 passed in 0.12s

Note on finalizer order
""""""""""""""""""""""""

Finalizers are executed in a first-in-last-out order.
For yield fixtures, the first teardown code to run is from the right-most fixture, i.e. the last test parameter.


.. code-block:: python

    # content of test_finalizers.py
    import pytest


    def test_bar(fix_w_yield1, fix_w_yield2):
        print("test_bar")


    @pytest.fixture
    def fix_w_yield1():
        yield
        print("after_yield_1")


    @pytest.fixture
    def fix_w_yield2():
        yield
        print("after_yield_2")


.. code-block:: pytest

    $ pytest -s test_finalizers.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_finalizers.py test_bar
    .after_yield_2
    after_yield_1


    ============================ 1 passed in 0.12s =============================

For finalizers, the first fixture to run is last call to `request.addfinalizer`.

.. code-block:: python

    # content of test_finalizers.py
    from functools import partial
    import pytest


    @pytest.fixture
    def fix_w_finalizers(request):
        request.addfinalizer(partial(print, "finalizer_2"))
        request.addfinalizer(partial(print, "finalizer_1"))


    def test_bar(fix_w_finalizers):
        print("test_bar")


.. code-block:: pytest

    $ pytest -s test_finalizers.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_finalizers.py test_bar
    .finalizer_1
    finalizer_2


    ============================ 1 passed in 0.12s =============================

This is so because yield fixtures use `addfinalizer` behind the scenes: when the fixture executes, `addfinalizer` registers a function that resumes the generator, which in turn calls the teardown code.


.. _`safe teardowns`:

Safe teardowns
--------------

The fixture system of pytest is *very* powerful, but it's still being run by a
computer, so it isn't able to figure out how to safely teardown everything we
throw at it. If we aren't careful, an error in the wrong spot might leave stuff
from our tests behind, and that can cause further issues pretty quickly.

For example, consider the following tests (based off of the mail example from
above):

.. code-block:: python

    # content of test_emaillib.py
    from emaillib import Email, MailAdminClient

    import pytest


    @pytest.fixture
    def setup():
        mail_admin = MailAdminClient()
        sending_user = mail_admin.create_user()
        receiving_user = mail_admin.create_user()
        email = Email(subject="Hey!", body="How's it going?")
        sending_user.send_email(email, receiving_user)
        yield receiving_user, email
        receiving_user.clear_mailbox()
        mail_admin.delete_user(sending_user)
        mail_admin.delete_user(receiving_user)


    def test_email_received(setup):
        receiving_user, email = setup
        assert email in receiving_user.inbox

This version is a lot more compact, but it's also harder to read, doesn't have a
very descriptive fixture name, and none of the fixtures can be reused easily.

There's also a more serious issue, which is that if any of those steps in the
setup raise an exception, none of the teardown code will run.

One option might be to go with the ``addfinalizer`` method instead of yield
fixtures, but that might get pretty complex and difficult to maintain (and it
wouldn't be compact anymore).

.. code-block:: pytest

   $ pytest -q test_emaillib.py
   .                                                                    [100%]
   1 passed in 0.12s

.. _`safe fixture structure`:

Safe fixture structure
^^^^^^^^^^^^^^^^^^^^^^

The safest and simplest fixture structure requires limiting fixtures to only
making one state-changing action each, and then bundling them together with
their teardown code, as :ref:`the email examples above <yield fixtures>` showed.

The chance that a state-changing operation can fail but still modify state is
negligible, as most of these operations tend to be `transaction
<https://en.wikipedia.org/wiki/Transaction_processing>`_-based (at least at the
level of testing where state could be left behind). So if we make sure that any
successful state-changing action gets torn down by moving it to a separate
fixture function and separating it from other, potentially failing
state-changing actions, then our tests will stand the best chance at leaving
the test environment the way they found it.

For an example, let's say we have a website with a login page, and we have
access to an admin API where we can generate users. For our test, we want to:

1. Create a user through that admin API
2. Launch a browser using Selenium
3. Go to the login page of our site
4. Log in as the user we created
5. Assert that their name is in the header of the landing page

We wouldn't want to leave that user in the system, nor would we want to leave
that browser session running, so we'll want to make sure the fixtures that
create those things clean up after themselves.

Here's what that might look like:

.. note::

    For this example, certain fixtures (i.e. ``base_url`` and
    ``admin_credentials``) are implied to exist elsewhere. So for now, let's
    assume they exist, and we're just not looking at them.

.. code-block:: python

    from uuid import uuid4
    from urllib.parse import urljoin

    from selenium.webdriver import Chrome
    import pytest

    from src.utils.pages import LoginPage, LandingPage
    from src.utils import AdminApiClient
    from src.utils.data_types import User


    @pytest.fixture
    def admin_client(base_url, admin_credentials):
        return AdminApiClient(base_url, **admin_credentials)


    @pytest.fixture
    def user(admin_client):
        _user = User(name="Susan", username=f"testuser-{uuid4()}", password="P4$$word")
        admin_client.create_user(_user)
        yield _user
        admin_client.delete_user(_user)


    @pytest.fixture
    def driver():
        _driver = Chrome()
        yield _driver
        _driver.quit()


    @pytest.fixture
    def login(driver, base_url, user):
        driver.get(urljoin(base_url, "/login"))
        page = LoginPage(driver)
        page.login(user)


    @pytest.fixture
    def landing_page(driver, login):
        return LandingPage(driver)


    def test_name_on_landing_page_after_login(landing_page, user):
        assert landing_page.header == f"Welcome, {user.name}!"

The way the dependencies are laid out means it's unclear if the ``user``
fixture would execute before the ``driver`` fixture. But that's ok, because
those are atomic operations, and so it doesn't matter which one runs first
because the sequence of events for the test is still `linearizable
<https://en.wikipedia.org/wiki/Linearizability>`_. But what *does* matter is
that, no matter which one runs first, if the one raises an exception while the
other would not have, neither will have left anything behind. If ``driver``
executes before ``user``, and ``user`` raises an exception, the driver will
still quit, and the user was never made. And if ``driver`` was the one to raise
the exception, then the driver would never have been started and the user would
never have been made.

.. note:

    While the ``user`` fixture doesn't *actually* need to happen before the
    ``driver`` fixture, if we made ``driver`` request ``user``, it might save
    some time in the event that making the user raises an exception, since it
    won't bother trying to start the driver, which is a fairly expensive
    operation.


Running multiple ``assert`` statements safely
---------------------------------------------

Sometimes you may want to run multiple asserts after doing all that setup, which
makes sense as, in more complex systems, a single action can kick off multiple
behaviors. pytest has a convenient way of handling this and it combines a bunch
of what we've gone over so far.

All that's needed is stepping up to a larger scope, then having the **act**
step defined as an autouse fixture, and finally, making sure all the fixtures
are targeting that higher level scope.

Let's pull :ref:`an example from above <safe fixture structure>`, and tweak it a
bit. Let's say that in addition to checking for a welcome message in the header,
we also want to check for a sign out button, and a link to the user's profile.

Let's take a look at how we can structure that so we can run multiple asserts
without having to repeat all those steps again.

.. note::

    For this example, certain fixtures (i.e. ``base_url`` and
    ``admin_credentials``) are implied to exist elsewhere. So for now, let's
    assume they exist, and we're just not looking at them.

.. code-block:: python

    # contents of tests/end_to_end/test_login.py
    from uuid import uuid4
    from urllib.parse import urljoin

    from selenium.webdriver import Chrome
    import pytest

    from src.utils.pages import LoginPage, LandingPage
    from src.utils import AdminApiClient
    from src.utils.data_types import User


    @pytest.fixture(scope="class")
    def admin_client(base_url, admin_credentials):
        return AdminApiClient(base_url, **admin_credentials)


    @pytest.fixture(scope="class")
    def user(admin_client):
        _user = User(name="Susan", username=f"testuser-{uuid4()}", password="P4$$word")
        admin_client.create_user(_user)
        yield _user
        admin_client.delete_user(_user)


    @pytest.fixture(scope="class")
    def driver():
        _driver = Chrome()
        yield _driver
        _driver.quit()


    @pytest.fixture(scope="class")
    def landing_page(driver, login):
        return LandingPage(driver)


    class TestLandingPageSuccess:
        @pytest.fixture(scope="class", autouse=True)
        @classmethod
        def login(cls, driver, base_url, user):
            driver.get(urljoin(base_url, "/login"))
            page = LoginPage(driver)
            page.login(user)

        def test_name_in_header(self, landing_page, user):
            assert landing_page.header == f"Welcome, {user.name}!"

        def test_sign_out_button(self, landing_page):
            assert landing_page.sign_out_button.is_displayed()

        def test_profile_link(self, landing_page, user):
            profile_href = urljoin(base_url, f"/profile?id={user.profile_id}")
            assert landing_page.profile_link.get_attribute("href") == profile_href

Notice that the methods are only referencing ``self`` in the signature as a
formality. No state is tied to the actual test class as it might be in the
``unittest.TestCase`` framework. Everything is managed by the pytest fixture
system.

Each method only has to request the fixtures that it actually needs without
worrying about order. This is because the **act** fixture is an autouse fixture,
and it made sure all the other fixtures executed before it. There's no more
changes of state that need to take place, so the tests are free to make as many
non-state-changing queries as they want without risking stepping on the toes of
the other tests.

The ``login`` fixture is defined inside the class as well, because not every one
of the other tests in the module will be expecting a successful login, and the **act** may need to
be handled a little differently for another test class. For example, if we
wanted to write another test scenario around submitting bad credentials, we
could handle it by adding something like this to the test file:

.. note:

    It's assumed that the page object for this (i.e. ``LoginPage``) raises a
    custom exception, ``BadCredentialsException``, when it recognizes text
    signifying that on the login form after attempting to log in.

.. code-block:: python

    class TestLandingPageBadCredentials:
        @pytest.fixture(scope="class")
        @classmethod
        def faux_user(cls, user):
            _user = deepcopy(user)
            _user.password = "badpass"
            return _user

        def test_raises_bad_credentials_exception(self, login_page, faux_user):
            with pytest.raises(BadCredentialsException):
                login_page.login(faux_user)


.. _`request-context`:

Fixtures can introspect the requesting test context
-------------------------------------------------------------

Fixture functions can accept the :py:class:`request <_pytest.fixtures.FixtureRequest>` object
to introspect the "requesting" test function, class or module context.
Further extending the previous ``smtp_connection`` fixture example, let's
read an optional server URL from the test module which uses our fixture:

.. code-block:: python

    # content of conftest.py
    import smtplib

    import pytest


    @pytest.fixture(scope="module")
    def smtp_connection(request):
        server = getattr(request.module, "smtpserver", "smtp.gmail.com")
        smtp_connection = smtplib.SMTP(server, 587, timeout=5)
        yield smtp_connection
        print(f"finalizing {smtp_connection} ({server})")
        smtp_connection.close()

We use the ``request.module`` attribute to optionally obtain an
``smtpserver`` attribute from the test module.  If we just execute
again, nothing much has changed:

.. code-block:: pytest

    $ pytest -s -q --tb=no test_module.py
    FFfinalizing <smtplib.SMTP object at 0xdeadbeef0002> (smtp.gmail.com)

    ========================= short test summary info ==========================
    FAILED test_module.py::test_ehlo - assert 0
    FAILED test_module.py::test_noop - assert 0
    2 failed in 0.12s

Let's quickly create another test module that actually sets the
server URL in its module namespace:

.. code-block:: python

    # content of test_anothersmtp.py

    smtpserver = "mail.python.org"  # will be read by smtp fixture


    def test_showhelo(smtp_connection):
        assert 0, smtp_connection.helo()

Running it:

.. code-block:: pytest

    $ pytest -qq --tb=short test_anothersmtp.py
    F                                                                    [100%]
    ================================= FAILURES =================================
    ______________________________ test_showhelo _______________________________
    test_anothersmtp.py:6: in test_showhelo
        assert 0, smtp_connection.helo()
    E   AssertionError: (250, b'mail.python.org')
    E   assert 0
    ------------------------- Captured stdout teardown -------------------------
    finalizing <smtplib.SMTP object at 0xdeadbeef0003> (mail.python.org)
    ========================= short test summary info ==========================
    FAILED test_anothersmtp.py::test_showhelo - AssertionError: (250, b'mail....

voila! The ``smtp_connection`` fixture function picked up our mail server name
from the module namespace.

.. _`using-markers`:

Using markers to pass data to fixtures
-------------------------------------------------------------

Using the :py:class:`request <_pytest.fixtures.FixtureRequest>` object, a fixture can also access
markers which are applied to a test function. This can be useful to pass data
into a fixture from a test:

.. code-block:: python

    import pytest


    @pytest.fixture
    def fixt(request):
        marker = request.node.get_closest_marker("fixt_data")
        if marker is None:
            # Handle missing marker in some way...
            data = None
        else:
            data = marker.args[0]

        # Do something with the data
        return data


    @pytest.mark.fixt_data(42)
    def test_fixt(fixt):
        assert fixt == 42

.. _`fixture-factory`:

Factories as fixtures
-------------------------------------------------------------

The "factory as fixture" pattern can help in situations where the result
of a fixture is needed multiple times in a single test. Instead of returning
data directly, the fixture instead returns a function which generates the data.
This function can then be called multiple times in the test.

Factories can have parameters as needed:

.. code-block:: python

    @pytest.fixture
    def make_customer_record():
        def _make_customer_record(name):
            return {"name": name, "orders": []}

        return _make_customer_record


    def test_customer_records(make_customer_record):
        customer_1 = make_customer_record("Lisa")
        customer_2 = make_customer_record("Mike")
        customer_3 = make_customer_record("Meredith")

If the data created by the factory requires managing, the fixture can take care of that:

.. code-block:: python

    @pytest.fixture
    def make_customer_record():
        created_records = []

        def _make_customer_record(name):
            record = models.Customer(name=name, orders=[])
            created_records.append(record)
            return record

        yield _make_customer_record

        for record in created_records:
            record.destroy()


    def test_customer_records(make_customer_record):
        customer_1 = make_customer_record("Lisa")
        customer_2 = make_customer_record("Mike")
        customer_3 = make_customer_record("Meredith")


.. _`fixture-parametrize`:

Parametrizing fixtures
-----------------------------------------------------------------

Fixture functions can be parametrized in which case they will be called
multiple times, each time executing the set of dependent tests, i.e. the
tests that depend on this fixture.  Test functions usually do not need
to be aware of their re-running.  Fixture parametrization helps to
write exhaustive functional tests for components which themselves can be
configured in multiple ways.

Extending the previous example, we can flag the fixture to create two
``smtp_connection`` fixture instances which will cause all tests using the fixture
to run twice.  The fixture function gets access to each parameter
through the special :py:class:`request <pytest.FixtureRequest>` object:

.. code-block:: python

    # content of conftest.py
    import smtplib

    import pytest


    @pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
    def smtp_connection(request):
        smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
        yield smtp_connection
        print(f"finalizing {smtp_connection}")
        smtp_connection.close()

The main change is the declaration of ``params`` with
:py:func:`@pytest.fixture <pytest.fixture>`, a list of values
for each of which the fixture function will execute and can access
a value via ``request.param``.  No test function code needs to change.
So let's just do another run:

.. code-block:: pytest

    $ pytest -q test_module.py
    FFFF                                                                 [100%]
    ================================= FAILURES =================================
    ________________________ test_ehlo[smtp.gmail.com] _________________________

    smtp_connection = <smtplib.SMTP object at 0xdeadbeef0004>

        def test_ehlo(smtp_connection):
            response, msg = smtp_connection.ehlo()
            assert response == 250
            assert b"smtp.gmail.com" in msg
    >       assert 0  # for demo purposes
            ^^^^^^^^
    E       assert 0

    test_module.py:7: AssertionError
    ________________________ test_noop[smtp.gmail.com] _________________________

    smtp_connection = <smtplib.SMTP object at 0xdeadbeef0004>

        def test_noop(smtp_connection):
            response, msg = smtp_connection.noop()
            assert response == 250
    >       assert 0  # for demo purposes
            ^^^^^^^^
    E       assert 0

    test_module.py:13: AssertionError
    ________________________ test_ehlo[mail.python.org] ________________________

    smtp_connection = <smtplib.SMTP object at 0xdeadbeef0005>

        def test_ehlo(smtp_connection):
            response, msg = smtp_connection.ehlo()
            assert response == 250
    >       assert b"smtp.gmail.com" in msg
    E       AssertionError: assert b'smtp.gmail.com' in b'mail.python.org\nPIPELINING\nSIZE 51200000\nETRN\nSTARTTLS\nAUTH DIGEST-MD5 NTLM CRAM-MD5\nENHANCEDSTATUSCODES\n8BITMIME\nDSN\nSMTPUTF8\nCHUNKING'

    test_module.py:6: AssertionError
    -------------------------- Captured stdout setup ---------------------------
    finalizing <smtplib.SMTP object at 0xdeadbeef0004>
    ________________________ test_noop[mail.python.org] ________________________

    smtp_connection = <smtplib.SMTP object at 0xdeadbeef0005>

        def test_noop(smtp_connection):
            response, msg = smtp_connection.noop()
            assert response == 250
    >       assert 0  # for demo purposes
            ^^^^^^^^
    E       assert 0

    test_module.py:13: AssertionError
    ------------------------- Captured stdout teardown -------------------------
    finalizing <smtplib.SMTP object at 0xdeadbeef0005>
    ========================= short test summary info ==========================
    FAILED test_module.py::test_ehlo[smtp.gmail.com] - assert 0
    FAILED test_module.py::test_noop[smtp.gmail.com] - assert 0
    FAILED test_module.py::test_ehlo[mail.python.org] - AssertionError: asser...
    FAILED test_module.py::test_noop[mail.python.org] - assert 0
    4 failed in 0.12s

We see that our two test functions each ran twice, against the different
``smtp_connection`` instances.  Note also, that with the ``mail.python.org``
connection the second test fails in ``test_ehlo`` because a
different server string is expected than what arrived.

pytest will build a string that is the test ID for each fixture value
in a parametrized fixture, e.g. ``test_ehlo[smtp.gmail.com]`` and
``test_ehlo[mail.python.org]`` in the above examples.  These IDs can
be used with :option:`-k` to select specific cases to run, and they will
also identify the specific case when one is failing.  Running pytest
with :option:`--collect-only` will show the generated IDs.

Numbers, strings, booleans and ``None`` will have their usual string
representation used in the test ID. For other objects, pytest will
make a string based on the argument name.  It is possible to customise
the string used in a test ID for a certain fixture value by using the
``ids`` keyword argument:

.. code-block:: python

   # content of test_ids.py
   import pytest


   @pytest.fixture(params=[0, 1], ids=["spam", "ham"])
   def a(request):
       return request.param


   def test_a(a):
       pass


   def idfn(fixture_value):
       if fixture_value == 0:
           return "eggs"
       else:
           return None


   @pytest.fixture(params=[0, 1], ids=idfn)
   def b(request):
       return request.param


   def test_b(b):
       pass

The above shows how ``ids`` can be either a list of strings to use or
a function which will be called with the fixture value and then
has to return a string to use.  In the latter case if the function
returns ``None`` then pytest's auto-generated ID will be used.

Running the above tests results in the following test IDs being used:

.. code-block:: pytest

   $ pytest --collect-only
   =========================== test session starts ============================
   platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
   rootdir: /home/sweet/project
   collected 12 items

   <Dir fixtures.rst-236>
     <Module test_anothersmtp.py>
       <Function test_showhelo[smtp.gmail.com]>
       <Function test_showhelo[mail.python.org]>
     <Module test_emaillib.py>
       <Function test_email_received>
     <Module test_finalizers.py>
       <Function test_bar>
     <Module test_ids.py>
       <Function test_a[spam]>
       <Function test_a[ham]>
       <Function test_b[eggs]>
       <Function test_b[1]>
     <Module test_module.py>
       <Function test_ehlo[smtp.gmail.com]>
       <Function test_noop[smtp.gmail.com]>
       <Function test_ehlo[mail.python.org]>
       <Function test_noop[mail.python.org]>

   ======================= 12 tests collected in 0.12s ========================

.. _`fixture-parametrize-marks`:

Using marks with parametrized fixtures
--------------------------------------

:func:`pytest.param` can be used to apply marks in values sets of parametrized fixtures in the same way
that they can be used with :ref:`@pytest.mark.parametrize <@pytest.mark.parametrize>`.

Example:

.. code-block:: python

    # content of test_fixture_marks.py
    import pytest


    @pytest.fixture(params=[0, 1, pytest.param(2, marks=pytest.mark.skip)])
    def data_set(request):
        return request.param


    def test_data(data_set):
        pass

Running this test will *skip* the invocation of ``data_set`` with value ``2``:

.. code-block:: pytest

    $ pytest test_fixture_marks.py -v
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 3 items

    test_fixture_marks.py::test_data[0] PASSED                           [ 33%]
    test_fixture_marks.py::test_data[1] PASSED                           [ 66%]
    test_fixture_marks.py::test_data[2] SKIPPED (unconditional skip)     [100%]

    ======================= 2 passed, 1 skipped in 0.12s =======================

.. _`interdependent fixtures`:

Modularity: using fixtures from a fixture function
----------------------------------------------------------

In addition to using fixtures in test functions, fixture functions
can use other fixtures themselves.  This contributes to a modular design
of your fixtures and allows reuse of framework-specific fixtures across
many projects.  As a simple example, we can extend the previous example
and instantiate an object ``app`` where we stick the already defined
``smtp_connection`` resource into it:

.. code-block:: python

    # content of test_appsetup.py

    import pytest


    class App:
        def __init__(self, smtp_connection):
            self.smtp_connection = smtp_connection


    @pytest.fixture(scope="module")
    def app(smtp_connection):
        return App(smtp_connection)


    def test_smtp_connection_exists(app):
        assert app.smtp_connection

Here we declare an ``app`` fixture which receives the previously defined
``smtp_connection`` fixture and instantiates an ``App`` object with it.  Let's run it:

.. code-block:: pytest

    $ pytest -v test_appsetup.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 2 items

    test_appsetup.py::test_smtp_connection_exists[smtp.gmail.com] PASSED [ 50%]
    test_appsetup.py::test_smtp_connection_exists[mail.python.org] PASSED [100%]

    ============================ 2 passed in 0.12s =============================

Due to the parametrization of ``smtp_connection``, the test will run twice with two
different ``App`` instances and respective smtp servers.  There is no
need for the ``app`` fixture to be aware of the ``smtp_connection``
parametrization because pytest will fully analyse the fixture dependency graph.

Note that the ``app`` fixture has a scope of ``module`` and uses a
module-scoped ``smtp_connection`` fixture.  The example would still work if
``smtp_connection`` was cached on a ``session`` scope: it is fine for fixtures to use
"broader" scoped fixtures but not the other way round:
A session-scoped fixture could not use a module-scoped one in a
meaningful way.


.. _`automatic per-resource grouping`:

Automatic grouping of tests by fixture instances
----------------------------------------------------------

.. regendoc: wipe

pytest minimizes the number of active fixtures during test runs.
If you have a parametrized fixture, then all the tests using it will
first execute with one instance and then finalizers are called
before the next fixture instance is created.  Among other things,
this eases testing of applications which create and use global state.

The following example uses two parametrized fixtures, one of which is
scoped on a per-module basis, and all the functions perform ``print`` calls
to show the setup/teardown flow:

.. code-block:: python

    # content of test_module.py
    import pytest


    @pytest.fixture(scope="module", params=["mod1", "mod2"])
    def modarg(request):
        param = request.param
        print("  SETUP modarg", param)
        yield param
        print("  TEARDOWN modarg", param)


    @pytest.fixture(scope="function", params=[1, 2])
    def otherarg(request):
        param = request.param
        print("  SETUP otherarg", param)
        yield param
        print("  TEARDOWN otherarg", param)


    def test_0(otherarg):
        print("  RUN test0 with otherarg", otherarg)


    def test_1(modarg):
        print("  RUN test1 with modarg", modarg)


    def test_2(otherarg, modarg):
        print(f"  RUN test2 with otherarg {otherarg} and modarg {modarg}")


Let's run the tests in verbose mode and with looking at the print-output:

.. code-block:: pytest

    $ pytest -v -s test_module.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 8 items

    test_module.py::test_0[1]   SETUP otherarg 1
      RUN test0 with otherarg 1
    PASSED  TEARDOWN otherarg 1

    test_module.py::test_0[2]   SETUP otherarg 2
      RUN test0 with otherarg 2
    PASSED  TEARDOWN otherarg 2

    test_module.py::test_1[mod1]   SETUP modarg mod1
      RUN test1 with modarg mod1
    PASSED
    test_module.py::test_2[mod1-1]   SETUP otherarg 1
      RUN test2 with otherarg 1 and modarg mod1
    PASSED  TEARDOWN otherarg 1

    test_module.py::test_2[mod1-2]   SETUP otherarg 2
      RUN test2 with otherarg 2 and modarg mod1
    PASSED  TEARDOWN otherarg 2

    test_module.py::test_1[mod2]   TEARDOWN modarg mod1
      SETUP modarg mod2
      RUN test1 with modarg mod2
    PASSED
    test_module.py::test_2[mod2-1]   SETUP otherarg 1
      RUN test2 with otherarg 1 and modarg mod2
    PASSED  TEARDOWN otherarg 1

    test_module.py::test_2[mod2-2]   SETUP otherarg 2
      RUN test2 with otherarg 2 and modarg mod2
    PASSED  TEARDOWN otherarg 2
      TEARDOWN modarg mod2


    ============================ 8 passed in 0.12s =============================

You can see that the parametrized module-scoped ``modarg`` resource caused an
ordering of test execution that led to the fewest possible "active" resources.
The finalizer for the ``mod1`` parametrized resource was executed before the
``mod2`` resource was setup.

In particular notice that test_0 is completely independent and finishes first.
Then test_1 is executed with ``mod1``, then test_2 with ``mod1``, then test_1
with ``mod2`` and finally test_2 with ``mod2``.

The ``otherarg`` parametrized resource (having function scope) was set up before
and torn down after every test that used it.


.. _`usefixtures`:

Use fixtures in classes and modules with ``usefixtures``
--------------------------------------------------------

.. regendoc:wipe

Sometimes test functions do not directly need access to a fixture object.
For example, tests may require to operate with an empty directory as the
current working directory but otherwise do not care for the concrete
directory.  Here is how you can use the standard :mod:`tempfile`
and pytest fixtures to
achieve it.  We separate the creation of the fixture into a :file:`conftest.py`
file:

.. code-block:: python

    # content of conftest.py

    import os
    import tempfile

    import pytest


    @pytest.fixture
    def cleandir():
        with tempfile.TemporaryDirectory() as newpath:
            old_cwd = os.getcwd()
            os.chdir(newpath)
            yield
            os.chdir(old_cwd)

and declare its use in a test module via a ``usefixtures`` marker:

.. code-block:: python

    # content of test_setenv.py
    import os

    import pytest


    @pytest.mark.usefixtures("cleandir")
    class TestDirectoryInit:
        def test_cwd_starts_empty(self):
            assert os.listdir(os.getcwd()) == []
            with open("myfile", "w", encoding="utf-8") as f:
                f.write("hello")

        def test_cwd_again_starts_empty(self):
            assert os.listdir(os.getcwd()) == []

Due to the ``usefixtures`` marker, the ``cleandir`` fixture
will be required for the execution of each test method, just as if
you specified a "cleandir" function argument to each of them.  Let's run it
to verify our fixture is activated and the tests pass:

.. code-block:: pytest

    $ pytest -q
    ..                                                                   [100%]
    2 passed in 0.12s

You can specify multiple fixtures like this:

.. code-block:: python

    @pytest.mark.usefixtures("cleandir", "anotherfixture")
    def test(): ...

and you may specify fixture usage at the test module level using :globalvar:`pytestmark`:

.. code-block:: python

    pytestmark = pytest.mark.usefixtures("cleandir")


It is also possible to put fixtures required by all tests in your project
into a configuration file:

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    usefixtures = ["cleandir"]

.. warning::

    ``@pytest.mark.usefixtures`` cannot be used on **fixture functions**. For example,
    this is an error:

    .. code-block:: python

        @pytest.mark.usefixtures("my_other_fixture")
        @pytest.fixture
        def my_fixture_that_sadly_wont_use_my_other_fixture(): ...

.. _`override fixtures`:

Overriding fixtures on various levels
-------------------------------------

In a relatively large test suite, you may want to *override* a fixture, to augment
or change its behavior inside of certain test modules or directories.

Override a fixture on a directory (conftest) level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given the tests file structure is:

::

    tests/
        conftest.py
            # content of tests/conftest.py
            import pytest

            @pytest.fixture
            def username():
                return 'username'

        test_something.py
            # content of tests/test_something.py
            def test_username(username):
                assert username == 'username'

        subdir/
            conftest.py
                # content of tests/subdir/conftest.py
                import pytest

                @pytest.fixture
                def username(username):
                    return 'overridden-' + username

            test_something_else.py
                # content of tests/subdir/test_something_else.py
                def test_username(username):
                    assert username == 'overridden-username'

As you can see, a fixture with the same name can be overridden for a certain test directory level.
Note that the ``base`` or ``super`` fixture can be accessed from the ``overriding``
fixture easily - used in the example above.

Override a fixture on a test module level
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given the tests file structure is:

::

    tests/
        conftest.py
            # content of tests/conftest.py
            import pytest

            @pytest.fixture
            def username():
                return 'username'

        test_something.py
            # content of tests/test_something.py
            import pytest

            @pytest.fixture
            def username(username):
                return 'overridden-' + username

            def test_username(username):
                assert username == 'overridden-username'

        test_something_else.py
            # content of tests/test_something_else.py
            import pytest

            @pytest.fixture
            def username(username):
                return 'overridden-else-' + username

            def test_username(username):
                assert username == 'overridden-else-username'

In the example above, a fixture with the same name can be overridden for a certain test module.


Override a fixture with direct test parametrization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given the tests file structure is:

::

    tests/
        conftest.py
            # content of tests/conftest.py
            import pytest

            @pytest.fixture
            def username():
                return 'username'

            @pytest.fixture
            def other_username(username):
                return 'other-' + username

        test_something.py
            # content of tests/test_something.py
            import pytest

            @pytest.mark.parametrize('username', ['directly-overridden-username'])
            def test_username(username):
                assert username == 'directly-overridden-username'

            @pytest.mark.parametrize('username', ['directly-overridden-username-other'])
            def test_username_other(other_username):
                assert other_username == 'other-directly-overridden-username-other'

In the example above, a fixture value is overridden by the test parameter value. Note that the value of the fixture
can be overridden this way even if the test doesn't use it directly (doesn't mention it in the function prototype).


Override a parametrized fixture with non-parametrized one and vice versa
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given the tests file structure is:

::

    tests/
        conftest.py
            # content of tests/conftest.py
            import pytest

            @pytest.fixture(params=['one', 'two', 'three'])
            def parametrized_username(request):
                return request.param

            @pytest.fixture
            def non_parametrized_username(request):
                return 'username'

        test_something.py
            # content of tests/test_something.py
            import pytest

            @pytest.fixture
            def parametrized_username():
                return 'overridden-username'

            @pytest.fixture(params=['one', 'two', 'three'])
            def non_parametrized_username(request):
                return request.param

            def test_username(parametrized_username):
                assert parametrized_username == 'overridden-username'

            def test_parametrized_username(non_parametrized_username):
                assert non_parametrized_username in ['one', 'two', 'three']

        test_something_else.py
            # content of tests/test_something_else.py
            def test_username(parametrized_username):
                assert parametrized_username in ['one', 'two', 'three']

            def test_username(non_parametrized_username):
                assert non_parametrized_username == 'username'

In the example above, a parametrized fixture is overridden with a non-parametrized version, and
a non-parametrized fixture is overridden with a parametrized version for certain test module.
The same applies for the test directory level obviously.


Using fixtures from other projects
----------------------------------

Usually projects that provide pytest support will use :ref:`entry points <pip-installable plugins>`,
so just installing those projects into an environment will make those fixtures available for use.

In case you want to use fixtures from a project that does not use entry points, you can
define :globalvar:`pytest_plugins` in your top ``conftest.py`` file to register that module
as a plugin.

Suppose you have some fixtures in ``mylibrary.fixtures`` and you want to reuse them into your
``app/tests`` directory.

All you need to do is to define :globalvar:`pytest_plugins` in ``app/tests/conftest.py``
pointing to that module.

.. code-block:: python

    pytest_plugins = "mylibrary.fixtures"

This effectively registers ``mylibrary.fixtures`` as a plugin, making all its fixtures and
hooks available to tests in ``app/tests``.

.. note::

    Sometimes users will *import* fixtures from other projects for use, however this is not
    recommended: importing fixtures into a module will register them in pytest
    as *defined* in that module.

    This has minor consequences, such as appearing multiple times in ``pytest --help``,
    but it is not **recommended** because this behavior might change/stop working
    in future versions.

# How to mark test functions with attributes
Source: https://docs.pytest.org/en/stable/how-to/mark.html

.. _mark:

How to mark test functions with attributes
===========================================

By using the ``pytest.mark`` helper you can easily set
metadata on your test functions. You can find the full list of builtin markers
in the :ref:`API Reference<marks ref>`. Or you can list all the markers, including
builtin and custom, using the CLI - :code:`pytest --markers`.

Here are some of the builtin markers:

* :ref:`usefixtures <usefixtures>` - use fixtures on a test function or class
* :ref:`filterwarnings <filterwarnings>` - filter certain warnings of a test function
* :ref:`skip <skip>` - always skip a test function
* :ref:`skipif <skipif>` - skip a test function if a certain condition is met
* :ref:`xfail <xfail>` - produce an "expected failure" outcome if a certain
  condition is met
* :ref:`parametrize <parametrizemark>` - perform multiple calls
  to the same test function.

It's easy to create custom markers or to apply markers
to whole test classes or modules. Those markers can be used by plugins, and also
are commonly used to :ref:`select tests <mark run>` on the command-line with the :option:`-m` option.

See :ref:`mark examples` for examples which also serve as documentation.

.. note::

    Marks can only be applied to tests, having no effect on
    :ref:`fixtures <fixtures>`.


Registering marks
-----------------

You can register custom marks in your configuration file like this:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        markers = [
            "slow: marks tests as slow (deselect with '-m \"not slow\"')",
            "serial",
        ]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        markers =
            slow: marks tests as slow (deselect with '-m "not slow"')
            serial

Note that everything past the ``:`` after the mark name is an optional description.

Alternatively, you can register new markers programmatically in a
:ref:`pytest_configure <initialization-hooks>` hook:

.. code-block:: python

    def pytest_configure(config):
        config.addinivalue_line(
            "markers", "env(name): mark test to run only on named environment"
        )


Registered marks appear in pytest's help text and do not emit warnings (see the next section). It
is recommended that third-party plugins always :ref:`register their markers <registering-markers>`.

.. _unknown-marks:

Raising errors on unknown marks
-------------------------------

Unregistered marks applied with the ``@pytest.mark.name_of_the_mark`` decorator
will always emit a warning in order to avoid silently doing something
surprising due to mistyped names. As described in the previous section, you can disable
the warning for custom marks by registering them in your configuration file or
using a custom ``pytest_configure`` hook.

When the :confval:`strict_markers` configuration option is set, any unknown marks applied
with the ``@pytest.mark.name_of_the_mark`` decorator will trigger an error. You can
enforce this validation in your project by setting :confval:`strict_markers` in your configuration:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        addopts = ["--strict-markers"]
        markers = [
            "slow: marks tests as slow (deselect with '-m \"not slow\"')",
            "serial",
        ]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        strict_markers = true
        markers =
            slow: marks tests as slow (deselect with '-m "not slow"')
            serial

# How to parametrize fixtures and test functions
Source: https://docs.pytest.org/en/stable/how-to/parametrize.html

.. _`test generators`:
.. _`parametrizing-tests`:
.. _`parametrized test functions`:
.. _`parametrize`:

.. _`parametrize-basics`:

How to parametrize fixtures and test functions
==========================================================================

pytest enables test parametrization at several levels:

- :py:func:`pytest.fixture` allows one to :ref:`parametrize fixture
  functions <fixture-parametrize>`.

* `@pytest.mark.parametrize`_ allows one to define multiple sets of
  arguments and fixtures at the test function or class.

* `pytest_generate_tests`_ allows one to define custom parametrization
  schemes or extensions.


.. note::

    See :ref:`subtests` for an alternative to parametrization.

.. _parametrizemark:
.. _`@pytest.mark.parametrize`:


``@pytest.mark.parametrize``: parametrizing test functions
---------------------------------------------------------------------

.. regendoc: wipe

The builtin :ref:`pytest.mark.parametrize ref` decorator enables
parametrization of arguments for a test function.  Here is a typical example
of a test function that implements checking that a certain input leads
to an expected output:

.. code-block:: python

    # content of test_expectation.py
    import pytest


    @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    def test_eval(test_input, expected):
        assert eval(test_input) == expected

Here, the ``@parametrize`` decorator defines three different ``(test_input,expected)``
tuples so that the ``test_eval`` function will run three times using
them in turn:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 3 items

    test_expectation.py ..F                                              [100%]

    ================================= FAILURES =================================
    ____________________________ test_eval[6*9-42] _____________________________

    test_input = '6*9', expected = 42

        @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
        def test_eval(test_input, expected):
    >       assert eval(test_input) == expected
    E       AssertionError: assert 54 == 42
    E        +  where 54 = eval('6*9')

    test_expectation.py:6: AssertionError
    ========================= short test summary info ==========================
    FAILED test_expectation.py::test_eval[6*9-42] - AssertionError: assert 54...
    ======================= 1 failed, 2 passed in 0.12s ========================

.. note::

    Parameter values are passed as-is to tests (no copy whatsoever).

    For example, if you pass a list or a dict as a parameter value, and
    the test case code mutates it, the mutations will be reflected in subsequent
    test case calls.

.. note::

    pytest by default escapes any non-ascii characters used in unicode strings
    for the parametrization because it has several downsides.
    If however you would like to use unicode strings in parametrization
    and see them in the terminal as is (non-escaped), use this option
    in your configuration file:

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true

    Keep in mind however that this might cause unwanted side effects and
    even bugs depending on the OS used and plugins currently installed,
    so use it at your own risk.


As designed in this example, only one pair of input/output values fails
the simple test function.  And as usual with test function arguments,
you can see the ``input`` and ``output`` values in the traceback.

Note that you could also use the parametrize marker on a class or a module
(see :ref:`mark`) which would invoke several functions with the argument sets,
for instance:


.. code-block:: python

    import pytest


    @pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])
    class TestClass:
        def test_simple_case(self, n, expected):
            assert n + 1 == expected

        def test_weird_simple_case(self, n, expected):
            assert (n * 1) + 1 == expected


To parametrize all tests in a module, you can assign to the :globalvar:`pytestmark` global variable:


.. code-block:: python

    import pytest

    pytestmark = pytest.mark.parametrize("n,expected", [(1, 2), (3, 4)])


    class TestClass:
        def test_simple_case(self, n, expected):
            assert n + 1 == expected

        def test_weird_simple_case(self, n, expected):
            assert (n * 1) + 1 == expected


It is also possible to mark individual test instances within parametrize,
for example with the builtin ``mark.xfail``:

.. code-block:: python

    # content of test_expectation.py
    import pytest


    @pytest.mark.parametrize(
        "test_input,expected",
        [("3+5", 8), ("2+4", 6), pytest.param("6*9", 42, marks=pytest.mark.xfail)],
    )
    def test_eval(test_input, expected):
        assert eval(test_input) == expected

Let's run this:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 3 items

    test_expectation.py ..x                                              [100%]

    ======================= 2 passed, 1 xfailed in 0.12s =======================

The one parameter set which caused a failure previously now
shows up as an "xfailed" (expected to fail) test.

In case the values provided to ``parametrize`` result in an empty list - for
example, if they're dynamically generated by some function - the behaviour of
pytest is defined by the :confval:`empty_parameter_set_mark` option.

To get all combinations of multiple parametrized arguments you can stack
``parametrize`` decorators:

.. code-block:: python

    import pytest


    @pytest.mark.parametrize("x", [0, 1])
    @pytest.mark.parametrize("y", [2, 3])
    def test_foo(x, y):
        pass

This will run the test with the arguments set to ``x=0/y=2``, ``x=1/y=2``,
``x=0/y=3``, and ``x=1/y=3`` exhausting parameters in the order of the decorators.


.. _`pytest_generate_tests`:

Basic ``pytest_generate_tests`` example
---------------------------------------------

Sometimes you may want to implement your own parametrization scheme
or implement some dynamism for determining the parameters or scope
of a fixture.   For this, you can use the ``pytest_generate_tests`` hook
which is called when collecting a test function.  Through the passed in
``metafunc`` object you can inspect the requesting test context and, most
importantly, you can call ``metafunc.parametrize()`` to cause
parametrization.

For example, let's say we want to run a test taking string inputs which
we want to set via a new ``pytest`` command line option.  Let's first write
a simple test accepting a ``stringinput`` fixture function argument:

.. code-block:: python

    # content of test_strings.py


    def test_valid_string(stringinput):
        assert stringinput.isalpha()

Now we add a ``conftest.py`` file containing the addition of a
command line option and the parametrization of our test function:

.. code-block:: python

    # content of conftest.py


    def pytest_addoption(parser):
        parser.addoption(
            "--stringinput",
            action="append",
            default=[],
            help="list of stringinputs to pass to test functions",
        )


    def pytest_generate_tests(metafunc):
        if "stringinput" in metafunc.fixturenames:
            metafunc.parametrize("stringinput", metafunc.config.getoption("stringinput"))

.. note::

    The :hook:`pytest_generate_tests` hook can also be implemented directly in a test
    module or inside a test class; unlike other hooks, pytest will discover it there
    as well. Other hooks must live in a :ref:`conftest.py <localplugin>` or a plugin.
    See :ref:`writinghooks`.

If we now pass two stringinput values, our test will run twice:

.. code-block:: pytest

    $ pytest -q --stringinput="hello" --stringinput="world" test_strings.py
    ..                                                                   [100%]
    2 passed in 0.12s

Let's also run with a stringinput that will lead to a failing test:

.. code-block:: pytest

    $ pytest -q --stringinput="!" test_strings.py
    F                                                                    [100%]
    ================================= FAILURES =================================
    ___________________________ test_valid_string[!] ___________________________

    stringinput = '!'

        def test_valid_string(stringinput):
    >       assert stringinput.isalpha()
    E       AssertionError: assert False
    E        +  where False = <built-in method isalpha of str object at 0xdeadbeef0001>()
    E        +    where <built-in method isalpha of str object at 0xdeadbeef0001> = '!'.isalpha

    test_strings.py:4: AssertionError
    ========================= short test summary info ==========================
    FAILED test_strings.py::test_valid_string[!] - AssertionError: assert False
    1 failed in 0.12s

As expected our test function fails.

If you don't specify a stringinput it will be skipped because
``metafunc.parametrize()`` will be called with an empty parameter
list:

.. code-block:: pytest

    $ pytest -q -rs test_strings.py
    s                                                                    [100%]
    ========================= short test summary info ==========================
    SKIPPED [1] test_strings.py: got empty parameter set for (stringinput)
    1 skipped in 0.12s

Note that when calling ``metafunc.parametrize`` multiple times with different parameter sets, all parameter names across
those sets cannot be duplicated, otherwise an error will be raised.

More examples
-------------

For further examples, you might want to look at :ref:`more
parametrization examples <paramexamples>`.

# How to use subtests
Source: https://docs.pytest.org/en/stable/how-to/subtests.html

.. _subtests:

How to use subtests
===================

.. versionadded:: 9.0

.. note::

    This feature is experimental. Its behavior, particularly how failures are reported, may evolve in future releases. However, the core functionality and usage are considered stable.

pytest allows for grouping assertions within a normal test, known as *subtests*.

Subtests are an alternative to parametrization, particularly useful when the exact parametrization values are not known at collection time.


.. code-block:: python

    # content of test_subtest.py


    def test(subtests):
        for i in range(5):
            with subtests.test(msg="custom message", i=i):
                assert i % 2 == 0

Each assertion failure or error is caught by the context manager and reported individually:

.. code-block:: text

    $ pytest -q test_subtest.py
    uuuuuF                                                               [100%]
    ================================= FAILURES =================================
    _______________________ test [custom message] (i=1) ________________________

    subtests = <_pytest.subtests.Subtests object at 0xdeadbeef0001>

        def test(subtests):
            for i in range(5):
                with subtests.test(msg="custom message", i=i):
    >               assert i % 2 == 0
    E               assert (1 % 2) == 0

    test_subtest.py:6: AssertionError
    _______________________ test [custom message] (i=3) ________________________

    subtests = <_pytest.subtests.Subtests object at 0xdeadbeef0001>

        def test(subtests):
            for i in range(5):
                with subtests.test(msg="custom message", i=i):
    >               assert i % 2 == 0
    E               assert (3 % 2) == 0

    test_subtest.py:6: AssertionError
    ___________________________________ test ___________________________________
    contains 2 failed subtests
    ========================= short test summary info ==========================
    SUBFAILED[custom message] (i=1) test_subtest.py::test - assert (1 % 2) == 0
    SUBFAILED[custom message] (i=3) test_subtest.py::test - assert (3 % 2) == 0
    FAILED test_subtest.py::test - contains 2 failed subtests
    3 failed, 3 subtests passed in 0.12s

In the output above:

* The compact progress output uses ``u`` for both passed and failed subtests;
  see the short test summary for each failed subtest.
* Subtest failures are reported as ``SUBFAILED``.
* Subtests are reported first and the "top-level" test is reported at the end on its own.

Note that it is possible to use ``subtests`` multiple times in the same test, or even mix and match with normal assertions
outside the ``subtests.test`` block:

.. code-block:: python

    def test(subtests):
        for i in range(5):
            with subtests.test("stage 1", i=i):
                assert i % 2 == 0

        assert func() == 10

        for i in range(10, 20):
            with subtests.test("stage 2", i=i):
                assert i % 2 == 0

.. note::

    See :ref:`parametrize` for an alternative to subtests.


Verbosity
---------

By default, only **subtest failures** are shown. Higher verbosity levels (:option:`-v`) will also show progress output for **passed** subtests.

It is possible to control the verbosity of subtests by setting :confval:`verbosity_subtests`.


Typing
------

:class:`pytest.Subtests` is exported so it can be used in type annotations:

.. code-block:: python

    def test(subtests: pytest.Subtests) -> None: ...

.. _parametrize_vs_subtests:

Parametrization vs Subtests
---------------------------

While :ref:`traditional pytest parametrization <parametrize>` and ``subtests`` are similar, they have important differences and use cases.


Parametrization
~~~~~~~~~~~~~~~

* Happens at collection time.
* Generates individual tests.
* Parametrized tests can be referenced from the command line.
* Plays well with plugins that handle test execution, such as :option:`--last-failed`.
* Ideal for decision table testing.

Subtests
~~~~~~~~

* Happen during test execution.
* Are not known at collection time.
* Can be generated dynamically.
* Cannot be referenced individually from the command line.
* Plugins that handle test execution cannot target individual subtests.
* An assertion failure inside a subtest does not interrupt the test, letting users see all failures in the same report.


.. note::

    This feature was originally implemented as a separate plugin in `pytest-subtests <https://github.com/pytest-dev/pytest-subtests>`__, but since ``9.0`` has been merged into the core.

    The core implementation should be compatible with the plugin implementation, except it does not contain custom command-line options to control subtest output.

# How to use temporary directories and files in tests
Source: https://docs.pytest.org/en/stable/how-to/tmp_path.html

.. _`tmp_path handling`:
.. _tmp_path:

How to use temporary directories and files in tests
===================================================

The ``tmp_path`` fixture
------------------------

You can use the ``tmp_path`` fixture which will provide a temporary directory
unique to each test function.

``tmp_path`` is a :class:`pathlib.Path` object. Here is an example test usage:

.. code-block:: python

    # content of test_tmp_path.py
    CONTENT = "content"


    def test_create_file(tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "hello.txt"
        p.write_text(CONTENT, encoding="utf-8")
        assert p.read_text(encoding="utf-8") == CONTENT
        assert len(list(tmp_path.iterdir())) == 1
        assert 0

Running this would result in a passed test except for the last
``assert 0`` line which we use to look at values:

.. code-block:: pytest

    $ pytest test_tmp_path.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_tmp_path.py F                                                   [100%]

    ================================= FAILURES =================================
    _____________________________ test_create_file _____________________________

    tmp_path = PosixPath('PYTEST_TMPDIR/test_create_file0')

        def test_create_file(tmp_path):
            d = tmp_path / "sub"
            d.mkdir()
            p = d / "hello.txt"
            p.write_text(CONTENT, encoding="utf-8")
            assert p.read_text(encoding="utf-8") == CONTENT
            assert len(list(tmp_path.iterdir())) == 1
    >       assert 0
    E       assert 0

    test_tmp_path.py:11: AssertionError
    ========================= short test summary info ==========================
    FAILED test_tmp_path.py::test_create_file - assert 0
    ============================ 1 failed in 0.12s =============================

By default, ``pytest`` retains the temporary directory for the last 3 ``pytest``
invocations. Concurrent invocations of the same test function are supported by
configuring the base temporary directory to be unique for each concurrent
run. See `temporary directory location and retention`_ for details.

.. _`tmp_path_factory example`:

The ``tmp_path_factory`` fixture
--------------------------------

The ``tmp_path_factory`` is a session-scoped fixture which can be used
to create arbitrary temporary directories from any other fixture or test.

For example, suppose your test suite needs a large image on disk, which is
generated procedurally. Instead of computing the same image for each test
that uses it into its own ``tmp_path``, you can generate it once per-session
to save time:

.. code-block:: python

    # contents of conftest.py
    import pytest


    @pytest.fixture(scope="session")
    def image_file(tmp_path_factory):
        img = compute_expensive_image()
        fn = tmp_path_factory.mktemp("data") / "img.png"
        img.save(fn)
        return fn


    # contents of test_image.py
    def test_histogram(image_file):
        img = load_image(image_file)
        # compute and test histogram

See :ref:`tmp_path_factory API <tmp_path_factory factory api>` for details.

.. _`tmpdir and tmpdir_factory`:
.. _tmpdir:

The ``tmpdir`` and ``tmpdir_factory`` fixtures
----------------------------------------------

The ``tmpdir`` and ``tmpdir_factory`` fixtures are similar to ``tmp_path``
and ``tmp_path_factory``, but use/return legacy `py.path.local`_ objects
rather than standard :class:`pathlib.Path` objects.

.. note::
    These days, it is preferred to use ``tmp_path`` and ``tmp_path_factory``.

    In order to help modernize old code bases, one can run pytest with the legacypath
    plugin disabled:

    .. code-block:: bash

        pytest -p no:legacypath

    This will trigger errors on tests using the legacy paths.
    It can also be permanently set as part of the :confval:`addopts` parameter in the
    config file.

See :fixture:`tmpdir <tmpdir>` :fixture:`tmpdir_factory <tmpdir_factory>`
API for details.


.. _`temporary directory location and retention`:

Temporary directory location and retention
------------------------------------------

The temporary directories,
as returned by the :fixture:`tmp_path` and (now deprecated) :fixture:`tmpdir` fixtures,
are automatically created under a base temporary directory,
in a structure that depends on the :option:`--basetemp` option:

- By default (when the :option:`--basetemp` option is not set),
  the temporary directories will follow this template:

  .. code-block:: text

      {temproot}/pytest-of-{user}/pytest-{num}/{testname}/

  where:

  - ``{temproot}`` is the system temporary directory
    as determined by :py:func:`tempfile.gettempdir`.
    It can be overridden by the :envvar:`PYTEST_DEBUG_TEMPROOT` environment variable.
  - ``{user}`` is the user name running the tests,
  - ``{num}`` is a number that is incremented with each test suite run
  - ``{testname}`` is a sanitized version of :py:attr:`the name of the current test <_pytest.nodes.Node.name>`.

  The auto-incrementing ``{num}`` placeholder provides a basic retention feature
  and avoids that existing results of previous test runs are blindly removed.
  By default, the last 3 temporary directories are kept,
  but this behavior can be configured with
  :confval:`tmp_path_retention_count` and :confval:`tmp_path_retention_policy`.

- When the :option:`--basetemp` option is used (e.g. ``pytest --basetemp=mydir``),
  it will be used directly as base temporary directory:

  .. code-block:: text

      {basetemp}/{testname}/

  Note that there is no retention feature in this case:
  only the results of the most recent run will be kept.

  .. warning::

      The directory given to :option:`--basetemp` will be cleared blindly before each test run,
      so make sure to use a directory for that purpose only.

When distributing tests on the local machine using ``pytest-xdist``, care is taken to
automatically configure a `basetemp` directory for the sub processes such that all temporary
data lands below a single per-test run temporary directory.

.. _`py.path.local`: https://py.readthedocs.io/en/latest/path.html

# How to monkeypatch/mock modules and environments
Source: https://docs.pytest.org/en/stable/how-to/monkeypatch.html

.. _monkeypatching:

How to monkeypatch/mock modules and environments
================================================================

.. currentmodule:: pytest

Sometimes tests need to invoke functionality which depends
on global settings or which invokes code which cannot be easily
tested such as network access.  The ``monkeypatch`` fixture
helps you to safely set/delete an attribute, dictionary item or
environment variable, or to modify ``sys.path`` for importing.

The ``monkeypatch`` fixture provides these helper methods for safely patching and mocking
functionality in tests:

* :meth:`monkeypatch.setattr(obj, name, value, raising=True) <pytest.MonkeyPatch.setattr>`
* :meth:`monkeypatch.delattr(obj, name, raising=True) <pytest.MonkeyPatch.delattr>`
* :meth:`monkeypatch.setitem(mapping, name, value) <pytest.MonkeyPatch.setitem>`
* :meth:`monkeypatch.delitem(obj, name, raising=True) <pytest.MonkeyPatch.delitem>`
* :meth:`monkeypatch.setenv(name, value, prepend=None) <pytest.MonkeyPatch.setenv>`
* :meth:`monkeypatch.delenv(name, raising=True) <pytest.MonkeyPatch.delenv>`
* :meth:`monkeypatch.syspath_prepend(path) <pytest.MonkeyPatch.syspath_prepend>`
* :meth:`monkeypatch.chdir(path) <pytest.MonkeyPatch.chdir>`
* :meth:`monkeypatch.context() <pytest.MonkeyPatch.context>`


All modifications will be undone after the requesting
test function or fixture has finished. The ``raising``
parameter determines if a ``KeyError`` or ``AttributeError``
will be raised if the target of the set/deletion operation does not exist.

Consider the following scenarios:

1. Modifying the behavior of a function or the property of a class for a test e.g.
there is an API call or database connection you will not make for a test but you know
what the expected output should be. Use :py:meth:`monkeypatch.setattr <MonkeyPatch.setattr>` to patch the
function or property with your desired testing behavior. This can include your own functions.
Use :py:meth:`monkeypatch.delattr <MonkeyPatch.delattr>` to remove the function or property for the test.

2. Modifying the values of dictionaries e.g. you have a global configuration that
you want to modify for certain test cases. Use :py:meth:`monkeypatch.setitem <MonkeyPatch.setitem>` to patch the
dictionary for the test. :py:meth:`monkeypatch.delitem <MonkeyPatch.delitem>` can be used to remove items.

3. Modifying environment variables for a test e.g. to test program behavior if an
environment variable is missing, or to set multiple values to a known variable.
:py:meth:`monkeypatch.setenv <MonkeyPatch.setenv>` and :py:meth:`monkeypatch.delenv <MonkeyPatch.delenv>` can be used for
these patches.

4. Use ``monkeypatch.setenv("PATH", value, prepend=os.pathsep)`` to modify ``$PATH``, and
:py:meth:`monkeypatch.chdir <MonkeyPatch.chdir>` to change the context of the current working directory
during a test.

5. Use :py:meth:`monkeypatch.syspath_prepend <MonkeyPatch.syspath_prepend>` to modify ``sys.path`` which will also
call ``pkg_resources.fixup_namespace_packages`` and :py:func:`importlib.invalidate_caches`.

6. Use :py:meth:`monkeypatch.context <MonkeyPatch.context>` to apply patches only in a specific scope, which can help
control teardown of complex fixtures or patches to the stdlib.

See the `monkeypatch blog post`_ for some introduction material
and a discussion of its motivation.

.. _`monkeypatch blog post`: https://tetamap.wordpress.com//2009/03/03/monkeypatching-in-unit-tests-done-right/

Monkeypatching functions
------------------------

Consider a scenario where you are working with user directories. In the context of
testing, you do not want your test to depend on the running user. ``monkeypatch``
can be used to patch functions dependent on the user to always return a
specific value.

In this example, :py:meth:`monkeypatch.setattr <MonkeyPatch.setattr>` is used to patch ``Path.home``
so that the known testing path ``Path("/abc")`` is always used when the test is run.
This removes any dependency on the running user for testing purposes.
:py:meth:`monkeypatch.setattr <MonkeyPatch.setattr>` must be called before the function which will use
the patched function is called.
After the test function finishes the ``Path.home`` modification will be undone.

.. code-block:: python

    # contents of test_module.py with source code and the test
    from pathlib import Path


    def getssh():
        """Simple function to return expanded homedir ssh path."""
        return Path.home() / ".ssh"


    def test_getssh(monkeypatch):
        # mocked return function to replace Path.home
        # always return '/abc'
        def mockreturn():
            return Path("/abc")

        # Application of the monkeypatch to replace Path.home
        # with the behavior of mockreturn defined above.
        monkeypatch.setattr(Path, "home", mockreturn)

        # Calling getssh() will use mockreturn in place of Path.home
        # for this test with the monkeypatch.
        x = getssh()
        assert x == Path("/abc/.ssh")

Monkeypatching returned objects: building mock classes
------------------------------------------------------

:py:meth:`monkeypatch.setattr <MonkeyPatch.setattr>` can be used in conjunction with classes to mock returned
objects from functions instead of values.
Imagine a simple function to take an API url and return the json response.

.. code-block:: python

    # contents of app.py, a simple API retrieval example
    import requests


    def get_json(url):
        """Takes a URL, and returns the JSON."""
        r = requests.get(url)
        return r.json()

We need to mock ``r``, the returned response object for testing purposes.
The mock of ``r`` needs a ``.json()`` method which returns a dictionary.
This can be done in our test file by defining a class to represent ``r``.

.. code-block:: python

    # contents of test_app.py, a simple test for our API retrieval
    # import requests for the purposes of monkeypatching
    import requests

    # our app.py that includes the get_json() function
    # this is the previous code block example
    import app


    # custom class to be the mock return value
    # will override the requests.Response returned from requests.get
    class MockResponse:
        # mock json() method always returns a specific testing dictionary
        @staticmethod
        def json():
            return {"mock_key": "mock_response"}


    def test_get_json(monkeypatch):
        # Any arguments may be passed and mock_get() will always return our
        # mocked object, which only has the .json() method.
        def mock_get(*args, **kwargs):
            return MockResponse()

        # apply the monkeypatch for requests.get to mock_get
        monkeypatch.setattr(requests, "get", mock_get)

        # app.get_json, which contains requests.get, uses the monkeypatch
        result = app.get_json("https://fakeurl")
        assert result["mock_key"] == "mock_response"


``monkeypatch`` applies the mock for ``requests.get`` with our ``mock_get`` function.
The ``mock_get`` function returns an instance of the ``MockResponse`` class, which
has a ``json()`` method defined to return a known testing dictionary and does not
require any outside API connection.

You can build the ``MockResponse`` class with the appropriate degree of complexity for
the scenario you are testing. For instance, it could include an ``ok`` property that
always returns ``True``, or return different values from the ``json()`` mocked method
based on input strings.

This mock can be shared across tests using a ``fixture``:

.. code-block:: python

    # contents of test_app.py, a simple test for our API retrieval
    import pytest
    import requests

    # app.py that includes the get_json() function
    import app


    # custom class to be the mock return value of requests.get()
    class MockResponse:
        @staticmethod
        def json():
            return {"mock_key": "mock_response"}


    # monkeypatched requests.get moved to a fixture
    @pytest.fixture
    def mock_response(monkeypatch):
        """Requests.get() mocked to return {'mock_key':'mock_response'}."""

        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mock_get)


    # notice our test uses the custom fixture instead of monkeypatch directly
    def test_get_json(mock_response):
        result = app.get_json("https://fakeurl")
        assert result["mock_key"] == "mock_response"


Furthermore, if the mock was designed to be applied to all tests, the ``fixture`` could
be moved to a ``conftest.py`` file and use the with ``autouse=True`` option.


Global patch example: preventing "requests" from remote operations
------------------------------------------------------------------

If you want to prevent the "requests" library from performing http
requests in all your tests, you can do:

.. code-block:: python

    # contents of conftest.py
    import pytest


    @pytest.fixture(autouse=True)
    def no_requests(monkeypatch):
        """Remove requests.sessions.Session.request for all tests."""
        monkeypatch.delattr("requests.sessions.Session.request")

This autouse fixture will be executed for each test function and it
will delete the method ``request.session.Session.request``
so that any attempts within tests to create http requests will fail.


.. note::

    Be advised that it is not recommended to patch builtin functions such as ``open``,
    ``compile``, etc., because it might break pytest's internals. If that's
    unavoidable, passing :option:`--tb=native`, :option:`--assert=plain` and :option:`--capture=no` might
    help although there's no guarantee.

.. note::

    Mind that patching ``stdlib`` functions and some third-party libraries used by pytest
    might break pytest itself. Prefer patching the reference that your code uses
    instead of patching the original object in the standard library. For example,
    if your module does ``from os import getcwd``, patch ``mymodule.getcwd``
    rather than ``os.getcwd``.

    For code that you control, a safer long-term pattern is to make dependencies
    explicit so they can be passed into the code under test instead of patched
    globally. When patching a stdlib object is unavoidable, use
    :meth:`MonkeyPatch.context` to limit the patching to the block you want tested:

    .. code-block:: python

        import functools


        def test_partial(monkeypatch):
            with monkeypatch.context() as m:
                m.setattr(functools, "partial", 3)
                assert functools.partial == 3

    See :issue:`3290` for details.


Monkeypatching environment variables
------------------------------------

If you are working with environment variables you often need to safely change the values
or delete them from the system for testing purposes. ``monkeypatch`` provides a mechanism
to do this using the ``setenv`` and ``delenv`` method. Our example code to test:

.. code-block:: python

    # contents of our original code file e.g. code.py
    import os


    def get_os_user_lower():
        """Simple retrieval function.
        Returns lowercase USER or raises OSError."""
        username = os.getenv("USER")

        if username is None:
            raise OSError("USER environment is not set.")

        return username.lower()

There are two potential paths. First, the ``USER`` environment variable is set to a
value. Second, the ``USER`` environment variable does not exist. Using ``monkeypatch``
both paths can be safely tested without impacting the running environment:

.. code-block:: python

    # contents of our test file e.g. test_code.py
    import pytest


    def test_upper_to_lower(monkeypatch):
        """Set the USER env var to assert the behavior."""
        monkeypatch.setenv("USER", "TestingUser")
        assert get_os_user_lower() == "testinguser"


    def test_raise_exception(monkeypatch):
        """Remove the USER env var and assert OSError is raised."""
        monkeypatch.delenv("USER", raising=False)

        with pytest.raises(OSError):
            _ = get_os_user_lower()

This behavior can be moved into ``fixture`` structures and shared across tests:

.. code-block:: python

    # contents of our test file e.g. test_code.py
    import pytest


    @pytest.fixture
    def mock_env_user(monkeypatch):
        monkeypatch.setenv("USER", "TestingUser")


    @pytest.fixture
    def mock_env_missing(monkeypatch):
        monkeypatch.delenv("USER", raising=False)


    # notice the tests reference the fixtures for mocks
    def test_upper_to_lower(mock_env_user):
        assert get_os_user_lower() == "testinguser"


    def test_raise_exception(mock_env_missing):
        with pytest.raises(OSError):
            _ = get_os_user_lower()


Monkeypatching dictionaries
---------------------------

:py:meth:`monkeypatch.setitem <MonkeyPatch.setitem>` can be used to safely set the values of dictionaries
to specific values during tests. Take this simplified connection string example:

.. code-block:: python

    # contents of app.py to generate a simple connection string
    DEFAULT_CONFIG = {"user": "user1", "database": "db1"}


    def create_connection_string(config=None):
        """Creates a connection string from input or defaults."""
        config = config or DEFAULT_CONFIG
        return f"User Id={config['user']}; Location={config['database']};"

For testing purposes we can patch the ``DEFAULT_CONFIG`` dictionary to specific values.

.. code-block:: python

    # contents of test_app.py
    # app.py with the connection string function (prior code block)
    import app


    def test_connection(monkeypatch):
        # Patch the values of DEFAULT_CONFIG to specific
        # testing values only for this test.
        monkeypatch.setitem(app.DEFAULT_CONFIG, "user", "test_user")
        monkeypatch.setitem(app.DEFAULT_CONFIG, "database", "test_db")

        # expected result based on the mocks
        expected = "User Id=test_user; Location=test_db;"

        # the test uses the monkeypatched dictionary settings
        result = app.create_connection_string()
        assert result == expected

You can use the :py:meth:`monkeypatch.delitem <MonkeyPatch.delitem>` to remove values.

.. code-block:: python

    # contents of test_app.py
    import pytest

    # app.py with the connection string function
    import app


    def test_missing_user(monkeypatch):
        # patch the DEFAULT_CONFIG to be missing the 'user' key
        monkeypatch.delitem(app.DEFAULT_CONFIG, "user", raising=False)

        # Key error expected because a config is not passed, and the
        # default is now missing the 'user' entry.
        with pytest.raises(KeyError):
            _ = app.create_connection_string()


The modularity of fixtures gives you the flexibility to define
separate fixtures for each potential mock and reference them in the needed tests.

.. code-block:: python

    # contents of test_app.py
    import pytest

    # app.py with the connection string function
    import app


    # all of the mocks are moved into separated fixtures
    @pytest.fixture
    def mock_test_user(monkeypatch):
        """Set the DEFAULT_CONFIG user to test_user."""
        monkeypatch.setitem(app.DEFAULT_CONFIG, "user", "test_user")


    @pytest.fixture
    def mock_test_database(monkeypatch):
        """Set the DEFAULT_CONFIG database to test_db."""
        monkeypatch.setitem(app.DEFAULT_CONFIG, "database", "test_db")


    @pytest.fixture
    def mock_missing_default_user(monkeypatch):
        """Remove the user key from DEFAULT_CONFIG"""
        monkeypatch.delitem(app.DEFAULT_CONFIG, "user", raising=False)


    # tests reference only the fixture mocks that are needed
    def test_connection(mock_test_user, mock_test_database):
        expected = "User Id=test_user; Location=test_db;"

        result = app.create_connection_string()
        assert result == expected


    def test_missing_user(mock_missing_default_user):
        with pytest.raises(KeyError):
            _ = app.create_connection_string()


.. currentmodule:: pytest

API Reference
-------------

Consult the docs for the :class:`MonkeyPatch` class.

# How to run doctests
Source: https://docs.pytest.org/en/stable/how-to/doctest.html

.. _doctest:

How to run doctests
=========================================================

By default, all files matching the ``test*.txt`` pattern will
be run through the python standard :mod:`doctest` module.  You
can change the pattern by issuing:

.. code-block:: bash

    pytest --doctest-glob="*.rst"

on the command line. :option:`--doctest-glob` can be given multiple times in the command-line.

If you then have a text file like this:

.. code-block:: text

    # content of test_example.txt

    hello this is a doctest
    >>> x = 3
    >>> x
    3

then you can just invoke ``pytest`` directly:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_example.txt .                                                   [100%]

    ============================ 1 passed in 0.12s =============================

By default, pytest will collect ``test*.txt`` files looking for doctest directives, but you
can pass additional globs using the :option:`--doctest-glob` option (multi-allowed).

In addition to text files, you can also execute doctests directly from docstrings of your classes
and functions, including from test modules, using the :option:`--doctest-modules` option:

.. code-block:: python

    # content of mymodule.py
    def something():
        """a doctest in a docstring
        >>> something()
        42
        """
        return 42

.. code-block:: bash

    $ pytest --doctest-modules
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    mymodule.py .                                                        [ 50%]
    test_example.txt .                                                   [100%]

    ============================ 2 passed in 0.12s =============================

You can make these changes permanent in your project by
putting them into a configuration file like this:

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    addopts = ["--doctest-modules"]

Encoding
--------

The default encoding is **UTF-8**, but you can specify the encoding
that will be used for those doctest files using the
:confval:`doctest_encoding` configuration option:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        doctest_encoding = "latin1"

.. tab:: ini

    .. code-block:: ini

        [pytest]
        doctest_encoding = latin1

.. _using doctest options:

Using 'doctest' options
-----------------------

Python's standard :mod:`doctest` module provides some :ref:`options <python:option-flags-and-directives>`
to configure the strictness of doctest tests. In pytest, you can enable those flags using the
configuration file.

For example, to make pytest ignore trailing whitespaces and ignore
lengthy exception stack traces you can just write:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        doctest_optionflags = ["NORMALIZE_WHITESPACE", "IGNORE_EXCEPTION_DETAIL"]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        doctest_optionflags = NORMALIZE_WHITESPACE IGNORE_EXCEPTION_DETAIL

Alternatively, options can be enabled by an inline comment in the doc test
itself:

.. code-block:: rst

    >>> something_that_raises()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ValueError: ...

pytest also introduces new options:

* ``ALLOW_UNICODE``: when enabled, the ``u`` prefix is stripped from unicode
  strings in expected doctest output. This allows doctests to run in Python 2
  and Python 3 unchanged.

* ``ALLOW_BYTES``: similarly, the ``b`` prefix is stripped from byte strings
  in expected doctest output.

* ``NUMBER``: when enabled, floating-point numbers only need to match as far as
  the precision you have written in the expected doctest output. The numbers are
  compared using :func:`pytest.approx` with relative tolerance equal to the
  precision. For example, the following output would only need to match to 2
  decimal places when comparing ``3.14`` to
  ``pytest.approx(math.pi, rel=10**-2)``::

      >>> math.pi
      3.14

  If you wrote ``3.1416`` then the actual output would need to match to
  approximately 4 decimal places; and so on.

  This avoids false positives caused by limited floating-point precision, like
  this::

      Expected:
          0.233
      Got:
          0.23300000000000001

  ``NUMBER`` also supports lists of floating-point numbers -- in fact, it
  matches floating-point numbers appearing anywhere in the output, even inside
  a string! This means that it may not be appropriate to enable globally in
  ``doctest_optionflags`` in your configuration file.

  .. versionadded:: 5.1


Continue on failure
-------------------

By default, pytest would report only the first failure for a given doctest. If
you want to continue the test even when you have failures, do:

.. code-block:: bash

    pytest --doctest-modules --doctest-continue-on-failure


Output format
-------------

You can change the diff output format on failure for your doctests
by using one of the standard doctest module's format options
(see :data:`python:doctest.REPORT_UDIFF`, :data:`python:doctest.REPORT_CDIFF`,
:data:`python:doctest.REPORT_NDIFF`, :data:`python:doctest.REPORT_ONLY_FIRST_FAILURE`):

.. code-block:: bash

    pytest --doctest-modules --doctest-report none
    pytest --doctest-modules --doctest-report udiff
    pytest --doctest-modules --doctest-report cdiff
    pytest --doctest-modules --doctest-report ndiff
    pytest --doctest-modules --doctest-report only_first_failure


pytest-specific features
------------------------

Some features are provided to make writing doctests easier or with better integration with
your existing test suite. Keep in mind however that by using those features you will make
your doctests incompatible with the standard ``doctests`` module.

Using fixtures
^^^^^^^^^^^^^^

It is possible to use fixtures using the ``getfixture`` helper:

.. code-block:: text

    # content of example.rst
    >>> tmp = getfixture('tmp_path')
    >>> ...
    >>>

Note that the fixture needs to be defined in a place visible by pytest, for example, a `conftest.py`
file or plugin; normal python files containing docstrings are not normally scanned for fixtures
unless explicitly configured by :confval:`python_files`.

Also, the :ref:`usefixtures <usefixtures>` mark and fixtures marked as :ref:`autouse <autouse>` are supported
when executing text doctest files.

Python doctest modules are collected independently from Python test files.
Fixture scope is not shared between the two.

Doctests do not support fixtures that depend on parametrization, because doctest
collection does not perform the same test generation as normal test functions.
This includes parametrized autouse fixtures. If you need to run doctests against
multiple backends or configurations, consider moving those checks into normal
test functions or a dedicated doctest plugin.


.. _`doctest_namespace`:

'doctest_namespace' fixture
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``doctest_namespace`` fixture can be used to inject items into the
namespace in which your doctests run. It is intended to be used within
your own fixtures to provide the tests that use them with context.

``doctest_namespace`` is a standard ``dict`` object into which you
place the objects you want to appear in the doctest namespace:

.. code-block:: python

    # content of conftest.py
    import pytest
    import numpy


    @pytest.fixture(autouse=True)
    def add_np(doctest_namespace):
        doctest_namespace["np"] = numpy

which can then be used in your doctests directly:

.. code-block:: python

    # content of numpy.py
    def arange():
        """
        >>> a = np.arange(10)
        >>> len(a)
        10
        """

Note that like the normal ``conftest.py``, the fixtures are discovered in the directory tree conftest is in.
Meaning that if you put your doctest with your source code, the relevant conftest.py needs to be in the same directory tree.
Fixtures will not be discovered in a sibling directory tree!

Skipping tests
^^^^^^^^^^^^^^

For the same reasons one might want to skip normal tests, it is also possible to skip
tests inside doctests.

To skip a single check inside a doctest you can use the standard
:data:`doctest.SKIP` directive:

.. code-block:: python

    def test_random(y):
        """
        >>> random.random()  # doctest: +SKIP
        0.156231223

        >>> 1 + 1
        2
        """

This will skip the first check, but not the second.

pytest also allows using the standard pytest functions :func:`pytest.skip` and
:func:`pytest.xfail` inside doctests, which might be useful because you can
then skip/xfail tests based on external conditions:


.. code-block:: text

    >>> import sys, pytest
    >>> if sys.platform.startswith('win'):
    ...     pytest.skip('this doctest does not work on Windows')
    ...
    >>> import fcntl
    >>> ...

However using those functions is discouraged because it reduces the readability of the
docstring.

.. note::

    :func:`pytest.skip` and :func:`pytest.xfail` behave differently depending
    if the doctests are in a Python file (in docstrings) or a text file containing
    doctests intermingled with text:

    * Python modules (docstrings): the functions only act in that specific docstring,
      letting the other docstrings in the same module execute as normal.

    * Text files: the functions will skip/xfail the checks for the rest of the entire
      file.


Alternatives
------------

While the built-in pytest support provides a good set of functionalities for using
doctests, if you use them extensively you might be interested in those external packages
which add many more features, and include pytest integration:

* `pytest-doctestplus <https://github.com/scientific-python/pytest-doctestplus>`__: provides
  advanced doctest support and enables the testing of reStructuredText (".rst") files.

* `Sybil <https://sybil.readthedocs.io>`__: provides a way to test examples in
  your documentation by parsing them from the documentation source and evaluating
  the parsed examples as part of your normal test run.

# How to re-run failed tests and maintain state between test runs
Source: https://docs.pytest.org/en/stable/how-to/cache.html

.. _`cache_provider`:
.. _cache:


How to re-run failed tests and maintain state between test runs
===============================================================



Usage
---------

The plugin provides two command line options to rerun failures from the
last ``pytest`` invocation:

* :option:`--lf, --last-failed <--lf>` - to only re-run the failures.
* :option:`--ff, --failed-first <--ff>` - to run the failures first and then the rest of
  the tests.

For cleanup (usually not needed), a :option:`--cache-clear` option allows to remove
all cross-session cache contents ahead of a test run.

Other plugins may access the `config.cache`_ object to set/get
**json encodable** values between ``pytest`` invocations.

.. note::

    This plugin is enabled by default, but can be disabled if needed: see
    :ref:`cmdunregister` (the internal name for this plugin is
    ``cacheprovider``).


Rerunning only failures or failures first
-----------------------------------------------

First, let's create 50 test invocations of which only 2 fail:

.. code-block:: python

    # content of test_50.py
    import pytest


    @pytest.mark.parametrize("i", range(50))
    def test_num(i):
        if i in (17, 25):
            pytest.fail("bad luck")

If you run this for the first time you will see two failures:

.. code-block:: pytest

    $ pytest -q
    .................F.......F........................                   [100%]
    ================================= FAILURES =================================
    _______________________________ test_num[17] _______________________________

    i = 17

        @pytest.mark.parametrize("i", range(50))
        def test_num(i):
            if i in (17, 25):
    >           pytest.fail("bad luck")
    E           Failed: bad luck

    test_50.py:7: Failed
    _______________________________ test_num[25] _______________________________

    i = 25

        @pytest.mark.parametrize("i", range(50))
        def test_num(i):
            if i in (17, 25):
    >           pytest.fail("bad luck")
    E           Failed: bad luck

    test_50.py:7: Failed
    ========================= short test summary info ==========================
    FAILED test_50.py::test_num[17] - Failed: bad luck
    FAILED test_50.py::test_num[25] - Failed: bad luck
    2 failed, 48 passed in 0.12s

If you then run it with :option:`--lf`:

.. code-block:: pytest

    $ pytest --lf
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items
    run-last-failure: rerun previous 2 failures

    test_50.py FF                                                        [100%]

    ================================= FAILURES =================================
    _______________________________ test_num[17] _______________________________

    i = 17

        @pytest.mark.parametrize("i", range(50))
        def test_num(i):
            if i in (17, 25):
    >           pytest.fail("bad luck")
    E           Failed: bad luck

    test_50.py:7: Failed
    _______________________________ test_num[25] _______________________________

    i = 25

        @pytest.mark.parametrize("i", range(50))
        def test_num(i):
            if i in (17, 25):
    >           pytest.fail("bad luck")
    E           Failed: bad luck

    test_50.py:7: Failed
    ========================= short test summary info ==========================
    FAILED test_50.py::test_num[17] - Failed: bad luck
    FAILED test_50.py::test_num[25] - Failed: bad luck
    ============================ 2 failed in 0.12s =============================

You have run only the two failing tests from the last run, while the 48 passing
tests have not been run ("deselected").

Now, if you run with the :option:`--ff` option, all tests will be run but the first
previous failures will be executed first (as can be seen from the series
of ``FF`` and dots):

.. code-block:: pytest

    $ pytest --ff
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 50 items
    run-last-failure: rerun previous 2 failures first

    test_50.py FF................................................        [100%]

    ================================= FAILURES =================================
    _______________________________ test_num[17] _______________________________

    i = 17

        @pytest.mark.parametrize("i", range(50))
        def test_num(i):
            if i in (17, 25):
    >           pytest.fail("bad luck")
    E           Failed: bad luck

    test_50.py:7: Failed
    _______________________________ test_num[25] _______________________________

    i = 25

        @pytest.mark.parametrize("i", range(50))
        def test_num(i):
            if i in (17, 25):
    >           pytest.fail("bad luck")
    E           Failed: bad luck

    test_50.py:7: Failed
    ========================= short test summary info ==========================
    FAILED test_50.py::test_num[17] - Failed: bad luck
    FAILED test_50.py::test_num[25] - Failed: bad luck
    ======================= 2 failed, 48 passed in 0.12s =======================

.. _`config.cache`:

New :option:`--nf, --new-first <--nf>` option: run new tests first followed by the rest
of the tests, in both cases tests are also sorted by the file modified time,
with more recent files coming first.

Behavior when no tests failed in the last run
---------------------------------------------

The :option:`--lfnf, --last-failed-no-failures <--lfnf>` option governs the behavior of :option:`--last-failed`.
Determines whether to execute tests when there are no previously (known)
failures or when no cached ``lastfailed`` data was found.

There are two options:

* ``all``:  when there are no known test failures, runs all tests (the full test suite). This is the default.
* ``none``: when there are no known test failures, just emits a message stating this and exit successfully.

Example:

.. code-block:: bash

    pytest --last-failed --last-failed-no-failures all    # runs the full test suite (default behavior)
    pytest --last-failed --last-failed-no-failures none   # runs no tests and exits successfully

The new config.cache object
--------------------------------

.. regendoc:wipe

Plugins or conftest.py support code can get a cached value using the
pytest ``config`` object.  Here is a basic example plugin which
implements a :ref:`fixture <fixture>` which reuses previously created state
across pytest invocations:

.. code-block:: python

    # content of test_caching.py
    import pytest


    def expensive_computation():
        print("running expensive computation...")


    @pytest.fixture
    def mydata(pytestconfig):
        cache = getattr(pytestconfig, "cache", None)
        if cache is None:
            # pytestconfig not having the cache attribute means the
            # cache plugin is disabled.
            expensive_computation()
            return 42

        val = cache.get("example/value", None)
        if val is None:
            expensive_computation()
            val = 42
            cache.set("example/value", val)
        return val


    def test_function(mydata):
        assert mydata == 23

If you run this command for the first time, you can see the print statement:

.. code-block:: pytest

    $ pytest -q
    F                                                                    [100%]
    ================================= FAILURES =================================
    ______________________________ test_function _______________________________

    mydata = 42

        def test_function(mydata):
    >       assert mydata == 23
    E       assert 42 == 23

    test_caching.py:26: AssertionError
    -------------------------- Captured stdout setup ---------------------------
    running expensive computation...
    ========================= short test summary info ==========================
    FAILED test_caching.py::test_function - assert 42 == 23
    1 failed in 0.12s

If you run it a second time, the value will be retrieved from
the cache and nothing will be printed:

.. code-block:: pytest

    $ pytest -q
    F                                                                    [100%]
    ================================= FAILURES =================================
    ______________________________ test_function _______________________________

    mydata = 42

        def test_function(mydata):
    >       assert mydata == 23
    E       assert 42 == 23

    test_caching.py:26: AssertionError
    ========================= short test summary info ==========================
    FAILED test_caching.py::test_function - assert 42 == 23
    1 failed in 0.12s

See the :fixture:`config.cache fixture <cache>` for more details.


Inspecting Cache content
------------------------

You can always peek at the content of the cache using the
:option:`--cache-show` command line option:

.. code-block:: pytest

    $ pytest --cache-show
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    cachedir: /home/sweet/project/.pytest_cache
    --------------------------- cache values for '*' ---------------------------
    cache/lastfailed contains:
      {'test_caching.py::test_function': True}
    cache/nodeids contains:
      ['test_caching.py::test_function']
    example/value contains:
      42

    ========================== no tests ran in 0.12s ===========================

:option:`--cache-show` takes an optional argument to specify a glob pattern for
filtering:

.. code-block:: pytest

    $ pytest --cache-show example/*
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    cachedir: /home/sweet/project/.pytest_cache
    ----------------------- cache values for 'example/*' -----------------------
    example/value contains:
      42

    ========================== no tests ran in 0.12s ===========================

Clearing Cache content
----------------------

You can instruct pytest to clear all cache files and values
by adding the :option:`--cache-clear` option like this:

.. code-block:: bash

    pytest --cache-clear

This is recommended for invocations from Continuous Integration
servers where isolation and correctness is more important
than speed.


.. _cache stepwise:

Stepwise
--------

As an alternative to :option:`--lf` :option:`-x`, especially for cases where you expect a large part of the test suite will fail, :option:`--sw, --stepwise <--sw>` allows you to fix them one at a time. The test suite will run until the first failure and then stop. At the next invocation, tests will continue from the last failing test and then run until the next failing test. You may use the :option:`--stepwise-skip` option to ignore one failing test and stop the test execution on the second failing test instead. This is useful if you get stuck on a failing test and just want to ignore it until later.  Providing ``--stepwise-skip`` will also enable ``--stepwise`` implicitly.

# How to handle test failures
Source: https://docs.pytest.org/en/stable/how-to/failures.html

.. _how-to-handle-failures:

How to handle test failures
=============================

.. _maxfail:

Stopping after the first (or N) failures
---------------------------------------------------

To stop the testing process after the first (N) failures:

.. code-block:: bash

    pytest -x           # stop after first failure
    pytest --maxfail=2  # stop after two failures


.. _pdb-option:

Using :doc:`python:library/pdb` with pytest
-------------------------------------------

Dropping to :doc:`pdb <python:library/pdb>` on failures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python comes with a builtin Python debugger called :doc:`pdb <python:library/pdb>`.  ``pytest``
allows one to drop into the :doc:`pdb <python:library/pdb>` prompt via a command line option:

.. code-block:: bash

    pytest --pdb

This will invoke the Python debugger on every failure (or KeyboardInterrupt).
Often you might only want to do this for the first failing test to understand
a certain failure situation:

.. code-block:: bash

    pytest -x --pdb   # drop to PDB on first failure, then end test session
    pytest --pdb --maxfail=3  # drop to PDB for first three failures

Note that on any failure the exception information is stored on
``sys.last_value``, ``sys.last_type`` and ``sys.last_traceback``. In
interactive use, this allows one to drop into postmortem debugging with
any debug tool. One can also manually access the exception information,
for example::

    >>> import sys
    >>> sys.last_traceback.tb_lineno
    42
    >>> sys.last_value
    AssertionError('assert result == "ok"',)


.. _trace-option:

Dropping to :doc:`pdb <python:library/pdb>` at the start of a test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pytest`` allows one to drop into the :doc:`pdb <python:library/pdb>` prompt immediately at the start of each test via a command line option:

.. code-block:: bash

    pytest --trace

This will invoke the Python debugger at the start of every test.

.. _breakpoints:

Setting breakpoints
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. versionadded: 2.4.0

To set a breakpoint in your code use the native Python ``import pdb;pdb.set_trace()`` call
in your code and pytest automatically disables its output capture for that test:

* Output capture in other tests is not affected.
* Any prior test output that has already been captured and will be processed as
  such.
* Output capture gets resumed when ending the debugger session (via the
  ``continue`` command).


.. _`breakpoint-builtin`:

Using the builtin breakpoint function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python 3.7 introduces a builtin ``breakpoint()`` function.
Pytest supports the use of ``breakpoint()`` with the following behaviours:

 - When ``breakpoint()`` is called and ``PYTHONBREAKPOINT`` is set to the default value, pytest will use the custom internal PDB trace UI instead of the system default ``Pdb``.
 - When tests are complete, the system will default back to the system ``Pdb`` trace UI.
 - With :option:`--pdb` passed to pytest, the custom internal Pdb trace UI is used with both ``breakpoint()`` and failed tests/unhandled exceptions.
 - :option:`--pdbcls` can be used to specify a custom debugger class.


.. _faulthandler:

Fault Handler
-------------

.. versionadded:: 5.0

The :mod:`faulthandler` standard module
can be used to dump Python tracebacks on a segfault or after a timeout.

The module is automatically enabled for pytest runs, unless the ``-p no:faulthandler`` is given
on the command-line.

Also the :confval:`faulthandler_timeout=X<faulthandler_timeout>` configuration option can be used
to dump the traceback of all threads if a test takes longer than ``X``
seconds to finish.

.. note::

    This functionality has been integrated from the external
    `pytest-faulthandler <https://github.com/pytest-dev/pytest-faulthandler>`__ plugin, with two
    small differences:

    * To disable it, use ``-p no:faulthandler`` instead of ``--no-faulthandler``: the former
      can be used with any plugin, so it saves one option.

    * The ``--faulthandler-timeout`` command-line option has become the
      :confval:`faulthandler_timeout` configuration option. It can still be configured from
      the command-line using ``-o faulthandler_timeout=X``.


.. _unraisable:

Warning about unraisable exceptions and unhandled thread exceptions
-------------------------------------------------------------------

.. versionadded:: 6.2

Unhandled exceptions are exceptions that are raised in a situation in which
they cannot propagate to a caller. The most common case is an exception raised
in a :meth:`__del__ <object.__del__>` implementation.

Unhandled thread exceptions are exceptions raised in a :class:`~threading.Thread`
but not handled, causing the thread to terminate uncleanly.

Both types of exceptions are normally considered bugs, but may go unnoticed
because they don't cause the program itself to crash. Pytest detects these
conditions and issues a warning that is visible in the test run summary.

The plugins are automatically enabled for pytest runs, unless the
``-p no:unraisableexception`` (for unraisable exceptions) and
``-p no:threadexception`` (for thread exceptions) options are given on the
command-line.

The warnings may be silenced selectively using the :ref:`pytest.mark.filterwarnings ref`
mark. The warning categories are :class:`pytest.PytestUnraisableExceptionWarning` and
:class:`pytest.PytestUnhandledThreadExceptionWarning`.

# Managing pytest's output
Source: https://docs.pytest.org/en/stable/how-to/output.html

.. _how-to-manage-output:

Managing pytest's output
=========================

.. _how-to-modifying-python-tb-printing:

Modifying Python traceback printing
--------------------------------------------------

Examples for modifying traceback printing:

.. code-block:: bash

    pytest --showlocals     # show local variables in tracebacks
    pytest -l               # show local variables (shortcut)
    pytest --no-showlocals  # hide local variables (if addopts enables them)

    pytest --capture=fd  # default, capture at the file descriptor level
    pytest --capture=sys # capture at the sys level
    pytest --capture=no  # don't capture
    pytest -s            # don't capture (shortcut)
    pytest --capture=tee-sys # capture to logs but also output to sys level streams

    pytest --tb=auto    # (default) 'long' tracebacks for the first and last
                         # entry, but 'short' style for the other entries
    pytest --tb=long    # exhaustive, informative traceback formatting
    pytest --tb=short   # shorter traceback format
    pytest --tb=line    # only one line per failure
    pytest --tb=native  # Python standard library formatting
    pytest --tb=no      # no traceback at all

The :option:`--full-trace` causes very long traces to be printed on error (longer
than :option:`--tb=long`). It also ensures that a stack trace is printed on
**KeyboardInterrupt** (Ctrl+C).
This is very useful if the tests are taking too long and you interrupt them
with Ctrl+C to find out where the tests are *hanging*. By default no output
will be shown (because KeyboardInterrupt is caught by pytest). By using this
option you make sure a trace is shown.


Verbosity
--------------------------------------------------

Examples for modifying printing verbosity:

.. code-block:: bash

    pytest --quiet          # quiet - less verbose - mode
    pytest -q               # quiet - less verbose - mode (shortcut)
    pytest -v               # increase verbosity, display individual test names
    pytest -vv              # more verbose, display more details from the test output
    pytest -vvv             # not a standard , but may be used for even more detail in certain setups

The :option:`-v` flag controls the verbosity of pytest output in various aspects: test session progress, assertion
details when tests fail, fixtures details with :option:`--fixtures`, etc.

.. regendoc:wipe

Consider this simple file:

.. code-block:: python

    # content of test_verbosity_example.py
    def test_ok():
        pass


    def test_words_fail():
        fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
        fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
        assert fruits1 == fruits2


    def test_numbers_fail():
        number_to_text1 = {str(x): x for x in range(5)}
        number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
        assert number_to_text1 == number_to_text2


    def test_long_text_fail():
        long_text = "Lorem ipsum dolor sit amet " * 10
        assert "hello world" in long_text

Executing pytest normally gives us this output (we are skipping the header to focus on the rest):

.. code-block:: pytest

    $ pytest --no-header
    =========================== test session starts ============================
    collected 4 items

    test_verbosity_example.py .FFF                                       [100%]

    ================================= FAILURES =================================
    _____________________________ test_words_fail ______________________________

        def test_words_fail():
            fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
            fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
    >       assert fruits1 == fruits2
    E       AssertionError: assert ['banana', 'a...elon', 'kiwi'] == ['banana', 'a...elon', 'kiwi']
    E
    E         At index 2 diff: 'grapes' != 'orange'
    E         Use -v to get more diff

    test_verbosity_example.py:8: AssertionError
    ____________________________ test_numbers_fail _____________________________

        def test_numbers_fail():
            number_to_text1 = {str(x): x for x in range(5)}
            number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
    >       assert number_to_text1 == number_to_text2
    E       AssertionError: assert {'0': 0, '1':..., '3': 3, ...} == {'0': 0, '10'...'30': 30, ...}
    E
    E         Omitting 1 identical items, use -vv to show
    E         Left contains 4 more items:
    E         {'1': 1, '2': 2, '3': 3, '4': 4}
    E         Right contains 4 more items:
    E         {'10': 10, '20': 20, '30': 30, '40': 40}
    E         Use -v to get more diff

    test_verbosity_example.py:14: AssertionError
    ___________________________ test_long_text_fail ____________________________

        def test_long_text_fail():
            long_text = "Lorem ipsum dolor sit amet " * 10
    >       assert "hello world" in long_text
    E       AssertionError: assert 'hello world' in 'Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ips... sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet '

    test_verbosity_example.py:19: AssertionError
    ========================= short test summary info ==========================
    FAILED test_verbosity_example.py::test_words_fail - AssertionError: asser...
    FAILED test_verbosity_example.py::test_numbers_fail - AssertionError: ass...
    FAILED test_verbosity_example.py::test_long_text_fail - AssertionError: a...
    ======================= 3 failed, 1 passed in 0.12s ========================

Notice that:

* Each test inside the file is shown by a single character in the output: ``.`` for passing, ``F`` for failure.
* ``test_words_fail`` failed, and we are shown a short summary indicating the index 2 of the two lists differ.
* ``test_numbers_fail`` failed, and we are shown a summary of left/right differences on dictionary items. Identical items are omitted.
* ``test_long_text_fail`` failed, and the right hand side of the ``in`` statement is truncated using ``...```
  because it is longer than an internal threshold (240 characters currently).

Now we can increase pytest's verbosity:

.. code-block:: pytest

    $ pytest --no-header -v
    =========================== test session starts ============================
    collecting ... collected 4 items

    test_verbosity_example.py::test_ok PASSED                            [ 25%]
    test_verbosity_example.py::test_words_fail FAILED                    [ 50%]
    test_verbosity_example.py::test_numbers_fail FAILED                  [ 75%]
    test_verbosity_example.py::test_long_text_fail FAILED                [100%]

    ================================= FAILURES =================================
    _____________________________ test_words_fail ______________________________

        def test_words_fail():
            fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
            fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
    >       assert fruits1 == fruits2
    E       AssertionError: assert ['banana', 'a...elon', 'kiwi'] == ['banana', 'a...elon', 'kiwi']
    E
    E         At index 2 diff: 'grapes' != 'orange'
    E
    E         Full diff:
    E           [
    E               'banana',
    E               'apple',...
    E
    E         ...Full output truncated (7 lines hidden), use '-vv' to show

    test_verbosity_example.py:8: AssertionError
    ____________________________ test_numbers_fail _____________________________

        def test_numbers_fail():
            number_to_text1 = {str(x): x for x in range(5)}
            number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
    >       assert number_to_text1 == number_to_text2
    E       AssertionError: assert {'0': 0, '1':..., '3': 3, ...} == {'0': 0, '10'...'30': 30, ...}
    E
    E         Omitting 1 identical items, use -vv to show
    E         Left contains 4 more items:
    E         {'1': 1, '2': 2, '3': 3, '4': 4}
    E         Right contains 4 more items:
    E         {'10': 10, '20': 20, '30': 30, '40': 40}
    E         ...
    E
    E         ...Full output truncated (16 lines hidden), use '-vv' to show

    test_verbosity_example.py:14: AssertionError
    ___________________________ test_long_text_fail ____________________________

        def test_long_text_fail():
            long_text = "Lorem ipsum dolor sit amet " * 10
    >       assert "hello world" in long_text
    E       AssertionError: assert 'hello world' in 'Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet '

    test_verbosity_example.py:19: AssertionError
    ========================= short test summary info ==========================
    FAILED test_verbosity_example.py::test_words_fail - AssertionError: asser...
    FAILED test_verbosity_example.py::test_numbers_fail - AssertionError: ass...
    FAILED test_verbosity_example.py::test_long_text_fail - AssertionError: a...
    ======================= 3 failed, 1 passed in 0.12s ========================

Notice now that:

* Each test inside the file gets its own line in the output.
* ``test_words_fail`` now shows the two failing lists in full, in addition to which index differs.
* ``test_numbers_fail`` now shows a text diff of the two dictionaries, truncated.
* ``test_long_text_fail`` no longer truncates the right hand side of the ``in`` statement, because the internal
  threshold for truncation is larger now (2400 characters currently).

Now if we increase verbosity even more:

.. code-block:: pytest

    $ pytest --no-header -vv
    =========================== test session starts ============================
    collecting ... collected 4 items

    test_verbosity_example.py::test_ok PASSED                            [ 25%]
    test_verbosity_example.py::test_words_fail FAILED                    [ 50%]
    test_verbosity_example.py::test_numbers_fail FAILED                  [ 75%]
    test_verbosity_example.py::test_long_text_fail FAILED                [100%]

    ================================= FAILURES =================================
    _____________________________ test_words_fail ______________________________

        def test_words_fail():
            fruits1 = ["banana", "apple", "grapes", "melon", "kiwi"]
            fruits2 = ["banana", "apple", "orange", "melon", "kiwi"]
    >       assert fruits1 == fruits2
    E       AssertionError: assert ['banana', 'apple', 'grapes', 'melon', 'kiwi'] == ['banana', 'apple', 'orange', 'melon', 'kiwi']
    E
    E         At index 2 diff: 'grapes' != 'orange'
    E
    E         Full diff:
    E           [
    E               'banana',
    E               'apple',
    E         -     'orange',
    E         ?      ^  ^^
    E         +     'grapes',
    E         ?      ^  ^ +
    E               'melon',
    E               'kiwi',
    E           ]

    test_verbosity_example.py:8: AssertionError
    ____________________________ test_numbers_fail _____________________________

        def test_numbers_fail():
            number_to_text1 = {str(x): x for x in range(5)}
            number_to_text2 = {str(x * 10): x * 10 for x in range(5)}
    >       assert number_to_text1 == number_to_text2
    E       AssertionError: assert {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4} == {'0': 0, '10': 10, '20': 20, '30': 30, '40': 40}
    E
    E         Common items:
    E         {'0': 0}
    E         Left contains 4 more items:
    E         {'1': 1, '2': 2, '3': 3, '4': 4}
    E         Right contains 4 more items:
    E         {'10': 10, '20': 20, '30': 30, '40': 40}
    E
    E         Full diff:
    E           {
    E               '0': 0,
    E         -     '10': 10,
    E         ?       -    -
    E         +     '1': 1,
    E         -     '20': 20,
    E         ?       -    -
    E         +     '2': 2,
    E         -     '30': 30,
    E         ?       -    -
    E         +     '3': 3,
    E         -     '40': 40,
    E         ?       -    -
    E         +     '4': 4,
    E           }

    test_verbosity_example.py:14: AssertionError
    ___________________________ test_long_text_fail ____________________________

        def test_long_text_fail():
            long_text = "Lorem ipsum dolor sit amet " * 10
    >       assert "hello world" in long_text
    E       AssertionError: assert 'hello world' in 'Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet '

    test_verbosity_example.py:19: AssertionError
    ========================= short test summary info ==========================
    FAILED test_verbosity_example.py::test_words_fail - AssertionError: assert ['banana', 'apple', 'grapes', 'melon', 'kiwi'] == ['banana', 'apple', 'orange', 'melon', 'kiwi']

      At index 2 diff: 'grapes' != 'orange'

      Full diff:
        [
            'banana',
            'apple',
      -     'orange',
      ?      ^  ^^
      +     'grapes',
      ?      ^  ^ +
            'melon',
            'kiwi',
        ]
    FAILED test_verbosity_example.py::test_numbers_fail - AssertionError: assert {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4} == {'0': 0, '10': 10, '20': 20, '30': 30, '40': 40}

      Common items:
      {'0': 0}
      Left contains 4 more items:
      {'1': 1, '2': 2, '3': 3, '4': 4}
      Right contains 4 more items:
      {'10': 10, '20': 20, '30': 30, '40': 40}

      Full diff:
        {
            '0': 0,
      -     '10': 10,
      ?       -    -
      +     '1': 1,
      -     '20': 20,
      ?       -    -
      +     '2': 2,
      -     '30': 30,
      ?       -    -
      +     '3': 3,
      -     '40': 40,
      ?       -    -
      +     '4': 4,
        }
    FAILED test_verbosity_example.py::test_long_text_fail - AssertionError: assert 'hello world' in 'Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet '
    ======================= 3 failed, 1 passed in 0.12s ========================

Notice now that:

* Each test inside the file gets its own line in the output.
* ``test_words_fail`` gives the same output as before in this case.
* ``test_numbers_fail`` now shows a full text diff of the two dictionaries.
* ``test_long_text_fail`` also doesn't truncate on the right hand side as before, but now pytest won't truncate any
  text at all, regardless of its size.

Those were examples of how verbosity affects normal test session output, but verbosity also is used in other
situations, for example you are shown even fixtures that start with ``_`` if you use ``pytest --fixtures -v``.

Using higher verbosity levels (``-vvv``, ``-vvvv``, ...) is supported, but has no effect in pytest itself at the moment,
however some plugins might make use of higher verbosity.

.. _`pytest.fine_grained_verbosity`:

Fine-grained verbosity
~~~~~~~~~~~~~~~~~~~~~~

In addition to specifying the application wide verbosity level, it is possible to control specific aspects independently.
This is done by setting a verbosity level in the configuration file for the specific aspect of the output.

:confval:`verbosity_assertions`: Controls how verbose the assertion output should be when pytest is executed. Running
``pytest --no-header`` with a value of ``2`` would have the same output as the previous example, but each test inside
the file is shown by a single character in the output.

:confval:`assertion_text_diff_style`: Controls how pytest renders ``str == str`` failures.

  * ``ndiff`` (the default) outputs the differences using inline diff markers.
  * ``block`` prints string comparisons as separate ``Left:`` and ``Right:`` blocks, which can be easier to read when whitespace or indentation differences dominate.

  Note that it is possible to set this option (as any other configuration option) directly in the command line using ``-o assertion_text_diff_style=block``.

:confval:`verbosity_test_cases`: Controls how verbose the test execution output should be when pytest is executed.
Running ``pytest --no-header`` with a value of ``2`` would have the same output as the first verbosity example, but each
test inside the file gets its own line in the output.

.. _`pytest.detailed_failed_tests_usage`:

Producing a detailed summary report
--------------------------------------------------

The :option:`-r` flag can be used to display a "short test summary info" at the end of the test session,
making it easy in large test suites to get a clear picture of all failures, skips, xfails, etc.

It defaults to ``fE`` to list failures and errors.

.. regendoc:wipe

Example:

.. code-block:: python

    # content of test_example.py
    import pytest


    @pytest.fixture
    def error_fixture():
        assert 0


    def test_ok():
        print("ok")


    def test_fail():
        assert 0


    def test_error(error_fixture):
        pass


    def test_skip():
        pytest.skip("skipping this test")


    def test_xfail():
        pytest.xfail("xfailing this test")


    @pytest.mark.xfail(reason="always xfail")
    def test_xpass():
        pass


.. code-block:: pytest

    $ pytest -ra
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 6 items

    test_example.py .FEsxX                                               [100%]

    ================================== ERRORS ==================================
    _______________________ ERROR at setup of test_error _______________________

        @pytest.fixture
        def error_fixture():
    >       assert 0
    E       assert 0

    test_example.py:6: AssertionError
    ================================= FAILURES =================================
    ________________________________ test_fail _________________________________

        def test_fail():
    >       assert 0
    E       assert 0

    test_example.py:14: AssertionError
    ================================= XPASSES ==================================
    ========================= short test summary info ==========================
    SKIPPED [1] test_example.py:22: skipping this test
    XFAIL test_example.py::test_xfail - xfailing this test
    XPASS test_example.py::test_xpass - always xfail
    ERROR test_example.py::test_error - assert 0
    FAILED test_example.py::test_fail - assert 0
    == 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12s ===

The :option:`-r` options accepts a number of characters after it, with ``a`` used
above meaning "all except passes".

Here is the full list of available characters that can be used:

 - ``f`` - failed
 - ``E`` - error
 - ``s`` - skipped
 - ``x`` - xfailed
 - ``X`` - xpassed
 - ``p`` - passed
 - ``P`` - passed with output

Special characters for (de)selection of groups:

 - ``a`` - all except ``pP``
 - ``A`` - all
 - ``N`` - none, this can be used to display nothing (since ``fE`` is the default)

More than one character can be used, so for example to only see failed and skipped tests, you can execute:

.. code-block:: pytest

    $ pytest -rfs
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 6 items

    test_example.py .FEsxX                                               [100%]

    ================================== ERRORS ==================================
    _______________________ ERROR at setup of test_error _______________________

        @pytest.fixture
        def error_fixture():
    >       assert 0
    E       assert 0

    test_example.py:6: AssertionError
    ================================= FAILURES =================================
    ________________________________ test_fail _________________________________

        def test_fail():
    >       assert 0
    E       assert 0

    test_example.py:14: AssertionError
    ========================= short test summary info ==========================
    FAILED test_example.py::test_fail - assert 0
    SKIPPED [1] test_example.py:22: skipping this test
    == 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12s ===

Using ``p`` lists the passing tests, whilst ``P`` adds an extra section "PASSES" with those tests that passed but had
captured output:

.. code-block:: pytest

    $ pytest -rpP
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 6 items

    test_example.py .FEsxX                                               [100%]

    ================================== ERRORS ==================================
    _______________________ ERROR at setup of test_error _______________________

        @pytest.fixture
        def error_fixture():
    >       assert 0
    E       assert 0

    test_example.py:6: AssertionError
    ================================= FAILURES =================================
    ________________________________ test_fail _________________________________

        def test_fail():
    >       assert 0
    E       assert 0

    test_example.py:14: AssertionError
    ================================== PASSES ==================================
    _________________________________ test_ok __________________________________
    --------------------------- Captured stdout call ---------------------------
    ok
    ========================= short test summary info ==========================
    PASSED test_example.py::test_ok
    == 1 failed, 1 passed, 1 skipped, 1 xfailed, 1 xpassed, 1 error in 0.12s ===

.. note::

    By default, parametrized variants of skipped tests are grouped together if
    they share the same skip reason. You can use :option:`--no-fold-skipped` to print each skipped test separately.


.. _truncation-params:

Modifying truncation limits
--------------------------------------------------

.. versionadded: 8.4

Default truncation limits are 8 lines or 640 characters, whichever comes first.
To set custom truncation limits you can use the following configuration file options:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        truncation_limit_lines = 10
        truncation_limit_chars = 90

.. tab:: ini

    .. code-block:: ini

        [pytest]
        truncation_limit_lines = 10
        truncation_limit_chars = 90

That will cause pytest to truncate the assertions to 10 lines or 90 characters, whichever comes first.

Setting both :confval:`truncation_limit_lines` and :confval:`truncation_limit_chars` to ``0`` will disable the truncation.
However, setting only one of those values will disable one truncation mode, but will leave the other one intact.


Creating JUnitXML format files
----------------------------------------------------

To create result files which can be read by Jenkins_ or other Continuous
integration servers, use this invocation:

.. code-block:: bash

    pytest --junit-xml=path

to create an XML file at ``path``.



To set the name of the root test suite xml item, you can configure the ``junit_suite_name`` option in your config file:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        junit_suite_name = "my_suite"

.. tab:: ini

    .. code-block:: ini

        [pytest]
        junit_suite_name = my_suite

.. versionadded:: 4.0

JUnit XML specification seems to indicate that ``"time"`` attribute
should report total test execution times, including setup and teardown
(`1 <http://windyroad.com.au/dl/Open%20Source/JUnit.xsd>`_, `2
<https://www.ibm.com/support/knowledgecenter/en/SSQ2R2_14.1.0/com.ibm.rsar.analysis.codereview.cobol.doc/topics/cac_useresults_junit.html>`_).
It is the default pytest behavior. To report just call durations
instead, configure the ``junit_duration_report`` option like this:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        junit_duration_report = "call"

.. tab:: ini

    .. code-block:: ini

        [pytest]
        junit_duration_report = call

.. _record_property example:

record_property
~~~~~~~~~~~~~~~~~

If you want to log additional information for a test, you can use the
``record_property`` fixture:

.. code-block:: python

    def test_function(record_property):
        record_property("example_key", 1)
        assert True

This will add an extra property ``example_key="1"`` to the generated
``testcase`` tag:

.. code-block:: xml

    <testcase classname="test_function" file="test_function.py" line="0" name="test_function" time="0.0009">
      <properties>
        <property name="example_key" value="1" />
      </properties>
    </testcase>

Alternatively, you can integrate this functionality with custom markers:

.. code-block:: python

    # content of conftest.py


    def pytest_collection_modifyitems(session, config, items):
        for item in items:
            for marker in item.iter_markers(name="test_id"):
                test_id = marker.args[0]
                item.user_properties.append(("test_id", test_id))

And in your tests:

.. code-block:: python

    # content of test_function.py
    import pytest


    @pytest.mark.test_id(1501)
    def test_function():
        assert True

Will result in:

.. code-block:: xml

    <testcase classname="test_function" file="test_function.py" line="0" name="test_function" time="0.0009">
      <properties>
        <property name="test_id" value="1501" />
      </properties>
    </testcase>

.. warning::

    Please note that using this feature will break schema verifications for the latest JUnitXML schema.
    This might be a problem when used with some CI servers.


record_xml_attribute
~~~~~~~~~~~~~~~~~~~~~~~

To add an additional xml attribute to a testcase element, you can use
``record_xml_attribute`` fixture. This can also be used to override existing values:

.. code-block:: python

    def test_function(record_xml_attribute):
        record_xml_attribute("assertions", "REQ-1234")
        record_xml_attribute("classname", "custom_classname")
        print("hello world")
        assert True

Unlike ``record_property``, this will not add a new child element.
Instead, this will add an attribute ``assertions="REQ-1234"`` inside the generated
``testcase`` tag and override the default ``classname`` with ``"classname=custom_classname"``:

.. code-block:: xml

    <testcase classname="custom_classname" file="test_function.py" line="0" name="test_function" time="0.003" assertions="REQ-1234">
        <system-out>
            hello world
        </system-out>
    </testcase>

.. warning::

    ``record_xml_attribute`` is an experimental feature, and its interface might be replaced
    by something more powerful and general in future versions. The
    functionality per-se will be kept, however.

    Using this over ``record_xml_property`` can help when using ci tools to parse the xml report.
    However, some parsers are quite strict about the elements and attributes that are allowed.
    Many tools use an xsd schema (like the example below) to validate incoming xml.
    Make sure you are using attribute names that are allowed by your parser.

    Below is the Scheme used by Jenkins to validate the XML report:

    .. code-block:: xml

        <xs:element name="testcase">
            <xs:complexType>
                <xs:sequence>
                    <xs:element ref="skipped" minOccurs="0" maxOccurs="1"/>
                    <xs:element ref="error" minOccurs="0" maxOccurs="unbounded"/>
                    <xs:element ref="failure" minOccurs="0" maxOccurs="unbounded"/>
                    <xs:element ref="system-out" minOccurs="0" maxOccurs="unbounded"/>
                    <xs:element ref="system-err" minOccurs="0" maxOccurs="unbounded"/>
                </xs:sequence>
                <xs:attribute name="name" type="xs:string" use="required"/>
                <xs:attribute name="assertions" type="xs:string" use="optional"/>
                <xs:attribute name="time" type="xs:string" use="optional"/>
                <xs:attribute name="classname" type="xs:string" use="optional"/>
                <xs:attribute name="status" type="xs:string" use="optional"/>
            </xs:complexType>
        </xs:element>

.. warning::

    Please note that using this feature will break schema verifications for the latest JUnitXML schema.
    This might be a problem when used with some CI servers.

.. _record_testsuite_property example:

record_testsuite_property
^^^^^^^^^^^^^^^^^^^^^^^^^

.. versionadded:: 4.5

If you want to add a properties node at the test-suite level, which may contain properties
that are relevant to all tests, you can use the ``record_testsuite_property`` session-scoped fixture:

The ``record_testsuite_property`` session-scoped fixture can be used to add properties relevant
to all tests.

.. code-block:: python

    import pytest


    @pytest.fixture(scope="session", autouse=True)
    def log_global_env_facts(record_testsuite_property):
        record_testsuite_property("ARCH", "PPC")
        record_testsuite_property("STORAGE_TYPE", "CEPH")


    class TestMe:
        def test_foo(self):
            assert True

The fixture is a callable which receives ``name`` and ``value`` of a ``<property>`` tag
added at the test-suite level of the generated xml:

.. code-block:: xml

    <testsuite errors="0" failures="0" name="pytest" skipped="0" tests="1" time="0.006">
      <properties>
        <property name="ARCH" value="PPC"/>
        <property name="STORAGE_TYPE" value="CEPH"/>
      </properties>
      <testcase classname="test_me.TestMe" file="test_me.py" line="16" name="test_foo" time="0.000243663787842"/>
    </testsuite>

``name`` must be a string, ``value`` will be converted to a string and properly xml-escaped.

The generated XML is compatible with the latest ``xunit`` standard, contrary to `record_property`_
and `record_xml_attribute`_.


Sending test report to an online pastebin service
--------------------------------------------------

**Creating a URL for each test failure**:

.. code-block:: bash

    pytest --pastebin=failed

This will submit test run information to a remote Paste service and
provide a URL for each failure.  You may select tests as usual or add
for example :option:`-x` if you only want to send one particular failure.

**Creating a URL for a whole test session log**:

.. code-block:: bash

    pytest --pastebin=all

Currently only pasting to the https://bpaste.net/ service is implemented.

.. versionchanged:: 5.2

If creating the URL fails for any reason, a warning is generated instead of failing the
entire test suite.

.. _jenkins: https://jenkins-ci.org

# How to manage logging
Source: https://docs.pytest.org/en/stable/how-to/logging.html

.. _logging:

How to manage logging
---------------------

pytest captures log messages of level ``WARNING`` or above automatically and displays them in their own section
for each failed test in the same manner as captured stdout and stderr.

Running without options:

.. code-block:: bash

    pytest

Shows failed tests like so:

.. code-block:: pytest

    ----------------------- Captured stdlog call ----------------------
    test_reporting.py    26 WARNING  text going to logger
    ----------------------- Captured stdout call ----------------------
    text going to stdout
    ----------------------- Captured stderr call ----------------------
    text going to stderr
    ==================== 2 failed in 0.02 seconds =====================

By default each captured log message shows the module, line number, log level
and message.

If desired the log and date format can be specified to
anything that the logging module supports by passing specific formatting options:

.. code-block:: bash

    pytest --log-format="%(asctime)s %(levelname)s %(message)s" \
            --log-date-format="%Y-%m-%d %H:%M:%S"

Shows failed tests like so:

.. code-block:: pytest

    ----------------------- Captured stdlog call ----------------------
    2010-04-10 14:48:44 WARNING text going to logger
    ----------------------- Captured stdout call ----------------------
    text going to stdout
    ----------------------- Captured stderr call ----------------------
    text going to stderr
    ==================== 2 failed in 0.02 seconds =====================

These options can also be customized through a configuration file:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        log_format = "%(asctime)s %(levelname)s %(message)s"
        log_date_format = "%Y-%m-%d %H:%M:%S"

.. tab:: ini

    .. code-block:: ini

        [pytest]
        log_format = %(asctime)s %(levelname)s %(message)s
        log_date_format = %Y-%m-%d %H:%M:%S

Specific loggers can be disabled via :option:`--log-disable={logger_name}`.
This argument can be passed multiple times:

.. code-block:: bash

    pytest --log-disable=main --log-disable=testing

Further it is possible to disable reporting of captured content (stdout,
stderr and logs) on failed tests completely with:

.. code-block:: bash

    pytest --show-capture=no


caplog fixture
^^^^^^^^^^^^^^

Inside tests it is possible to change the log level for the captured log
messages.  This is supported by the ``caplog`` fixture:

.. code-block:: python

    def test_foo(caplog):
        caplog.set_level(logging.INFO)

By default the level is set on the root logger,
however as a convenience it is also possible to set the log level of any
logger:

.. code-block:: python

    def test_foo(caplog):
        caplog.set_level(logging.CRITICAL, logger="root.baz")

The log levels set are restored automatically at the end of the test.

It is also possible to use a context manager to temporarily change the log
level inside a ``with`` block:

.. code-block:: python

    def test_bar(caplog):
        with caplog.at_level(logging.INFO):
            pass

Again, by default the level of the root logger is affected but the level of any
logger can be changed instead with:

.. code-block:: python

    def test_bar(caplog):
        with caplog.at_level(logging.CRITICAL, logger="root.baz"):
            pass

Lastly all the logs sent to the logger during the test run are made available on
the fixture in the form of both the ``logging.LogRecord`` instances and the final log text.
This is useful for when you want to assert on the contents of a message:

.. code-block:: python

    def test_baz(caplog):
        func_under_test()
        for record in caplog.records:
            assert record.levelname != "CRITICAL"
        assert "wally" not in caplog.text

For all the available attributes of the log records see the
``logging.LogRecord`` class.

You can also resort to ``record_tuples`` if all you want to do is to ensure,
that certain messages have been logged under a given logger name with a given
severity and message:

.. code-block:: python

    def test_foo(caplog):
        logging.getLogger().info("boo %s", "arg")

        assert caplog.record_tuples == [("root", logging.INFO, "boo arg")]

You can call ``caplog.clear()`` to reset the captured log records in a test:

.. code-block:: python

    def test_something_with_clearing_records(caplog):
        some_method_that_creates_log_records()
        caplog.clear()
        your_test_method()
        assert ["Foo"] == [rec.message for rec in caplog.records]


The ``caplog.records`` attribute contains records from the current stage only, so
inside the ``setup`` phase it contains only setup logs, same with the ``call`` and
``teardown`` phases.

To access logs from other stages, use the ``caplog.get_records(when)`` method. As an example,
if you want to make sure that tests which use a certain fixture never log any warnings, you can inspect
the records for the ``setup`` and ``call`` stages during teardown like so:

.. code-block:: python

    @pytest.fixture
    def window(caplog):
        window = create_window()
        yield window
        for when in ("setup", "call"):
            messages = [
                x.message for x in caplog.get_records(when) if x.levelno == logging.WARNING
            ]
            if messages:
                pytest.fail(f"warning messages encountered during testing: {messages}")



The full API is available at :class:`pytest.LogCaptureFixture`.

.. warning::

    The ``caplog`` fixture adds a handler to the root logger to capture logs. If the root logger is
    modified during a test, for example with ``logging.config.dictConfig``, this handler may be
    removed and cause no logs to be captured. To avoid this, ensure that any root logger configuration
    only adds to the existing handlers.


.. _live_logs:

Live Logs
^^^^^^^^^

By setting the :confval:`log_cli` configuration option to ``true``, pytest will output
logging records as they are emitted directly into the console.

You can specify the logging level for which log records with equal or higher
level are printed to the console by passing :option:`--log-cli-level`. This setting
accepts the logging level names or numeric values as seen in
:ref:`logging's documentation <python:levels>`.

Additionally, you can also specify :option:`--log-cli-format` and
:option:`--log-cli-date-format` which mirror and default to :option:`--log-format` and
:option:`--log-date-format` if not provided, but are applied only to the console
logging handler.

All of the CLI log options can also be set in the configuration file. The
option names are:

* :confval:`log_cli_level`
* :confval:`log_cli_format`
* :confval:`log_cli_date_format`

If you need to record the whole test suite logging calls to a file, you can pass
:option:`--log-file=/path/to/log/file`. This log file is opened in write mode by default, which
means that it will be overwritten at each test session.
If you'd like the file opened in append mode instead, then you can pass :option:`--log-file-mode=a`.
Note that relative paths for the log-file location, whether passed on the CLI or declared in a
config file, are always resolved relative to the current working directory.

You can also specify the logging level for the log file by passing
:option:`--log-file-level`. This setting accepts the logging level names or numeric
values as seen in :ref:`logging's documentation <python:levels>`.

Additionally, you can also specify :option:`--log-file-format` and
:option:`--log-file-date-format` which are equal to ``--log-format`` and
:option:`--log-date-format` but are applied to the log file logging handler.

All of the log file options can also be set in the configuration file. The
option names are:

* :confval:`log_file`
* :confval:`log_file_mode`
* :confval:`log_file_level`
* :confval:`log_file_format`
* :confval:`log_file_date_format`

You can call ``set_log_path()`` to customize the log_file path dynamically. This functionality
is considered **experimental**. Note that ``set_log_path()`` respects the :confval:`log_file_mode` option.

.. _log_colors:

Customizing Colors
^^^^^^^^^^^^^^^^^^

Log levels are colored if colored terminal output is enabled. Changing
from default colors or putting color on custom log levels is supported
through ``add_color_level()``. Example:

.. code-block:: python

    @pytest.hookimpl(trylast=True)
    def pytest_configure(config):
        logging_plugin = config.pluginmanager.get_plugin("logging-plugin")

        # Change color on existing log level
        logging_plugin.log_cli_handler.formatter.add_color_level(logging.INFO, "cyan")

        # Add color to a custom log level (a custom log level `SPAM` is already set up)
        logging_plugin.log_cli_handler.formatter.add_color_level(logging.SPAM, "blue")
.. warning::

    This feature and its API are considered **experimental** and might change
    between releases without a deprecation notice.
.. _log_release_notes:

Release notes
^^^^^^^^^^^^^

This feature was introduced as a drop-in replacement for the
:pypi:`pytest-catchlog` plugin and they conflict
with each other. The backward compatibility API with ``pytest-capturelog``
has been dropped when this feature was introduced, so if for that reason you
still need ``pytest-catchlog`` you can disable the internal feature by
adding to your configuration file:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        addopts = ["-p", "no:logging"]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        addopts = -p no:logging


.. _log_changes_3_4:

Incompatible changes in pytest 3.4
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This feature was introduced in ``3.3`` and some **incompatible changes** have been
made in ``3.4`` after community feedback:

* Log levels are no longer changed unless explicitly requested by the :confval:`log_level` configuration
  or :option:`--log-level` command-line options. This allows users to configure logger objects themselves.
  Setting :confval:`log_level` will set the level that is captured globally so if a specific test requires
  a lower level than this, use the ``caplog.set_level()`` functionality otherwise that test will be prone to
  failure.
* :ref:`Live Logs <live_logs>` is now disabled by default and can be enabled setting the
  :confval:`log_cli` configuration option to ``true``. When enabled, the verbosity is increased so logging for each
  test is visible.
* :ref:`Live Logs <live_logs>` are now sent to ``sys.stdout`` and no longer require the :option:`-s` command-line option
  to work.

If you want to partially restore the logging behavior of version ``3.3``, you can add these options to your configuration
file:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        log_cli = true
        log_level = "NOTSET"

.. tab:: ini

    .. code-block:: ini

        [pytest]
        log_cli = true
        log_level = NOTSET

More details about the discussion that led to these changes can be read in :issue:`3013`.

# How to capture stdout/stderr output
Source: https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html

.. _`captures`:

How to capture stdout/stderr output
=========================================================

Pytest intercepts stdout and stderr as configured by the :option:`--capture=`
command-line argument or by using fixtures. The ``--capture=`` flag configures
reporting, whereas the fixtures offer more granular control and allow
inspection of output during testing. The reports can be customized with the
:option:`-r` flag.

Default stdout/stderr/stdin capturing behaviour
---------------------------------------------------------

During test execution any output sent to ``stdout`` and ``stderr`` is
captured.  If a test or a setup method fails its according captured
output will usually be shown along with the failure traceback. (This
behavior can be configured by the :option:`--show-capture` command-line option).

In addition, ``stdin`` is set to a "null" object which will
fail on attempts to read from it because it is rarely desired
to wait for interactive input when running automated tests.

By default capturing is done by intercepting writes to low level
file descriptors.  This allows capturing output from simple
print statements as well as output from a subprocess started by
a test.

.. _capture-method:

Setting capturing methods or disabling capturing
-------------------------------------------------

There are three ways in which ``pytest`` can perform capturing:

* ``fd`` (file descriptor) level capturing (default): All writes going to the
  operating system file descriptors 1 and 2 will be captured.

* ``sys`` level capturing: Only writes to Python files ``sys.stdout``
  and ``sys.stderr`` will be captured.  No capturing of writes to
  filedescriptors is performed.

* ``tee-sys`` capturing: Python writes to ``sys.stdout`` and ``sys.stderr``
  will be captured, however the writes will also be passed-through to
  the actual ``sys.stdout`` and ``sys.stderr``. This allows output to be
  'live printed' and captured for plugin use, such as junitxml (new in pytest 5.4).

.. _`disable capturing`:

You can influence output capturing mechanisms from the command line:

.. code-block:: bash

    pytest -s                  # disable all capturing
    pytest --capture=sys       # replace sys.stdout/stderr with in-mem files
    pytest --capture=fd        # also point filedescriptors 1 and 2 to temp file
    pytest --capture=tee-sys   # combines 'sys' and '-s', capturing sys.stdout/stderr
                               # and passing it along to the actual sys.stdout/stderr

.. _printdebugging:

Using print statements for debugging
---------------------------------------------------

One primary benefit of the default capturing of stdout/stderr output
is that you can use print statements for debugging:

.. code-block:: python

    # content of test_module.py


    def setup_function(function):
        print("setting up", function)


    def test_func1():
        assert True


    def test_func2():
        assert False

and running this module will show you precisely the output
of the failing function and hide the other one:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    test_module.py .F                                                    [100%]

    ================================= FAILURES =================================
    ________________________________ test_func2 ________________________________

        def test_func2():
    >       assert False
    E       assert False

    test_module.py:12: AssertionError
    -------------------------- Captured stdout setup ---------------------------
    setting up <function test_func2 at 0xdeadbeef0001>
    ========================= short test summary info ==========================
    FAILED test_module.py::test_func2 - assert False
    ======================= 1 failed, 1 passed in 0.12s ========================

.. _accessing-captured-output:

Accessing captured output from a test function
---------------------------------------------------

The :fixture:`capsys`, :fixture:`capteesys`, :fixture:`capsysbinary`, :fixture:`capfd`, and :fixture:`capfdbinary`
fixtures allow access to ``stdout``/``stderr`` output created during test execution.

Here is an example test function that performs some output related checks:

.. code-block:: python

    def test_myoutput(capsys):  # or use "capfd" for fd-level
        print("hello")
        sys.stderr.write("world\n")
        captured = capsys.readouterr()
        assert captured.out == "hello\n"
        assert captured.err == "world\n"
        print("next")
        captured = capsys.readouterr()
        assert captured.out == "next\n"

The ``readouterr()`` call snapshots the output so far -
and capturing will be continued.  After the test
function finishes the original streams will
be restored.  Using :fixture:`capsys` this way frees your
test from having to care about setting/resetting
output streams and also interacts well with pytest's
own per-test capturing.

The return value of ``readouterr()`` is a ``namedtuple`` with two attributes, ``out`` and ``err``.

If the code under test writes non-textual data (``bytes``), you can capture this using
the :fixture:`capsysbinary` fixture which instead returns ``bytes`` from
the ``readouterr`` method.

If you want to capture at the file descriptor level you can use
the :fixture:`capfd` fixture which offers the exact
same interface but allows to also capture output from
libraries or subprocesses that directly write to operating
system level output streams (FD1 and FD2). Similarly to :fixture:`capsysbinary`, :fixture:`capfdbinary` can be
used to capture ``bytes`` at the file descriptor level.


To temporarily disable capture within a test, the capture fixtures
have a ``disabled()`` method that can be used
as a context manager, disabling capture inside the ``with`` block:

.. code-block:: python

    def test_disabling_capturing(capsys):
        print("this output is captured")
        with capsys.disabled():
            print("output not captured, going directly to sys.stdout")
        print("this output is also captured")

.. note::

   When a capture fixture such as :fixture:`capsys` or :fixture:`capfd` is used,
   it takes precedence over the global capturing configuration set via
   command-line options such as ``-s`` or ``--capture=no``.

   This means that output produced within a test using a capture fixture will
   still be captured and available via ``readouterr()``, even if global capturing
   is disabled.

# How to capture warnings
Source: https://docs.pytest.org/en/stable/how-to/capture-warnings.html

.. _`warnings`:

How to capture warnings
=======================



Starting from version ``3.1``, pytest now automatically catches warnings during test execution
and displays them at the end of the session:

.. code-block:: python

    # content of test_show_warnings.py
    import warnings


    def api_v1():
        warnings.warn(UserWarning("api v1, should use functions from v2"))
        return 1


    def test_one():
        assert api_v1() == 1

Running pytest now produces this output:

.. code-block:: pytest

    $ pytest test_show_warnings.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_show_warnings.py .                                              [100%]

    ============================= warnings summary =============================
    test_show_warnings.py::test_one
      /home/sweet/project/test_show_warnings.py:5: UserWarning: api v1, should use functions from v2
        warnings.warn(UserWarning("api v1, should use functions from v2"))

    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    ======================= 1 passed, 1 warning in 0.12s =======================

.. _`controlling-warnings`:

Controlling warnings
--------------------

Similar to Python's `warning filter`_ and :option:`-W option <python:-W>` flag, pytest provides
its own ``-W`` flag to control which warnings are ignored, displayed, or turned into
errors. See the `warning filter`_ documentation for more
advanced use-cases.

.. _`warning filter`: https://docs.python.org/3/library/warnings.html#warning-filter

This code sample shows how to treat any ``UserWarning`` category class of warning
as an error:

.. code-block:: pytest

    $ pytest -q test_show_warnings.py -W error::UserWarning
    F                                                                    [100%]
    ================================= FAILURES =================================
    _________________________________ test_one _________________________________

        def test_one():
    >       assert api_v1() == 1
                   ^^^^^^^^

    test_show_warnings.py:10:
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

        def api_v1():
    >       warnings.warn(UserWarning("api v1, should use functions from v2"))
    E       UserWarning: api v1, should use functions from v2

    test_show_warnings.py:5: UserWarning
    ========================= short test summary info ==========================
    FAILED test_show_warnings.py::test_one - UserWarning: api v1, should use ...
    1 failed in 0.12s

The same option can be set in the configuration file using the
:confval:`filterwarnings` configuration option. For example, the configuration below will ignore all
user warnings and specific deprecation warnings matching a regex, but will transform
all other warnings into errors.

.. tab:: toml

    .. code-block:: toml

        [pytest]
        filterwarnings = [
            'error',
            'ignore::UserWarning',
            # Note the use of single quote below to denote "raw" strings in TOML.
            'ignore:function ham\(\) is deprecated:DeprecationWarning',
        ]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        filterwarnings =
            error
            ignore::UserWarning
            ignore:function ham\(\) is deprecated:DeprecationWarning


When a warning matches more than one option in the list, the action for the last matching option
is performed.


.. note::

    The ``-W`` flag and the :confval:`filterwarnings` configuration option use warning filters that are
    similar in structure, but each configuration option interprets its filter
    differently. For example, *message* in ``filterwarnings`` is a string containing a
    regular expression that the start of the warning message must match,
    case-insensitively, while *message* in ``-W`` is a literal string that the start of
    the warning message must contain (case-insensitively), ignoring any whitespace at
    the start or end of message. Consult the `warning filter`_ documentation for more
    details.


.. _`filterwarnings`:

``@pytest.mark.filterwarnings``
-------------------------------



You can use the :ref:`@pytest.mark.filterwarnings <pytest.mark.filterwarnings ref>` mark to add warning filters to specific test items,
allowing you to have finer control of which warnings should be captured at test, class or
even module level:

.. code-block:: python

    import warnings


    def api_v1():
        warnings.warn(UserWarning("api v1, should use functions from v2"))
        return 1


    @pytest.mark.filterwarnings("ignore:api v1")
    def test_one():
        assert api_v1() == 1


You can specify multiple filters with separate decorators:

.. code-block:: python

    # Ignore "api v1" warnings, but fail on all other warnings
    @pytest.mark.filterwarnings("ignore:api v1")
    @pytest.mark.filterwarnings("error")
    def test_one():
        assert api_v1() == 1

You can also pass multiple filters to a single mark by providing multiple arguments:

.. code-block:: python

    # Later arguments take precedence, matching warnings.filterwarnings behavior.
    @pytest.mark.filterwarnings("error", "ignore:api v1")
    def test_one():
        assert api_v1() == 1

.. important::

    Regarding decorator order and filter precedence:
    it's important to remember that decorators are evaluated in reverse order,
    so you have to list the warning filters in the reverse order
    compared to traditional :py:func:`warnings.filterwarnings` and :option:`-W option <python:-W>` usage.
    This means in practice that filters from earlier :ref:`@pytest.mark.filterwarnings <pytest.mark.filterwarnings ref>` decorators
    take precedence over filters from later decorators, as illustrated in the example above.


Filters applied using a mark take precedence over filters passed on the command line or configured
by the :confval:`filterwarnings` configuration option.

You may apply a filter to all tests of a class by using the :ref:`filterwarnings <pytest.mark.filterwarnings ref>` mark as a class
decorator or to all tests in a module by setting the :globalvar:`pytestmark` variable:

.. code-block:: python

    # turns all warnings into errors for this module
    pytestmark = pytest.mark.filterwarnings("error")


.. note::

    If you want to apply multiple filters
    (by assigning a list of :ref:`filterwarnings <pytest.mark.filterwarnings ref>` mark to :globalvar:`pytestmark`),
    you must use the traditional :py:func:`warnings.filterwarnings` ordering approach (later filters take precedence),
    which is the reverse of the decorator approach mentioned above.


*Credits go to Florian Schulze for the reference implementation in the* `pytest-warnings`_
*plugin.*

.. _`pytest-warnings`: https://github.com/fschulze/pytest-warnings

Setting a maximum number of warnings
-------------------------------------

.. versionadded:: 9.1

You can use the :option:`--max-warnings` command-line option to fail the test run
if the total number of warnings exceeds a given threshold:

.. code-block:: bash

    pytest --max-warnings=10

If all tests pass but the number of warnings exceeds the threshold, pytest will exit with code ``6``
(:class:`~pytest.ExitCode` ``MAX_WARNINGS_ERROR``). This is useful for gradually
ratcheting down warnings in a codebase.

Note that :confval:`filtered warnings <filterwarnings>` do not count toward this maximum total.

The threshold can also be set in the configuration file using :confval:`max_warnings`:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        max_warnings = 10

.. tab:: ini

    .. code-block:: ini

        [pytest]
        max_warnings = 10

.. note::

    If tests fail, the exit code will be ``1`` (:class:`~pytest.ExitCode` ``TESTS_FAILED``)
    regardless of the warning count. ``MAX_WARNINGS_ERROR`` is only reported when all tests pass
    but the warning threshold is exceeded.

Disabling warnings summary
--------------------------

Although not recommended, you can use the :option:`--disable-warnings` command-line option to suppress the
warning summary entirely from the test run output.

Disabling warning capture entirely
----------------------------------

This plugin is enabled by default but can be disabled entirely in your configuration file with:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        addopts = ["-p", "no:warnings"]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        addopts = -p no:warnings

Or passing ``-p no:warnings`` in the command-line. This might be useful if your test suite handles warnings
using an external system.


.. _`deprecation-warnings`:

DeprecationWarning and PendingDeprecationWarning
------------------------------------------------

By default pytest will display ``DeprecationWarning`` and ``PendingDeprecationWarning`` warnings from
user code and third-party libraries, as recommended by :pep:`565`.
This helps users keep their code modern and avoid breakages when deprecated warnings are effectively removed.

However, in the specific case where users capture any type of warnings in their test, either with
:func:`pytest.warns`, :func:`pytest.deprecated_call` or using the :fixture:`recwarn` fixture,
no warning will be displayed at all.

Sometimes it is useful to hide some specific deprecation warnings that happen in code that you have no control over
(such as third-party libraries), in which case you might use the warning filters options (configuration or marks) to ignore
those warnings.

For example:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        filterwarnings = [
            'ignore:.*U.*mode is deprecated:DeprecationWarning',
        ]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        filterwarnings =
            ignore:.*U.*mode is deprecated:DeprecationWarning


This will ignore all warnings of type ``DeprecationWarning`` where the start of the message matches
the regular expression ``".*U.*mode is deprecated"``.

See :ref:`@pytest.mark.filterwarnings <filterwarnings>` and
:ref:`Controlling warnings <controlling-warnings>` for more examples.

.. note::

    If warnings are configured at the interpreter level, using
    the :envvar:`python:PYTHONWARNINGS` environment variable or the
    ``-W`` command-line option, pytest will not configure any filters by default.

    Also pytest doesn't follow :pep:`565` suggestion of resetting all warning filters because
    it might break test suites that configure warning filters themselves
    by calling :func:`warnings.simplefilter` (see :issue:`2430` for an example of that).


.. _`ensuring a function triggers a deprecation warning`:

.. _ensuring_function_triggers:

Ensuring code triggers a deprecation warning
--------------------------------------------

You can also use :func:`pytest.deprecated_call` for checking
that a certain function call triggers a ``DeprecationWarning``, ``PendingDeprecationWarning`` or
``FutureWarning``:

.. code-block:: python

    import pytest


    def test_myfunction_deprecated():
        with pytest.deprecated_call():
            myfunction(17)

This test will fail if ``myfunction`` does not issue a deprecation warning
when called with a ``17`` argument.




.. _`asserting warnings`:

.. _assertwarnings:

.. _`asserting warnings with the warns function`:

.. _warns:

Asserting warnings with the warns function
------------------------------------------

You can check that code raises a particular warning using :func:`pytest.warns`,
which works in a similar manner to :ref:`raises <assertraises>` (except that
:ref:`raises <assertraises>` does not capture all exceptions, only the
``expected_exception``):

.. code-block:: python

    import warnings

    import pytest


    def test_warning():
        with pytest.warns(UserWarning):
            warnings.warn("my warning", UserWarning)

The test will fail if the warning in question is not raised. Use the keyword
argument ``match`` to assert that the warning matches a text or regex.
To match a literal string that may contain regular expression metacharacters like ``(`` or ``.``, the pattern can
first be escaped with ``re.escape``.

Some examples:

.. code-block:: pycon


    >>> with warns(UserWarning, match="must be 0 or None"):
    ...     warnings.warn("value must be 0 or None", UserWarning)
    ...

    >>> with warns(UserWarning, match=r"must be \d+$"):
    ...     warnings.warn("value must be 42", UserWarning)
    ...

    >>> with warns(UserWarning, match=r"must be \d+$"):
    ...     warnings.warn("this is not here", UserWarning)
    ...
    Traceback (most recent call last):
      ...
    Failed: Regex pattern did not match any of the 1 warnings emitted.
     Regex: ...
     Emitted warnings: ...UserWarning...

    >>> with warns(UserWarning, match=re.escape("issue with foo() func")):
    ...     warnings.warn("issue with foo() func")
    ...

The function also returns a list of all raised warnings (as
``warnings.WarningMessage`` objects), which you can query for
additional information:

.. code-block:: python

    with pytest.warns(RuntimeWarning) as record:
        warnings.warn("another warning", RuntimeWarning)

    # check that only one warning was raised
    assert len(record) == 1
    # check that the message matches
    assert record[0].message.args[0] == "another warning"

Alternatively, you can examine raised warnings in detail using the
:fixture:`recwarn` fixture (see :ref:`below <recwarn>`).


The :fixture:`recwarn` fixture automatically ensures to reset the warnings
filter at the end of the test, so no global state is leaked.

.. _`recording warnings`:

.. _recwarn:

Recording warnings
------------------

You can record raised warnings either using the :func:`pytest.warns` context manager or with
the :fixture:`recwarn` fixture.

To record with :func:`pytest.warns` without asserting anything about the warnings,
pass no arguments as the expected warning type and it will default to a generic Warning:

.. code-block:: python

    with pytest.warns() as record:
        warnings.warn("user", UserWarning)
        warnings.warn("runtime", RuntimeWarning)

    assert len(record) == 2
    assert str(record[0].message) == "user"
    assert str(record[1].message) == "runtime"

The :fixture:`recwarn` fixture will record warnings for the whole function:

.. code-block:: python

    import warnings


    def test_hello(recwarn):
        warnings.warn("hello", UserWarning)
        assert len(recwarn) == 1
        w = recwarn.pop(UserWarning)
        assert issubclass(w.category, UserWarning)
        assert str(w.message) == "hello"
        assert w.filename
        assert w.lineno

Both the :fixture:`recwarn` fixture and the :func:`pytest.warns` context manager return the same interface for recorded
warnings: a :class:`~_pytest.recwarn.WarningsRecorder` instance. To view the recorded warnings, you can
iterate over this instance, call ``len`` on it to get the number of recorded
warnings, or index into it to get a particular recorded warning.


.. _`warns use cases`:

Additional use cases of warnings in tests
-----------------------------------------

Here are some use cases involving warnings that often come up in tests, and suggestions on how to deal with them:

- To ensure that **at least one** of the indicated warnings is issued, use:

.. code-block:: python

    def test_warning():
        with pytest.warns((RuntimeWarning, UserWarning)):
            ...

- To ensure that **only** certain warnings are issued, use:

.. code-block:: python

    def test_warning(recwarn):
        ...
        assert len(recwarn) == 1
        user_warning = recwarn.pop(UserWarning)
        assert issubclass(user_warning.category, UserWarning)

-  To ensure that **no** warnings are emitted, use:

.. code-block:: python

    def test_warning():
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            ...

- To suppress warnings, use:

.. code-block:: python

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        ...


.. _custom_failure_messages:

Custom failure messages
-----------------------

Recording warnings provides an opportunity to produce custom test
failure messages for when no warnings are issued or other conditions
are met.

.. code-block:: python

    def test():
        with pytest.warns(Warning) as record:
            f()
            if not record:
                pytest.fail("Expected a warning!")

If no warnings are issued when calling ``f``, then ``not record`` will
evaluate to ``True``.  You can then call :func:`pytest.fail` with a
custom error message.

.. _internal-warnings:

Internal pytest warnings
------------------------

pytest may generate its own warnings in some situations, such as improper usage or deprecated features.

For example, pytest will emit a warning if it encounters a class that matches :confval:`python_classes` but also
defines an ``__init__`` constructor, as this prevents the class from being instantiated:

.. code-block:: python

    # content of test_pytest_warnings.py
    class Test:
        def __init__(self):
            pass

        def test_foo(self):
            assert 1 == 1

.. code-block:: pytest

    $ pytest test_pytest_warnings.py -q

    ============================= warnings summary =============================
    test_pytest_warnings.py:1
      /home/sweet/project/test_pytest_warnings.py:1: PytestCollectionWarning: cannot collect test class 'Test' because it has a __init__ constructor (from: test_pytest_warnings.py)
        class Test:

    -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
    1 warning in 0.12s

These warnings might be filtered using the same builtin mechanisms used to filter other types of warnings.

Please read our :ref:`backwards-compatibility` to learn how we proceed about deprecating and eventually removing
features.

The full list of warnings is listed in :ref:`the reference documentation <warnings ref>`.


.. _`resource-warnings`:

Resource Warnings
-----------------

Additional information of the source of a :class:`ResourceWarning` can be obtained when captured by pytest if
:mod:`tracemalloc` module is enabled.

One convenient way to enable :mod:`tracemalloc` when running tests is to set the :envvar:`PYTHONTRACEMALLOC` to a large
enough number of frames (say ``20``, but that number is application dependent).

For more information, consult the `Python Development Mode <https://docs.python.org/3/library/devmode.html>`__
section in the Python documentation.

# How to use skip and xfail to deal with tests that cannot succeed
Source: https://docs.pytest.org/en/stable/how-to/skipping.html

.. _`skip and xfail`:

.. _skipping:

How to use skip and xfail to deal with tests that cannot succeed
=================================================================

You can mark test functions that cannot be run on certain platforms
or that you expect to fail so pytest can deal with them accordingly and
present a summary of the test session, while keeping the test suite *green*.

A **skip** means that you expect your test to pass only if some conditions are met,
otherwise pytest should skip running the test altogether. Common examples are skipping
windows-only tests on non-windows platforms, or skipping tests that depend on an external
resource which is not available at the moment (for example a database).

An **xfail** means that you expect a test to fail for some reason.
A common example is a test for a feature not yet implemented, or a bug not yet fixed.
When a test passes despite being expected to fail (marked with ``pytest.mark.xfail``),
it's an **xpass** and will be reported in the test summary.

``pytest`` counts and lists *skip* and *xfail* tests separately. Detailed
information about skipped/xfailed tests is not shown by default to avoid
cluttering the output.  You can use the :option:`-r` option to see details
corresponding to the "short" letters shown in the test progress:

.. code-block:: bash

    pytest -rxXs  # show extra info on xfailed, xpassed, and skipped tests

More details on the :option:`-r` option can be found by running ``pytest -h``.

(See :ref:`how to change command line options defaults`)

.. _skipif:
.. _skip:
.. _`condition booleans`:

Skipping test functions
-----------------------



The simplest way to skip a test function is to mark it with the ``skip`` decorator
which may be passed an optional ``reason``:

.. code-block:: python

    @pytest.mark.skip(reason="no way of currently testing this")
    def test_the_unknown(): ...


Alternatively, it is also possible to skip imperatively during test execution or setup
by calling the ``pytest.skip(reason)`` function:

.. code-block:: python

    def test_function():
        if not valid_config():
            pytest.skip("unsupported configuration")

The imperative method is useful when it is not possible to evaluate the skip condition
during import time.

It is also possible to skip the whole module using
``pytest.skip(reason, allow_module_level=True)`` at the module level:

.. code-block:: python

    import sys

    import pytest

    if not sys.platform.startswith("win"):
        pytest.skip("skipping windows-only tests", allow_module_level=True)


**Reference**: :ref:`pytest.mark.skip ref`

``skipif``
~~~~~~~~~~



If you wish to skip something conditionally then you can use ``skipif`` instead.
Here is an example of marking a test function to be skipped
when run on an interpreter earlier than Python3.13:

.. code-block:: python

    import sys


    @pytest.mark.skipif(sys.version_info < (3, 13), reason="requires python3.13 or higher")
    def test_function(): ...

If the condition evaluates to ``True`` during collection, the test function will be skipped,
with the specified reason appearing in the summary when using ``-rs``.

You can share ``skipif`` markers between modules.  Consider this test module:

.. code-block:: python

    # content of test_mymodule.py
    import mymodule

    minversion = pytest.mark.skipif(
        mymodule.__versioninfo__ < (1, 1), reason="at least mymodule-1.1 required"
    )


    @minversion
    def test_function(): ...

You can import the marker and reuse it in another test module:

.. code-block:: python

    # test_myothermodule.py
    from test_mymodule import minversion


    @minversion
    def test_anotherfunction(): ...

For larger test suites it's usually a good idea to have one file
where you define the markers which you then consistently apply
throughout your test suite.

Alternatively, you can use :ref:`condition strings
<string conditions>` instead of booleans, but they can't be shared between modules easily
so they are supported mainly for backward compatibility reasons.

**Reference**: :ref:`pytest.mark.skipif ref`


Skip all test functions of a class or module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can use the ``skipif`` marker (as any other marker) on classes:

.. code-block:: python

    @pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
    class TestPosixCalls:
        def test_function(self):
            "will not be setup or run under 'win32' platform"

If the condition is ``True``, this marker will produce a skip result for
each of the test methods of that class.

If you want to skip all test functions of a module, you may use the
:globalvar:`pytestmark` global:

.. code-block:: python

    # test_module.py
    pytestmark = pytest.mark.skipif(...)

If multiple ``skipif`` decorators are applied to a test function, it
will be skipped if any of the skip conditions is true.

.. _`whole class- or module level`: mark.html#scoped-marking


Skipping files or directories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes you may need to skip an entire file or directory, for example if the
tests rely on Python version-specific features or contain code that you do not
wish pytest to run. In this case, you must exclude the files and directories
from collection. Refer to :ref:`customizing-test-collection` for more
information.


Skipping on a missing import dependency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can skip tests on a missing import by using :ref:`pytest.importorskip ref`
at module level, within a test, or test setup function.

.. code-block:: python

    docutils = pytest.importorskip("docutils")

If ``docutils`` cannot be imported here, this will lead to a skip outcome of
the test. You can also skip based on the version number of a library:

.. code-block:: python

    docutils = pytest.importorskip("docutils", minversion="0.3")

The version will be read from the specified
module's ``__version__`` attribute.

Summary
~~~~~~~

Here's a quick guide on how to skip tests in a module in different situations:

1. Skip all tests in a module unconditionally:

  .. code-block:: python

        pytestmark = pytest.mark.skip("all tests still WIP")

2. Skip all tests in a module based on some condition:

  .. code-block:: python

        pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="tests for linux only")

3. Skip all tests in a module if some import is missing:

  .. code-block:: python

        pexpect = pytest.importorskip("pexpect")


.. _xfail:

XFail: mark test functions as expected to fail
----------------------------------------------

You can use the ``xfail`` marker to indicate that you
expect a test to fail:

.. code-block:: python

    @pytest.mark.xfail
    def test_function(): ...

This test will run but no traceback will be reported when it fails. Instead, terminal
reporting will list it in the "expected to fail" (``XFAIL``) or "unexpectedly
passing" (``XPASS``) sections.

Alternatively, you can also mark a test as ``XFAIL`` from within the test or its setup function
imperatively:

.. code-block:: python

    def test_function():
        if not valid_config():
            pytest.xfail("failing configuration (but should work)")

.. code-block:: python

    def test_function2():
        import slow_module

        if slow_module.slow_function():
            pytest.xfail("slow_module taking too long")

These two examples illustrate situations where you don't want to check for a condition
at the module level, which is when a condition would otherwise be evaluated for marks.

This will make ``test_function`` ``XFAIL``. Note that no other code is executed after
the :func:`pytest.xfail` call, differently from the marker. That's because it is implemented
internally by raising a known exception.

**Reference**: :ref:`pytest.mark.xfail ref`


``condition`` parameter
~~~~~~~~~~~~~~~~~~~~~~~

If a test is only expected to fail under a certain condition, you can pass
that condition as the first parameter:

.. code-block:: python

    @pytest.mark.xfail(sys.platform == "win32", reason="bug in a 3rd party library")
    def test_function(): ...

Note that you have to pass a reason as well (see the parameter description at
:ref:`pytest.mark.xfail ref`).

``reason`` parameter
~~~~~~~~~~~~~~~~~~~~

You can specify the motive of an expected failure with the ``reason`` parameter:

.. code-block:: python

    @pytest.mark.xfail(reason="known parser issue")
    def test_function(): ...


``raises`` parameter
~~~~~~~~~~~~~~~~~~~~

If you want to be more specific as to why the test is failing, you can specify
a single exception, or a tuple of exceptions, in the ``raises`` argument.

.. code-block:: python

    @pytest.mark.xfail(raises=RuntimeError)
    def test_function(): ...

Then the test will be reported as a regular failure if it fails with an
exception not mentioned in ``raises``.

``run`` parameter
~~~~~~~~~~~~~~~~~

If a test should be marked as xfail and reported as such but should not be
even executed, use the ``run`` parameter as ``False``:

.. code-block:: python

    @pytest.mark.xfail(run=False)
    def test_function(): ...

This is particularly useful for xfailing tests that are crashing the interpreter and should be
investigated later.

.. _`xfail strict tutorial`:

``strict`` parameter
~~~~~~~~~~~~~~~~~~~~

Both ``XFAIL`` and ``XPASS`` don't fail the test suite by default.
You can change this by setting the ``strict`` keyword-only parameter to ``True``:

.. code-block:: python

    @pytest.mark.xfail(strict=True)
    def test_function(): ...


This will make ``XPASS`` ("unexpectedly passing") results from this test to fail the test suite.

You can change the default value of the ``strict`` parameter using the
``strict_xfail`` ini option:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        xfail_strict = true

.. tab:: ini

    .. code-block:: ini

        [pytest]
        strict_xfail = true


Ignoring xfail
~~~~~~~~~~~~~~

By specifying on the commandline:

.. code-block:: bash

    pytest --runxfail

you can force the running and reporting of an ``xfail`` marked test
as if it weren't marked at all. This also causes :func:`pytest.xfail` to produce no effect.

Examples
~~~~~~~~

Here is a simple test file with the several usages:

.. literalinclude:: /example/xfail_demo.py

Running it with the report-on-xfail option gives this output:

.. FIXME: Use $ instead of ! again to re-enable regendoc once it's fixed:
   https://github.com/pytest-dev/pytest/issues/8807

.. code-block:: pytest

    ! pytest -rx xfail_demo.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-6.x.y, py-1.x.y, pluggy-1.x.y
    cachedir: $PYTHON_PREFIX/.pytest_cache
    rootdir: $REGENDOC_TMPDIR/example
    collected 7 items

    xfail_demo.py xxxxxxx                                                [100%]

    ========================= short test summary info ==========================
    XFAIL xfail_demo.py::test_hello
    XFAIL xfail_demo.py::test_hello2
      reason: [NOTRUN]
    XFAIL xfail_demo.py::test_hello3
      condition: hasattr(os, 'sep')
    XFAIL xfail_demo.py::test_hello4
      bug 110
    XFAIL xfail_demo.py::test_hello5
      condition: pytest.__version__[0] != "17"
    XFAIL xfail_demo.py::test_hello6
      reason: reason
    XFAIL xfail_demo.py::test_hello7
    ============================ 7 xfailed in 0.12s ============================

.. _`skip/xfail with parametrize`:

Skip/xfail with parametrize
---------------------------

It is possible to apply markers like skip and xfail to individual
test instances when using parametrize:

.. code-block:: python

    import sys

    import pytest


    @pytest.mark.parametrize(
        ("n", "expected"),
        [
            (1, 2),
            pytest.param(1, 0, marks=pytest.mark.xfail),
            pytest.param(1, 3, marks=pytest.mark.xfail(reason="some bug")),
            (2, 3),
            (3, 4),
            (4, 5),
            pytest.param(
                10, 11, marks=pytest.mark.skipif(sys.version_info >= (3, 0), reason="py2k")
            ),
        ],
    )
    def test_increment(n, expected):
        assert n + 1 == expected

# How to install and use plugins
Source: https://docs.pytest.org/en/stable/how-to/plugins.html

.. _`external plugins`:
.. _`extplugins`:
.. _`using plugins`:

How to install and use plugins
===============================

This section talks about installing and using third party plugins.
For writing your own plugins, please refer to :ref:`writing-plugins`.

Installing a third party plugin can be easily done with ``pip``:

.. code-block:: bash

    pip install pytest-NAME
    pip uninstall pytest-NAME

If a plugin is installed, ``pytest`` automatically finds and integrates it,
there is no need to activate it.

Here is a little annotated list for some popular plugins:

* :pypi:`pytest-django`: write tests
  for `django <https://docs.djangoproject.com/>`_ apps, using pytest integration.

* :pypi:`pytest-twisted`: write tests
  for `twisted <https://twistedmatrix.com/>`_ apps, starting a reactor and
  processing deferreds from test functions.

* :pypi:`pytest-cov`:
  coverage reporting, compatible with distributed testing

* :pypi:`pytest-xdist`:
  to distribute tests to CPUs and remote hosts, to run in boxed
  mode that allows pytest to survive segmentation faults, to run in
  looponfailing mode, automatically re-running failing tests
  on file changes.

* :pypi:`pytest-instafail`:
  to report failures while the test run is happening.

* :pypi:`pytest-bdd`:
  to write tests using behaviour-driven testing.

* :pypi:`pytest-timeout`:
  to timeout tests based on function marks or global definitions.

* :pypi:`pytest-pep8`:
  a ``--pep8`` option to enable PEP8 compliance checking.

* :pypi:`pytest-flakes`:
  check source code with pyflakes.

* :pypi:`allure-pytest`:
  report test results via `allure-framework <https://github.com/allure-framework/>`_.

To see a complete list of all plugins with their latest testing
status against different pytest and Python versions, please visit
:ref:`plugin-list`.

You may also discover more plugins through a `pytest- pypi.org search`_.

.. _`pytest- pypi.org search`: https://pypi.org/search/?q=pytest-


.. _`available installable plugins`:

Requiring/Loading plugins in a test module or conftest file
-----------------------------------------------------------

You can require plugins in a test module or a conftest file using :globalvar:`pytest_plugins`:

.. code-block:: python

    pytest_plugins = ("myapp.testsupport.myplugin",)

When the test module or conftest plugin is loaded the specified plugins
will be loaded as well.

.. note::

    Requiring plugins using a ``pytest_plugins`` variable in non-root
    ``conftest.py`` files is deprecated. See
    :ref:`full explanation <requiring plugins in non-root conftests>`
    in the Writing plugins section.

.. note::
   The name ``pytest_plugins`` is reserved and should not be used as a
   name for a custom plugin module.


.. _`findpluginname`:

Finding out which plugins are active
------------------------------------

If you want to find out which plugins are active in your
environment you can type:

.. code-block:: bash

    pytest --trace-config

and will get an extended test header which shows activated plugins
and their names. It will also print local plugins aka
:ref:`conftest.py <conftest.py plugins>` files when they are loaded.

.. _`cmdunregister`:

Deactivating / unregistering a plugin by name
---------------------------------------------

You can prevent plugins from loading or unregister them:

.. code-block:: bash

    pytest -p no:NAME

This means that any subsequent try to activate/load the named
plugin will not work.

If you want to unconditionally disable a plugin for a project, you can add
this option to your configuration file:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        addopts = ["-p", "no:NAME"]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        addopts = -p no:NAME

Alternatively to disable it only in certain environments (for example in a
CI server), you can set ``PYTEST_ADDOPTS`` environment variable to
``-p no:name``.

See :ref:`findpluginname` for how to obtain the name of a plugin.

.. _`disable_plugin_autoload`:

Disabling plugins from autoloading
----------------------------------

If you want to disable plugins from loading automatically, instead of requiring you to
manually specify each plugin with :option:`-p` or :envvar:`PYTEST_PLUGINS`, you can use :option:`--disable-plugin-autoload` or :envvar:`PYTEST_DISABLE_PLUGIN_AUTOLOAD`.

.. code-block:: bash

   export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
   export PYTEST_PLUGINS=NAME,NAME2
   pytest

.. code-block:: bash

   pytest --disable-plugin-autoload -p NAME -p NAME2

.. tab:: toml

    .. code-block:: toml

        [pytest]
        addopts = ["--disable-plugin-autoload", "-p", "NAME", "-p", "NAME2"]

.. tab:: ini

    .. code-block:: ini

        [pytest]
        addopts =
            --disable-plugin-autoload
            -p NAME
            -p NAME2

.. versionadded:: 8.4

   The :option:`--disable-plugin-autoload` command-line flag.

.. note::

   :option:`-p` and :envvar:`PYTEST_PLUGINS` are both ways to explicitly control which
   plugins are loaded, but they serve slightly different use-cases.

   * :option:`-p` loads (or disables with ``-p no:<name>``) a plugin by name or entry point
     for a specific pytest invocation, and is processed early during startup.
   * :envvar:`PYTEST_PLUGINS` is a comma-separated list of Python modules that are imported
     and registered as plugins during startup. This mechanism is commonly used by test
     suites, for example when testing a plugin.

   When explicitly controlling plugin loading (especially with
   :envvar:`PYTEST_DISABLE_PLUGIN_AUTOLOAD` or :option:`--disable-plugin-autoload`),
   avoid specifying the same plugin via multiple mechanisms. Registering the same plugin
   more than once can lead to errors during plugin registration.

Examples:

.. code-block:: bash

   # Disable auto-loading and load only specific plugins for this invocation
   PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 pytest -p xdist

.. code-block:: bash

   # Disable auto-loading and load plugin modules during startup
   PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTEST_PLUGINS=mymodule.plugin,xdist pytest

# Writing plugins
Source: https://docs.pytest.org/en/stable/how-to/writing_plugins.html

.. _plugins:
.. _`writing-plugins`:

Writing plugins
===============

It is easy to implement `local conftest plugins`_ for your own project
or `pip-installable plugins`_ that can be used throughout many projects,
including third party projects.  Please refer to :ref:`using plugins` if you
only want to use but not write plugins.

A plugin contains one or multiple hook functions. :ref:`Writing hooks <writinghooks>`
explains the basics and details of how you can write a hook function yourself.
``pytest`` implements all aspects of configuration, collection, running and
reporting by calling :ref:`well specified hooks <hook-reference>` of the following plugins:

* builtin plugins: loaded from pytest's internal ``_pytest`` directory.

* :ref:`external plugins <extplugins>`: installed third-party modules discovered
  through :ref:`entry points <pip-installable plugins>` in their packaging metadata

* `conftest.py plugins`_: modules auto-discovered in test directories

In principle, each hook call is a ``1:N`` Python function call where ``N`` is the
number of registered implementation functions for a given specification.
All specifications and implementations follow the ``pytest_`` prefix
naming convention, making them easy to distinguish and find.

.. _`pluginorder`:

Plugin discovery order at tool startup
--------------------------------------

``pytest`` loads plugin modules at tool startup in the following way:

1. by scanning the command line for the ``-p no:name`` option
   and *blocking* that plugin from being loaded (even builtin plugins can
   be blocked this way). This happens before normal command-line parsing.

2. by loading all builtin plugins.

3. by scanning the command line for the ``-p name`` option
   and loading the specified plugin. This happens before normal command-line parsing.

4. by loading all plugins registered through installed third-party package
   :ref:`entry points <pip-installable plugins>`, unless the
   :envvar:`PYTEST_DISABLE_PLUGIN_AUTOLOAD` environment variable is set.

5. by loading all plugins specified through the :envvar:`PYTEST_PLUGINS` environment variable.

6. by loading all "initial" :file:`conftest.py` files:

   - determine the test paths: specified on the command line, otherwise in
     :confval:`testpaths` if defined and running from the rootdir, otherwise the
     current dir
   - for each test path, load ``conftest.py`` and ``test*/conftest.py`` relative
     to the directory part of the test path, if exist. Before a ``conftest.py``
     file is loaded, load ``conftest.py`` files in all of its parent directories.
     After a ``conftest.py`` file is loaded, recursively load all plugins specified
     in its :globalvar:`pytest_plugins` variable if present.


.. _`conftest.py plugins`:
.. _`localplugin`:
.. _`local conftest plugins`:

conftest.py: local per-directory plugins
----------------------------------------

Local ``conftest.py`` plugins contain directory-specific hook
implementations.  Hook Session and test running activities will
invoke all hooks defined in ``conftest.py`` files closer to the
root of the filesystem.  Example of implementing the
``pytest_runtest_setup`` hook so that is called for tests in the ``a``
sub directory but not for other directories::

    a/conftest.py:
        def pytest_runtest_setup(item):
            # called for running each test in 'a' directory
            print("setting up", item)

    a/test_sub.py:
        def test_sub():
            pass

    test_flat.py:
        def test_flat():
            pass

Here is how you might run it::

     pytest test_flat.py --capture=no  # will not show "setting up"
     pytest a/test_sub.py --capture=no  # will show "setting up"

.. note::
    If you have ``conftest.py`` files which do not reside in a
    python package directory (i.e. one containing an ``__init__.py``) then
    "import conftest" can be ambiguous because there might be other
    ``conftest.py`` files as well on your ``PYTHONPATH`` or ``sys.path``.
    It is thus good practice for projects to either put ``conftest.py``
    under a package scope or to never import anything from a
    ``conftest.py`` file.

    See also: :ref:`pythonpath`.

.. note::
    Some hooks cannot be implemented in conftest.py files which are not
    :ref:`initial <pluginorder>` due to how pytest discovers plugins during
    startup. See the documentation of each hook for details.

Writing your own plugin
-----------------------

If you want to write a plugin, there are many real-life examples
you can copy from:

* a custom collection example plugin: :ref:`yaml plugin`
* builtin plugins which provide pytest's own functionality
* many :ref:`external plugins <plugin-list>` providing additional features

All of these plugins implement :ref:`hooks <hook-reference>` and/or :ref:`fixtures <fixture>`
to extend and add functionality.

.. note::
    Make sure to check out the excellent
    `cookiecutter-pytest-plugin <https://github.com/pytest-dev/cookiecutter-pytest-plugin>`_
    project, which is a `cookiecutter template <https://github.com/audreyr/cookiecutter>`_
    for authoring plugins.

    The template provides an excellent starting point with a working plugin,
    tests running with tox, a comprehensive README file as well as a
    pre-configured entry-point.

Also consider :ref:`contributing your plugin to pytest-dev<submitplugin>`
once it has some happy users other than yourself.


.. _`setuptools entry points`:
.. _`pip-installable plugins`:

Making your plugin installable by others
----------------------------------------

If you want to make your plugin externally available, you
may define a so-called entry point for your distribution so
that ``pytest`` finds your plugin module. Entry points are
a feature that is provided by :std:doc:`packaging tools
<packaging:specifications/entry-points>`.

pytest looks up the ``pytest11`` entrypoint to discover its
plugins, thus you can make your plugin available by defining
it in your ``pyproject.toml`` file.

.. sourcecode:: toml

    # sample ./pyproject.toml file
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [project]
    name = "myproject"
    classifiers = [
        "Framework :: Pytest",
    ]

    [project.entry-points.pytest11]
    myproject = "myproject.pluginmodule"

If a package is installed this way, ``pytest`` will load
``myproject.pluginmodule`` as a plugin which can define
:ref:`hooks <hook-reference>`. Confirm registration with ``pytest --trace-config``

.. note::

    Make sure to include ``Framework :: Pytest`` in your list of
    `PyPI classifiers <https://pypi.org/classifiers/>`_
    to make it easy for users to find your plugin.


.. _assertion-rewriting:

Assertion Rewriting
-------------------

One of the main features of ``pytest`` is the use of plain assert
statements and the detailed introspection of expressions upon
assertion failures.  This is provided by "assertion rewriting" which
modifies the parsed AST before it gets compiled to bytecode.  This is
done via a :pep:`302` import hook which gets installed early on when
``pytest`` starts up and will perform this rewriting when modules get
imported.  However, since we do not want to test different bytecode
from what you will run in production, this hook only rewrites test modules
themselves (as defined by the :confval:`python_files` configuration option),
and any modules which are part of plugins.
Any other imported module will not be rewritten and normal assertion behaviour
will happen.

If you have assertion helpers in other modules where you would need
assertion rewriting to be enabled you need to ask ``pytest``
explicitly to rewrite this module before it gets imported.

.. autofunction:: pytest.register_assert_rewrite
    :noindex:

This is especially important when you write a pytest plugin which is
created using a package.  The import hook only treats ``conftest.py``
files and any modules which are listed in the ``pytest11`` entrypoint
as plugins.  As an example consider the following package::

   pytest_foo/__init__.py
   pytest_foo/plugin.py
   pytest_foo/helper.py

With the following typical ``setup.py`` extract:

.. code-block:: python

   setup(..., entry_points={"pytest11": ["foo = pytest_foo.plugin"]}, ...)

In this case only ``pytest_foo/plugin.py`` will be rewritten.  If the
helper module also contains assert statements which need to be
rewritten it needs to be marked as such, before it gets imported.
This is easiest by marking it for rewriting inside the
``__init__.py`` module, which will always be imported first when a
module inside a package is imported.  This way ``plugin.py`` can still
import ``helper.py`` normally.  The contents of
``pytest_foo/__init__.py`` will then need to look like this:

.. code-block:: python

   import pytest

   pytest.register_assert_rewrite("pytest_foo.helper")


Requiring/Loading plugins in a test module or conftest file
-----------------------------------------------------------

You can require plugins in a test module or a ``conftest.py`` file using :globalvar:`pytest_plugins`:

.. code-block:: python

    pytest_plugins = ["name1", "name2"]

When the test module or conftest plugin is loaded the specified plugins
will be loaded as well. Any module can be blessed as a plugin, including internal
application modules:

.. code-block:: python

    pytest_plugins = "myapp.testsupport.myplugin"

:globalvar:`pytest_plugins` are processed recursively, so note that in the example above
if ``myapp.testsupport.myplugin`` also declares :globalvar:`pytest_plugins`, the contents
of the variable will also be loaded as plugins, and so on.

.. _`requiring plugins in non-root conftests`:

.. note::
    Requiring plugins using :globalvar:`pytest_plugins` variable in non-root
    ``conftest.py`` files is deprecated.

    This is important because ``conftest.py`` files implement per-directory
    hook implementations, but once a plugin is imported, it will affect the
    entire directory tree. In order to avoid confusion, defining
    :globalvar:`pytest_plugins` in any ``conftest.py`` file which is not located in the
    tests root directory is deprecated, and will raise a warning.

This mechanism makes it easy to share fixtures within applications or even
external applications without the need to create external plugins using the
:std:doc:`entry point packaging metadata
<packaging:guides/creating-and-discovering-plugins>` technique.

Plugins imported by :globalvar:`pytest_plugins` will also automatically be marked
for assertion rewriting (see :func:`pytest.register_assert_rewrite`).
However for this to have any effect the module must not be
imported already; if it was already imported at the time the
:globalvar:`pytest_plugins` statement is processed, a warning will result and
assertions inside the plugin will not be rewritten.  To fix this you
can either call :func:`pytest.register_assert_rewrite` yourself before
the module is imported, or you can arrange the code to delay the
importing until after the plugin is registered.


Accessing another plugin by name
--------------------------------

If a plugin wants to collaborate with code from
another plugin it can obtain a reference through
the plugin manager like this:

.. sourcecode:: python

    plugin = config.pluginmanager.get_plugin("name_of_plugin")

If you want to look at the names of existing plugins, use
the :option:`--trace-config` option.


.. _registering-markers:

Registering custom markers
--------------------------

If your plugin uses any markers, you should register them so that they appear in
pytest's help text and do not :ref:`cause spurious warnings <unknown-marks>`.
For example, the following plugin would register ``cool_marker`` and
``mark_with`` for all users:

.. code-block:: python

    def pytest_configure(config):
        config.addinivalue_line("markers", "cool_marker: this one is for cool tests.")
        config.addinivalue_line(
            "markers", "mark_with(arg, arg2): this marker takes arguments."
        )


Testing plugins
---------------

pytest comes with a plugin named ``pytester`` that helps you write tests for
your plugin code. The plugin is disabled by default, so you will have to enable
it before you can use it.

You can do so by adding the following line to a ``conftest.py`` file in your
testing directory:

.. code-block:: python

    # content of conftest.py

    pytest_plugins = ["pytester"]

Alternatively you can invoke pytest with the ``-p pytester`` command line
option.

This will allow you to use the :py:class:`pytester <pytest.Pytester>`
fixture for testing your plugin code.

Let's demonstrate what you can do with the plugin with an example. Imagine we
developed a plugin that provides a fixture ``hello`` which yields a function
and we can invoke this function with one optional parameter. It will return a
string value of ``Hello World!`` if we do not supply a value or ``Hello
{value}!`` if we do supply a string value.

.. code-block:: python

    import pytest


    def pytest_addoption(parser):
        group = parser.getgroup("helloworld")
        group.addoption(
            "--name",
            action="store",
            dest="name",
            default="World",
            help='Default "name" for hello().',
        )


    @pytest.fixture
    def hello(request):
        name = request.config.getoption("name")

        def _hello(name=None):
            if not name:
                name = request.config.getoption("name")
            return f"Hello {name}!"

        return _hello


Now the ``pytester`` fixture provides a convenient API for creating temporary
``conftest.py`` files and test files. It also allows us to run the tests and
return a result object, with which we can assert the tests' outcomes.

.. code-block:: python

    def test_hello(pytester):
        """Make sure that our plugin works."""

        # create a temporary conftest.py file
        pytester.makeconftest(
            """
            import pytest

            @pytest.fixture(params=[
                "Brianna",
                "Andreas",
                "Floris",
            ])
            def name(request):
                return request.param
        """
        )

        # create a temporary pytest test file
        pytester.makepyfile(
            """
            def test_hello_default(hello):
                assert hello() == "Hello World!"

            def test_hello_name(hello, name):
                assert hello(name) == "Hello {0}!".format(name)
        """
        )

        # run all tests with pytest
        result = pytester.runpytest()

        # check that all 4 tests passed
        result.assert_outcomes(passed=4)


Additionally it is possible to copy examples to the ``pytester``'s isolated environment
before running pytest on it. This way we can abstract the tested logic to separate files,
which is especially useful for longer tests and/or longer ``conftest.py`` files.

Note that for ``pytester.copy_example`` to work we need to set `pytester_example_dir`
in our configuration file to tell pytest where to look for example files.

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    pytester_example_dir = "."


.. code-block:: python

    # content of test_example.py


    def test_plugin(pytester):
        pytester.copy_example("test_example.py")
        pytester.runpytest("-k", "test_example")


    def test_example():
        pass

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    configfile: pytest.toml
    collected 2 items

    test_example.py ..                                                   [100%]

    ============================ 2 passed in 0.12s =============================

For more information about the result object that ``runpytest()`` returns, and
the methods that it provides please check out the :py:class:`RunResult
<_pytest.pytester.RunResult>` documentation.

# Writing hook functions
Source: https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html

.. _`writinghooks`:

Writing hook functions
======================


.. _validation:

hook function validation and execution
--------------------------------------

pytest calls hook functions from registered plugins for any
given hook specification.  Let's look at a typical hook function
for the ``pytest_collection_modifyitems(session, config,
items)`` hook which pytest calls after collection of all test items is
completed.

When we implement a ``pytest_collection_modifyitems`` function in our plugin
pytest will during registration verify that you use argument
names which match the specification and bail out if not.

Let's look at a possible implementation:

.. code-block:: python

    def pytest_collection_modifyitems(config, items):
        # called after collection is completed
        # you can modify the ``items`` list
        ...

Here, ``pytest`` will pass in ``config`` (the pytest config object)
and ``items`` (the list of collected test items) but will not pass
in the ``session`` argument because we didn't list it in the function
signature.  This dynamic "pruning" of arguments allows ``pytest`` to
be "future-compatible": we can introduce new hook named parameters without
breaking the signatures of existing hook implementations.  It is one of
the reasons for the general long-lived compatibility of pytest plugins.

Note that hook functions other than ``pytest_runtest_*`` are not
allowed to raise exceptions.  Doing so will break the pytest run.



.. _firstresult:

firstresult: stop at first non-None result
-------------------------------------------

Most calls to ``pytest`` hooks result in a **list of results** which contains
all non-None results of the called hook functions.

Some hook specifications use the ``firstresult=True`` option so that the hook
call only executes until the first of N registered functions returns a
non-None result which is then taken as result of the overall hook call.
The remaining hook functions will not be called in this case.

.. _`hookwrapper`:

hook wrappers: executing around other hooks
-------------------------------------------------

pytest plugins can implement hook wrappers which wrap the execution
of other hook implementations.  A hook wrapper is a generator function
which yields exactly once. When pytest invokes hooks it first executes
hook wrappers and passes the same arguments as to the regular hooks.

At the yield point of the hook wrapper pytest will execute the next hook
implementations and return their result to the yield point, or will
propagate an exception if they raised.

Here is an example definition of a hook wrapper:

.. code-block:: python

    import pytest


    @pytest.hookimpl(wrapper=True)
    def pytest_pyfunc_call(pyfuncitem):
        do_something_before_next_hook_executes()

        # If the outcome is an exception, will raise the exception.
        res = yield

        new_res = post_process_result(res)

        # Override the return value to the plugin system.
        return new_res

The hook wrapper needs to return a result for the hook, or raise an exception.

In many cases, the wrapper only needs to perform tracing or other side effects
around the actual hook implementations, in which case it can return the result
value of the ``yield``. The simplest (though useless) hook wrapper is
``return (yield)``.

In other cases, the wrapper wants to adjust or adapt the result, in which case
it can return a new value. If the result of the underlying hook is a mutable
object, the wrapper may modify that result, but it's probably better to avoid it.

If the hook implementation failed with an exception, the wrapper can handle that
exception using a ``try-catch-finally`` around the ``yield``, by propagating it,
suppressing it, or raising a different exception entirely.

For more information, consult the
:ref:`pluggy documentation about hook wrappers <pluggy:hookwrappers>`.

.. _plugin-hookorder:

Hook function ordering / call example
-------------------------------------

For any given hook specification there may be more than one
implementation and we thus generally view ``hook`` execution as a
``1:N`` function call where ``N`` is the number of registered functions.
There are ways to influence if a hook implementation comes before or
after others, i.e.  the position in the ``N``-sized list of functions:

.. code-block:: python

    # Plugin 1
    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(items):
        # will execute as early as possible
        ...


    # Plugin 2
    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(items):
        # will execute as late as possible
        ...


    # Plugin 3
    @pytest.hookimpl(wrapper=True)
    def pytest_collection_modifyitems(items):
        # will execute even before the tryfirst one above!
        try:
            return (yield)
        finally:
            # will execute after all non-wrappers executed
            ...

Here is the order of execution:

1. Plugin3's pytest_collection_modifyitems called until the yield point
   because it is a hook wrapper.

2. Plugin1's pytest_collection_modifyitems is called because it is marked
   with ``tryfirst=True``.

3. Plugin2's pytest_collection_modifyitems is called because it is marked
   with ``trylast=True`` (but even without this mark it would come after
   Plugin1).

4. Plugin3's pytest_collection_modifyitems then executing the code after the yield
   point.  The yield receives the result from calling the non-wrappers, or raises
   an exception if the non-wrappers raised.

It's possible to use ``tryfirst`` and ``trylast`` also on hook wrappers
in which case it will influence the ordering of hook wrappers among each other.

.. note::

    pytest only searches for hook implementations whose names start with
    ``pytest_``.  The ``specname`` argument to ``@pytest.hookimpl`` can be used
    to give an implementation a different suffix, for example
    ``pytest_collection_modifyitems_tryfirst``, but the function name still
    needs to start with ``pytest_``.  A hook implementation named
    ``my_collection_modifyitems`` is ignored even if it is decorated with
    ``@pytest.hookimpl(specname="pytest_collection_modifyitems")``.

.. _`declaringhooks`:

Declaring new hooks
------------------------

.. note::

    This is a quick overview on how to add new hooks and how they work in general, but a more complete
    overview can be found in `the pluggy documentation <https://pluggy.readthedocs.io/en/latest/>`__.

Plugins and ``conftest.py`` files may declare new hooks that can then be
implemented by other plugins in order to alter behaviour or interact with
the new plugin:

.. autofunction:: _pytest.hookspec.pytest_addhooks
    :noindex:

Hooks are usually declared as do-nothing functions that contain only
documentation describing when the hook will be called and what return values
are expected. The names of the functions must start with `pytest_` otherwise pytest won't recognize them.

Here's an example. Let's assume this code is in the ``sample_hook.py`` module.

.. code-block:: python

    def pytest_my_hook(config):
        """
        Receives the pytest config and does things with it
        """

To register the hooks with pytest they need to be structured in their own module or class. This
class or module can then be passed to the ``pluginmanager`` using the ``pytest_addhooks`` function
(which itself is a hook exposed by pytest).

.. code-block:: python

    def pytest_addhooks(pluginmanager):
        """This example assumes the hooks are grouped in the 'sample_hook' module."""
        from my_app.tests import sample_hook

        pluginmanager.add_hookspecs(sample_hook)

For a real world example, see `newhooks.py`_ from `xdist <https://github.com/pytest-dev/pytest-xdist>`_.

.. _`newhooks.py`: https://github.com/pytest-dev/pytest-xdist/blob/v3.8.0/src/xdist/newhooks.py

Hooks may be called both from fixtures or from other hooks. In both cases, hooks are called
through the ``hook`` object, available in the ``config`` object. Most hooks receive a
``config`` object directly, while fixtures may use the ``pytestconfig`` fixture which provides the same object.

.. code-block:: python

    @pytest.fixture()
    def my_fixture(pytestconfig):
        # call the hook called "pytest_my_hook"
        # 'result' will be a list of return values from all registered functions.
        result = pytestconfig.hook.pytest_my_hook(config=pytestconfig)

.. note::
    Hooks receive parameters using only keyword arguments.

Now your hook is ready to be used. To register a function at the hook, other plugins or users must
now simply define the function ``pytest_my_hook`` with the correct signature in their ``conftest.py``.

Example:

.. code-block:: python

    def pytest_my_hook(config):
        """
        Print all active hooks to the screen.
        """
        print(config.hook)

.. note::

    Unlike other hooks, the :hook:`pytest_generate_tests` hook is also discovered when
    defined inside a test module or test class. Other hooks must live in
    :ref:`conftest.py plugins <localplugin>` or external plugins.
    See :ref:`parametrize-basics` and the :ref:`hook-reference`.

.. _`addoptionhooks`:


Using hooks in pytest_addoption
-------------------------------

Occasionally, it is necessary to change the way in which command line options
are defined by one plugin based on hooks in another plugin. For example,
a plugin may expose a command line option for which another plugin needs
to define the default value. The pluginmanager can be used to install and
use hooks to accomplish this. The plugin would define and add the hooks
and use pytest_addoption as follows:

.. code-block:: python

   # contents of hooks.py


   # Use firstresult=True because we only want one plugin to define this
   # default value
   @hookspec(firstresult=True)
   def pytest_config_file_default_value():
       """Return the default value for the config file command line option."""


   # contents of myplugin.py


   def pytest_addhooks(pluginmanager):
       """This example assumes the hooks are grouped in the 'hooks' module."""
       from . import hooks

       pluginmanager.add_hookspecs(hooks)


   def pytest_addoption(parser, pluginmanager):
       default_value = pluginmanager.hook.pytest_config_file_default_value()
       parser.addoption(
           "--config-file",
           help="Config file to use, defaults to %(default)s",
           default=default_value,
       )

Another plugin (installed via setuptools entry points, or via the ``-p`` command-line
option) could then define the hook implementation to provide the default value:

.. code-block:: python

    # contents of third_party_plugin.py


    def pytest_config_file_default_value():
        return "config.yaml"

.. note::

    **Hook implementations in conftest.py files are not available to other plugins during**
    **their** ``pytest_addoption()`` **execution**. This is because conftest.py files are
    discovered and loaded *after* builtin plugins, third-party plugins, and command-line
    plugins have already been initialized (including the execution of their
    ``pytest_addoption()`` hooks).

    However, :ref:`initial conftest files <pluginorder>` themselves *can* implement
    ``pytest_addoption()`` to add their own command-line options. When an initial conftest
    is loaded, its ``pytest_addoption()`` hook will be called immediately.

    During a plugin's ``pytest_addoption()`` execution, only hook implementations from
    plugins that were loaded earlier will be available. These include:

    * builtin plugins
    * plugins explicitly loaded with ``-p`` on the command line
    * installed third-party plugins (via setuptools entry points)
    * plugins specified via the ``PYTEST_PLUGINS`` environment variable

    See :ref:`pluginorder` for the complete plugin discovery order.


Optionally using hooks from 3rd party plugins
---------------------------------------------

Using new hooks from plugins as explained above might be a little tricky
because of the standard :ref:`validation mechanism <validation>`:
if you depend on a plugin that is not installed, validation will fail and
the error message will not make much sense to your users.

One approach is to defer the hook implementation to a new plugin instead of
declaring the hook functions directly in your plugin module, for example:

.. code-block:: python

    # contents of myplugin.py


    class DeferPlugin:
        """Simple plugin to defer pytest-xdist hook functions."""

        def pytest_testnodedown(self, node, error):
            """standard xdist hook function."""


    def pytest_configure(config):
        if config.pluginmanager.hasplugin("xdist"):
            config.pluginmanager.register(DeferPlugin())

This has the added benefit of allowing you to conditionally install hooks
depending on which plugins are installed.

.. _plugin-stash:

Storing data on items across hook functions
-------------------------------------------

Plugins often need to store data on :class:`~pytest.Item`\s in one hook
implementation, and access it in another. One common solution is to just
assign some private attribute directly on the item, but type-checkers like
mypy frown upon this, and it may also cause conflicts with other plugins.
So pytest offers a better way to do this, :attr:`item.stash <_pytest.nodes.Node.stash>`.

To use the "stash" in your plugins, first create "stash keys" somewhere at the
top level of your plugin:

.. code-block:: python

    been_there_key = pytest.StashKey[bool]()
    done_that_key = pytest.StashKey[str]()

then use the keys to stash your data at some point:

.. code-block:: python

    def pytest_runtest_setup(item: pytest.Item) -> None:
        item.stash[been_there_key] = True
        item.stash[done_that_key] = "no"

and retrieve them at another point:

.. code-block:: python

    def pytest_runtest_teardown(item: pytest.Item) -> None:
        if not item.stash[been_there_key]:
            print("Oh?")
        item.stash[done_that_key] = "yes!"

Stashes are available on all node types (like :class:`~pytest.Class`,
:class:`~pytest.Session`) and also on :class:`~pytest.Config`, if needed.

# How to use pytest with an existing test suite
Source: https://docs.pytest.org/en/stable/how-to/existingtestsuite.html

.. _existingtestsuite:

How to use pytest with an existing test suite
==============================================

Pytest can be used with most existing test suites, but its
behavior differs from other test runners such as Python's
default unittest framework.

Before using this section you will want to :ref:`install pytest <getstarted>`.

Running an existing test suite with pytest
---------------------------------------------

Say you want to contribute to an existing repository somewhere.
After pulling the code into your development space using some
flavor of version control and (optionally) setting up a virtualenv
you will want to run:

.. code-block:: bash

    cd <repository>
    pip install -e .  # Environment dependent alternatives include
                      # 'python setup.py develop' and 'conda develop'

in your project root.  This will set up a symlink to your code in
site-packages, allowing you to edit your code while your tests
run against it as if it were installed.

Setting up your project in development mode lets you avoid having to
reinstall every time you want to run your tests, and is less brittle than
mucking about with sys.path to point your tests at local code.

Also consider using :ref:`tox <use tox>`.

# How to use ``unittest``-based tests with pytest
Source: https://docs.pytest.org/en/stable/how-to/unittest.html

.. _`unittest.TestCase`:
.. _`unittest`:

How to use ``unittest``-based tests with pytest
===============================================

``pytest`` supports running Python ``unittest``-based tests out of the box.
It's meant for leveraging existing ``unittest``-based test suites
to use pytest as a test runner and also allow to incrementally adapt
the test suite to take full advantage of pytest's features.

To run an existing ``unittest``-style test suite using ``pytest``, type:

.. code-block:: bash

    pytest tests


pytest will automatically collect ``unittest.TestCase`` subclasses and
their ``test`` methods in ``test_*.py`` or ``*_test.py`` files.

Almost all ``unittest`` features are supported:

* :func:`unittest.skip`/:func:`unittest.skipIf` style decorators
* :meth:`unittest.TestCase.setUp`/:meth:`unittest.TestCase.tearDown`
* :meth:`unittest.TestCase.setUpClass`/:meth:`unittest.TestCase.tearDownClass`
* :func:`unittest.setUpModule`/:func:`unittest.tearDownModule`
* :meth:`unittest.TestCase.subTest` (since version ``9.0``)

.. _`load_tests protocol`: https://docs.python.org/3/library/unittest.html#load-tests-protocol

Up to this point pytest does not have support for the following features:

* `load_tests protocol`_;

Benefits out of the box
-----------------------

By running your test suite with pytest you can make use of several features,
in most cases without having to modify existing code:

* Obtain :ref:`more informative tracebacks <tbreportdemo>`;
* :ref:`stdout and stderr <captures>` capturing;
* :ref:`Test selection options <select-tests>` using :option:`-k` and :option:`-m` flags;
* :ref:`maxfail`;
* :ref:`--pdb <pdb-option>` command-line option for debugging on test failures
  (see :ref:`note <pdb-unittest-note>` below);
* Distribute tests to multiple CPUs using the :pypi:`pytest-xdist` plugin;
* Use :ref:`plain assert-statements <assert>` instead of ``self.assert*`` functions
  (:pypi:`unittest2pytest` is immensely helpful in this);


pytest features in ``unittest.TestCase`` subclasses
---------------------------------------------------

The following pytest features work in ``unittest.TestCase`` subclasses:

* :ref:`Marks <mark>`: :ref:`skip <skip>`, :ref:`skipif <skipif>`, :ref:`xfail <xfail>`;
* :ref:`Auto-use fixtures <mixing-fixtures>`;

The following pytest features **do not** work, and probably
never will due to different design philosophies:

* :ref:`Fixtures <fixture>` (except for ``autouse`` fixtures, see :ref:`below <mixing-fixtures>`);
* :ref:`Parametrization <parametrize>`;
* :ref:`Custom hooks <writing-plugins>`;


Third party plugins may or may not work well, depending on the plugin and the test suite.

.. _mixing-fixtures:

Mixing pytest fixtures into ``unittest.TestCase`` subclasses using marks
------------------------------------------------------------------------

Running your unittest with ``pytest`` allows you to use its
:ref:`fixture mechanism <fixture>` with ``unittest.TestCase`` style
tests.  Assuming you have at least skimmed the pytest fixture features,
let's jump-start into an example that integrates a pytest ``db_class``
fixture, setting up a class-cached database object, and then reference
it from a unittest-style test:

.. code-block:: python

    # content of conftest.py

    # we define a fixture function below and it will be "used" by
    # referencing its name from tests

    import pytest


    @pytest.fixture(scope="class")
    def db_class(request):
        class DummyDB:
            pass

        # set a class attribute on the invoking test context
        request.cls.db = DummyDB()

This defines a fixture function ``db_class`` which - if used - is
called once for each test class and which sets the class-level
``db`` attribute to a ``DummyDB`` instance.  The fixture function
achieves this by receiving a special ``request`` object which gives
access to :ref:`the requesting test context <request-context>` such
as the ``cls`` attribute, denoting the class from which the fixture
is used.  This architecture de-couples fixture writing from actual test
code and allows reuse of the fixture by a minimal reference, the fixture
name.  So let's write an actual ``unittest.TestCase`` class using our
fixture definition:

.. code-block:: python

    # content of test_unittest_db.py

    import unittest

    import pytest


    @pytest.mark.usefixtures("db_class")
    class MyTest(unittest.TestCase):
        def test_method1(self):
            assert hasattr(self, "db")
            assert 0, self.db  # fail for demo purposes

        def test_method2(self):
            assert 0, self.db  # fail for demo purposes

The ``@pytest.mark.usefixtures("db_class")`` class-decorator makes sure that
the pytest fixture function ``db_class`` is called once per class.
Due to the deliberately failing assert statements, we can take a look at
the ``self.db`` values in the traceback:

.. code-block:: pytest

    $ pytest test_unittest_db.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    test_unittest_db.py FF                                               [100%]

    ================================= FAILURES =================================
    ___________________________ MyTest.test_method1 ____________________________

    self = <test_unittest_db.MyTest testMethod=test_method1>

        def test_method1(self):
            assert hasattr(self, "db")
    >       assert 0, self.db  # fail for demo purposes
            ^^^^^^^^^^^^^^^^^
    E       AssertionError: <conftest.db_class.<locals>.DummyDB object at 0xdeadbeef0001>
    E       assert 0

    test_unittest_db.py:11: AssertionError
    ___________________________ MyTest.test_method2 ____________________________

    self = <test_unittest_db.MyTest testMethod=test_method2>

        def test_method2(self):
    >       assert 0, self.db  # fail for demo purposes
            ^^^^^^^^^^^^^^^^^
    E       AssertionError: <conftest.db_class.<locals>.DummyDB object at 0xdeadbeef0001>
    E       assert 0

    test_unittest_db.py:14: AssertionError
    ========================= short test summary info ==========================
    FAILED test_unittest_db.py::MyTest::test_method1 - AssertionError: <conft...
    FAILED test_unittest_db.py::MyTest::test_method2 - AssertionError: <conft...
    ============================ 2 failed in 0.12s =============================

This default pytest traceback shows that the two test methods
share the same ``self.db`` instance which was our intention
when writing the class-scoped fixture function above.


Using autouse fixtures and accessing other fixtures
---------------------------------------------------

Although it's usually better to explicitly declare use of fixtures you need
for a given test, you may sometimes want to have fixtures that are
automatically used in a given context.  After all, the traditional
style of unittest-setup mandates the use of this implicit fixture writing
and chances are, you are used to it or like it.

You can flag fixture functions with ``@pytest.fixture(autouse=True)``
and define the fixture function in the context where you want it used.
Let's look at an ``initdir`` fixture which makes all test methods of a
``TestCase`` class execute in a temporary directory with a
pre-initialized ``samplefile.ini``.  Our ``initdir`` fixture itself uses
the pytest builtin :fixture:`tmp_path` fixture to delegate the
creation of a per-test temporary directory:

.. code-block:: python

    # content of test_unittest_cleandir.py
    import unittest

    import pytest


    class MyTest(unittest.TestCase):
        @pytest.fixture(autouse=True)
        def initdir(self, tmp_path, monkeypatch):
            monkeypatch.chdir(tmp_path)  # change to pytest-provided temporary directory
            tmp_path.joinpath("samplefile.ini").write_text("# testdata", encoding="utf-8")

        def test_method(self):
            with open("samplefile.ini", encoding="utf-8") as f:
                s = f.read()
            assert "testdata" in s

Due to the ``autouse`` flag the ``initdir`` fixture function will be
used for all methods of the class where it is defined.  This is a
shortcut for using a ``@pytest.mark.usefixtures("initdir")`` marker
on the class like in the previous example.

Running this test module ...:

.. code-block:: pytest

    $ pytest -q test_unittest_cleandir.py
    .                                                                    [100%]
    1 passed in 0.12s

... gives us one passed test because the ``initdir`` fixture function
was executed ahead of the ``test_method``.

.. note::

   ``unittest.TestCase`` methods cannot directly receive fixture
   arguments as implementing that is likely to inflict
   on the ability to run general unittest.TestCase test suites.

   The above ``usefixtures`` and ``autouse`` examples should help to mix in
   pytest fixtures into unittest suites.

   You can also gradually move away from subclassing from ``unittest.TestCase`` to *plain asserts*
   and then start to benefit from the full pytest feature set step by step.

.. _pdb-unittest-note:

.. note::

    Due to architectural differences between the two frameworks, setup and
    teardown for ``unittest``-based tests is performed during the ``call`` phase
    of testing instead of in ``pytest``'s standard ``setup`` and ``teardown``
    stages. This can be important to understand in some situations, particularly
    when reasoning about errors. For example, if a ``unittest``-based suite
    exhibits errors during setup, ``pytest`` will report no errors during its
    ``setup`` phase and will instead raise the error during ``call``.

# How to implement xunit-style set-up
Source: https://docs.pytest.org/en/stable/how-to/xunit_setup.html

.. _`classic xunit`:
.. _xunitsetup:

How to implement xunit-style set-up
========================================

This section describes a classic and popular way how you can implement
fixtures (setup and teardown test state) on a per-module/class/function basis.


.. note::

    While these setup/teardown methods are simple and familiar to those
    coming from a ``unittest`` or ``nose`` background, you may also consider
    using pytest's more powerful :ref:`fixture mechanism
    <fixture>` which leverages the concept of dependency injection, allowing
    for a more modular and more scalable approach for managing test state,
    especially for larger projects and for functional testing.  You can
    mix both fixture mechanisms in the same file but
    test methods of ``unittest.TestCase`` subclasses
    cannot receive fixture arguments.


Module level setup/teardown
--------------------------------------

If you have multiple test functions and test classes in a single
module you can optionally implement the following fixture methods
which will usually be called once for all the functions:

.. code-block:: python

    def setup_module(module):
        """setup any state specific to the execution of the given module."""


    def teardown_module(module):
        """teardown any state that was previously setup with a setup_module
        method.
        """

As of pytest-3.0, the ``module`` parameter is optional.

Class level setup/teardown
----------------------------------

Similarly, the following methods are called at class level before
and after all test methods of the class are called:

.. code-block:: python

    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """


    @classmethod
    def teardown_class(cls):
        """teardown any state that was previously setup with a call to
        setup_class.
        """

.. _xunit-method-setup:

Method and function level setup/teardown
-----------------------------------------------

Similarly, the following methods are called around each method invocation:

.. code-block:: python

    def setup_method(self, method):
        """setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """


    def teardown_method(self, method):
        """teardown any state that was previously setup with a setup_method
        call.
        """

As of pytest-3.0, the ``method`` parameter is optional.

If you would rather define test functions directly at module level
you can also use the following functions to implement fixtures:

.. code-block:: python

    def setup_function(function):
        """setup any state tied to the execution of the given function.
        Invoked for every test function in the module.
        """


    def teardown_function(function):
        """teardown any state that was previously setup with a setup_function
        call.
        """

As of pytest-3.0, the ``function`` parameter is optional.

Remarks:

* It is possible for setup/teardown pairs to be invoked multiple times
  per testing process.

* teardown functions are not called if the corresponding setup function existed
  and failed/was skipped.

* Prior to pytest-4.2, xunit-style functions did not obey the scope rules of fixtures, so
  it was possible, for example, for a ``setup_method`` to be called before a
  session-scoped autouse fixture.

  Now the xunit-style functions are integrated with the fixture mechanism and obey the proper
  scope rules of fixtures involved in the call.

# How to set up bash completion
Source: https://docs.pytest.org/en/stable/how-to/bash-completion.html

.. _bash_completion:

How to set up bash completion
=============================

When using bash as your shell, ``pytest`` can use argcomplete
(https://kislyuk.github.io/argcomplete/) for auto-completion.
For this ``argcomplete`` needs to be installed **and** enabled.

Install argcomplete using:

.. code-block:: bash

    sudo pip install 'argcomplete>=0.5.7'

For global activation of all argcomplete enabled python applications run:

.. code-block:: bash

    sudo activate-global-python-argcomplete

For permanent (but not global) ``pytest`` activation, use:

.. code-block:: bash

    register-python-argcomplete pytest >> ~/.bashrc

For one-time activation of argcomplete for ``pytest`` only, use:

.. code-block:: bash

    eval "$(register-python-argcomplete pytest)"

# Reference guides
Source: https://docs.pytest.org/en/stable/reference/index.html

:orphan:

.. _reference:

Reference guides
================

.. toctree::
   :maxdepth: 1

   reference
   fixtures
   customize
   exit-codes
   plugin_list

# API Reference
Source: https://docs.pytest.org/en/stable/reference/reference.html

:tocdepth: 3

.. _`api-reference`:

API Reference
=============

This page contains the full reference to pytest's API.


Constants
---------

pytest.__version__
~~~~~~~~~~~~~~~~~~

The current pytest version, as a string::

    >>> import pytest
    >>> pytest.__version__
    '9.0.2'

.. _`hidden-param`:

pytest.HIDDEN_PARAM
~~~~~~~~~~~~~~~~~~~

.. versionadded:: 8.4

Can be passed to ``ids`` of :py:func:`Metafunc.parametrize <pytest.Metafunc.parametrize>`
or to ``id`` of :func:`pytest.param` to hide a parameter set from the test name.
Can only be used at most 1 time, as test names need to be unique.

.. _`version-tuple`:

pytest.version_tuple
~~~~~~~~~~~~~~~~~~~~

.. versionadded:: 7.0

The current pytest version, as a tuple::

    >>> import pytest
    >>> pytest.version_tuple
    (7, 0, 0)

For pre-releases, the last component will be a string with the prerelease version::

    >>> import pytest
    >>> pytest.version_tuple
    (7, 0, '0rc1')


Functions
---------

pytest.approx
~~~~~~~~~~~~~

.. autofunction:: pytest.approx

pytest.fail
~~~~~~~~~~~

**Tutorial**: :ref:`skipping`

.. autofunction:: pytest.fail(reason, [pytrace=True])

.. class:: pytest.fail.Exception

    The exception raised by :func:`pytest.fail`.

pytest.skip
~~~~~~~~~~~

.. autofunction:: pytest.skip(reason, [allow_module_level=False])

.. class:: pytest.skip.Exception

    The exception raised by :func:`pytest.skip`.

.. _`pytest.importorskip ref`:

pytest.importorskip
~~~~~~~~~~~~~~~~~~~

.. autofunction:: pytest.importorskip

pytest.xfail
~~~~~~~~~~~~

.. autofunction:: pytest.xfail

.. class:: pytest.xfail.Exception

    The exception raised by :func:`pytest.xfail`.

pytest.exit
~~~~~~~~~~~

.. autofunction:: pytest.exit(reason, [returncode=None])

.. class:: pytest.exit.Exception

    The exception raised by :func:`pytest.exit`.

pytest.main
~~~~~~~~~~~

**Tutorial**: :ref:`pytest.main-usage`

.. autofunction:: pytest.main

pytest.param
~~~~~~~~~~~~

.. autofunction:: pytest.param(*values, [id], [marks])

pytest.raises
~~~~~~~~~~~~~

**Tutorial**: :ref:`assertraises`

.. autofunction:: pytest.raises(expected_exception: Exception [, *, match])
    :with: excinfo

pytest.deprecated_call
~~~~~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`ensuring_function_triggers`

.. autofunction:: pytest.deprecated_call([match])
    :with:

pytest.register_assert_rewrite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`assertion-rewriting`

.. autofunction:: pytest.register_assert_rewrite

pytest.register_fixture
~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: pytest.register_fixture

pytest.warns
~~~~~~~~~~~~

**Tutorial**: :ref:`assertwarnings`

.. autofunction:: pytest.warns(expected_warning: Exception, [match])
    :with:

pytest.freeze_includes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`freezing-pytest`

.. autofunction:: pytest.freeze_includes

.. _`marks ref`:

Marks
-----

Marks can be used to apply metadata to *test functions* (but not fixtures), which can then be accessed by
fixtures or plugins.




.. _`pytest.mark.filterwarnings ref`:

pytest.mark.filterwarnings
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`filterwarnings`

Add warning filters to marked test items.

.. py:function:: pytest.mark.filterwarnings(filter)

    :keyword str filter:
        A *warning specification string*, which is composed of contents of the tuple ``(action, message, category, module, lineno)``
        as specified in :ref:`python:warning-filter` section of
        the Python documentation, separated by ``":"``. Optional fields can be omitted.
        Module names passed for filtering are not regex-escaped.

        For example:

        .. code-block:: python

            @pytest.mark.filterwarnings(r"ignore:.*usage will be deprecated.*:DeprecationWarning")
            def test_foo(): ...


.. _`pytest.mark.parametrize ref`:

pytest.mark.parametrize
~~~~~~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`parametrize`

This mark has the same signature as :py:meth:`pytest.Metafunc.parametrize`; see there.


.. _`pytest.mark.skip ref`:

pytest.mark.skip
~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`skip`

Unconditionally skip a test function.

.. py:function:: pytest.mark.skip(reason=None)

    :keyword str reason: Reason why the test function is being skipped.


.. _`pytest.mark.skipif ref`:

pytest.mark.skipif
~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`skipif`

Skip a test function if a condition is ``True``.

.. py:function:: pytest.mark.skipif(condition, *, reason=None)

    :type condition: bool or str
    :param condition: ``True/False`` if the condition should be skipped or a :ref:`condition string <string conditions>`.
    :keyword str reason: Reason why the test function is being skipped.


.. _`pytest.mark.usefixtures ref`:

pytest.mark.usefixtures
~~~~~~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`usefixtures`

Mark a test function as using the given fixture names.

.. py:function:: pytest.mark.usefixtures(*names)

    :param args: The names of the fixture to use, as strings.

.. note::

    When using `usefixtures` in hooks, it can only load fixtures when applied to a test function before test setup
    (for example in the `pytest_collection_modifyitems` hook).

    Also note that this mark has no effect when applied to **fixtures**.



.. _`pytest.mark.xfail ref`:

pytest.mark.xfail
~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`xfail`

Marks a test function as *expected to fail*.

.. py:function:: pytest.mark.xfail(condition=False, *, reason=None, raises=None, run=True, strict=strict_xfail)

    :keyword Union[bool, str] condition:
        Condition for marking the test function as xfail (``True/False`` or a
        :ref:`condition string <string conditions>`). If a ``bool``, you also have
        to specify ``reason`` (see :ref:`condition string <string conditions>`).
    :keyword str reason:
        Reason why the test function is marked as xfail.
    :keyword raises:
        Exception class (or tuple of classes) expected to be raised by the test function; other exceptions will fail the test.
        Note that subclasses of the classes passed will also result in a match (similar to how the ``except`` statement works).
    :type raises: Type[:py:exc:`Exception`]

    :keyword bool run:
        Whether the test function should actually be executed. If ``False``, the function will always xfail and will
        not be executed (useful if a function is segfaulting).
    :keyword bool strict:
        * If ``False`` the function will be shown in the terminal output as ``xfailed`` if it fails
          and as ``xpass`` if it passes. In both cases this will not cause the test suite to fail as a whole. This
          is particularly useful to mark *flaky* tests (tests that fail at random) to be tackled later.
        * If ``True``, the function will be shown in the terminal output as ``xfailed`` if it fails, but if it
          unexpectedly passes then it will **fail** the test suite. This is particularly useful to mark functions
          that are always failing and there should be a clear indication if they unexpectedly start to pass (for example
          a new release of a library fixes a known bug).

        Defaults to :confval:`strict_xfail`, which is ``False`` by default.


Custom marks
~~~~~~~~~~~~

Marks are created dynamically using the factory object ``pytest.mark`` and applied as a decorator.

For example:

.. code-block:: python

    @pytest.mark.timeout(10, "slow", method="thread")
    def test_function(): ...

Will create and attach a :class:`Mark <pytest.Mark>` object to the collected
:class:`Item <pytest.Item>`, which can then be accessed by fixtures or hooks with
:meth:`Node.iter_markers <_pytest.nodes.Node.iter_markers>`. The ``mark`` object will have the following attributes:

.. code-block:: python

    mark.args == (10, "slow")
    mark.kwargs == {"method": "thread"}

Example for using multiple custom markers:

.. code-block:: python

    @pytest.mark.timeout(10, "slow", method="thread")
    @pytest.mark.slow
    def test_function(): ...

When :meth:`Node.iter_markers <_pytest.nodes.Node.iter_markers>` or :meth:`Node.iter_markers_with_node <_pytest.nodes.Node.iter_markers_with_node>` is used with multiple markers, the marker closest to the function will be iterated over first. The above example will result in ``@pytest.mark.slow`` followed by ``@pytest.mark.timeout(...)``.

.. _`fixtures-api`:

Fixtures
--------

**Tutorial**: :ref:`fixture`

Fixtures are requested by test functions or other fixtures by declaring them as argument names.


Example of a test requiring a fixture:

.. code-block:: python

    def test_output(capsys):
        print("hello")
        out, err = capsys.readouterr()
        assert out == "hello\n"


Example of a fixture requiring another fixture:

.. code-block:: python

    @pytest.fixture
    def db_session(tmp_path):
        fn = tmp_path / "db.file"
        return connect(fn)

For more details, consult the full :ref:`fixtures docs <fixture>`.


.. _`pytest.fixture-api`:

@pytest.fixture
~~~~~~~~~~~~~~~

.. autofunction:: pytest.fixture
    :decorator:


.. fixture:: capfd

capfd
~~~~~~

**Tutorial**: :ref:`captures`

.. autofunction:: _pytest.capture.capfd()
    :no-auto-options:


.. fixture:: capfdbinary

capfdbinary
~~~~~~~~~~~~

**Tutorial**: :ref:`captures`

.. autofunction:: _pytest.capture.capfdbinary()
    :no-auto-options:


.. fixture:: caplog

caplog
~~~~~~

**Tutorial**: :ref:`logging`

.. autofunction:: _pytest.logging.caplog()
    :no-auto-options:

    Returns a :class:`pytest.LogCaptureFixture` instance.

.. autoclass:: pytest.LogCaptureFixture()
    :members:


.. fixture:: capsys

capsys
~~~~~~

**Tutorial**: :ref:`captures`

.. autofunction:: _pytest.capture.capsys()
    :no-auto-options:

.. autoclass:: pytest.CaptureFixture()
    :members:

.. fixture:: capteesys

capteesys
~~~~~~~~~

**Tutorial**: :ref:`captures`

.. autofunction:: _pytest.capture.capteesys()
    :no-auto-options:

.. fixture:: capsysbinary

capsysbinary
~~~~~~~~~~~~

**Tutorial**: :ref:`captures`

.. autofunction:: _pytest.capture.capsysbinary()
    :no-auto-options:


.. fixture:: cache

config.cache
~~~~~~~~~~~~

**Tutorial**: :ref:`cache`

The ``config.cache`` object allows other plugins and fixtures
to store and retrieve values across test runs. To access it from fixtures
request ``pytestconfig`` into your fixture and get it with ``pytestconfig.cache``.

Under the hood, the cache plugin uses the simple
``dumps``/``loads`` API of the :py:mod:`json` stdlib module.

``config.cache`` is an instance of :class:`pytest.Cache`:

.. autoclass:: pytest.Cache()
   :members:


.. fixture:: doctest_namespace

doctest_namespace
~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`doctest`

.. autofunction:: _pytest.doctest.doctest_namespace()


.. fixture:: monkeypatch

monkeypatch
~~~~~~~~~~~

**Tutorial**: :ref:`monkeypatching`

.. autofunction:: _pytest.monkeypatch.monkeypatch()
    :no-auto-options:

    Returns a :class:`~pytest.MonkeyPatch` instance.

.. autoclass:: pytest.MonkeyPatch
    :members:


.. fixture:: pytestconfig

pytestconfig
~~~~~~~~~~~~

.. autofunction:: _pytest.fixtures.pytestconfig()


.. fixture:: pytester

pytester
~~~~~~~~

.. versionadded:: 6.2

Provides a :class:`~pytest.Pytester` instance that can be used to run and test pytest itself.

It provides an empty directory where pytest can be executed in isolation, and contains facilities
to write tests, configuration files, and match against expected output.

To use it, include in your topmost ``conftest.py`` file:

.. code-block:: python

    pytest_plugins = "pytester"



.. autoclass:: pytest.Pytester()
    :members:

.. autoclass:: pytest.RunResult()
    :members:

.. autoclass:: pytest.LineMatcher()
    :members:
    :special-members: __str__

.. autoclass:: pytest.HookRecorder()
    :members:

.. autoclass:: pytest.RecordedHookCall()
    :members:


.. fixture:: record_property

record_property
~~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`record_property example`

.. autofunction:: _pytest.junitxml.record_property()


.. fixture:: record_testsuite_property

record_testsuite_property
~~~~~~~~~~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`record_testsuite_property example`

.. autofunction:: _pytest.junitxml.record_testsuite_property()


.. fixture:: recwarn

recwarn
~~~~~~~

**Tutorial**: :ref:`recwarn`

.. autofunction:: _pytest.recwarn.recwarn()
    :no-auto-options:

.. autoclass:: pytest.WarningsRecorder()
    :members:
    :special-members: __getitem__, __iter__, __len__


.. fixture:: request

request
~~~~~~~

**Example**: :ref:`request example`

The ``request`` fixture is a special fixture providing information of the requesting test function.

.. autoclass:: pytest.FixtureRequest()
    :members:


.. fixture:: subtests

subtests
~~~~~~~~

The ``subtests`` fixture enables declaring subtests inside test functions.

**Tutorial**: :ref:`subtests`

.. autoclass:: pytest.Subtests()
    :members:


.. fixture:: testdir

testdir
~~~~~~~

Identical to :fixture:`pytester`, but provides an instance whose methods return
legacy ``py.path.local`` objects instead when applicable.

New code should avoid using :fixture:`testdir` in favor of :fixture:`pytester`.

.. autoclass:: pytest.Testdir()
    :members:
    :noindex: TimeoutExpired


.. fixture:: tmp_path

tmp_path
~~~~~~~~

**Tutorial**: :ref:`tmp_path`

.. autofunction:: _pytest.tmpdir.tmp_path()
    :no-auto-options:


.. fixture:: tmp_path_factory

tmp_path_factory
~~~~~~~~~~~~~~~~

**Tutorial**: :ref:`tmp_path_factory example`

.. _`tmp_path_factory factory api`:

``tmp_path_factory`` is an instance of :class:`~pytest.TempPathFactory`:

.. autoclass:: pytest.TempPathFactory()
    :members:


.. fixture:: tmpdir

tmpdir
~~~~~~

**Tutorial**: :ref:`tmpdir and tmpdir_factory`

.. autofunction:: _pytest.legacypath.LegacyTmpdirPlugin.tmpdir()
    :no-auto-options:


.. fixture:: tmpdir_factory

tmpdir_factory
~~~~~~~~~~~~~~

**Tutorial**: :ref:`tmpdir and tmpdir_factory`

``tmpdir_factory`` is an instance of :class:`~pytest.TempdirFactory`:

.. autoclass:: pytest.TempdirFactory()
    :members:


.. _`hook-reference`:

Hooks
-----

**Tutorial**: :ref:`writing-plugins`

Reference to all hooks which can be implemented by :ref:`conftest.py files <localplugin>` and :ref:`plugins <plugins>`.

@pytest.hookimpl
~~~~~~~~~~~~~~~~

.. function:: pytest.hookimpl
    :decorator:

    pytest's decorator for marking functions as hook implementations.

    See :ref:`writinghooks` and :func:`pluggy.HookimplMarker`.

@pytest.hookspec
~~~~~~~~~~~~~~~~

.. function:: pytest.hookspec
    :decorator:

    pytest's decorator for marking functions as hook specifications.

    See :ref:`declaringhooks` and :func:`pluggy.HookspecMarker`.

.. currentmodule:: _pytest.hookspec

Bootstrapping hooks
~~~~~~~~~~~~~~~~~~~

Bootstrapping hooks called for plugins registered early enough (internal and third-party plugins).

.. hook:: pytest_load_initial_conftests
.. autofunction:: pytest_load_initial_conftests
.. hook:: pytest_cmdline_parse
.. autofunction:: pytest_cmdline_parse
.. hook:: pytest_cmdline_main
.. autofunction:: pytest_cmdline_main

.. _`initialization-hooks`:

Initialization hooks
~~~~~~~~~~~~~~~~~~~~

Initialization hooks called for plugins and ``conftest.py`` files.

.. hook:: pytest_addoption
.. autofunction:: pytest_addoption
.. hook:: pytest_addhooks
.. autofunction:: pytest_addhooks
.. hook:: pytest_configure
.. autofunction:: pytest_configure
.. hook:: pytest_unconfigure
.. autofunction:: pytest_unconfigure
.. hook:: pytest_sessionstart
.. autofunction:: pytest_sessionstart
.. hook:: pytest_sessionfinish
.. autofunction:: pytest_sessionfinish

.. hook:: pytest_plugin_registered
.. autofunction:: pytest_plugin_registered

Collection hooks
~~~~~~~~~~~~~~~~

``pytest`` calls the following hooks for collecting files and directories:

.. hook:: pytest_collection
.. autofunction:: pytest_collection
.. hook:: pytest_ignore_collect
.. autofunction:: pytest_ignore_collect
.. hook:: pytest_collect_directory
.. autofunction:: pytest_collect_directory
.. hook:: pytest_collect_file
.. autofunction:: pytest_collect_file
.. hook:: pytest_pycollect_makemodule
.. autofunction:: pytest_pycollect_makemodule

For influencing the collection of objects in Python modules
you can use the following hook:

.. hook:: pytest_pycollect_makeitem
.. autofunction:: pytest_pycollect_makeitem
.. hook:: pytest_generate_tests
.. autofunction:: pytest_generate_tests
.. hook:: pytest_make_parametrize_id
.. autofunction:: pytest_make_parametrize_id

Hooks for influencing test skipping:

.. hook:: pytest_markeval_namespace
.. autofunction:: pytest_markeval_namespace

After collection is complete, you can modify the order of
items, delete or otherwise amend the test items:

.. hook:: pytest_collection_modifyitems
.. autofunction:: pytest_collection_modifyitems

.. note::
    If this hook is implemented in ``conftest.py`` files, it always receives all collected items, not only those
    under the ``conftest.py`` where it is implemented.

.. hook:: pytest_collection_finish
.. autofunction:: pytest_collection_finish

Test running (runtest) hooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All runtest related hooks receive a :py:class:`pytest.Item <pytest.Item>` object.

.. hook:: pytest_runtestloop
.. autofunction:: pytest_runtestloop
.. hook:: pytest_runtest_protocol
.. autofunction:: pytest_runtest_protocol
.. hook:: pytest_runtest_logstart
.. autofunction:: pytest_runtest_logstart
.. hook:: pytest_runtest_logfinish
.. autofunction:: pytest_runtest_logfinish
.. hook:: pytest_runtest_setup
.. autofunction:: pytest_runtest_setup
.. hook:: pytest_runtest_call
.. autofunction:: pytest_runtest_call
.. hook:: pytest_runtest_teardown
.. autofunction:: pytest_runtest_teardown
.. hook:: pytest_runtest_makereport
.. autofunction:: pytest_runtest_makereport

For deeper understanding you may look at the default implementation of
these hooks in ``_pytest.runner`` and maybe also
in ``_pytest.pdb`` which interacts with ``_pytest.capture``
and its input/output capturing in order to immediately drop
into interactive debugging when a test failure occurs.

.. hook:: pytest_pyfunc_call
.. autofunction:: pytest_pyfunc_call

Reporting hooks
~~~~~~~~~~~~~~~

Session related reporting hooks:

.. hook:: pytest_collectstart
.. autofunction:: pytest_collectstart
.. hook:: pytest_make_collect_report
.. autofunction:: pytest_make_collect_report
.. hook:: pytest_itemcollected
.. autofunction:: pytest_itemcollected
.. hook:: pytest_collectreport
.. autofunction:: pytest_collectreport
.. hook:: pytest_deselected
.. autofunction:: pytest_deselected
.. hook:: pytest_report_header
.. autofunction:: pytest_report_header
.. hook:: pytest_report_collectionfinish
.. autofunction:: pytest_report_collectionfinish
.. hook:: pytest_report_teststatus
.. autofunction:: pytest_report_teststatus
.. hook:: pytest_report_to_serializable
.. autofunction:: pytest_report_to_serializable
.. hook:: pytest_report_from_serializable
.. autofunction:: pytest_report_from_serializable
.. hook:: pytest_terminal_summary
.. autofunction:: pytest_terminal_summary
.. hook:: pytest_fixture_setup
.. autofunction:: pytest_fixture_setup
.. hook:: pytest_fixture_post_finalizer
.. autofunction:: pytest_fixture_post_finalizer
.. hook:: pytest_warning_recorded
.. autofunction:: pytest_warning_recorded

Central hook for reporting about test execution:

.. hook:: pytest_runtest_logreport
.. autofunction:: pytest_runtest_logreport

Assertion related hooks:

.. hook:: pytest_assertrepr_compare
.. autofunction:: pytest_assertrepr_compare
.. hook:: pytest_assertion_pass
.. autofunction:: pytest_assertion_pass


Debugging/Interaction hooks
~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are few hooks which can be used for special
reporting or interaction with exceptions:

.. hook:: pytest_internalerror
.. autofunction:: pytest_internalerror
.. hook:: pytest_keyboard_interrupt
.. autofunction:: pytest_keyboard_interrupt
.. hook:: pytest_exception_interact
.. autofunction:: pytest_exception_interact
.. hook:: pytest_enter_pdb
.. autofunction:: pytest_enter_pdb
.. hook:: pytest_leave_pdb
.. autofunction:: pytest_leave_pdb


Collection tree objects
-----------------------

These are the collector and item classes (collectively called "nodes") which
make up the collection tree.

Node
~~~~

.. autoclass:: _pytest.nodes.Node()
    :members:
    :show-inheritance:

Collector
~~~~~~~~~

.. autoclass:: pytest.Collector()
    :members:
    :show-inheritance:

Item
~~~~

.. autoclass:: pytest.Item()
    :members:
    :show-inheritance:

File
~~~~

.. autoclass:: pytest.File()
    :members:
    :show-inheritance:

FSCollector
~~~~~~~~~~~

.. autoclass:: _pytest.nodes.FSCollector()
    :members:
    :show-inheritance:

Session
~~~~~~~

.. autoclass:: pytest.Session()
    :members:
    :show-inheritance:

Package
~~~~~~~

.. autoclass:: pytest.Package()
    :members:
    :show-inheritance:

Module
~~~~~~

.. autoclass:: pytest.Module()
    :members:
    :show-inheritance:

Class
~~~~~

.. autoclass:: pytest.Class()
    :members:
    :show-inheritance:

Function
~~~~~~~~

.. autoclass:: pytest.Function()
    :members:
    :show-inheritance:

FunctionDefinition
~~~~~~~~~~~~~~~~~~

.. autoclass:: _pytest.python.FunctionDefinition()
    :members:
    :show-inheritance:


Objects
-------

Objects accessible from :ref:`fixtures <fixture>` or :ref:`hooks <hook-reference>`
or importable from ``pytest``.


CallInfo
~~~~~~~~

.. autoclass:: pytest.CallInfo()
    :members:

CollectReport
~~~~~~~~~~~~~

.. autoclass:: pytest.CollectReport()
    :members:
    :show-inheritance:
    :inherited-members:

Config
~~~~~~

.. autoclass:: pytest.Config()
    :members:

Dir
~~~

.. autoclass:: pytest.Dir()
    :members:

Directory
~~~~~~~~~

.. autoclass:: pytest.Directory()
    :members:

ExceptionInfo
~~~~~~~~~~~~~

.. autoclass:: pytest.ExceptionInfo()
    :members:


ExitCode
~~~~~~~~

.. autoclass:: pytest.ExitCode
    :members:


FixtureDef
~~~~~~~~~~

.. autoclass:: pytest.FixtureDef()
    :members:
    :show-inheritance:

MarkDecorator
~~~~~~~~~~~~~

.. autoclass:: pytest.MarkDecorator()
    :members:


MarkGenerator
~~~~~~~~~~~~~

.. autoclass:: pytest.MarkGenerator()
    :members:


Mark
~~~~

.. autoclass:: pytest.Mark()
    :members:


Metafunc
~~~~~~~~

.. autoclass:: pytest.Metafunc()
    :members:

Parser
~~~~~~

.. autoclass:: pytest.Parser()
    :members:

OptionGroup
~~~~~~~~~~~

.. autoclass:: pytest.OptionGroup()
    :members:

PytestPluginManager
~~~~~~~~~~~~~~~~~~~

.. autoclass:: pytest.PytestPluginManager()
    :members:
    :undoc-members:
    :inherited-members:
    :show-inheritance:

RaisesExc
~~~~~~~~~

.. autoclass:: pytest.RaisesExc()
    :members:

    .. autoattribute:: fail_reason

RaisesGroup
~~~~~~~~~~~
**Tutorial**: :ref:`assert-matching-exception-groups`

.. autoclass:: pytest.RaisesGroup()
    :members:

    .. autoattribute:: fail_reason

TerminalReporter
~~~~~~~~~~~~~~~~

.. autoclass:: pytest.TerminalReporter
    :members:
    :inherited-members:

TestReport
~~~~~~~~~~

.. autoclass:: pytest.TestReport()
    :members:
    :show-inheritance:
    :inherited-members:

TestShortLogReport
~~~~~~~~~~~~~~~~~~

.. autoclass:: pytest.TestShortLogReport()
    :members:

Result
~~~~~~~

Result object used within :ref:`hook wrappers <hookwrapper>`, see :py:class:`Result in the pluggy documentation <pluggy.Result>` for more information.

Stash
~~~~~

.. autoclass:: pytest.Stash
    :special-members: __setitem__, __getitem__, __delitem__, __contains__, __len__
    :members:

.. autoclass:: pytest.StashKey
    :show-inheritance:
    :members:


Global Variables
----------------

pytest treats some global variables in a special manner when defined in a test module or
``conftest.py`` files.


.. globalvar:: collect_ignore

**Tutorial**: :ref:`customizing-test-collection`

Can be declared in *conftest.py files* to exclude test directories or modules.
Needs to be a list of paths (``str``, :class:`pathlib.Path` or any :class:`os.PathLike`).

.. code-block:: python

  collect_ignore = ["setup.py"]


.. globalvar:: collect_ignore_glob

**Tutorial**: :ref:`customizing-test-collection`

Can be declared in *conftest.py files* to exclude test directories or modules
with Unix shell-style wildcards. Needs to be ``list[str]`` where ``str`` can
contain glob patterns.

.. code-block:: python

  collect_ignore_glob = ["*_ignore.py"]


.. globalvar:: pytest_plugins

**Tutorial**: :ref:`available installable plugins`

Can be declared at the **global** level in *test modules* and *conftest.py files* to register additional plugins.
Can be either a ``str`` or ``Sequence[str]``.

.. code-block:: python

    pytest_plugins = "myapp.testsupport.myplugin"

.. code-block:: python

    pytest_plugins = ("myapp.testsupport.tools", "myapp.testsupport.regression")


.. globalvar:: pytestmark

**Tutorial**: :ref:`scoped-marking`

Can be declared at the **global** level in *test modules* to apply one or more :ref:`marks <marks ref>` to all
test functions and methods. Can be either a single mark or a list of marks (applied in left-to-right order).

.. code-block:: python

    import pytest

    pytestmark = pytest.mark.webtest


.. code-block:: python

    import pytest

    pytestmark = [pytest.mark.integration, pytest.mark.slow]


Environment Variables
---------------------

Environment variables that can be used to change pytest's behavior.

.. envvar:: CI

   When set to a non-empty value, pytest acknowledges that it is running in a CI process. See also :ref:`ci-pipelines`.

.. envvar:: BUILD_NUMBER

   When set to a non-empty value, pytest acknowledges that it is running in a CI process. Alternative to :envvar:`CI`. See also :ref:`ci-pipelines`.

.. envvar:: PYTEST_ADDOPTS

   This contains a command-line (parsed by the py:mod:`shlex` module) that will be **prepended** to the command line given
   by the user, see :ref:`adding default options` for more information.

.. envvar:: PYTEST_VERSION

   This environment variable is defined at the start of the pytest session and is undefined afterwards.
   It contains the value of ``pytest.__version__``, and among other things can be used to easily check if a code is running from within a pytest run.

.. envvar:: PYTEST_CURRENT_TEST

   This is not meant to be set by users, but is set by pytest internally with the name of the current test so other
   processes can inspect it, see :ref:`pytest current test env` for more information.

.. envvar:: PYTEST_DEBUG

   When set, pytest will print tracing and debug information.

.. envvar:: PYTEST_DEBUG_TEMPROOT

   Root for temporary directories produced by fixtures like :fixture:`tmp_path`
   as discussed in :ref:`temporary directory location and retention`.

.. envvar:: PYTEST_DISABLE_PLUGIN_AUTOLOAD

   When set, disables plugin auto-loading through :std:doc:`entry point packaging
   metadata <packaging:guides/creating-and-discovering-plugins>`. Only plugins
   explicitly specified in :envvar:`PYTEST_PLUGINS` or with :option:`-p` will be loaded.
   See also :ref:`--disable-plugin-autoload <disable_plugin_autoload>`.

.. envvar:: PYTEST_PLUGINS

   Contains comma-separated list of modules that should be loaded as plugins:

   .. code-block:: bash

       export PYTEST_PLUGINS=mymodule.plugin,xdist

   See also :option:`-p`.

.. envvar:: PYTEST_THEME

   Sets a `pygment style <https://pygments.org/docs/styles/>`_ to use for the code output.

.. envvar:: PYTEST_THEME_MODE

   Sets the :envvar:`PYTEST_THEME` to be either *dark* or *light*.

.. envvar:: PY_COLORS

   When set to ``1``, pytest will use color in terminal output.
   When set to ``0``, pytest will not use color.
   ``PY_COLORS`` takes precedence over ``NO_COLOR`` and ``FORCE_COLOR``.

.. envvar:: NO_COLOR

   When set to a non-empty string (regardless of value), pytest will not use color in terminal output.
   ``PY_COLORS`` takes precedence over ``NO_COLOR``, which takes precedence over ``FORCE_COLOR``.
   See `no-color.org <https://no-color.org/>`__ for other libraries supporting this community standard.

.. envvar:: FORCE_COLOR

   When set to a non-empty string (regardless of value), pytest will use color in terminal output.
   ``PY_COLORS`` and ``NO_COLOR`` take precedence over ``FORCE_COLOR``.

Exceptions
----------

.. autoexception:: pytest.UsageError()
    :show-inheritance:

.. autoexception:: pytest.FixtureLookupError()
    :show-inheritance:

.. _`warnings ref`:

Warnings
--------

Custom warnings generated in some situations such as improper usage or deprecated features.

.. autoclass:: pytest.PytestWarning
   :show-inheritance:

.. autoclass:: pytest.PytestAssertRewriteWarning
   :show-inheritance:

.. autoclass:: pytest.PytestCacheWarning
   :show-inheritance:

.. autoclass:: pytest.PytestCollectionWarning
   :show-inheritance:

.. autoclass:: pytest.PytestConfigWarning
   :show-inheritance:

.. autoclass:: pytest.PytestDeprecationWarning
   :show-inheritance:

.. autoclass:: pytest.PytestExperimentalApiWarning
   :show-inheritance:

.. autoclass:: pytest.PytestReturnNotNoneWarning
  :show-inheritance:

.. autoclass:: pytest.PytestRemovedIn10Warning
  :show-inheritance:

.. autoclass:: pytest.PytestUnknownMarkWarning
   :show-inheritance:

.. autoclass:: pytest.PytestUnraisableExceptionWarning
   :show-inheritance:

.. autoclass:: pytest.PytestUnhandledThreadExceptionWarning
   :show-inheritance:


Consult the :ref:`internal-warnings` section in the documentation for more information.


.. _`ini options ref`:

Configuration Options
---------------------

Here is a list of builtin configuration options that may be written in a ``pytest.ini`` (or ``.pytest.ini``),
``pyproject.toml``, ``tox.ini``, or ``setup.cfg`` file, usually located at the root of your repository.

To see each file format in detail, see :ref:`config file formats`.

.. warning::
    Usage of ``setup.cfg`` is not recommended except for very simple use cases. ``.cfg``
    files use a different parser than ``pytest.ini`` and ``tox.ini`` which might cause hard to track
    down problems.
    When possible, it is recommended to use the latter files, or ``pytest.toml`` or ``pyproject.toml``, to hold your pytest configuration.

Configuration options may be overwritten in the command-line by using ``-o/--override-ini``, which can also be
passed multiple times. The expected format is ``name=value``. For example::

   pytest -o console_output_style=classic -o cache_dir=/tmp/mycache


.. confval:: addopts
   :type: ``list[str]``

   Add the specified ``OPTS`` to the set of command line arguments as if they
   had been specified by the user. Example: if you have this configuration file content:

   .. code-block:: toml

        # content of pytest.toml
        [pytest]
        addopts = ["--maxfail=2", "-rf"]  # exit after 2 failures, report fail info

   issuing ``pytest test_hello.py`` actually means:

   .. code-block:: bash

        pytest --maxfail=2 -rf test_hello.py


.. confval:: cache_dir
   :type: ``str``
   :default: ``".pytest_cache"``

   Sets the directory where the cache plugin's content is stored.
   Directory may be relative or absolute path. If setting relative path, then directory is created
   relative to :ref:`rootdir <rootdir>`. Additionally, a path may contain environment
   variables, that will be expanded. For more information about cache plugin
   please refer to :ref:`cache_provider`.

.. confval:: collect_imported_tests
   :type: ``bool``
   :default: ``true``

   .. versionadded:: 8.4

   Setting this to ``false`` will make pytest collect classes/functions from test
   files **only** if they are defined in that file (as opposed to imported there).

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            collect_imported_tests = false

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            collect_imported_tests = false

   pytest traditionally collects classes/functions in the test module namespace even if they are imported from another file.

   For example:

   .. code-block:: python

       # contents of src/domain.py
       class Testament: ...


       # contents of tests/test_testament.py
       from domain import Testament


       def test_testament(): ...

   In this scenario, with the default options, pytest will collect the class `Testament` from `tests/test_testament.py` because it starts with `Test`, even though in this case it is a production class being imported in the test module namespace.

   Set ``collected_imported_tests`` to ``false`` in the configuration file prevents that.

.. confval:: consider_namespace_packages
   :type: ``bool``
   :default: ``false``

   Controls if pytest should attempt to identify `namespace packages <https://packaging.python.org/en/latest/guides/packaging-namespace-packages>`__
   when collecting Python modules.

   Set to ``True`` if the package you are testing is part of a namespace package.
   Namespace packages are also supported as :option:`--pyargs` target.

   Only `native namespace packages <https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#native-namespace-packages>`__
   are supported, with no plans to support `legacy namespace packages <https://packaging.python.org/en/latest/guides/packaging-namespace-packages/#legacy-namespace-packages>`__.

   For best results when using `consider_namespace_packages`,
   pytest needs to be able to import your namespace packages.
   This is best achieved by installing the packages in your environment,
   most commonly in `"editable" mode <https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#working-in-development-mode>`_.
   If you can't install the packages, consider adding the namespace root paths to :confval:`pythonpath`.

   .. versionadded:: 8.1

.. confval:: console_output_style
   :type: ``str``
   :default: ``"progress"``

   Sets the console output style while running tests:

   * ``classic``: classic pytest output.
   * ``progress``: like classic pytest output, but with a progress indicator.
   * ``progress-even-when-capture-no``: allows the use of the progress indicator even when ``capture=no``.
   * ``count``: like progress, but shows progress as the number of tests completed instead of a percent.
   * ``times``: show tests duration.

   You can fallback to ``classic`` if you prefer or
   the new mode is causing unexpected problems:

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            console_output_style = "classic"

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            console_output_style = classic


.. confval:: disable_test_id_escaping_and_forfeit_all_rights_to_community_support
   :type: ``bool``
   :default: ``false``

   .. versionadded:: 4.4

   pytest by default escapes any non-ascii characters used in unicode strings
   for the parametrization because it has several downsides.
   If however you would like to use unicode strings in parametrization
   and see them in the terminal as is (non-escaped), use this option
   in your configuration file:

   .. tab:: toml

       .. code-block:: toml

           [pytest]
           disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true

   .. tab:: ini

       .. code-block:: ini

           [pytest]
           disable_test_id_escaping_and_forfeit_all_rights_to_community_support = true

   Keep in mind however that this might cause unwanted side effects and
   even bugs depending on the OS used and plugins currently installed,
   so use it at your own risk.

   See :ref:`parametrizemark`.

.. confval:: doctest_encoding
   :type: ``str``
   :default: ``"utf-8"``

   Default encoding to use to decode text files with docstrings.
   :ref:`See how pytest handles doctests <doctest>`.


.. confval:: doctest_optionflags
   :type: ``list[str]``

   One or more doctest flag names from the standard ``doctest`` module.
   :ref:`See how pytest handles doctests <doctest>`.


.. confval:: empty_parameter_set_mark
    :type: ``str``
    :default: ``"skip"``

    Allows to pick the action for empty parametersets in parameterization

    * ``skip`` skips tests with an empty parameterset
    * ``xfail`` marks tests with an empty parameterset as xfail(run=False)
    * ``fail_at_collect`` raises an exception if parametrize collects an empty parameter set

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            empty_parameter_set_mark = "xfail"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            empty_parameter_set_mark = xfail

    .. note::

      The default value of this option is planned to change to ``xfail`` in future releases
      as this is considered less error prone, see :issue:`3155` for more details.


.. confval:: enable_assertion_pass_hook
   :type: ``bool``
   :default: ``false``

   Enables the :hook:`pytest_assertion_pass` hook.
   Make sure to delete any previously generated ``.pyc`` cache files.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            enable_assertion_pass_hook = true

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            enable_assertion_pass_hook = true


.. confval:: faulthandler_exit_on_timeout
   :type: ``bool``
   :default: ``false``

   Exit the pytest process after the per-test timeout is reached by passing
   `exit=True` to the :func:`faulthandler.dump_traceback_later` function. This
   is particularly useful to avoid wasting CI resources for test suites that
   are prone to putting the main Python interpreter into a deadlock state.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            faulthandler_timeout = 5
            faulthandler_exit_on_timeout = true

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            faulthandler_timeout = 5
            faulthandler_exit_on_timeout = true



.. confval:: faulthandler_timeout
   :type: ``float``
   :default: ``0`` (disabled)

   Dumps the tracebacks of all threads if a test takes longer than ``X`` seconds to run (including
   fixture setup and teardown). Implemented using the :func:`faulthandler.dump_traceback_later` function,
   so all caveats there apply.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            faulthandler_timeout = 5

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            faulthandler_timeout = 5

   For more information please refer to :ref:`faulthandler`.


.. confval:: filterwarnings
   :type: ``list[str]``

   Sets a list of filters and actions that should be taken for matched
   warnings. By default all warnings emitted during the test session
   will be displayed in a summary at the end of the test session.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            filterwarnings = [
                'error',
                'ignore::DeprecationWarning',
                # Note the use of single quote below to denote "raw" strings in TOML.
                'ignore:function ham\(\) should not be used:UserWarning',
            ]

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            filterwarnings =
                error
                ignore::DeprecationWarning
                ignore:function ham\(\) should not be used:UserWarning

   This tells pytest to ignore deprecation warnings and turn all other warnings
   into errors. For more information please refer to :ref:`warnings`.


.. confval:: max_warnings
   :type: ``int``

   .. versionadded:: 9.1

   Maximum number of warnings allowed before the test run is considered a failure.
   When all tests pass, but the total number of warnings exceeds this value, pytest exits with
   :class:`pytest.ExitCode` ``MAX_WARNINGS_ERROR`` (code ``6``).

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            max_warnings = 10

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            max_warnings = 10

   Note that :confval:`filtered warnings <filterwarnings>` do not count toward this maximum total.

   Can also be set via the :option:`--max-warnings` command-line option.


.. confval:: junit_duration_report
    :type: ``str``
    :default: ``"total"``

    .. versionadded:: 4.1

    Configures how durations are recorded into the JUnit XML report:

    * ``total``: duration times reported include setup, call, and teardown times.
    * ``call``: duration times reported include only call times, excluding setup and teardown.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            junit_duration_report = "call"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            junit_duration_report = call


.. confval:: junit_family
    :type: ``str``
    :default: ``"xunit2"``

    .. versionadded:: 4.2
    .. versionchanged:: 6.1
        Default changed to ``xunit2``.

    Configures the format of the generated JUnit XML file. The possible options are:

    * ``xunit1`` (or ``legacy``): produces old style output, compatible with the xunit 1.0 format.
    * ``xunit2``: produces `xunit 2.0 style output <https://github.com/jenkinsci/xunit-plugin/blob/xunit-2.3.2/src/main/resources/org/jenkinsci/plugins/xunit/types/model/xsd/junit-10.xsd>`__, which should be more compatible with latest Jenkins versions.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            junit_family = "xunit2"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            junit_family = xunit2


.. confval:: junit_log_passing_tests
    :type: ``bool``
    :default: ``true``

    .. versionadded:: 4.6

    If ``junit_logging != "no"``, configures if the captured output should be written
    to the JUnit XML file for **passing** tests.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            junit_log_passing_tests = false

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            junit_log_passing_tests = False


.. confval:: junit_logging
    :type: ``str``
    :default: ``"no"``

    .. versionadded:: 3.5
    .. versionchanged:: 5.4
        ``log``, ``all``, ``out-err`` options added.

    Configures if captured output should be written to the JUnit XML file. Valid values are:

    * ``log``: write only ``logging`` captured output.
    * ``system-out``: write captured ``stdout`` contents.
    * ``system-err``: write captured ``stderr`` contents.
    * ``out-err``: write both captured ``stdout`` and ``stderr`` contents.
    * ``all``: write captured ``logging``, ``stdout`` and ``stderr`` contents.
    * ``no``: no captured output is written.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            junit_logging = "system-out"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            junit_logging = system-out


.. confval:: junit_suite_name
    :type: ``str``
    :default: ``"pytest"``

    To set the name of the root test suite xml item, you can configure the ``junit_suite_name`` option in your config file:

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            junit_suite_name = "my_suite"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            junit_suite_name = my_suite

.. confval:: log_auto_indent
    :type: ``str``
    :default: ``"false"``

    Allow selective auto-indentation of multiline log messages.

    Supports command line option :option:`--log-auto-indent=[value]`
    and config option ``log_auto_indent = [value]`` to set the
    auto-indentation behavior for all logging.

    ``[value]`` can be:
        * "True" or "On" - Dynamically auto-indent multiline log messages
        * "False" or "Off" or "0" - Do not auto-indent multiline log messages
        * "[positive integer]" - auto-indent multiline log messages by [value] spaces

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_auto_indent = "false"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_auto_indent = false

    Supports passing kwarg ``extra={"auto_indent": [value]}`` to
    calls to ``logging.log()`` to specify auto-indentation behavior for
    a specific entry in the log. ``extra`` kwarg overrides the value specified
    on the command line or in the config.

.. confval:: log_cli
    :type: ``bool``
    :default: ``false``

    Enable log display during test run (also known as :ref:`"live logging" <live_logs>`).

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_cli = true

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_cli = true

.. confval:: log_cli_date_format
    :type: ``str``
    :default: Fallback to ``log_date_format``

    Sets a :py:func:`time.strftime`-compatible string that will be used when formatting dates for live logging.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_cli_date_format = "%Y-%m-%d %H:%M:%S"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_cli_date_format = %Y-%m-%d %H:%M:%S

    For more information, see :ref:`live_logs`.

.. confval:: log_cli_format
    :type: ``str``
    :default: Fallback to ``log_format``

    Sets a :py:mod:`logging`-compatible string used to format live logging messages.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_cli_format = "%(asctime)s %(levelname)s %(message)s"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_cli_format = %(asctime)s %(levelname)s %(message)s

    For more information, see :ref:`live_logs`.


.. confval:: log_cli_level
    :type: ``str``
    :default: Fallback to ``log_level``

    Sets the minimum log message level that should be captured for live logging. The integer value or
    the names of the levels can be used. Note in TOML the integer must be quoted, as there is no support
    for config parameters of mixed type.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_cli_level = "INFO"
            log_cli_level = "10"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_cli_level = INFO
            log_cli_level = 10

    For more information, see :ref:`live_logs`.


.. confval:: log_date_format
    :type: ``str``
    :default: ``"%H:%M:%S"``

    Sets a :py:func:`time.strftime`-compatible string that will be used when formatting dates for logging capture.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_date_format = "%Y-%m-%d %H:%M:%S"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_date_format = %Y-%m-%d %H:%M:%S

    For more information, see :ref:`logging`.


.. confval:: log_file
    :type: ``str``

    Sets a file name relative to the current working directory where log messages should be written to, in addition
    to the other logging facilities that are active.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_file = "logs/pytest-logs.txt"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_file = logs/pytest-logs.txt

    For more information, see :ref:`logging`.


.. confval:: log_file_date_format
    :type: ``str``
    :default: Fallback to ``log_date_format``

    Sets a :py:func:`time.strftime`-compatible string that will be used when formatting dates for the logging file.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_file_date_format = "%Y-%m-%d %H:%M:%S"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_file_date_format = %Y-%m-%d %H:%M:%S

    For more information, see :ref:`logging`.

.. confval:: log_file_format
    :type: ``str``
    :default: Fallback to ``log_format``

    Sets a :py:mod:`logging`-compatible string used to format logging messages redirected to the logging file.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_file_format = "%(asctime)s %(levelname)s %(message)s"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_file_format = %(asctime)s %(levelname)s %(message)s

    For more information, see :ref:`logging`.

.. confval:: log_file_level
    :type: ``str``
    :default: Fallback to ``log_level``

    Sets the minimum log message level that should be captured for the logging file.
    The integer value (in TOML, as a string) or the names of the levels can be used.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_file_level = "INFO"
            log_cli_level = "10"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_file_level = INFO
            log_cli_level = 10

    For more information, see :ref:`logging`.


.. confval:: log_file_mode
    :type: ``str``
    :default: ``"w"``

    Sets the mode that the logging file is opened with.
    The options are ``"w"`` to recreate the file or ``"a"`` to append to the file.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_file_mode = "a"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_file_mode = a

    For more information, see :ref:`logging`.


.. confval:: log_format
    :type: ``str``
    :default: ``%(levelname)-8s %(name)s:%(filename)s:%(lineno)d %(message)s``

    Sets a :py:mod:`logging`-compatible string used to format captured logging messages.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_format = "%(asctime)s %(levelname)s %(message)s"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_format = %(asctime)s %(levelname)s %(message)s

    For more information, see :ref:`logging`.


.. confval:: log_level
    :type: ``str``

    Sets the minimum log message level that should be captured for logging capture.
    Not set by default, so it depends on the root/parent log handler's effective level,
    where it is ``"WARNING"`` by default.
    The integer value (in TOML, as a string) or the names of the levels can be used.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            log_level = "INFO"
            log_cli_level = "10"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            log_level = INFO
            log_cli_level = 10

    For more information, see :ref:`logging`.


.. confval:: markers
    :type: ``list[str]``

    When the :confval:`strict_markers` configuration option is set,
    only known markers - defined in code by core pytest or some plugin - are allowed.

    You can list additional markers in this setting to add them to the whitelist,
    in which case you probably want to set :confval:`strict_markers` to ``true``
    to avoid future regressions:

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            addopts = ["--strict-markers"]
            markers = ["slow", "serial"]

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            strict_markers = true
            markers =
                slow
                serial


.. confval:: minversion
   :type: ``str``

   Specifies a minimal pytest version required for running tests.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            minversion = 3.0  # will fail if we run with pytest-2.8

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            minversion = 3.0  # will fail if we run with pytest-2.8


.. confval:: norecursedirs
   :type: ``list[str]``
   :default: ``["*.egg", ".*", "_darcs", "build", "CVS", "dist", "node_modules", "venv", "{arch}"]``

   Set the directory basename patterns to avoid when recursing
   for test discovery.  The individual (fnmatch-style) patterns are
   applied to the basename of a directory to decide if to recurse into it.
   Pattern matching characters::

        *       matches everything
        ?       matches any single character
        [seq]   matches any character in seq
        [!seq]  matches any char not in seq

   Setting a ``norecursedirs`` replaces the default.  Here is an example of
   how to avoid certain directories:

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            norecursedirs = [".svn", "_build", "tmp*"]

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            norecursedirs = .svn _build tmp*

   This would tell ``pytest`` to not look into typical subversion or
   sphinx-build directories or into any ``tmp`` prefixed directory.

   Additionally, ``pytest`` will attempt to intelligently identify and ignore
   a virtualenv.  Any directory deemed to be the root of a virtual environment
   will not be considered during test collection unless
   :option:`--collect-in-virtualenv` is given.  Note also that ``norecursedirs``
   takes precedence over ``--collect-in-virtualenv``; e.g. if you intend to
   run tests in a virtualenv with a base directory that matches ``'.*'`` you
   *must* override ``norecursedirs`` in addition to using the
   ``--collect-in-virtualenv`` flag.


.. confval:: python_classes
   :type: ``list[str]``
   :default: ``["Test"]``

   One or more name prefixes or glob-style patterns determining which classes
   are considered for test collection. Search for multiple glob patterns by
   adding a space between patterns. By default, pytest will consider any
   class prefixed with ``Test`` as a test collection.  Here is an example of how
   to collect tests from classes that end in ``Suite``:

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            python_classes = ["*Suite"]

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            python_classes = *Suite

   Note that ``unittest.TestCase`` derived classes are always collected
   regardless of this option, as ``unittest``'s own collection framework is used
   to collect those tests.


.. confval:: python_files
   :type: ``list[str]``
   :default: ``["test_*.py", "*_test.py"]``

   One or more Glob-style file patterns determining which python files
   are considered as test modules. Search for multiple glob patterns by
   adding a space between patterns:

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            python_files = ["test_*.py", "check_*.py", "example_*.py"]

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            python_files = test_*.py check_*.py example_*.py

       Or one per line:

       .. code-block:: ini

            [pytest]
            python_files =
                test_*.py
                check_*.py
                example_*.py



.. confval:: python_functions
   :type: ``list[str]``
   :default: ``["test"]``

   One or more name prefixes or glob-patterns determining which test functions
   and methods are considered tests. Search for multiple glob patterns by
   adding a space between patterns. By default, pytest will consider any
   function prefixed with ``test`` as a test.  Here is an example of how
   to collect test functions and methods that end in ``_test``:

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            python_functions = ["*_test"]

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            python_functions = *_test

   Note that this has no effect on methods that live on a ``unittest.TestCase``
   derived class, as ``unittest``'s own collection framework is used
   to collect those tests.

   See :ref:`change naming conventions` for more detailed examples.


.. confval:: pythonpath
   :type: ``list[str]``

   Sets list of directories that should be added to the python search path.
   Directories will be added to the head of :data:`sys.path`.
   Similar to the :envvar:`PYTHONPATH` environment variable, the directories will be
   included in where Python will look for imported modules.
   Paths are relative to the :ref:`rootdir <rootdir>` directory.
   Directories remain in path for the duration of the test session.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            pythonpath = ["src1", "src2"]

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            pythonpath = src1 src2


.. confval:: required_plugins
   :type: ``list[str]``

   A space separated list of plugins that must be present for pytest to run.
   Plugins can be listed with or without version specifiers directly following
   their name. Whitespace between different version specifiers is not allowed.
   If any one of the plugins is not found, emit an error.

   .. tab:: toml

       .. code-block:: toml

           [pytest]
           required_plugins = ["pytest-django>=3.0.0,<4.0.0", "pytest-html", "pytest-xdist>=1.0.0"]

   .. tab:: ini

       .. code-block:: ini

           [pytest]
           required_plugins = pytest-django>=3.0.0,<4.0.0 pytest-html pytest-xdist>=1.0.0


.. confval:: strict
    :type: ``bool``
    :default: ``false``

    If set to ``true``, enable "strict mode", which enables the following options:

    * :confval:`strict_config`
    * :confval:`strict_markers`
    * :confval:`strict_parametrization_ids`
    * :confval:`strict_xfail`

    Plugins may also enable their own strictness options.

    If you explicitly set an individual strictness option, it takes precedence over ``strict``.

    .. note::
        If pytest adds new strictness options in the future, they will also be enabled in strict mode.
        Therefore, you should only enable strict mode if you use a pinned/locked version of pytest,
        or if you want to proactively adopt new strictness options as they are added.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            strict = true

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            strict = true

    .. versionadded:: 9.0


.. confval:: strict_config
    :type: ``bool``
    :default: ``false``

    If set to ``true``, any warnings encountered while parsing the ``pytest`` section of the configuration file will raise errors.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            strict_config = true

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            strict_config = true

    You can also enable this option via the :confval:`strict` option.


.. confval:: strict_markers
    :type: ``bool``
    :default: ``false``

    If set to ``true``, markers not registered in the ``markers`` section of the configuration file will raise errors.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            strict_markers = true

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            strict_markers = true

    You can also enable this option via the :confval:`strict` option.


.. confval:: strict_parametrization_ids
    :type: ``bool``
    :default: ``false``

    If set to ``true``, pytest emits an error if it detects non-unique parameter set IDs.

    If not set, pytest automatically handles this by adding `0`, `1`, ... to duplicate IDs,
    making them unique.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            strict_parametrization_ids = true

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            strict_parametrization_ids = true

    You can also enable this option via the :confval:`strict` option.

    For example,

    .. code-block:: python

        import pytest


        @pytest.mark.parametrize("letter", ["a", "a"])
        def test_letter_is_ascii(letter):
            assert letter.isascii()

    will emit an error because both cases (parameter sets) have the same auto-generated ID "a".

    To fix the error, if you decide to keep the duplicates, explicitly assign unique IDs:

    .. code-block:: python

        import pytest


        @pytest.mark.parametrize("letter", ["a", "a"], ids=["a0", "a1"])
        def test_letter_is_ascii(letter):
            assert letter.isascii()

    See :func:`parametrize <pytest.Metafunc.parametrize>` and :func:`pytest.param` for other ways to set IDs.


.. confval:: strict_xfail
    :type: ``bool``
    :default: ``false``

    If set to ``true``, tests marked with ``@pytest.mark.xfail`` that actually succeed will by default fail the
    test suite.
    For more information, see :ref:`xfail strict tutorial`.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            strict_xfail = true

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            strict_xfail = true

    You can also enable this option via the :confval:`strict` option.

    .. versionchanged:: 9.0
        Renamed from ``xfail_strict`` to ``strict_xfail``.
        ``xfail_strict`` is accepted as an alias for ``strict_xfail``.


.. confval:: testpaths
   :type: ``list[str]``

   Sets list of directories that should be searched for tests when
   no specific directories, files or test ids are given in the command line when
   executing pytest from the :ref:`rootdir <rootdir>` directory.
   File system paths may use shell-style wildcards, including the recursive
   ``**`` pattern.

   Useful when all project tests are in a known location to speed up
   test collection and to avoid picking up undesired tests by accident.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            testpaths = ["testing", "doc"]

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            testpaths = testing doc

   This configuration means that executing:

   .. code-block:: console

       pytest

   has the same practical effects as executing:

   .. code-block:: console

       pytest testing doc

.. confval:: tmp_path_retention_count
   :type: ``str``
   :default: ``"3"``

   How many sessions should pytest keep the `tmp_path` directories,
   according to :confval:`tmp_path_retention_policy`.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            tmp_path_retention_count = "3"

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            tmp_path_retention_count = 3


.. confval:: tmp_path_retention_policy
   :type: ``str``
   :default: ``"all"``

   Controls which directories created by the `tmp_path` fixture are kept around,
   based on test outcome.

    * `all`: retains directories for all tests, regardless of the outcome.
    * `failed`: retains directories only for tests with outcome `error` or `failed`.
    * `none`: directories are always removed after each test ends, regardless of the outcome.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            tmp_path_retention_policy = "all"

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            tmp_path_retention_policy = all


.. confval:: truncation_limit_chars
   :type: ``int``
   :default: ``640``

   Controls maximum number of characters to truncate assertion message contents.

   Setting value to ``0`` disables the character limit for truncation.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            truncation_limit_chars = 640

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            truncation_limit_chars = 640

   pytest truncates the assert messages to a certain limit by default to prevent comparison with large data to overload the console output.

   .. note::

        If pytest detects it is :ref:`running on CI <ci-pipelines>`, truncation is disabled automatically.


.. confval:: truncation_limit_lines
   :type: ``int``
   :default: ``8``

   Controls maximum number of lines to truncate assertion message contents.

   Setting value to ``0`` disables the lines limit for truncation.

   .. tab:: toml

       .. code-block:: toml

            [pytest]
            truncation_limit_lines = 8

   .. tab:: ini

       .. code-block:: ini

            [pytest]
            truncation_limit_lines = 8

   pytest truncates the assert messages to a certain limit by default to prevent comparison with large data to overload the console output.

   .. note::

        If pytest detects it is :ref:`running on CI <ci-pipelines>`, truncation is disabled automatically.


.. confval:: usefixtures
    :type: ``list[str]``

    List of fixtures that will be applied to all test functions; this is semantically the same to apply
    the ``@pytest.mark.usefixtures`` marker to all test functions.


    .. tab:: toml

        .. code-block:: toml

            [pytest]
            usefixtures = ["clean_db"]

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            usefixtures =
                clean_db


.. confval:: verbosity_assertions
    :type: ``str``
    :default: ``"auto"``

    Set a verbosity level specifically for assertion related output, overriding the application wide level.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            verbosity_assertions = "2"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            verbosity_assertions = 2

    A special value of ``"auto"`` can be used to explicitly use the global verbosity level.


.. confval:: assertion_text_diff_style
    :type: ``str``
    :default: ``"ndiff"``

    Set how pytest renders diffs for string equality assertions.

    Supported values are:

    * ``ndiff``: use the inline diff rendering markers.
    * ``block``: render each string in separate ``Left:`` and ``Right:`` blocks.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            assertion_text_diff_style = "block"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            assertion_text_diff_style = block


.. confval:: verbosity_subtests
    :type: ``str``
    :default: ``"auto"``

    Set the verbosity level specifically for **passed** subtests.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            verbosity_subtests = "1"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            verbosity_subtests = 1

    A value of ``1`` or higher will show output for **passed** subtests (**failed** subtests are always reported).
    Passed subtests output can be suppressed with the value ``0``, which overwrites the :option:`-v` command-line option.

    A special value of ``"auto"`` can be used to explicitly use the global verbosity level.

    See also: :ref:`subtests`.


.. confval:: verbosity_test_cases
    :type: ``str``
    :default: ``"auto"``

    Set a verbosity level specifically for test case execution related output, overriding the application wide level.

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            verbosity_test_cases = "2"

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            verbosity_test_cases = 2

    A special value of ``"auto"`` can be used to explicitly use the global verbosity level.


.. _`command-line-flags`:

Command-line Flags
------------------

This section documents all command-line options provided by pytest's core plugins.

.. note::

    External plugins can add their own command-line options.
    This reference documents only the options from pytest's core plugins.
    To see all available options including those from installed plugins, run ``pytest --help``.

Test Selection
~~~~~~~~~~~~~~

.. option:: -k EXPRESSION

    Only run tests which match the given substring expression.
    An expression is a Python evaluable expression where all names are substring-matched against test names and their parent classes.

    Examples::

        pytest -k "test_method or test_other"  # matches names containing 'test_method' OR 'test_other'
        pytest -k "not test_method"            # matches names NOT containing 'test_method'
        pytest -k "not test_method and not test_other"  # excludes both

    The matching is case-insensitive.
    Keywords are also matched to classes and functions containing extra names in their ``extra_keyword_matches`` set.

    See :ref:`select-tests` for more information and examples.

.. option:: -m MARKEXPR

    Only run tests matching given mark expression.
    Supports ``and``, ``or``, and ``not`` operators.

    Examples::

        pytest -m slow                  # run tests marked with @pytest.mark.slow
        pytest -m "not slow"            # run tests NOT marked slow
        pytest -m "mark1 and not mark2" # run tests marked mark1 but not mark2

    See :ref:`mark` for more information on markers.

.. option:: --markers

    Show all available markers (builtin, plugin, and per-project markers defined in configuration).

Test Execution Control
~~~~~~~~~~~~~~~~~~~~~~~

.. option:: -x, --exitfirst

    Exit instantly on first error or failed test.

.. option:: --maxfail=NUM

    Exit after first ``num`` failures or errors.
    Useful for CI environments where you want to fail fast but see a few failures.

.. option:: --last-failed, --lf

    Rerun only the tests that failed at the last run.
    If no tests failed (or no cached data exists), all tests are run.
    See also :confval:`cache_dir` and :ref:`cache`.

.. option:: --failed-first, --ff

    Run all tests, but run the last failures first.
    This may re-order tests and thus lead to repeated fixture setup/teardown.

.. option:: --new-first, --nf

    Run tests from new files first, then the rest of the tests sorted by file modification time.

.. option:: --stepwise, --sw

    Exit on test failure and continue from last failing test next time.
    Useful for fixing multiple test failures one at a time.

    See :ref:`cache stepwise` for more information.

.. option:: --stepwise-skip, --sw-skip

    Ignore the first failing test but stop on the next failing test.
    Implicitly enables :option:`--stepwise`.

.. option:: --stepwise-reset, --sw-reset

    Resets stepwise state, restarting the stepwise workflow.
    Implicitly enables :option:`--stepwise`.

.. option:: --last-failed-no-failures, --lfnf

    With :option:`--last-failed`, determines whether to execute tests when there are no previously known failures or when no cached ``lastfailed`` data was found.

    * ``all`` (default): runs the full test suite again
    * ``none``: just emits a message about no known failures and exits successfully

.. option:: --runxfail

    Report the results of xfail tests as if they were not marked.
    Useful for debugging xfailed tests.
    See :ref:`xfail`.

Collection
~~~~~~~~~~

.. option:: --collect-only, --co

    Only collect tests, don't execute them.
    Shows which tests would be collected and run.

.. option:: --pyargs

    Try to interpret all arguments as Python packages.
    Useful for running tests of installed packages::

        pytest --pyargs pkg.testing

.. option:: --ignore=PATH

    Ignore path during collection (multi-allowed).
    Can be specified multiple times.

.. option:: --ignore-glob=PATTERN

    Ignore path pattern during collection (multi-allowed).
    Supports glob patterns.

.. option:: --deselect=NODEID_PREFIX

    Deselect item (via node id prefix) during collection (multi-allowed).

.. option:: --confcutdir=DIR

    Only load ``conftest.py`` files relative to specified directory.

.. option:: --noconftest

    Don't load any ``conftest.py`` files.

.. option:: --keep-duplicates

    Keep duplicate tests. By default, pytest removes duplicate test items.

.. option:: --collect-in-virtualenv

    Don't ignore tests in a local virtualenv directory.
    By default, pytest skips tests in virtualenv directories.

.. option:: --continue-on-collection-errors

    Force test execution even if collection errors occur.

.. option:: --import-mode

    Prepend/append to sys.path when importing test modules and conftest files.

    * ``prepend`` (default): prepend to sys.path
    * ``append``: append to sys.path
    * ``importlib``: use importlib to import test modules

    See :ref:`pythonpath` for more information.

Fixtures
~~~~~~~~

.. option:: --fixtures, --funcargs

    Show available fixtures, sorted by plugin appearance.
    Fixtures with leading ``_`` are only shown with :option:`--verbose`.

.. option:: --fixtures-per-test

    Show fixtures per test.

.. option:: --setup-only

    Only setup fixtures, do not execute tests.
    See :ref:`how-to-fixtures`.

.. option:: --setup-show

    Show setup of fixtures while executing tests.

.. option:: --setup-plan

    Show what fixtures and tests would be executed but don't execute anything.

Debugging
~~~~~~~~~

.. option:: --pdb

    Start the interactive Python debugger on errors or KeyboardInterrupt.
    See :ref:`pdb-option`.

.. option:: --pdbcls=MODULENAME:CLASSNAME

    Specify a custom interactive Python debugger for use with :option:`--pdb`.

    Example::

        pytest --pdbcls=IPython.terminal.debugger:TerminalPdb

.. option:: --trace

    Immediately break when running each test.

    See :ref:`trace-option` for more information.

.. option:: --full-trace

    Don't cut any tracebacks (default is to cut).

    See :ref:`how-to-modifying-python-tb-printing` for more information.

.. option:: --debug, --debug=DEBUG_FILE_NAME

    Store internal tracing debug information in this log file.
    This file is opened with ``'w'`` and truncated as a result, care advised.
    Default file name if not specified: ``pytestdebug.log``.

.. option:: --trace-config

    Trace considerations of conftest.py files.

Output and Reporting
~~~~~~~~~~~~~~~~~~~~

.. option:: -v, --verbose

    Increase verbosity.
    Can be specified multiple times (e.g., ``-vv``) for even more verbose output.

    See :ref:`pytest.fine_grained_verbosity` for fine-grained control over verbosity.

.. option:: -q, --quiet

    Decrease verbosity.

.. option:: --verbosity=NUM

    Set verbosity level explicitly. Default: 0.

.. option:: -r CHARS, --report-chars=CHARS

    Show extra test summary info as specified by chars:

    * ``f``: failed
    * ``E``: error
    * ``s``: skipped
    * ``x``: xfailed
    * ``X``: xpassed
    * ``p``: passed
    * ``P``: passed with output
    * ``a``: all except passed (p/P)
    * ``A``: all
    * ``w``: warnings (enabled by default)
    * ``N``: resets the list

    Default: ``'fE'``

    Examples::

        pytest -rA           # show all outcomes
        pytest -rfE          # show only failed and errors (default)
        pytest -rfs          # show failed and skipped

    See :ref:`pytest.detailed_failed_tests_usage` for more information.

.. option:: --no-header

    Disable header.

.. option:: --no-summary

    Disable summary.

.. option:: --no-fold-skipped

    Do not fold skipped tests in short summary.

.. option:: --force-short-summary

    Force condensed summary output regardless of verbosity level.

.. option:: -l, --showlocals

    Show locals in tracebacks (disabled by default).

.. option:: --no-showlocals

    Hide locals in tracebacks (negate :option:`--showlocals` passed through addopts).

.. option:: --tb=STYLE

    Traceback print mode:

    * ``auto``: intelligent traceback formatting (default)
    * ``long``: exhaustive, informative traceback formatting
    * ``short``: shorter traceback format
    * ``line``: only the failing line
    * ``native``: Python's standard traceback
    * ``no``: no traceback

    See :ref:`how-to-modifying-python-tb-printing` for examples.

.. option:: --xfail-tb

    Show tracebacks for xfail (as long as :option:`--tb` != ``no``).

.. option:: --show-capture

    Controls how captured stdout/stderr/log is shown on failed tests.

    * ``no``: don't show captured output
    * ``stdout``: show captured stdout
    * ``stderr``: show captured stderr
    * ``log``: show captured logging
    * ``all`` (default): show all captured output

.. option:: --color=WHEN

    Color terminal output:

    * ``yes``: always use color
    * ``no``: never use color
    * ``auto`` (default): use color if terminal supports it

.. option:: --code-highlight={yes,no}

    Whether code should be highlighted (only if :option:`--color` is also enabled).
    Default: ``yes``.

.. option:: --pastebin=MODE

    Send failed|all info to bpaste.net pastebin service.

.. option:: --durations=NUM

    Show N slowest setup/test durations (N=0 for all).
    See :ref:`durations`.

.. option:: --durations-min=NUM

    Minimal duration in seconds for inclusion in slowest list.
    Default: 0.005 (or 0.0 if ``-vv`` is given).

Output Capture
~~~~~~~~~~~~~~

.. option:: --capture=METHOD

    Per-test capturing method:

    * ``fd``: capture at file descriptor level (default)
    * ``sys``: capture at sys level
    * ``no``: don't capture output
    * ``tee-sys``: capture but also show output on terminal

    See :ref:`captures`.

.. option:: -s

    Shortcut for :option:`--capture=no`.

JUnit XML
~~~~~~~~~

.. option:: --junit-xml=PATH, --junitxml=PATH

    Create junit-xml style report file at given path.

.. option:: --junit-prefix=STR, --junitprefix=STR

    Prepend prefix to classnames in junit-xml output.

Cache
~~~~~

.. option:: --cache-show[=PATTERN]

    Show cache contents, don't perform collection or tests.
    Default glob pattern: ``'*'``.

.. option:: --cache-clear

    Remove all cache contents at start of test run.
    See :ref:`cache`.

Warnings
~~~~~~~~

.. option:: --disable-pytest-warnings, --disable-warnings

    Disable warnings summary.

.. option:: -W WARNING, --pythonwarnings=WARNING

    Set which warnings to report, see ``-W`` option of Python itself.
    Can be specified multiple times.

.. option:: --max-warnings=NUM

    Exit with :class:`pytest.ExitCode` ``MAX_WARNINGS_ERROR`` (code ``6``) if all the tests pass, but the number
    of warnings exceeds the given threshold. By default there is no limit.
    Can also be set via the :confval:`max_warnings` configuration option.

Doctest
~~~~~~~

.. option:: --doctest-modules

    Run doctests in all .py modules.

    See :ref:`doctest` for more information on using doctests with pytest.

.. option:: --doctest-report

    Choose another output format for diffs on doctest failure:

    * ``none``
    * ``cdiff``
    * ``ndiff``
    * ``udiff``
    * ``only_first_failure``

.. option:: --doctest-glob=PATTERN

    Doctests file matching pattern.
    Default: ``test*.txt``.

.. option:: --doctest-ignore-import-errors

    Ignore doctest collection errors.

.. option:: --doctest-continue-on-failure

    For a given doctest, continue to run after the first failure.

Configuration
~~~~~~~~~~~~~

.. option:: -c FILE, --config-file=FILE

    Load configuration from ``FILE`` instead of trying to locate one of the implicit configuration files.

.. option:: --rootdir=ROOTDIR

    Define root directory for tests.
    Can be relative path: ``'root_dir'``, ``'./root_dir'``, ``'root_dir/another_dir/'``; absolute path: ``'/home/user/root_dir'``; path with variables: ``'$HOME/root_dir'``.

.. option:: --basetemp=DIR

    Base temporary directory for this test run.
    Warning: this directory is removed if it exists.

    See :ref:`temporary directory location and retention` for more information.

.. option:: -o OPTION=VALUE, --override-ini=OPTION=VALUE

    Override configuration option with ``option=value`` style.
    Can be specified multiple times.

    Example::

        pytest -o strict_xfail=true -o cache_dir=cache

.. option:: --strict-config

    Enables the :confval:`strict_config` option.

.. option:: --strict-markers

    Enables the :confval:`strict_markers` option.

.. option:: --strict

    Enables the :confval:`strict` option (which enables all strictness options).

.. option:: --assert=MODE

    Control assertion debugging tools:

    * ``plain``: performs no assertion debugging
    * ``rewrite`` (default): rewrites assert statements in test modules on import to provide assert expression information

Logging
~~~~~~~

See :ref:`logging` for a guide on using these flags.

.. option:: --log-level=LEVEL

    Level of messages to catch/display.
    Not set by default, so it depends on the root/parent log handler's effective level, where it is ``WARNING`` by default.

.. option:: --log-format=FORMAT

    Log format used by the logging module.

.. option:: --log-date-format=FORMAT

    Log date format used by the logging module.

.. option:: --log-cli-level=LEVEL

    CLI logging level. See :ref:`live_logs`.

.. option:: --log-cli-format=FORMAT

    Log format used by the logging module for CLI output.

.. option:: --log-cli-date-format=FORMAT

    Log date format used by the logging module for CLI output.

.. option:: --log-file=PATH

    Path to a file logging will be written to.

.. option:: --log-file-mode

    Log file open mode:

    * ``w`` (default): recreate the file
    * ``a``: append to the file

.. option:: --log-file-level=LEVEL

    Log file logging level.

.. option:: --log-file-format=FORMAT

    Log format used by the logging module for the log file.

.. option:: --log-file-date-format=FORMAT

    Log date format used by the logging module for the log file.

.. option:: --log-auto-indent=VALUE

    Auto-indent multiline messages passed to the logging module.
    Accepts ``true|on``, ``false|off`` or an integer.

.. option:: --log-disable=LOGGER

    Disable a logger by name. Can be passed multiple times.

Plugin and Extension Management
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. option:: -p NAME

    Early-load given plugin module name or entry point (multi-allowed).
    To avoid loading of plugins, use the ``no:`` prefix, e.g. ``no:doctest``.
    See also :option:`--disable-plugin-autoload`.

.. option:: --disable-plugin-autoload

    Disable plugin auto-loading through entry point packaging metadata.
    Only plugins explicitly specified in :option:`-p` or env var :envvar:`PYTEST_PLUGINS` will be loaded.

Version and Help
~~~~~~~~~~~~~~~~

.. option:: -V, --version

    Display pytest version and information about plugins. When given twice, also display information about plugins.

.. option:: -h, --help

    Show help message and configuration info.

Complete Help Output
~~~~~~~~~~~~~~~~~~~~

All the command-line flags can also be obtained by running ``pytest --help``::

    $ pytest --help
    usage: pytest [options] [file_or_dir] [file_or_dir] [...]

    positional arguments:
      file_or_dir

    general:
      -k EXPRESSION         Only run tests which match the given substring
                            expression. An expression is a Python evaluable
                            expression where all names are substring-matched
                            against test names and their parent classes.
                            Example: -k 'test_method or test_other' matches all
                            test functions and classes whose name contains
                            'test_method' or 'test_other', while -k 'not
                            test_method' matches those that don't contain
                            'test_method' in their names. -k 'not test_method
                            and not test_other' will eliminate the matches.
                            Additionally keywords are matched to classes and
                            functions containing extra names in their
                            'extra_keyword_matches' set, as well as functions
                            which have names assigned directly to them. The
                            matching is case-insensitive.
      -m MARKEXPR           Only run tests matching given mark expression. For
                            example: -m 'mark1 and not mark2'.
      --markers             show markers (builtin, plugin and per-project ones).
      -x, --exitfirst       Exit instantly on first error or failed test
      --maxfail=num         Exit after first num failures or errors
      --strict-config       Enables the strict_config option
      --strict-markers      Enables the strict_markers option
      --strict              Enables the strict option
      --fixtures, --funcargs
                            Show available fixtures, sorted by plugin appearance
                            (fixtures with leading '_' are only shown with '-v')
      --fixtures-per-test   Show fixtures per test
      --pdb                 Start the interactive Python debugger on errors or
                            KeyboardInterrupt
      --pdbcls=modulename:classname
                            Specify a custom interactive Python debugger for use
                            with --pdb.For example:
                            --pdbcls=IPython.terminal.debugger:TerminalPdb
      --trace               Immediately break when running each test
      --capture=method      Per-test capturing method: one of fd|sys|no|tee-sys
      -s                    Shortcut for --capture=no
      --runxfail            Report the results of xfail tests as if they were
                            not marked
      --lf, --last-failed   Rerun only the tests that failed at the last run (or
                            all if none failed)
      --ff, --failed-first  Run all tests, but run the last failures first. This
                            may re-order tests and thus lead to repeated fixture
                            setup/teardown.
      --nf, --new-first     Run tests from new files first, then the rest of the
                            tests sorted by file mtime
      --cache-show=[CACHESHOW]
                            Show cache contents, don't perform collection or
                            tests. Optional argument: glob (default: '*').
      --cache-clear         Remove all cache contents at start of test run
      --lfnf, --last-failed-no-failures={all,none}
                            With ``--lf``, determines whether to execute tests
                            when there are no previously (known) failures or
                            when no cached ``lastfailed`` data was found.
                            ``all`` (the default) runs the full test suite
                            again. ``none`` just emits a message about no known
                            failures and exits successfully.
      --sw, --stepwise      Exit on test failure and continue from last failing
                            test next time
      --sw-skip, --stepwise-skip
                            Ignore the first failing test but stop on the next
                            failing test. Implicitly enables --stepwise.
      --sw-reset, --stepwise-reset
                            Resets stepwise state, restarting the stepwise
                            workflow. Implicitly enables --stepwise.

    Reporting:
      --durations=N         Show N slowest setup/test durations (N=0 for all)
      --durations-min=N     Minimal duration in seconds for inclusion in slowest
                            list. Default: 0.005 (or 0.0 if -vv is given).
      -v, --verbose         Increase verbosity
      --no-header           Disable header
      --no-summary          Disable summary
      --no-fold-skipped     Do not fold skipped tests in short summary.
      --force-short-summary
                            Force condensed summary output regardless of
                            verbosity level.
      -q, --quiet           Decrease verbosity
      --verbosity=VERBOSE   Set verbosity. Default: 0.
      -r, --report-chars chars
                            Show extra test summary info as specified by chars:
                            (f)ailed, (E)rror, (s)kipped, (x)failed, (X)passed,
                            (p)assed, (P)assed with output, (a)ll except passed
                            (p/P), or (A)ll. (w)arnings are enabled by default
                            (see --disable-warnings), 'N' can be used to reset
                            the list. (default: 'fE').
      --disable-warnings, --disable-pytest-warnings
                            Disable warnings summary
      -l, --showlocals      Show locals in tracebacks (disabled by default)
      --no-showlocals       Hide locals in tracebacks (negate --showlocals
                            passed through addopts)
      --tb=style            Traceback print mode
                            (auto/long/short/line/native/no)
      --xfail-tb            Show tracebacks for xfail (as long as --tb != no)
      --show-capture={no,stdout,stderr,log,all}
                            Controls how captured stdout/stderr/log is shown on
                            failed tests. Default: all.
      --full-trace          Don't cut any tracebacks (default is to cut)
      --color=color         Color terminal output (yes/no/auto)
      --code-highlight={yes,no}
                            Whether code should be highlighted (only if --color
                            is also enabled). Default: yes.
      --pastebin=mode       Send failed|all info to bpaste.net pastebin service
      --junitxml, --junit-xml=path
                            Create junit-xml style report file at given path
      --junitprefix, --junit-prefix=str
                            Prepend prefix to classnames in junit-xml output

    pytest-warnings:
      -W, --pythonwarnings PYTHONWARNINGS
                            Set which warnings to report, see -W option of
                            Python itself
      --max-warnings=num    Exit with error if all tests pass but the number of
                            warnings exceeds this threshold

    collection:
      --collect-only, --co  Only collect tests, don't execute them
      --pyargs              Try to interpret all arguments as Python packages
      --ignore=path         Ignore path during collection (multi-allowed)
      --ignore-glob=path    Ignore path pattern during collection (multi-
                            allowed)
      --deselect=nodeid_prefix
                            Deselect item (via node id prefix) during collection
                            (multi-allowed)
      --confcutdir=dir      Only load conftest.py's relative to specified dir
      --noconftest          Don't load any conftest.py files
      --keep-duplicates     Keep duplicate tests
      --collect-in-virtualenv
                            Don't ignore tests in a local virtualenv directory
      --continue-on-collection-errors
                            Force test execution even if collection errors occur
      --import-mode={prepend,append,importlib}
                            Prepend/append to sys.path when importing test
                            modules and conftest files. Default: prepend.
      --doctest-modules     Run doctests in all .py modules
      --doctest-report={none,cdiff,ndiff,udiff,only_first_failure}
                            Choose another output format for diffs on doctest
                            failure
      --doctest-glob=pat    Doctests file matching pattern, default: test*.txt
      --doctest-ignore-import-errors
                            Ignore doctest collection errors
      --doctest-continue-on-failure
                            For a given doctest, continue to run after the first
                            failure

    test session debugging and configuration:
      -c, --config-file FILE
                            Load configuration from `FILE` instead of trying to
                            locate one of the implicit configuration files.
      --rootdir=ROOTDIR     Define root directory for tests. Can be relative
                            path: 'root_dir', './root_dir',
                            'root_dir/another_dir/'; absolute path:
                            '/home/user/root_dir'; path with variables:
                            '$HOME/root_dir'.
      --basetemp=dir        Base temporary directory for this test run.
                            (Warning: this directory is removed if it exists.)
      -V, --version         Display pytest version and information about
                            plugins. When given twice, also display information
                            about plugins.
      -h, --help            Show help message and configuration info
      -p name               Early-load given plugin module name or entry point
                            (multi-allowed). To avoid loading of plugins, use
                            the `no:` prefix, e.g. `no:doctest`. See also
                            --disable-plugin-autoload.
      --disable-plugin-autoload
                            Disable plugin auto-loading through entry point
                            packaging metadata. Only plugins explicitly
                            specified in -p or env var PYTEST_PLUGINS will be
                            loaded.
      --trace-config        Trace considerations of conftest.py files
      --debug=[DEBUG_FILE_NAME]
                            Store internal tracing debug information in this log
                            file. This file is opened with 'w' and truncated as
                            a result, care advised. Default: pytestdebug.log.
      -o, --override-ini OVERRIDE_INI
                            Override configuration option with "option=value"
                            style, e.g. `-o strict_xfail=True -o
                            cache_dir=cache`.
      --assert=MODE         Control assertion debugging tools.
                            'plain' performs no assertion debugging.
                            'rewrite' (the default) rewrites assert statements
                            in test modules on import to provide assert
                            expression information.
      --setup-only          Only setup fixtures, do not execute tests
      --setup-show          Show setup of fixtures while executing tests
      --setup-plan          Show what fixtures and tests would be executed but
                            don't execute anything

    logging:
      --log-level=LEVEL     Level of messages to catch/display. Not set by
                            default, so it depends on the root/parent log
                            handler's effective level, where it is "WARNING" by
                            default.
      --log-format=LOG_FORMAT
                            Log format used by the logging module
      --log-date-format=LOG_DATE_FORMAT
                            Log date format used by the logging module
      --log-cli-level=LOG_CLI_LEVEL
                            CLI logging level
      --log-cli-format=LOG_CLI_FORMAT
                            Log format used by the logging module
      --log-cli-date-format=LOG_CLI_DATE_FORMAT
                            Log date format used by the logging module
      --log-file=LOG_FILE   Path to a file when logging will be written to
      --log-file-mode={w,a}
                            Log file open mode
      --log-file-level=LOG_FILE_LEVEL
                            Log file logging level
      --log-file-format=LOG_FILE_FORMAT
                            Log format used by the logging module
      --log-file-date-format=LOG_FILE_DATE_FORMAT
                            Log date format used by the logging module
      --log-auto-indent=LOG_AUTO_INDENT
                            Auto-indent multiline messages passed to the logging
                            module. Accepts true|on, false|off or an integer.
      --log-disable=LOGGER_DISABLE
                            Disable a logger by name. Can be passed multiple
                            times.

    [pytest] configuration options in the first pytest.toml|pytest.ini|tox.ini|setup.cfg|pyproject.toml file found:

      markers (linelist):   Register new markers for test functions
      empty_parameter_set_mark (string):
                            Default marker for empty parametersets
      strict_config (bool): Any warnings encountered while parsing the `pytest`
                            section of the configuration file raise errors
      strict_markers (bool):
                            Markers not registered in the `markers` section of
                            the configuration file raise errors
      strict (bool):        Enables all strictness options, currently:
                            strict_config, strict_markers, strict_xfail,
                            strict_parametrization_ids
      filterwarnings (linelist):
                            Each line specifies a pattern for
                            warnings.filterwarnings. Processed after
                            -W/--pythonwarnings.
      max_warnings (string):
                            Exit with error if all tests pass but the number of
                            warnings exceeds this threshold
      norecursedirs (args): Directory patterns to avoid for recursion
      testpaths (args):     Directories to search for tests when no files or
                            directories are given on the command line
      collect_imported_tests (bool):
                            Whether to collect tests in imported modules outside
                            `testpaths`
      consider_namespace_packages (bool):
                            Consider namespace packages when resolving module
                            names during import
      usefixtures (args):   List of default fixtures to be used with this
                            project
      python_files (args):  Glob-style file patterns for Python test module
                            discovery
      python_classes (args):
                            Prefixes or glob names for Python test class
                            discovery
      python_functions (args):
                            Prefixes or glob names for Python test function and
                            method discovery
      disable_test_id_escaping_and_forfeit_all_rights_to_community_support (bool):
                            Disable string escape non-ASCII characters, might
                            cause unwanted side effects(use at your own risk)
      strict_parametrization_ids (bool):
                            Emit an error if non-unique parameter set IDs are
                            detected
      console_output_style (string):
                            Console output: "classic", or with additional
                            progress information ("progress" (percentage) |
                            "count" | "progress-even-when-capture-no" (forces
                            progress even when capture=no)
      verbosity_test_cases (string):
                            Specify a verbosity level for test case execution,
                            overriding the main level. Higher levels will
                            provide more detailed information about each test
                            case executed.
      strict_xfail (bool):  Default for the strict parameter of xfail markers
                            when not given explicitly (default: False) (alias:
                            xfail_strict)
      tmp_path_retention_count (string):
                            How many sessions should we keep the `tmp_path`
                            directories, according to
                            `tmp_path_retention_policy`.
      tmp_path_retention_policy (string):
                            Controls which directories created by the `tmp_path`
                            fixture are kept around, based on test outcome.
                            (all/failed/none)
      enable_assertion_pass_hook (bool):
                            Enables the pytest_assertion_pass hook. Make sure to
                            delete any previously generated pyc cache files.
      truncation_limit_lines (string):
                            Set threshold of LINES after which truncation will
                            take effect
      truncation_limit_chars (string):
                            Set threshold of CHARS after which truncation will
                            take effect
      assertion_text_diff_style (string):
                            Choose how pytest renders diffs for string equality
                            assertions: ndiff or block
      verbosity_assertions (string):
                            Specify a verbosity level for assertions, overriding
                            the main level. Higher levels will provide more
                            detailed explanation when an assertion fails.
      junit_suite_name (string):
                            Test suite name for JUnit report
      junit_logging (string):
                            Write captured log messages to JUnit report: one of
                            no|log|system-out|system-err|out-err|all
      junit_log_passing_tests (bool):
                            Capture log information for passing tests to JUnit
                            report:
      junit_duration_report (string):
                            Duration time to report: one of total|call
      junit_family (string):
                            Emit XML for schema: one of legacy|xunit1|xunit2
      doctest_optionflags (args):
                            Option flags for doctests
      doctest_encoding (string):
                            Encoding used for doctest files
      cache_dir (string):   Cache directory path
      log_level (string):   Default value for --log-level
      log_format (string):  Default value for --log-format
      log_date_format (string):
                            Default value for --log-date-format
      log_cli (bool):       Enable log display during test run (also known as
                            "live logging")
      log_cli_level (string):
                            Default value for --log-cli-level
      log_cli_format (string):
                            Default value for --log-cli-format
      log_cli_date_format (string):
                            Default value for --log-cli-date-format
      log_file (string):    Default value for --log-file
      log_file_mode (string):
                            Default value for --log-file-mode
      log_file_level (string):
                            Default value for --log-file-level
      log_file_format (string):
                            Default value for --log-file-format
      log_file_date_format (string):
                            Default value for --log-file-date-format
      log_auto_indent (string):
                            Default value for --log-auto-indent
      faulthandler_timeout (string):
                            Dump the traceback of all threads if a test takes
                            more than TIMEOUT seconds to finish
      faulthandler_exit_on_timeout (bool):
                            Exit the test process if a test takes more than
                            faulthandler_timeout seconds to finish
      verbosity_subtests (string):
                            Specify verbosity level for subtests. Higher levels
                            will generate output for passed subtests. Failed
                            subtests are always reported.
      addopts (args):       Extra command line options
      minversion (string):  Minimally required pytest version
      pythonpath (paths):   Add paths to sys.path
      required_plugins (args):
                            Plugins that must be present for pytest to run

    Environment variables:
      CI                       When set to a non-empty value, pytest knows it is running in a CI process and does not truncate summary info
      BUILD_NUMBER             Equivalent to CI
      PYTEST_ADDOPTS           Extra command line options
      PYTEST_PLUGINS           Comma-separated plugins to load during startup
      PYTEST_DISABLE_PLUGIN_AUTOLOAD Set to disable plugin auto-loading
      PYTEST_DEBUG             Set to enable debug tracing of pytest's internals
      PYTEST_DEBUG_TEMPROOT    Override the system temporary directory
      PYTEST_THEME             The Pygments style to use for code output
      PYTEST_THEME_MODE        Set the PYTEST_THEME to be either 'dark' or 'light'


    to see available markers type: pytest --markers
    to see available fixtures type: pytest --fixtures
    (shown according to specified file_or_dir or current dir if not specified; fixtures with leading '_' are only shown with the '-v' option

# Fixtures reference
Source: https://docs.pytest.org/en/stable/reference/fixtures.html

.. _reference-fixtures:
.. _fixture:
.. _fixtures:
.. _`@pytest.fixture`:
.. _`pytest.fixture`:


Fixtures reference
========================================================

.. seealso:: :ref:`about-fixtures`
.. seealso:: :ref:`how-to-fixtures`

.. _`Dependency injection`: https://en.wikipedia.org/wiki/Dependency_injection


Built-in fixtures
-----------------

:ref:`Fixtures <fixtures-api>` are defined using the :ref:`@pytest.fixture
<pytest.fixture-api>` decorator. Pytest has several useful built-in fixtures:

   :fixture:`capfd`
        Capture, as text, output to file descriptors ``1`` and ``2``.

   :fixture:`capfdbinary`
        Capture, as bytes, output to file descriptors ``1`` and ``2``.

   :fixture:`caplog`
        Control logging and access log entries.

   :fixture:`capsys`
        Capture, as text, output to ``sys.stdout`` and ``sys.stderr``.

   :fixture:`capteesys`
        Capture in the same manner as :fixture:`capsys`, but also pass text
        through according to :option:`--capture`.

   :fixture:`capsysbinary`
        Capture, as bytes, output to ``sys.stdout`` and ``sys.stderr``.

   :fixture:`cache`
        Store and retrieve values across pytest runs.

   :fixture:`doctest_namespace`
        Provide a dict injected into the doctests namespace.

   :fixture:`monkeypatch`
       Temporarily modify classes, functions, dictionaries,
       ``os.environ``, and other objects.

   :fixture:`pytestconfig`
        Access to configuration values, pluginmanager and plugin hooks.

   :fixture:`subtests`
        Enable declaring subtests inside test functions.

   :fixture:`record_property`
       Add extra properties to the test.

   :fixture:`record_testsuite_property`
       Add extra properties to the test suite.

   :fixture:`recwarn`
        Record warnings emitted by test functions.

   :fixture:`request`
       Provide information on the executing test function.

   :fixture:`testdir`
        Provide a temporary test directory to aid in running, and
        testing, pytest plugins.

   :fixture:`tmp_path`
       Provide a :class:`pathlib.Path` object to a temporary directory
       which is unique to each test function.

   :fixture:`tmp_path_factory`
        Make session-scoped temporary directories and return
        :class:`pathlib.Path` objects.

   :fixture:`tmpdir`
        Provide a `py.path.local <https://py.readthedocs.io/en/latest/path.html>`_ object to a temporary
        directory which is unique to each test function;
        replaced by :fixture:`tmp_path`.

   :fixture:`tmpdir_factory`
        Make session-scoped temporary directories and return
        ``py.path.local`` objects;
        replaced by :fixture:`tmp_path_factory`.


.. _`conftest.py`:
.. _`conftest`:

Fixture availability
---------------------

Fixture availability is determined from the perspective of the test. A fixture
is only available for tests to request if they are in the scope that fixture is
defined in. If a fixture is defined inside a class, it can only be requested by
tests inside that class. But if a fixture is defined inside the global scope of
the module, then every test in that module, even if it's defined inside a class,
can request it.

Similarly, a test can also only be affected by an autouse fixture if that test
is in the same scope that autouse fixture is defined in (see
:ref:`autouse order`).

A fixture can also request any other fixture, no matter where it's defined, so
long as the test requesting them can see all fixtures involved.

For example, here's a test file with a fixture (``outer``) that requests a
fixture (``inner``) from a scope it wasn't defined in:

.. literalinclude:: /example/fixtures/test_fixtures_request_different_scope.py

From the tests' perspectives, they have no problem seeing each of the fixtures
they're dependent on:

.. image:: /example/fixtures/test_fixtures_request_different_scope.*
    :align: center

So when they run, ``outer`` will have no problem finding ``inner``, because
pytest searched from the tests' perspectives.

.. note::
    The scope a fixture is defined in has no bearing on the order it will be
    instantiated in: the order is mandated by the logic described
    :ref:`here <fixture order>`.

``conftest.py``: sharing fixtures across multiple files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``conftest.py`` file serves as a means of providing fixtures for an entire
directory. Fixtures defined in a ``conftest.py`` can be used by any test
in that package without needing to import them (pytest will automatically
discover them).

You can have multiple nested directories/packages containing your tests, and
each directory can have its own ``conftest.py`` with its own fixtures, adding on
to the ones provided by the ``conftest.py`` files in parent directories.

For example, given a test file structure like this:

::

    tests/
        __init__.py

        conftest.py
            # content of tests/conftest.py
            import pytest

            @pytest.fixture
            def order():
                return []

            @pytest.fixture
            def top(order, innermost):
                order.append("top")

        test_top.py
            # content of tests/test_top.py
            import pytest

            @pytest.fixture
            def innermost(order):
                order.append("innermost top")

            def test_order(order, top):
                assert order == ["innermost top", "top"]

        subpackage/
            __init__.py

            conftest.py
                # content of tests/subpackage/conftest.py
                import pytest

                @pytest.fixture
                def mid(order):
                    order.append("mid subpackage")

            test_subpackage.py
                # content of tests/subpackage/test_subpackage.py
                import pytest

                @pytest.fixture
                def innermost(order, mid):
                    order.append("innermost subpackage")

                def test_order(order, top):
                    assert order == ["mid subpackage", "innermost subpackage", "top"]

The boundaries of the scopes can be visualized like this:

.. image:: /example/fixtures/fixture_availability.*
    :align: center

The directories become their own sort of scope where fixtures that are defined
in a ``conftest.py`` file in that directory become available for that whole
scope.

Tests are allowed to search upward (stepping outside a circle) for fixtures, but
can never go down (stepping inside a circle) to continue their search. So
``tests/subpackage/test_subpackage.py::test_order`` would be able to find the
``innermost`` fixture defined in ``tests/subpackage/test_subpackage.py``, but
the one defined in ``tests/test_top.py`` would be unavailable to it because it
would have to step down a level (step inside a circle) to find it.

The first fixture the test finds is the one that will be used, so
:ref:`fixtures can be overridden <override fixtures>` if you need to change or
extend what one does for a particular scope.

You can also use the ``conftest.py`` file to implement
:ref:`local per-directory plugins <conftest.py plugins>`.

Fixtures from third-party plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fixtures don't have to be defined in this structure to be available for tests,
though. They can also be provided by third-party plugins that are installed, and
this is how many pytest plugins operate. As long as those plugins are installed,
the fixtures they provide can be requested from anywhere in your test suite.

Because they're provided from outside the structure of your test suite,
third-party plugins don't really provide a scope like `conftest.py` files and
the directories in your test suite do. As a result, pytest will search for
fixtures stepping out through scopes as explained previously, only reaching
fixtures defined in plugins *last*.

For example, given the following file structure:

::

    tests/
        __init__.py

        conftest.py
            # content of tests/conftest.py
            import pytest

            @pytest.fixture
            def order():
                return []

        subpackage/
            __init__.py

            conftest.py
                # content of tests/subpackage/conftest.py
                import pytest

                @pytest.fixture(autouse=True)
                def mid(order, b_fix):
                    order.append("mid subpackage")

            test_subpackage.py
                # content of tests/subpackage/test_subpackage.py
                import pytest

                @pytest.fixture
                def inner(order, mid, a_fix):
                    order.append("inner subpackage")

                def test_order(order, inner):
                    assert order == ["b_fix", "mid subpackage", "a_fix", "inner subpackage"]

If ``plugin_a`` is installed and provides the fixture ``a_fix``, and
``plugin_b`` is installed and provides the fixture ``b_fix``, then this is what
the test's search for fixtures would look like:

.. image:: /example/fixtures/fixture_availability_plugins.svg
    :align: center

pytest will only search for ``a_fix`` and ``b_fix`` in the plugins after
searching for them first in the scopes inside ``tests/``.

.. note::

    pytest can tell you what fixtures are available for a given test if you call
    ``pytest`` along with the test's name (or the scope it's in), and provide
    the :option:`--fixtures` flag, e.g. ``pytest --fixtures test_something.py``
    (fixtures with names that start with ``_`` will only be shown if you also
    provide the :option:`-v` flag).


.. _`fixture order`:

Fixture instantiation order
---------------------------

When pytest wants to execute a test, once it knows what fixtures will be
executed, it has to figure out the order they'll be executed in. To do this, it
considers 3 factors:

1. scope
2. dependencies
3. autouse

Names of fixtures or tests, where they're defined, the order they're defined in,
and the order fixtures are requested in have no bearing on execution order
beyond coincidence. While pytest will try to make sure coincidences like these
stay consistent from run to run, it's not something that should be depended on.
If you want to control the order, it's safest to rely on these 3 things and make
sure dependencies are clearly established.

Higher-scoped fixtures are executed first
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within a function request for fixtures, those of higher-scopes (such as
``session``) are executed before lower-scoped fixtures (such as ``function`` or
``class``).

Here's an example:

.. literalinclude:: /example/fixtures/test_fixtures_order_scope.py

The test will pass because the larger scoped fixtures are executing first.

The order breaks down to this:

.. image:: /example/fixtures/test_fixtures_order_scope.*
    :align: center

Fixtures of the same order execute based on dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When a fixture requests another fixture, the other fixture is executed first.
So if fixture ``a`` requests fixture ``b``, fixture ``b`` will execute first,
because ``a`` depends on ``b`` and can't operate without it. Even if ``a``
doesn't need the result of ``b``, it can still request ``b`` if it needs to make
sure it is executed after ``b``.

For example:

.. literalinclude:: /example/fixtures/test_fixtures_order_dependencies.py

If we map out what depends on what, we get something that looks like this:

.. image:: /example/fixtures/test_fixtures_order_dependencies.*
    :align: center

The rules provided by each fixture (as to what fixture(s) each one has to come
after) are comprehensive enough that it can be flattened to this:

.. image:: /example/fixtures/test_fixtures_order_dependencies_flat.*
    :align: center

Enough information has to be provided through these requests in order for pytest
to be able to figure out a clear, linear chain of dependencies, and as a result,
an order of operations for a given test. If there's any ambiguity, and the order
of operations can be interpreted more than one way, you should assume pytest
could go with any one of those interpretations at any point.

For example, if ``d`` didn't request ``c``, i.e. the graph would look like this:

.. image:: /example/fixtures/test_fixtures_order_dependencies_unclear.*
    :align: center

Because nothing requested ``c`` other than ``g``, and ``g`` also requests ``f``,
it's now unclear if ``c`` should go before/after ``f``, ``e``, or ``d``. The
only rules that were set for ``c`` is that it must execute after ``b`` and
before ``g``.

pytest doesn't know where ``c`` should go in the case, so it should be assumed
that it could go anywhere between ``g`` and ``b``.

This isn't necessarily bad, but it's something to keep in mind. If the order
they execute in could affect the behavior a test is targeting, or could
otherwise influence the result of a test, then the order should be defined
explicitly in a way that allows pytest to linearize/"flatten" that order.

.. _`autouse order`:

Autouse fixtures are executed first within their scope
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Autouse fixtures are assumed to apply to every test that could reference them,
so they are executed before other fixtures in that scope. Fixtures that are
requested by autouse fixtures effectively become autouse fixtures themselves for
the tests that the real autouse fixture applies to.

So if fixture ``a`` is autouse and fixture ``b`` is not, but fixture ``a``
requests fixture ``b``, then fixture ``b`` will effectively be an autouse
fixture as well, but only for the tests that ``a`` applies to.

In the last example, the graph became unclear if ``d`` didn't request ``c``. But
if ``c`` was autouse, then ``b`` and ``a`` would effectively also be autouse
because ``c`` depends on them. As a result, they would all be shifted above
non-autouse fixtures within that scope.

So if the test file looked like this:

.. literalinclude:: /example/fixtures/test_fixtures_order_autouse.py

the graph would look like this:

.. image:: /example/fixtures/test_fixtures_order_autouse.*
    :align: center

Because ``c`` can now be put above ``d`` in the graph, pytest can once again
linearize the graph to this:

.. image:: /example/fixtures/test_fixtures_order_autouse_flat.*
    :align: center

In this example, ``c`` makes ``b`` and ``a`` effectively autouse fixtures as
well.

Be careful with autouse, though, as an autouse fixture will automatically
execute for every test that can reach it, even if they don't request it. For
example, consider this file:

.. literalinclude:: /example/fixtures/test_fixtures_order_autouse_multiple_scopes.py

Even though nothing in ``TestClassWithoutC1Request`` is requesting ``c1``, it still
is executed for the tests inside it anyway:

.. image:: /example/fixtures/test_fixtures_order_autouse_multiple_scopes.*
    :align: center

But just because one autouse fixture requested a non-autouse fixture, that
doesn't mean the non-autouse fixture becomes an autouse fixture for all contexts
that it can apply to. It only effectively becomes an autouse fixture for the
contexts the real autouse fixture (the one that requested the non-autouse
fixture) can apply to.

For example, take a look at this test file:

.. literalinclude:: /example/fixtures/test_fixtures_order_autouse_temp_effects.py

It would break down to something like this:

.. image:: /example/fixtures/test_fixtures_order_autouse_temp_effects.*
    :align: center

For ``test_req`` and ``test_no_req`` inside ``TestClassWithAutouse``, ``c3``
effectively makes ``c2`` an autouse fixture, which is why ``c2`` and ``c3`` are
executed for both tests, despite not being requested, and why ``c2`` and ``c3``
are executed before ``c1`` for ``test_req``.

If this made ``c2`` an *actual* autouse fixture, then ``c2`` would also execute
for the tests inside ``TestClassWithoutAutouse``, since they can reference
``c2`` if they wanted to. But it doesn't, because from the perspective of the
``TestClassWithoutAutouse`` tests, ``c2`` isn't an autouse fixture, since they
can't see ``c3``.


.. note::

    pytest can tell you what order the fixtures will execute in for a given test
    if you call ``pytest`` along with the test's name (or the scope it's in),
    and provide the :option:`--setup-plan` flag, e.g.
    ``pytest --setup-plan test_something.py`` (fixtures with names that start
    with ``_`` will only be shown if you also provide the :option:`-v` flag).

# Configuration
Source: https://docs.pytest.org/en/stable/reference/customize.html

Configuration
=============

Command line options and configuration file settings
-----------------------------------------------------------------

You can get help on command line and configuration options by using the general help option:

.. code-block:: bash

    pytest -h   # prints options _and_ config file settings

This will display command line and configuration file settings
which were registered by installed plugins.

.. _`config file formats`:

Configuration file formats
--------------------------

Many :ref:`pytest settings <ini options ref>` can be set in a *configuration file*, which
by convention resides in the root directory of your repository.

A quick example of the configuration files supported by pytest:

pytest.toml
~~~~~~~~~~~

.. versionadded:: 9.0

``pytest.toml`` files take precedence over other files, even when empty.

Alternatively, the hidden version ``.pytest.toml`` can be used.

.. tab:: toml

    .. code-block:: toml

        # pytest.toml or .pytest.toml
        [pytest]
        minversion = "9.0"
        addopts = ["-ra", "-q"]
        testpaths = [
            "tests",
            "integration",
        ]

pytest.ini
~~~~~~~~~~

``pytest.ini`` files take precedence over other files (except ``pytest.toml`` and ``.pytest.toml``), even when empty.

Alternatively, the hidden version ``.pytest.ini`` can be used.

.. tab:: ini

    .. code-block:: ini

        # pytest.ini or .pytest.ini
        [pytest]
        minversion = 6.0
        addopts = -ra -q
        testpaths =
            tests
            integration


pyproject.toml
~~~~~~~~~~~~~~

.. versionadded:: 6.0
.. versionchanged:: 9.0

``pyproject.toml`` files are supported for configuration.

.. tab:: toml

    Use ``[tool.pytest]`` to leverage native TOML types (supported since pytest 9.0):

    .. code-block:: toml

        # pyproject.toml
        [tool.pytest]
        minversion = "9.0"
        addopts = ["-ra", "-q"]
        testpaths = [
            "tests",
            "integration",
        ]

.. tab:: ini

    Use ``[tool.pytest.ini_options]`` for INI-style configuration (supported since pytest 6.0):

    .. code-block:: toml

        # pyproject.toml
        [tool.pytest.ini_options]
        minversion = "6.0"
        addopts = "-ra -q"
        testpaths = [
            "tests",
            "integration",
        ]

    For projects that still run pytest versions older than 6.0, keep
    ``minversion`` in ``pytest.ini`` or ``setup.cfg`` too. Those versions
    do not read ``pyproject.toml``.

tox.ini
~~~~~~~

``tox.ini`` files are the configuration files of the `tox <https://tox.readthedocs.io>`__ project,
and can also be used to hold pytest configuration if they have a ``[pytest]`` section.

.. tab:: ini

    .. code-block:: ini

        # tox.ini
        [pytest]
        minversion = 6.0
        addopts = -ra -q
        testpaths =
            tests
            integration


setup.cfg
~~~~~~~~~

``setup.cfg`` files are general purpose configuration files, used originally by ``distutils`` (now deprecated) and :std:doc:`setuptools <setuptools:userguide/declarative_config>`, and can also be used to hold pytest configuration
if they have a ``[tool:pytest]`` section.

.. tab:: ini

    .. code-block:: ini

        # setup.cfg
        [tool:pytest]
        minversion = 6.0
        addopts = -ra -q
        testpaths =
            tests
            integration

.. warning::

    Usage of ``setup.cfg`` is not recommended unless for very simple use cases. ``.cfg``
    files use a different parser than ``pytest.ini`` and ``tox.ini`` which might cause hard to track
    down problems.
    When possible, it is recommended to use the latter files, or ``pyproject.toml``, to hold your
    pytest configuration.


.. _rootdir:
.. _configfiles:

Initialization: determining rootdir and configfile
--------------------------------------------------

pytest determines a ``rootdir`` for each test run which depends on
the command line arguments (specified test files, paths) and on
the existence of configuration files.  The determined ``rootdir`` and ``configfile`` are
printed as part of the pytest header during startup.

Here's a summary of what ``pytest`` uses ``rootdir`` for:

* Construct *nodeids* during collection; each test is assigned
  a unique *nodeid* which is rooted at the ``rootdir`` and takes into account
  the full path, class name, function name and parametrization (if any).

* Is used by plugins as a stable location to store project/test run specific information;
  for example, the internal :ref:`cache <cache>` plugin creates a ``.pytest_cache`` subdirectory
  in ``rootdir`` to store its cross-test run state.

``rootdir`` is **NOT** used to modify ``sys.path``/``PYTHONPATH`` or
influence how modules are imported. See :ref:`pythonpath` for more details.

The :option:`--rootdir=path` command-line option can be used to force a specific directory.
Note that contrary to other command-line options, ``--rootdir`` cannot be used with
:confval:`addopts` inside a configuration file because the ``rootdir`` is used to *find* the configuration file
already.

Finding the ``rootdir``
~~~~~~~~~~~~~~~~~~~~~~~

Here is the algorithm which finds the rootdir from ``args``:

- If :option:`-c` is passed in the command-line, use that as configuration file, and its directory as ``rootdir``.

- Determine the common ancestor directory for the specified ``args`` that are
  recognised as paths that exist in the file system. If no such paths are
  found, the common ancestor directory is set to the current working directory.

- Look for ``pytest.toml``, ``.pytest.toml``, ``pytest.ini``, ``.pytest.ini``, ``pyproject.toml``, ``tox.ini``, and ``setup.cfg`` files in the ancestor
  directory and upwards.  If one is matched, it becomes the ``configfile`` and its
  directory becomes the ``rootdir``.

- If no configuration file was found, look for ``setup.py`` upwards from the common
  ancestor directory to determine the ``rootdir``.

- If no ``setup.py`` was found, look for ``pytest.toml``, ``.pytest.toml``, ``pytest.ini``, ``.pytest.ini``, ``pyproject.toml``, ``tox.ini``, and
  ``setup.cfg`` in each of the specified ``args`` and upwards. If one is
  matched, it becomes the ``configfile`` and its directory becomes the ``rootdir``.

- If no ``configfile`` was found and no configuration argument is passed, use the already determined common ancestor as root
  directory. This allows the use of pytest in structures that are not part of
  a package and don't have any particular configuration file.

If no ``args`` are given, pytest collects tests below the current working
directory and also starts determining the ``rootdir`` from there.

Files will only be matched for configuration if:

* ``pytest.toml``: will always match and take highest precedence, even if empty.
* ``pytest.ini``: will always match and take precedence (after ``pytest.toml`` and ``.pytest.toml``), even if empty.
* ``pyproject.toml``: contains a ``[tool.pytest]`` or ``[tool.pytest.ini_options]`` table.
* ``tox.ini``: contains a ``[pytest]`` section.
* ``setup.cfg``: contains a ``[tool:pytest]`` section.

Finally, a ``pyproject.toml`` file will be considered the ``configfile`` if no other match was found, in this case
even if it does not contain a ``[tool.pytest]`` table (since version ``9.0``) or a ``[tool.pytest.ini_options]``
table (since version ``8.1``).

The files are considered in the order above. Options from multiple ``configfiles`` candidates
are never merged - the first match wins.

The configuration file also determines the value of the ``rootpath``.

The :class:`Config <pytest.Config>` object (accessible via hooks or through the :fixture:`pytestconfig` fixture)
will subsequently carry these attributes:

- :attr:`config.rootpath <pytest.Config.rootpath>`: the determined root directory, guaranteed to exist. It is used as
  a reference directory for constructing test addresses ("nodeids") and can be used also by plugins for storing
  per-testrun information.

- :attr:`config.inipath <pytest.Config.inipath>`: the determined ``configfile``, may be ``None``
  (it is named ``inipath`` for historical reasons).

.. versionadded:: 6.1
    The ``config.rootpath`` and ``config.inipath`` properties. They are :class:`pathlib.Path`
    versions of the older ``config.rootdir`` and ``config.inifile``, which have type
    ``py.path.local``, and still exist for backward compatibility.



Example:

.. code-block:: bash

    pytest path/to/testdir path/other/

will determine the common ancestor as ``path`` and then
check for configuration files as follows:

.. code-block:: text

    # first look for path/pytest.toml
    path/pytest.toml
    path/pytest.ini
    path/pyproject.toml  # must contain a [tool.pytest] table to match
    path/tox.ini         # must contain [pytest] section to match
    path/setup.cfg       # must contain [tool:pytest] section to match
    pytest.toml
    pytest.ini
    ... # all the way up to the root

    # now look for setup.py
    path/setup.py
    setup.py
    ... # all the way up to the root


.. warning::

    Custom pytest plugin commandline arguments may include a path, as in
    ``pytest --log-output ../../test.log args``. Then ``args`` is mandatory,
    otherwise pytest uses the directory of test.log for rootdir determination
    (see also :issue:`1435`).
    A dot ``.`` for referencing the current working directory is also
    possible.


.. _`how to change command line options defaults`:
.. _`adding default options`:


Builtin configuration file options
----------------------------------------------

For the full list of options consult the :ref:`reference documentation <ini options ref>`.

Syntax highlighting theme customization
---------------------------------------

The syntax highlighting themes used by pytest can be customized using two environment variables:

- :envvar:`PYTEST_THEME` sets a `pygment style <https://pygments.org/docs/styles/>`_ to use.
- :envvar:`PYTEST_THEME_MODE` sets this style to *light* or *dark*.

# Exit codes
Source: https://docs.pytest.org/en/stable/reference/exit-codes.html

.. _exit-codes:

Exit codes
========================================================

Running ``pytest`` can result in seven different exit codes:

:Exit code 0: All tests were collected and passed successfully
:Exit code 1: Tests were collected and run but some of the tests failed
:Exit code 2: Test execution was interrupted by the user
:Exit code 3: Internal error happened while executing tests
:Exit code 4: pytest command line usage error
:Exit code 5: No tests were collected
:Exit code 6: Maximum number of warnings exceeded (see :option:`--max-warnings`)

They are represented by the :class:`pytest.ExitCode` enum. The exit codes being a part of the public API can be imported and accessed directly using:

.. code-block:: python

    from pytest import ExitCode

.. note::

    If you would like to customize the exit code in some scenarios, specifically when
    no tests are collected, consider using the
    `pytest-custom_exit_code <https://github.com/yashtodi94/pytest-custom_exit_code>`__
    plugin.

# Explanation
Source: https://docs.pytest.org/en/stable/explanation/index.html

:orphan:

.. _explanation:

Explanation
================

.. toctree::
   :maxdepth: 1

   anatomy
   fixtures
   goodpractices
   pythonpath
   types
   ci
   flaky

# Anatomy of a test
Source: https://docs.pytest.org/en/stable/explanation/anatomy.html

.. _test-anatomy:

Anatomy of a test
=================

In the simplest terms, a test is meant to look at the result of a particular
behavior, and make sure that result aligns with what you would expect.
Behavior is not something that can be empirically measured, which is why writing
tests can be challenging.

"Behavior" is the way in which some system **acts in response** to a particular
situation and/or stimuli. But exactly *how* or *why* something is done is not
quite as important as *what* was done.

You can think of a test as being broken down into four steps:

1. **Arrange**
2. **Act**
3. **Assert**
4. **Cleanup**

**Arrange** is where we prepare everything for our test. This means pretty
much everything except for the "**act**". It's lining up the dominoes so that
the **act** can do its thing in one, state-changing step. This can mean
preparing objects, starting/killing services, entering records into a database,
or even things like defining a URL to query, generating some credentials for a
user that doesn't exist yet, or just waiting for some process to finish.

**Act** is the singular, state-changing action that kicks off the **behavior**
we want to test. This behavior is what carries out the changing of the state of
the system under test (SUT), and it's the resulting changed state that we can
look at to make a judgement about the behavior. This typically takes the form of
a function/method call.

**Assert** is where we look at that resulting state and check if it looks how
we'd expect after the dust has settled. It's where we gather evidence to say the
behavior does or does not align with what we expect. The ``assert`` in our test
is where we take that measurement/observation and apply our judgement to it. If
something should be green, we'd say ``assert thing == "green"``.

**Cleanup** is where the test picks up after itself, so other tests aren't being
accidentally influenced by it.

At its core, the test is ultimately the **act** and **assert** steps, with the
**arrange** step only providing the context. **Behavior** exists between **act**
and **assert**.

# About fixtures
Source: https://docs.pytest.org/en/stable/explanation/fixtures.html

.. _about-fixtures:

About fixtures
===============

.. seealso:: :ref:`how-to-fixtures`
.. seealso:: :ref:`Fixtures reference <reference-fixtures>`

pytest fixtures are designed to be explicit, modular and scalable.

What fixtures are
-----------------

In testing, a `fixture <https://en.wikipedia.org/wiki/Test_fixture#Software>`_
provides a defined, reliable and consistent context for the tests. This could
include environment (for example a database configured with known parameters)
or content (such as a dataset).

Fixtures define the steps and data that constitute the *arrange* phase of a
test (see :ref:`test-anatomy`). In pytest, they are functions you define that
serve this purpose. They can also be used to define a test's *act* phase; this
is a powerful technique for designing more complex tests.

The services, state, or other operating environments set up by fixtures are
accessed by test functions through arguments. For each fixture used by a test
function there is typically a parameter (named after the fixture) in the test
function's definition.

We can tell pytest that a particular function is a fixture by decorating it with
:py:func:`@pytest.fixture <pytest.fixture>`. Here's a simple example of
what a fixture in pytest might look like:

.. code-block:: python

    import pytest


    class Fruit:
        def __init__(self, name):
            self.name = name

        def __eq__(self, other):
            return self.name == other.name


    @pytest.fixture
    def my_fruit():
        return Fruit("apple")


    @pytest.fixture
    def fruit_basket(my_fruit):
        return [Fruit("banana"), my_fruit]


    def test_my_fruit_in_basket(my_fruit, fruit_basket):
        assert my_fruit in fruit_basket

Tests don't have to be limited to a single fixture, either. They can depend on
as many fixtures as you want, and fixtures can use other fixtures, as well. This
is where pytest's fixture system really shines.


Improvements over xUnit-style setup/teardown functions
-----------------------------------------------------------

pytest fixtures offer dramatic improvements over the classic xUnit
style of setup/teardown functions:

* fixtures have explicit names and are activated by declaring their use
  from test functions, modules, classes or whole projects.

* fixtures are implemented in a modular manner, as each fixture name
  triggers a *fixture function* which can itself use other fixtures.

* fixture management scales from simple unit to complex
  functional testing, allowing to parametrize fixtures and tests according
  to configuration and component options, or to reuse fixtures
  across function, class, module or whole test session scopes.

* teardown logic can be easily, and safely managed, no matter how many fixtures
  are used, without the need to carefully handle errors by hand or micromanage
  the order that cleanup steps are added.

In addition, pytest continues to support :ref:`xunitsetup`.  You can mix
both styles, moving incrementally from classic to new style, as you
prefer.  You can also start out from existing :ref:`unittest.TestCase
style <unittest.TestCase>`.



Fixture errors
--------------

pytest does its best to put all the fixtures for a given test in a linear order
so that it can see which fixture happens first, second, third, and so on. If an
earlier fixture has a problem, though, and raises an exception, pytest will stop
executing fixtures for that test and mark the test as having an error.

When a test is marked as having an error, it doesn't mean the test failed,
though. It just means the test couldn't even be attempted because one of the
things it depends on had a problem.

This is one reason why it's a good idea to cut out as many unnecessary
dependencies as possible for a given test. That way a problem in something
unrelated isn't causing us to have an incomplete picture of what may or may not
have issues.

Here's a quick example to help explain:

.. code-block:: python

    import pytest


    @pytest.fixture
    def order():
        return []


    @pytest.fixture
    def append_first(order):
        order.append(1)


    @pytest.fixture
    def append_second(order, append_first):
        order.extend([2])


    @pytest.fixture(autouse=True)
    def append_third(order, append_second):
        order += [3]


    def test_order(order):
        assert order == [1, 2, 3]


If, for whatever reason, ``order.append(1)`` had a bug and it raises an exception,
we wouldn't be able to know if ``order.extend([2])`` or ``order += [3]`` would
also have problems. After ``append_first`` throws an exception, pytest won't run
any more fixtures for ``test_order``, and it won't even try to run
``test_order`` itself. The only things that would've run would be ``order`` and
``append_first``.


Sharing test data
-----------------

If you want to make test data from files available to your tests, a good way
to do this is by loading these data in a fixture for use by your tests.
This makes use of the automatic caching mechanisms of pytest.

Another good approach is by adding the data files in the ``tests`` directory.
There are also community plugins available to help to manage this aspect of
testing, e.g. :pypi:`pytest-datadir` and :pypi:`pytest-datafiles`.

.. _fixtures-signal-cleanup:

A note about fixture cleanup
----------------------------

pytest does not do any special processing for :data:`SIGTERM <signal.SIGTERM>` and
``SIGQUIT`` signals (:data:`SIGINT <signal.SIGINT>` is handled naturally
by the Python runtime via :class:`KeyboardInterrupt`), so fixtures that manage external resources which are important
to be cleared when the Python process is terminated (by those signals) might leak resources.

The reason pytest does not handle those signals to perform fixture cleanup is that signal handlers are global,
and changing them might interfere with the code under execution.

If fixtures in your suite need special care regarding termination in those scenarios,
see :issue:`this comment <5243#issuecomment-491522595>` in the issue
tracker for a possible workaround.

# Good Integration Practices
Source: https://docs.pytest.org/en/stable/explanation/goodpractices.html

.. highlight:: python
.. _`goodpractices`:

Good Integration Practices
=================================================

Install package with pip
-------------------------------------------------

For development, we recommend you use :mod:`venv` for virtual environments and
:doc:`pip:index` for installing your application and any dependencies,
as well as the ``pytest`` package itself.
This ensures your code and dependencies are isolated from your system Python installation.

Create a ``pyproject.toml`` file in the root of your repository as described in
:doc:`packaging:tutorials/packaging-projects`.
The first few lines should look like this:

.. code-block:: toml

    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [project]
    name = "PACKAGENAME"
    version = "PACKAGEVERSION"

where ``PACKAGENAME`` and ``PACKAGEVERSION`` are the name and version of your package respectively.

You can then install your package in "editable" mode by running from the same directory:

.. code-block:: bash

    pip install -e .

which lets you change your source code (both tests and application) and rerun tests at will.

.. _`test discovery`:
.. _`Python test discovery`:

Conventions for Python test discovery
-------------------------------------------------

``pytest`` implements the following standard test discovery:

* If no arguments are specified then collection starts from :confval:`testpaths`
  (if configured) or the current directory. Alternatively, command line arguments
  can be used in any combination of directories, file names or node ids.
* Recurse into directories, unless they match :confval:`norecursedirs`.
* In those directories, search for ``test_*.py`` or ``*_test.py`` files, imported by their `test package name`_.
* From those files, collect test items:

  * ``test`` prefixed test functions or methods outside of class.
  * ``test`` prefixed test functions or methods inside ``Test`` prefixed test classes (without an ``__init__`` method). Methods decorated with ``@staticmethod`` and ``@classmethods`` are also considered.

For examples of how to customize your test discovery :doc:`/example/pythoncollection`.

Within Python modules, ``pytest`` also discovers tests using the standard
:ref:`unittest.TestCase <unittest.TestCase>` subclassing technique.


.. _`test layout`:

Choosing a test layout
----------------------

``pytest`` supports two common test layouts:

Tests outside application code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Putting tests into an extra directory outside your actual application code
might be useful if you have many functional tests or for other reasons want
to keep tests separate from actual application code (often a good idea):

.. code-block:: text

    pyproject.toml
    src/
        mypkg/
            __init__.py
            app.py
            view.py
    tests/
        test_app.py
        test_view.py
        ...

This has the following benefits:

* Your tests can run against an installed version after executing ``pip install .``.
* Your tests can run against the local copy with an editable install after executing ``pip install --editable .``.

For new projects, we recommend to use ``importlib`` :ref:`import mode <import-modes>`
(see which-import-mode_ for a detailed explanation).
To this end, add the following to your configuration file:

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    addopts = ["--import-mode=importlib"]

.. _src-layout:

Generally, but especially if you use the default import mode ``prepend``,
it is **strongly** suggested to use a ``src`` layout.
Here, your application root package resides in a sub-directory of your root,
i.e. ``src/mypkg/`` instead of ``mypkg``.

This layout prevents a lot of common pitfalls and has many benefits,
which are better explained in this excellent `blog post`_ by Ionel Cristian Mărieș.

.. _blog post: https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure>

.. note::

    If you do not use an editable install and use the ``src`` layout as above you need to extend the Python's
    search path for module files to execute the tests against the local copy directly. You can do it in an
    ad-hoc manner by setting the ``PYTHONPATH`` environment variable:

    .. code-block:: bash

       PYTHONPATH=src pytest

    or in a permanent manner by using the :confval:`pythonpath` configuration variable and adding the
    following to your configuration file:

    .. tab:: toml

        .. code-block:: toml

            [pytest]
            pythonpath = ["src"]

    .. tab:: ini

        .. code-block:: ini

            [pytest]
            pythonpath = src

.. note::

    If you do not use an editable install and do not use the ``src`` layout (``mypkg`` directly in the root
    directory) you can rely on the fact that Python by default puts the current directory in ``sys.path`` to
    import your package and run ``python -m pytest`` to execute the tests against the local copy directly.

    See :ref:`pytest vs python -m pytest` for more information about the difference between calling ``pytest`` and
    ``python -m pytest``.

.. seealso::

    :doc:`packaging:discussions/src-layout-vs-flat-layout`
        The Python Packaging User Guide discusses the trade-offs between the ``src`` layout and ``flat`` layout.

Tests as part of application code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inlining test directories into your application package
is useful if you have direct relation between tests and application modules and
want to distribute them along with your application:

.. code-block:: text

    pyproject.toml
    [src/]mypkg/
        __init__.py
        app.py
        view.py
        tests/
            __init__.py
            test_app.py
            test_view.py
            ...

In this scheme, it is easy to run your tests using the :option:`--pyargs` option:

.. code-block:: bash

    pytest --pyargs mypkg

``pytest`` will discover where ``mypkg`` is installed and collect tests from there.

Note that this layout also works in conjunction with the ``src`` layout mentioned in the previous section.


.. note::

    You can use namespace packages (PEP420) for your application
    but pytest will still perform `test package name`_ discovery based on the
    presence of ``__init__.py`` files.  If you use one of the
    two recommended file system layouts above but leave away the ``__init__.py``
    files from your directories, it should just work.  From
    "inlined tests", however, you will need to use absolute imports for
    getting at your application code.

.. _`test package name`:

.. note::

    In ``prepend`` and ``append`` import-modes, if pytest finds a ``"a/b/test_module.py"``
    test file while recursing into the filesystem it determines the import name
    as follows:

    * determine ``basedir``: this is the first "upward" (towards the root)
      directory not containing an ``__init__.py``.  If e.g. both ``a``
      and ``b`` contain an ``__init__.py`` file then the parent directory
      of ``a`` will become the ``basedir``.

    * perform ``sys.path.insert(0, basedir)`` to make the test module
      importable under the fully qualified import name.

    * ``import a.b.test_module`` where the path is determined
      by converting path separators ``/`` into "." characters.  This means
      you must follow the convention of having directory and file
      names map directly to the import names.

    The reason for this somewhat evolved importing technique is
    that in larger projects multiple test modules might import
    from each other and thus deriving a canonical import name helps
    to avoid surprises such as a test module getting imported twice.

    With :option:`--import-mode=importlib` things are less convoluted because
    pytest doesn't need to change ``sys.path``, making things much less
    surprising.


.. _which-import-mode:

Choosing an import mode
^^^^^^^^^^^^^^^^^^^^^^^

For historical reasons, pytest defaults to the ``prepend`` :ref:`import mode <import-modes>`
instead of the ``importlib`` import mode we recommend for new projects.
The reason lies in the way the ``prepend`` mode works:

Since there are no packages to derive a full package name from,
``pytest`` will import your test files as *top-level* modules.
The test files in the first example (:ref:`src layout <src-layout>`) would be imported as
``test_app`` and ``test_view`` top-level modules by adding ``tests/`` to ``sys.path``.

This results in a drawback compared to the import mode ``importlib``:
your test files must have **unique names**.

If you need to have test modules with the same name,
as a workaround you might add ``__init__.py`` files to your ``tests`` directory and subdirectories,
changing them to packages:

.. code-block:: text

    pyproject.toml
    mypkg/
        ...
    tests/
        __init__.py
        foo/
            __init__.py
            test_view.py
        bar/
            __init__.py
            test_view.py

Now pytest will load the modules as ``tests.foo.test_view`` and ``tests.bar.test_view``,
allowing you to have modules with the same name.
But now this introduces a subtle problem:
in order to load the test modules from the ``tests`` directory,
pytest prepends the root of the repository to ``sys.path``,
which adds the side-effect that now ``mypkg`` is also importable.

This is problematic if you are using a tool like tox_ to test your package in a virtual environment,
because you want to test the *installed* version of your package,
not the local code from the repository.

The ``importlib`` import mode does not have any of the drawbacks above,
because ``sys.path`` is not changed when importing test modules.


.. _`buildout`: http://www.buildout.org/en/latest/

.. _`use tox`:

tox
---

Once you are done with your work and want to make sure that your actual
package passes all tests you may want to look into :doc:`tox <tox:index>`, the
virtualenv test automation tool.
``tox`` helps you to setup virtualenv environments with pre-defined
dependencies and then executing a pre-configured test command with
options.  It will run tests against the installed package and not
against your source code checkout, helping to detect packaging
glitches.

Do not run via setuptools
-------------------------

Integration with setuptools is **not recommended**,
i.e. you should not be using ``python setup.py test`` or ``pytest-runner``,
and may stop working in the future.

This is deprecated since it depends on deprecated features of setuptools
and relies on features that break security mechanisms in pip.
For example 'setup_requires' and 'tests_require' bypass ``pip --require-hashes``.
For more information and migration instructions,
see the `pytest-runner notice <https://github.com/pytest-dev/pytest-runner#deprecation-notice>`_.
See also `pypa/setuptools#1684 <https://github.com/pypa/setuptools/issues/1684>`_.

setuptools intends to
`remove the test command <https://github.com/pypa/setuptools/issues/931>`_.

Checking with flake8-pytest-style
---------------------------------

In order to ensure that pytest is being used correctly in your project,
it can be helpful to use the `flake8-pytest-style <https://github.com/m-burst/flake8-pytest-style>`_ flake8 plugin.

flake8-pytest-style checks for common mistakes and coding style violations in pytest code,
such as incorrect use of fixtures, test function names, and markers.
By using this plugin, you can catch these errors early in the development process
and ensure that your pytest code is consistent and easy to maintain.

A list of the lints detected by flake8-pytest-style can be found on its `PyPI page <https://pypi.org/project/flake8-pytest-style/>`_.

.. note::

    flake8-pytest-style is not an official pytest project. Some of the rules enforce certain style choices, such as using `@pytest.fixture()` over `@pytest.fixture`, but you can configure the plugin to fit your preferred style.

.. _`strict mode`:

Using pytest's strict mode
--------------------------

.. versionadded:: 9.0

Pytest contains a set of configuration options that make it more strict.
The options are off by default for compatibility or other reasons,
but you should enable them if you can.

You can enable all of the strictness options at once by setting the :confval:`strict` configuration option:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        strict = true

.. tab:: ini

    .. code-block:: ini

        [pytest]
        strict = true

See the :confval:`strict` documentation for the options it enables and their effect.

If pytest adds new strictness options in the future, they will also be enabled in strict mode.
Therefore, you should only enable strict mode if you use a pinned/locked version of pytest,
or if you want to proactively adopt new strictness options as they are added.
If you don't want to automatically pick up new options, you can enable options individually:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        strict_config = true
        strict_markers = true
        strict_parametrization_ids = true
        strict_xfail = true

.. tab:: ini

    .. code-block:: ini

        [pytest]
        strict_config = true
        strict_markers = true
        strict_parametrization_ids = true
        strict_xfail = true

If you want to use strict mode but are having trouble with a specific option, you can turn it off individually:

.. tab:: toml

    .. code-block:: toml

        [pytest]
        strict = true
        strict_parametrization_ids = false

.. tab:: ini

    .. code-block:: ini

        [pytest]
        strict = true
        strict_parametrization_ids = false

# pytest import mechanisms and ``sys.path``/``PYTHONPATH``
Source: https://docs.pytest.org/en/stable/explanation/pythonpath.html

.. _pythonpath:

pytest import mechanisms and ``sys.path``/``PYTHONPATH``
========================================================

.. _`import-modes`:

Import modes
------------

pytest as a testing framework needs to import test modules and ``conftest.py`` files for execution.

Importing files in Python is a non-trivial process, so aspects of the
import process can be controlled through the :option:`--import-mode` command-line flag, which can assume
these values:

.. _`import-mode-prepend`:

* ``prepend`` (default): The directory path containing each module will be inserted into the *beginning*
  of :py:data:`sys.path` if not already there, and then imported with
  the :func:`importlib.import_module <importlib.import_module>` function.

  It is highly recommended to arrange your test modules as packages by adding ``__init__.py`` files to your directories
  containing tests. This will make the tests part of a proper Python package, allowing pytest to resolve their full
  name (for example ``tests.core.test_core`` for ``test_core.py`` inside the ``tests.core`` package).

  If the test directory tree is not arranged as packages, then each test file needs to have a unique name
  compared to the other test files, otherwise pytest will raise an error if it finds two tests with the same name.

  This is the classic mechanism, dating back from the time Python 2 was still supported.

.. _`import-mode-append`:

* ``append``: the directory containing each module is appended to the end of :py:data:`sys.path` if not already
  there, and imported with :func:`importlib.import_module <importlib.import_module>`.

  This better allows users to run test modules against installed versions of a package even if the
  package under test has the same import root. For example:

  ::

        testing/__init__.py
        testing/test_pkg_under_test.py
        pkg_under_test/

  the tests will run against the installed version
  of ``pkg_under_test`` when :option:`--import-mode=append` is used whereas
  with ``prepend``, they would pick up the local version. This kind of confusion is why
  we advocate for using :ref:`src-layouts <src-layout>`.

  Same as ``prepend``, requires test module names to be unique when the test directory tree is
  not arranged in packages, because the modules will be put in :py:data:`sys.modules` after importing.

.. _`import-mode-importlib`:

* ``importlib``: this mode uses more fine control mechanisms provided by :mod:`importlib` to import test modules, without changing :py:data:`sys.path`.

  Advantages of this mode:

  * pytest will not change :py:data:`sys.path` at all.
  * Test module names do not need to be unique -- pytest will generate a unique name automatically based on the ``rootdir``.

  Disadvantages:

  * Test modules can't import each other.
  * Testing utility modules in the tests directories (for example a ``tests.helpers`` module containing test-related functions/classes)
    are not importable. The recommendation in this case is to place testing utility modules together with the application/library
    code, for example ``app.testing.helpers``.

    Important: by "test utility modules", we mean functions/classes which are imported by
    other tests directly; this does not include fixtures, which should be placed in ``conftest.py`` files, along
    with the test modules, and are discovered automatically by pytest.

  It works like this:

  1. Given a certain module path, for example ``tests/core/test_models.py``, derives a canonical name
     like ``tests.core.test_models`` and tries to import it.

     For non-test modules, this will work if they are accessible via :py:data:`sys.path`. So
     for example, ``.env/lib/site-packages/app/core.py`` will be importable as ``app.core``.
     This happens when plugins import non-test modules (for example doctesting).

     If this step succeeds, the module is returned.

     For test modules, unless they are reachable from :py:data:`sys.path`, this step will fail.

  2. If the previous step fails, we import the module directly using ``importlib`` facilities, which lets us import it without
     changing :py:data:`sys.path`.

     Because Python requires the module to also be available in :py:data:`sys.modules`, pytest derives a unique name for it based
     on its relative location from the ``rootdir``, and adds the module to :py:data:`sys.modules`.

     For example, ``tests/core/test_models.py`` will end up being imported as the module ``tests.core.test_models``.

  .. versionadded:: 6.0

.. note::

    Initially we intended to make ``importlib`` the default in future releases, however it is clear now that
    it has its own set of drawbacks so the default will remain ``prepend`` for the foreseeable future.

.. note::

    By default, pytest will not attempt to resolve namespace packages automatically, but that can
    be changed via the :confval:`consider_namespace_packages` configuration variable.

.. seealso::

    The :confval:`pythonpath` configuration variable.

    The :confval:`consider_namespace_packages` configuration variable.

    :ref:`test layout`.


``prepend`` and ``append`` import modes scenarios
-------------------------------------------------

Here's a list of scenarios when using ``prepend`` or ``append`` import modes where pytest needs to
change :py:data:`sys.path` in order to import test modules or ``conftest.py`` files, and the issues users
might encounter because of that.

Test modules / ``conftest.py`` files inside packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider this file and directory layout::

    root/
    |- foo/
       |- __init__.py
       |- conftest.py
       |- bar/
          |- __init__.py
          |- tests/
             |- __init__.py
             |- test_foo.py


When executing:

.. code-block:: bash

    pytest root/

pytest will find ``foo/bar/tests/test_foo.py`` and realize it is part of a package given that
there's an ``__init__.py`` file in the same directory. It will then search upwards until it can find the
last directory which still contains an ``__init__.py`` file in order to find the package *root* (in
this case ``foo/``). To load the module, it will insert ``root/``  to the front of
:py:data:`sys.path` (if not there already) in order to load
``test_foo.py`` as the *module* ``foo.bar.tests.test_foo``.

The same logic applies to the ``conftest.py`` file: it will be imported as ``foo.conftest`` module.

Preserving the full package name is important when tests live in a package to avoid problems
and allow test modules to have duplicated names. This is also discussed in detail in
:ref:`test discovery`.

Standalone test modules / ``conftest.py`` files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider this file and directory layout::

    root/
    |- foo/
       |- conftest.py
       |- bar/
          |- tests/
             |- test_foo.py


When executing:

.. code-block:: bash

    pytest root/

pytest will find ``foo/bar/tests/test_foo.py`` and realize it is NOT part of a package given that
there's no ``__init__.py`` file in the same directory. It will then add ``root/foo/bar/tests`` to
:py:data:`sys.path` in order to import ``test_foo.py`` as the *module* ``test_foo``. The same is done
with the ``conftest.py`` file by adding ``root/foo`` to :py:data:`sys.path` to import it as ``conftest``.

For this reason this layout cannot have test modules with the same name, as they all will be
imported in the global import namespace.

This is also discussed in detail in :ref:`test discovery`.

.. _`pytest vs python -m pytest`:

Invoking ``pytest`` versus ``python -m pytest``
-----------------------------------------------

Running pytest with ``pytest [...]`` instead of ``python -m pytest [...]`` yields nearly
equivalent behaviour, except that the latter will add the current directory to :py:data:`sys.path`, which
is standard ``python`` behavior.

See also :ref:`invoke-python`.

# Typing in pytest
Source: https://docs.pytest.org/en/stable/explanation/types.html

.. _types:

Typing in pytest
================

.. note::
    This page assumes the reader is familiar with Python's typing system and its advantages.

    For more information, refer to `Python's Typing Documentation <https://docs.python.org/3/library/typing.html>`_.

Why type tests?
---------------

Typing tests provides significant advantages:

- **Readability:** Clearly defines expected inputs and outputs, improving readability, especially in complex or parameterized tests.

- **Refactoring:** This is the main benefit in typing tests, as it will greatly help with refactoring, letting the type checker point out the necessary changes in both production and tests, without needing to run the full test suite.

For production code, typing also helps catching some bugs that might not be caught by tests at all (regardless of coverage), for example:

.. code-block:: python

    def get_caption(target: int, items: list[tuple[int, str]]) -> str:
        for value, caption in items:
            if value == target:
                return caption


The type checker will correctly error out that the function might return `None`, however even a full coverage test suite might miss that case:

.. code-block:: python

    def test_get_caption() -> None:
        assert get_caption(10, [(1, "foo"), (10, "bar")]) == "bar"


Note the code above has 100% coverage, but the bug is not caught (of course the example is "obvious", but serves to illustrate the point).



Using typing in test suites
---------------------------

To type fixtures in pytest, just add normal types to the fixture functions -- there is nothing special that needs to be done just because of the `fixture` decorator.

.. code-block:: python

    import pytest


    @pytest.fixture
    def sample_fixture() -> int:
        return 38

In the same manner, the fixtures passed to test functions need be annotated with the fixture's return type:

.. code-block:: python

    def test_sample_fixture(sample_fixture: int) -> None:
        assert sample_fixture == 38

From the POV of the type checker, it does not matter that `sample_fixture` is actually a fixture managed by pytest, all it matters to it is that `sample_fixture` is a parameter of type `int`.


The same logic applies to :ref:`@pytest.mark.parametrize <@pytest.mark.parametrize>`:

.. code-block:: python


    @pytest.mark.parametrize("input_value, expected_output", [(1, 2), (5, 6), (10, 11)])
    def test_increment(input_value: int, expected_output: int) -> None:
        assert input_value + 1 == expected_output


The same logic applies when typing fixture functions which receive other fixtures:

.. code-block:: python

    @pytest.fixture
    def mock_env_user(monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("USER", "TestingUser")


Conclusion
----------

Incorporating typing into pytest tests enhances **clarity**, improves **debugging** and **maintenance**, and ensures **type safety**.
These practices lead to a **robust**, **readable**, and **easily maintainable** test suite that is better equipped to handle future changes with minimal risk of errors.

# CI Pipelines
Source: https://docs.pytest.org/en/stable/explanation/ci.html

.. _`ci-pipelines`:

CI Pipelines
============

Rationale
---------

The goal of testing in a CI pipeline is different from testing locally. Indeed,
you can quickly edit some code and run your tests again on your computer, but
it is not possible with CI pipelines. They run on a separate server and are
triggered by specific actions.

From that observation, pytest can detect when it is in a CI environment and
adapt some of its behaviours.

How CI is detected
------------------

Pytest knows it is in a CI environment when either one of these environment variables is set to a non-empty value:

* :envvar:`CI`: used by many CI systems.
* :envvar:`BUILD_NUMBER`: used by Jenkins.

Effects on CI
-------------

For now, the effects on pytest of being in a CI environment are limited.

When a CI environment is detected, the output of the short test summary info is no longer truncated to the terminal size i.e. the entire message will be shown.

  .. code-block:: python

        # content of test_ci.py
        import pytest


        def test_db_initialized():
            pytest.fail(
                "deliberately failing for demo purpose, Lorem ipsum dolor sit amet, "
                "consectetur adipiscing elit. Cras facilisis, massa in suscipit "
                "dignissim, mauris lacus molestie nisi, quis varius metus nulla ut ipsum."
            )


Running this locally, without any extra options, will output:

  .. code-block:: pytest

     $ pytest test_ci.py
     ...
     ========================= short test summary info ==========================
     FAILED test_ci.py::test_db_initialized - Failed: deliberately f...

*(Note the truncated text)*


While running this on CI will output:

  .. code-block:: pytest

     $ export CI=true
     $ pytest test_ci.py
     ...
     ========================= short test summary info ==========================
     FAILED test_ci.py::test_db_initialized - Failed: deliberately failing
     for demo purpose, Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras
     facilisis, massa in suscipit dignissim, mauris lacus molestie nisi, quis varius
     metus nulla ut ipsum.

# Flaky tests
Source: https://docs.pytest.org/en/stable/explanation/flaky.html

Flaky tests
-----------

A "flaky" test is one that exhibits intermittent or sporadic failure, that seems to have non-deterministic behaviour. Sometimes it passes, sometimes it fails, and it's not clear why. This page discusses pytest features that can help and other general strategies for identifying, fixing or mitigating them.

Why flaky tests are a problem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Flaky tests are particularly troublesome when a continuous integration (CI) server is being used, so that all tests must pass before a new code change can be merged. If the test result is not a reliable signal -- that a test failure means the code change broke the test -- developers can become mistrustful of the test results, which can lead to overlooking genuine failures. It is also a source of wasted time as developers must re-run test suites and investigate spurious failures.


Potential root causes
^^^^^^^^^^^^^^^^^^^^^

System state
~~~~~~~~~~~~

Broadly speaking, a flaky test indicates that the test relies on some system state that is not being appropriately controlled - the test environment is not sufficiently isolated. Higher level tests are more likely to be flaky as they rely on more state.

Flaky tests sometimes appear when a test suite is run in parallel (such as use of `pytest-xdist`_). This can indicate a test is reliant on test ordering.

-  Perhaps a different test is failing to clean up after itself and leaving behind data which causes the flaky test to fail.
- The flaky test is reliant on data from a previous test that doesn't clean up after itself, and in parallel runs that previous test is not always present
- Tests that modify global state typically cannot be run in parallel.


Overly strict assertion
~~~~~~~~~~~~~~~~~~~~~~~

Overly strict assertions can cause problems with floating point comparison as well as timing issues. :func:`pytest.approx` is useful here.

Thread safety
~~~~~~~~~~~~~

pytest is single-threaded, executing its tests always in the same thread, sequentially, never spawning any threads itself.

Even in case of plugins which run tests in parallel, for example `pytest-xdist`_, usually work by spawning multiple *processes* and running tests in batches, without using multiple threads.

It is of course possible (and common) for tests and fixtures to spawn threads themselves as part of their testing workflow (for example, a fixture that starts a server thread in the background, or a test which executes production code that spawns threads), but some care must be taken:

* Make sure to eventually wait on any spawned threads -- for example at the end of a test, or during the teardown of a fixture.
* Avoid using primitives provided by pytest (:func:`pytest.warns`, :func:`pytest.raises`, etc) from multiple threads, as they are not thread-safe.

If your test suite uses threads and you are seeing flaky test results, do not discount the possibility that the test is implicitly using global state in pytest itself.

Related features
^^^^^^^^^^^^^^^^

Xfail strict
~~~~~~~~~~~~

:ref:`pytest.mark.xfail ref` with ``strict=False`` can be used to mark a test so that its failure does not cause the whole build to break. This could be considered like a manual quarantine, and is rather dangerous to use permanently.


PYTEST_CURRENT_TEST
~~~~~~~~~~~~~~~~~~~

:envvar:`PYTEST_CURRENT_TEST` may be useful for figuring out "which test got stuck".
See :ref:`pytest current test env` for more details.


Plugins
~~~~~~~

Rerunning any failed tests can mitigate the negative effects of flaky tests by giving them additional chances to pass, so that the overall build does not fail. Several pytest plugins support this:

* `pytest-rerunfailures <https://github.com/pytest-dev/pytest-rerunfailures>`_
* `pytest-replay <https://github.com/ESSS/pytest-replay>`_: This plugin helps to reproduce locally crashes or flaky tests observed during CI runs.
* `pytest-flakefinder <https://github.com/dropbox/pytest-flakefinder>`_ - `blog post <https://blogs.dropbox.com/tech/2016/03/open-sourcing-pytest-tools/>`_

Plugins to deliberately randomize tests can help expose tests with state problems:

* `pytest-random-order <https://github.com/jbasko/pytest-random-order>`_
* `pytest-randomly <https://github.com/pytest-dev/pytest-randomly>`_


Other general strategies
^^^^^^^^^^^^^^^^^^^^^^^^

Split up test suites
~~~~~~~~~~~~~~~~~~~~

It can be common to split a single test suite into two, such as unit vs integration, and only use the unit test suite as a CI gate. This also helps keep build times manageable as high level tests tend to be slower. However, it means it does become possible for code that breaks the build to be merged, so extra vigilance is needed for monitoring the integration test results.


Video/screenshot on failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For UI tests these are important for understanding what the state of the UI was when the test failed. pytest-splinter can be used with plugins like pytest-bdd and can `save a screenshot on test failure <https://pytest-splinter.readthedocs.io/en/latest/#automatic-screenshots-on-test-failure>`_, which can help to isolate the cause.


Delete or rewrite the test
~~~~~~~~~~~~~~~~~~~~~~~~~~

If the functionality is covered by other tests, perhaps the test can be removed. If not, perhaps it can be rewritten at a lower level which will remove the flakiness or make its source more apparent.


Quarantine
~~~~~~~~~~

Mark Lapierre discusses the `Pros and Cons of Quarantined Tests <https://dev.to/mlapierre/pros-and-cons-of-quarantined-tests-2emj>`_ in a post from 2018.



CI tools that rerun on failure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Azure Pipelines (the Azure cloud CI/CD tool, formerly Visual Studio Team Services or VSTS) has a feature to `identify flaky tests <https://docs.microsoft.com/en-us/previous-versions/azure/devops/2017/dec-11-vsts?view=tfs-2017#identify-flaky-tests>`_ and rerun failed tests.



Research
^^^^^^^^

This is a limited list, please submit an issue or pull request to expand it!

* Gao, Zebao, Yalan Liang, Myra B. Cohen, Atif M. Memon, and Zhen Wang. "Making system user interactive tests repeatable: When and what should we control?." In *Software Engineering (ICSE), 2015 IEEE/ACM 37th IEEE International Conference on*, vol. 1, pp. 55-65. IEEE, 2015.  `PDF <http://www.cs.umd.edu/~atif/pubs/gao-icse15.pdf>`__
* Palomba, Fabio, and Andy Zaidman. "Does refactoring of test smells induce fixing flaky tests?." In *Software Maintenance and Evolution (ICSME), 2017 IEEE International Conference on*, pp. 1-12. IEEE, 2017. `PDF in Google Drive <https://drive.google.com/file/d/10HdcCQiuQVgW3yYUJD-TSTq1NbYEprl0/view>`__
* Bell, Jonathan, Owolabi Legunsen, Michael Hilton, Lamyaa Eloussi, Tifany Yung, and Darko Marinov. "DeFlaker: Automatically detecting flaky tests." In *Proceedings of the 2018 International Conference on Software Engineering*. 2018. `PDF <https://www.jonbell.net/icse18-deflaker.pdf#section-Research>`__
* Dutta, Saikat and Shi, August and Choudhary, Rutvik and Zhang, Zhekun and Jain, Aryaman and Misailovic, Sasa. "Detecting flaky tests in probabilistic and machine learning applications." In *Proceedings of the 29th ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA)*, pp. 211-224. ACM, 2020. `PDF <https://www.cs.cornell.edu/~saikatd/papers/flash-issta20.pdf>`__
* Habchi, Sarra and Haben, Guillaume and Sohn, Jeongju and Franci, Adriano and Papadakis, Mike and Cordy, Maxime and Le Traon, Yves. "What Made This Test Flake? Pinpointing Classes Responsible for Test Flakiness." In Proceedings of the 38th IEEE International Conference on Software Maintenance and Evolution (ICSME), IEEE, 2022. `PDF <https://arxiv.org/abs/2207.10143>`__
* Lamprou, Sokrates. "Non-deterministic tests and where to find them: Empirically investigating the relationship between flaky tests and test smells by examining test order dependency." Bachelor thesis, Department of Computer and Information Science, Linköping University, 2022. LIU-IDA/LITH-EX-G–19/056–SE. `PDF <https://www.diva-portal.org/smash/get/diva2:1713691/FULLTEXT01.pdf>`__
* Leinen, Fabian and Elsner, Daniel and Pretschner, Alexander and Stahlbauer, Andreas and Sailer, Michael and Jürgens, Elmar. "Cost of Flaky Tests in Continuous Integration: An Industrial Case Study." Technical University of Munich and CQSE GmbH, Munich, Germany, 2023. `PDF <https://mediatum.ub.tum.de/doc/1730194/1730194.pdf>`__

Resources
^^^^^^^^^

* `Eradicating Non-Determinism in Tests <https://martinfowler.com/articles/nonDeterminism.html>`_ by Martin Fowler, 2011
* `No more flaky tests on the Go team <https://www.thoughtworks.com/insights/blog/no-more-flaky-tests-go-team>`_ by Pavan Sudarshan, 2012
* `The Build That Cried Broken: Building Trust in your Continuous Integration Tests <https://www.youtube.com/embed/VotJqV4n8ig>`_ talk (video) by `Angie Jones <https://angiejones.tech/>`_ at SeleniumConf Austin 2017
* `Test and Code Podcast: Flaky Tests and How to Deal with Them <https://testandcode.com/50>`_ by Brian Okken and Anthony Shaw, 2018
* Microsoft:

  * `How we approach testing VSTS to enable continuous delivery <https://blogs.msdn.microsoft.com/bharry/2017/06/28/testing-in-a-cloud-delivery-cadence/>`_ by Brian Harry MS, 2017
  * `Eliminating Flaky Tests <https://docs.microsoft.com/en-us/azure/devops/learn/devops-at-microsoft/eliminating-flaky-tests>`_ blog and talk (video) by Munil Shah, 2017

* Google:

  * `Flaky Tests at Google and How We Mitigate Them <https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html>`_ by John Micco, 2016
  * `Where do Google's flaky tests come from? <https://testing.googleblog.com/2017/04/where-do-our-flaky-tests-come-from.html>`_  by Jeff Listfield, 2017

* Dropbox:
  * `Athena: Our automated build health management system <https://dropbox.tech/infrastructure/athena-our-automated-build-health-management-system>`_ by Utsav Shah, 2019
  * `How To Manage Flaky Tests in your CI Workflows <https://mill-build.org/blog/4-flaky-tests.html>`_ by Li Haoyi, 2025

* Uber:
  * `Handling Flaky Unit Tests in Java <https://www.uber.com/blog/handling-flaky-tests-java/>`_ by Uber Engineering, 2021
  * `Flaky Tests Overhaul at Uber <https://www.uber.com/blog/flaky-tests-overhaul/>`_ by Uber Engineering, 2024

.. _pytest-xdist: https://github.com/pytest-dev/pytest-xdist

# Examples and customization tricks
Source: https://docs.pytest.org/en/stable/example/index.html

.. _examples:

Examples and customization tricks
=================================

Here is a (growing) list of examples. :ref:`Contact <contact>` us if you
need more examples or have questions. Also take a look at the
:ref:`comprehensive documentation <toc>` which contains many example
snippets as well.  Also, `pytest on stackoverflow.com
<http://stackoverflow.com/search?q=pytest>`_ often comes with example
answers.

For basic examples, see

- :ref:`get-started` for basic introductory examples
- :ref:`assert` for basic assertion examples
- :ref:`Fixtures <fixtures>` for basic fixture/setup examples
- :ref:`parametrize` for basic test function parametrization
- :ref:`unittest` for basic unittest integration

The following examples aim at various use cases you might encounter.

.. toctree::
   :maxdepth: 2

   reportingdemo
   simple
   parametrize
   markers
   special
   pythoncollection
   nonpython
   customdirectory

# Demo of Python failure reports with pytest
Source: https://docs.pytest.org/en/stable/example/reportingdemo.html

.. _`tbreportdemo`:

Demo of Python failure reports with pytest
==========================================

Here is a nice run of several failures and how ``pytest`` presents things:

.. code-block:: pytest

    assertion $ pytest failure_demo.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project/assertion
    collected 44 items

    failure_demo.py FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF         [100%]

    ================================= FAILURES =================================
    ___________________________ test_generative[3-6] ___________________________

    param1 = 3, param2 = 6

        @pytest.mark.parametrize("param1, param2", [(3, 6)])
        def test_generative(param1, param2):
    >       assert param1 * 2 < param2
    E       assert (3 * 2) < 6

    failure_demo.py:21: AssertionError
    _________________________ TestFailing.test_simple __________________________

    self = <failure_demo.TestFailing object at 0xdeadbeef0001>

        def test_simple(self):
            def f():
                return 42

            def g():
                return 43

    >       assert f() == g()
    E       assert 42 == 43
    E        +  where 42 = <function TestFailing.test_simple.<locals>.f at 0xdeadbeef0002>()
    E        +  and   43 = <function TestFailing.test_simple.<locals>.g at 0xdeadbeef0003>()

    failure_demo.py:32: AssertionError
    ____________________ TestFailing.test_simple_multiline _____________________

    self = <failure_demo.TestFailing object at 0xdeadbeef0004>

        def test_simple_multiline(self):
    >       otherfunc_multi(42, 6 * 9)

    failure_demo.py:35:
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    a = 42, b = 54

        def otherfunc_multi(a, b):
    >       assert a == b
    E       assert 42 == 54

    failure_demo.py:16: AssertionError
    ___________________________ TestFailing.test_not ___________________________

    self = <failure_demo.TestFailing object at 0xdeadbeef0005>

        def test_not(self):
            def f():
                return 42

    >       assert not f()
    E       assert not 42
    E        +  where 42 = <function TestFailing.test_not.<locals>.f at 0xdeadbeef0006>()

    failure_demo.py:41: AssertionError
    _________________ TestSpecialisedExplanations.test_eq_text _________________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0007>

        def test_eq_text(self):
    >       assert "spam" == "eggs"
    E       AssertionError: assert 'spam' == 'eggs'
    E
    E         - eggs
    E         + spam

    failure_demo.py:46: AssertionError
    _____________ TestSpecialisedExplanations.test_eq_similar_text _____________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0008>

        def test_eq_similar_text(self):
    >       assert "foo 1 bar" == "foo 2 bar"
    E       AssertionError: assert 'foo 1 bar' == 'foo 2 bar'
    E
    E         - foo 2 bar
    E         ?     ^
    E         + foo 1 bar
    E         ?     ^

    failure_demo.py:49: AssertionError
    ____________ TestSpecialisedExplanations.test_eq_multiline_text ____________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0009>

        def test_eq_multiline_text(self):
    >       assert "foo\nspam\nbar" == "foo\neggs\nbar"
    E       AssertionError: assert 'foo\nspam\nbar' == 'foo\neggs\nbar'
    E
    E           foo
    E         - eggs
    E         + spam
    E           bar

    failure_demo.py:52: AssertionError
    ______________ TestSpecialisedExplanations.test_eq_long_text _______________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef000a>

        def test_eq_long_text(self):
            a = "1" * 100 + "a" + "2" * 100
            b = "1" * 100 + "b" + "2" * 100
    >       assert a == b
    E       AssertionError: assert '111111111111...2222222222222' == '111111111111...2222222222222'
    E
    E         Skipping 90 identical leading characters in diff, use -v to show
    E         Skipping 91 identical trailing characters in diff, use -v to show
    E         - 1111111111b222222222
    E         ?           ^
    E         + 1111111111a222222222
    E         ?           ^

    failure_demo.py:57: AssertionError
    _________ TestSpecialisedExplanations.test_eq_long_text_multiline __________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef000b>

        def test_eq_long_text_multiline(self):
            a = "1\n" * 100 + "a" + "2\n" * 100
            b = "1\n" * 100 + "b" + "2\n" * 100
    >       assert a == b
    E       AssertionError: assert '1\n1\n1\n1\n...n2\n2\n2\n2\n' == '1\n1\n1\n1\n...n2\n2\n2\n2\n'
    E
    E         Skipping 190 identical leading characters in diff, use -v to show
    E         Skipping 191 identical trailing characters in diff, use -v to show
    E           1
    E           1
    E           1
    E           1...
    E
    E         ...Full output truncated (7 lines hidden), use '-vv' to show

    failure_demo.py:62: AssertionError
    _________________ TestSpecialisedExplanations.test_eq_list _________________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef000c>

        def test_eq_list(self):
    >       assert [0, 1, 2] == [0, 1, 3]
    E       assert [0, 1, 2] == [0, 1, 3]
    E
    E         At index 2 diff: 2 != 3
    E         Use -v to get more diff

    failure_demo.py:65: AssertionError
    ______________ TestSpecialisedExplanations.test_eq_list_long _______________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef000d>

        def test_eq_list_long(self):
            a = [0] * 100 + [1] + [3] * 100
            b = [0] * 100 + [2] + [3] * 100
    >       assert a == b
    E       assert [0, 0, 0, 0, 0, 0, ...] == [0, 0, 0, 0, 0, 0, ...]
    E
    E         At index 100 diff: 1 != 2
    E         Use -v to get more diff

    failure_demo.py:70: AssertionError
    _________________ TestSpecialisedExplanations.test_eq_dict _________________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef000e>

        def test_eq_dict(self):
    >       assert {"a": 0, "b": 1, "c": 0} == {"a": 0, "b": 2, "d": 0}
    E       AssertionError: assert {'a': 0, 'b': 1, 'c': 0} == {'a': 0, 'b': 2, 'd': 0}
    E
    E         Omitting 1 identical items, use -vv to show
    E         Differing items:
    E         {'b': 1} != {'b': 2}
    E         Left contains 1 more item:
    E         {'c': 0}
    E         Right contains 1 more item:
    E         {'d': 0}
    E         Use -v to get more diff

    failure_demo.py:73: AssertionError
    _________________ TestSpecialisedExplanations.test_eq_set __________________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef000f>

        def test_eq_set(self):
    >       assert {0, 10, 11, 12} == {0, 20, 21}
    E       assert {0, 10, 11, 12} == {0, 20, 21}
    E
    E         Extra items in the left set:
    E         10
    E         11
    E         12
    E         Extra items in the right set:
    E         20
    E         21
    E         Use -v to get more diff

    failure_demo.py:76: AssertionError
    _____________ TestSpecialisedExplanations.test_eq_longer_list ______________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0010>

        def test_eq_longer_list(self):
    >       assert [1, 2] == [1, 2, 3]
    E       assert [1, 2] == [1, 2, 3]
    E
    E         Right contains one more item: 3
    E         Use -v to get more diff

    failure_demo.py:79: AssertionError
    _________________ TestSpecialisedExplanations.test_in_list _________________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0011>

        def test_in_list(self):
    >       assert 1 in [0, 2, 3, 4, 5]
    E       assert 1 in [0, 2, 3, 4, 5]

    failure_demo.py:82: AssertionError
    __________ TestSpecialisedExplanations.test_not_in_text_multiline __________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0012>

        def test_not_in_text_multiline(self):
            text = "some multiline\ntext\nwhich\nincludes foo\nand a\ntail"
    >       assert "foo" not in text
    E       AssertionError: assert 'foo' not in 'some multil...nand a\ntail'
    E
    E         'foo' is contained here:
    E           some multiline
    E           text
    E           which
    E           includes foo
    E         ?          +++
    E           and a
    E           tail

    failure_demo.py:86: AssertionError
    ___________ TestSpecialisedExplanations.test_not_in_text_single ____________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0013>

        def test_not_in_text_single(self):
            text = "single foo line"
    >       assert "foo" not in text
    E       AssertionError: assert 'foo' not in 'single foo line'
    E
    E         'foo' is contained here:
    E           single foo line
    E         ?        +++

    failure_demo.py:90: AssertionError
    _________ TestSpecialisedExplanations.test_not_in_text_single_long _________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0014>

        def test_not_in_text_single_long(self):
            text = "head " * 50 + "foo " + "tail " * 20
    >       assert "foo" not in text
    E       AssertionError: assert 'foo' not in 'head head h...l tail tail '
    E
    E         'foo' is contained here:
    E           head head foo tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail
    E         ?           +++

    failure_demo.py:94: AssertionError
    ______ TestSpecialisedExplanations.test_not_in_text_single_long_term _______

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0015>

        def test_not_in_text_single_long_term(self):
            text = "head " * 50 + "f" * 70 + "tail " * 20
    >       assert "f" * 70 not in text
    E       AssertionError: assert 'fffffffffff...ffffffffffff' not in 'head head h...l tail tail '
    E
    E         'ffffffffffffffffff...fffffffffffffffffff' is contained here:
    E           head head fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffftail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail tail
    E         ?           ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    failure_demo.py:98: AssertionError
    ______________ TestSpecialisedExplanations.test_eq_dataclass _______________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0016>

        def test_eq_dataclass(self):
            from dataclasses import dataclass

            @dataclass
            class Foo:
                a: int
                b: str

            left = Foo(1, "b")
            right = Foo(1, "c")
    >       assert left == right
    E       AssertionError: assert TestSpecialis...oo(a=1, b='b') == TestSpecialis...oo(a=1, b='c')
    E
    E         Omitting 1 identical items, use -vv to show
    E         Differing attributes:
    E         ['b']
    E
    E         Drill down into differing attribute b:
    E           b: 'b' != 'c'
    E           - c
    E           + b

    failure_demo.py:110: AssertionError
    ________________ TestSpecialisedExplanations.test_eq_attrs _________________

    self = <failure_demo.TestSpecialisedExplanations object at 0xdeadbeef0017>

        def test_eq_attrs(self):
            import attr

            @attr.s
            class Foo:
                a = attr.ib()
                b = attr.ib()

            left = Foo(1, "b")
            right = Foo(1, "c")
    >       assert left == right
    E       AssertionError: assert Foo(a=1, b='b') == Foo(a=1, b='c')
    E
    E         Omitting 1 identical items, use -vv to show
    E         Differing attributes:
    E         ['b']
    E
    E         Drill down into differing attribute b:
    E           b: 'b' != 'c'
    E           - c
    E           + b

    failure_demo.py:122: AssertionError
    ______________________________ test_attribute ______________________________

        def test_attribute():
            class Foo:
                b = 1

            i = Foo()
    >       assert i.b == 2
    E       assert 1 == 2
    E        +  where 1 = <failure_demo.test_attribute.<locals>.Foo object at 0xdeadbeef0018>.b

    failure_demo.py:130: AssertionError
    _________________________ test_attribute_instance __________________________

        def test_attribute_instance():
            class Foo:
                b = 1

    >       assert Foo().b == 2
    E       AssertionError: assert 1 == 2
    E        +  where 1 = <failure_demo.test_attribute_instance.<locals>.Foo object at 0xdeadbeef0019>.b
    E        +    where <failure_demo.test_attribute_instance.<locals>.Foo object at 0xdeadbeef0019> = <class 'failure_demo.test_attribute_instance.<locals>.Foo'>()

    failure_demo.py:137: AssertionError
    __________________________ test_attribute_failure __________________________

        def test_attribute_failure():
            class Foo:
                def _get_b(self):
                    raise Exception("Failed to get attrib")

                b = property(_get_b)

            i = Foo()
    >       assert i.b == 2
                   ^^^

    failure_demo.py:148:
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    self = <failure_demo.test_attribute_failure.<locals>.Foo object at 0xdeadbeef001a>

        def _get_b(self):
    >       raise Exception("Failed to get attrib")
    E       Exception: Failed to get attrib

    failure_demo.py:143: Exception
    _________________________ test_attribute_multiple __________________________

        def test_attribute_multiple():
            class Foo:
                b = 1

            class Bar:
                b = 2

    >       assert Foo().b == Bar().b
    E       AssertionError: assert 1 == 2
    E        +  where 1 = <failure_demo.test_attribute_multiple.<locals>.Foo object at 0xdeadbeef001b>.b
    E        +    where <failure_demo.test_attribute_multiple.<locals>.Foo object at 0xdeadbeef001b> = <class 'failure_demo.test_attribute_multiple.<locals>.Foo'>()
    E        +  and   2 = <failure_demo.test_attribute_multiple.<locals>.Bar object at 0xdeadbeef001c>.b
    E        +    where <failure_demo.test_attribute_multiple.<locals>.Bar object at 0xdeadbeef001c> = <class 'failure_demo.test_attribute_multiple.<locals>.Bar'>()

    failure_demo.py:158: AssertionError
    __________________________ TestRaises.test_raises __________________________

    self = <failure_demo.TestRaises object at 0xdeadbeef001d>

        def test_raises(self):
            s = "qwe"
    >       raises(TypeError, int, s)
    E       ValueError: invalid literal for int() with base 10: 'qwe'

    failure_demo.py:168: ValueError
    ______________________ TestRaises.test_raises_doesnt _______________________

    self = <failure_demo.TestRaises object at 0xdeadbeef001e>

        def test_raises_doesnt(self):
    >       raises(OSError, int, "3")
    E       Failed: DID NOT RAISE OSError

    failure_demo.py:171: Failed
    __________________________ TestRaises.test_raise ___________________________

    self = <failure_demo.TestRaises object at 0xdeadbeef001f>

        def test_raise(self):
    >       raise ValueError("demo error")
    E       ValueError: demo error

    failure_demo.py:174: ValueError
    ________________________ TestRaises.test_tupleerror ________________________

    self = <failure_demo.TestRaises object at 0xdeadbeef0020>

        def test_tupleerror(self):
    >       a, b = [1]  # noqa: F841
            ^^^^
    E       ValueError: not enough values to unpack (expected 2, got 1)

    failure_demo.py:177: ValueError
    ______ TestRaises.test_reinterpret_fails_with_print_for_the_fun_of_it ______

    self = <failure_demo.TestRaises object at 0xdeadbeef0021>

        def test_reinterpret_fails_with_print_for_the_fun_of_it(self):
            items = [1, 2, 3]
            print(f"items is {items!r}")
    >       a, b = items.pop()
            ^^^^
    E       TypeError: cannot unpack non-iterable int object

    failure_demo.py:182: TypeError
    --------------------------- Captured stdout call ---------------------------
    items is [1, 2, 3]
    ________________________ TestRaises.test_some_error ________________________

    self = <failure_demo.TestRaises object at 0xdeadbeef0022>

        def test_some_error(self):
    >       if namenotexi:  # noqa: F821
               ^^^^^^^^^^
    E       NameError: name 'namenotexi' is not defined

    failure_demo.py:185: NameError
    ____________________ test_dynamic_compile_shows_nicely _____________________

        def test_dynamic_compile_shows_nicely():
            import importlib.util
            import sys

            src = "def foo():\n assert 1 == 0\n"
            name = "abc-123"
            spec = importlib.util.spec_from_loader(name, loader=None)
            module = importlib.util.module_from_spec(spec)
            code = compile(src, name, "exec")
            exec(code, module.__dict__)
            sys.modules[name] = module
    >       module.foo()

    failure_demo.py:204:
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    >   ???
    E   AssertionError

    abc-123:2: AssertionError
    ____________________ TestMoreErrors.test_complex_error _____________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef0023>

        def test_complex_error(self):
            def f():
                return 44

            def g():
                return 43

    >       somefunc(f(), g())

    failure_demo.py:215:
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    failure_demo.py:12: in somefunc
        otherfunc(x, y)
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

    a = 44, b = 43

        def otherfunc(a, b):
    >       assert a == b
    E       assert 44 == 43

    failure_demo.py:8: AssertionError
    ___________________ TestMoreErrors.test_z1_unpack_error ____________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef0024>

        def test_z1_unpack_error(self):
            items = []
    >       a, b = items
            ^^^^
    E       ValueError: not enough values to unpack (expected 2, got 0)

    failure_demo.py:219: ValueError
    ____________________ TestMoreErrors.test_z2_type_error _____________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef0025>

        def test_z2_type_error(self):
            items = 3
    >       a, b = items
            ^^^^
    E       TypeError: cannot unpack non-iterable int object

    failure_demo.py:223: TypeError
    ______________________ TestMoreErrors.test_startswith ______________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef0026>

        def test_startswith(self):
            s = "123"
            g = "456"
    >       assert s.startswith(g)
    E       AssertionError: assert False
    E        +  where False = <built-in method startswith of str object at 0xdeadbeef0027>('456')
    E        +    where <built-in method startswith of str object at 0xdeadbeef0027> = '123'.startswith

    failure_demo.py:228: AssertionError
    __________________ TestMoreErrors.test_startswith_nested ___________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef0028>

        def test_startswith_nested(self):
            def f():
                return "123"

            def g():
                return "456"

    >       assert f().startswith(g())
    E       AssertionError: assert False
    E        +  where False = <built-in method startswith of str object at 0xdeadbeef0027>('456')
    E        +    where <built-in method startswith of str object at 0xdeadbeef0027> = '123'.startswith
    E        +      where '123' = <function TestMoreErrors.test_startswith_nested.<locals>.f at 0xdeadbeef0029>()
    E        +    and   '456' = <function TestMoreErrors.test_startswith_nested.<locals>.g at 0xdeadbeef0002>()

    failure_demo.py:237: AssertionError
    _____________________ TestMoreErrors.test_global_func ______________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef002a>

        def test_global_func(self):
    >       assert isinstance(globf(42), float)
    E       assert False
    E        +  where False = isinstance(43, float)
    E        +    where 43 = globf(42)

    failure_demo.py:240: AssertionError
    _______________________ TestMoreErrors.test_instance _______________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef002b>

        def test_instance(self):
            self.x = 6 * 7
    >       assert self.x != 42
    E       assert 42 != 42
    E        +  where 42 = <failure_demo.TestMoreErrors object at 0xdeadbeef002b>.x

    failure_demo.py:244: AssertionError
    _______________________ TestMoreErrors.test_compare ________________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef002c>

        def test_compare(self):
    >       assert globf(10) < 5
    E       assert 11 < 5
    E        +  where 11 = globf(10)

    failure_demo.py:247: AssertionError
    _____________________ TestMoreErrors.test_try_finally ______________________

    self = <failure_demo.TestMoreErrors object at 0xdeadbeef002d>

        def test_try_finally(self):
            x = 1
            try:
    >           assert x == 0
    E           assert 1 == 0

    failure_demo.py:252: AssertionError
    ___________________ TestCustomAssertMsg.test_single_line ___________________

    self = <failure_demo.TestCustomAssertMsg object at 0xdeadbeef002e>

        def test_single_line(self):
            class A:
                a = 1

            b = 2
    >       assert A.a == b, "A.a appears not to be b"
    E       AssertionError: A.a appears not to be b
    E       assert 1 == 2
    E        +  where 1 = <class 'failure_demo.TestCustomAssertMsg.test_single_line.<locals>.A'>.a

    failure_demo.py:263: AssertionError
    ____________________ TestCustomAssertMsg.test_multiline ____________________

    self = <failure_demo.TestCustomAssertMsg object at 0xdeadbeef002f>

        def test_multiline(self):
            class A:
                a = 1

            b = 2
    >       assert A.a == b, (
                "A.a appears not to be b\nor does not appear to be b\none of those"
            )
    E       AssertionError: A.a appears not to be b
    E         or does not appear to be b
    E         one of those
    E       assert 1 == 2
    E        +  where 1 = <class 'failure_demo.TestCustomAssertMsg.test_multiline.<locals>.A'>.a

    failure_demo.py:270: AssertionError
    ___________________ TestCustomAssertMsg.test_custom_repr ___________________

    self = <failure_demo.TestCustomAssertMsg object at 0xdeadbeef0030>

        def test_custom_repr(self):
            class JSON:
                a = 1

                def __repr__(self):
                    return "This is JSON\n{\n  'foo': 'bar'\n}"

            a = JSON()
            b = 2
    >       assert a.a == b, a
    E       AssertionError: This is JSON
    E         {
    E           'foo': 'bar'
    E         }
    E       assert 1 == 2
    E        +  where 1 = This is JSON\n{\n  'foo': 'bar'\n}.a

    failure_demo.py:283: AssertionError
    ========================= short test summary info ==========================
    FAILED failure_demo.py::test_generative[3-6] - assert (3 * 2) < 6
    FAILED failure_demo.py::TestFailing::test_simple - assert 42 == 43
    FAILED failure_demo.py::TestFailing::test_simple_multiline - assert 42 == 54
    FAILED failure_demo.py::TestFailing::test_not - assert not 42
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_text - Asser...
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_similar_text
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_multiline_text
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_long_text - ...
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_long_text_multiline
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_list - asser...
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_list_long - ...
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_dict - Asser...
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_set - assert...
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_longer_list
    FAILED failure_demo.py::TestSpecialisedExplanations::test_in_list - asser...
    FAILED failure_demo.py::TestSpecialisedExplanations::test_not_in_text_multiline
    FAILED failure_demo.py::TestSpecialisedExplanations::test_not_in_text_single
    FAILED failure_demo.py::TestSpecialisedExplanations::test_not_in_text_single_long
    FAILED failure_demo.py::TestSpecialisedExplanations::test_not_in_text_single_long_term
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_dataclass - ...
    FAILED failure_demo.py::TestSpecialisedExplanations::test_eq_attrs - Asse...
    FAILED failure_demo.py::test_attribute - assert 1 == 2
    FAILED failure_demo.py::test_attribute_instance - AssertionError: assert ...
    FAILED failure_demo.py::test_attribute_failure - Exception: Failed to get...
    FAILED failure_demo.py::test_attribute_multiple - AssertionError: assert ...
    FAILED failure_demo.py::TestRaises::test_raises - ValueError: invalid lit...
    FAILED failure_demo.py::TestRaises::test_raises_doesnt - Failed: DID NOT ...
    FAILED failure_demo.py::TestRaises::test_raise - ValueError: demo error
    FAILED failure_demo.py::TestRaises::test_tupleerror - ValueError: not eno...
    FAILED failure_demo.py::TestRaises::test_reinterpret_fails_with_print_for_the_fun_of_it
    FAILED failure_demo.py::TestRaises::test_some_error - NameError: name 'na...
    FAILED failure_demo.py::test_dynamic_compile_shows_nicely - AssertionError
    FAILED failure_demo.py::TestMoreErrors::test_complex_error - assert 44 == 43
    FAILED failure_demo.py::TestMoreErrors::test_z1_unpack_error - ValueError...
    FAILED failure_demo.py::TestMoreErrors::test_z2_type_error - TypeError: c...
    FAILED failure_demo.py::TestMoreErrors::test_startswith - AssertionError:...
    FAILED failure_demo.py::TestMoreErrors::test_startswith_nested - Assertio...
    FAILED failure_demo.py::TestMoreErrors::test_global_func - assert False
    FAILED failure_demo.py::TestMoreErrors::test_instance - assert 42 != 42
    FAILED failure_demo.py::TestMoreErrors::test_compare - assert 11 < 5
    FAILED failure_demo.py::TestMoreErrors::test_try_finally - assert 1 == 0
    FAILED failure_demo.py::TestCustomAssertMsg::test_single_line - Assertion...
    FAILED failure_demo.py::TestCustomAssertMsg::test_multiline - AssertionEr...
    FAILED failure_demo.py::TestCustomAssertMsg::test_custom_repr - Assertion...
    ============================ 44 failed in 0.12s ============================

# Basic patterns and examples
Source: https://docs.pytest.org/en/stable/example/simple.html

Basic patterns and examples
==========================================================

How to change command line options defaults
-------------------------------------------

It can be tedious to type the same series of command line options
every time you use ``pytest``.  For example, if you always want to see
detailed info on skipped and xfailed tests, as well as have terser "dot"
progress output, you can write it into a configuration file:

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    addopts = ["-ra", "-q"]

Alternatively, you can set a ``PYTEST_ADDOPTS`` environment variable to add command
line options while the environment is in use:

.. code-block:: bash

    export PYTEST_ADDOPTS="-v"

Here's how the command-line is built in the presence of ``addopts`` or the environment variable:

.. code-block:: text

    <configuration file addopts> $PYTEST_ADDOPTS <extra command-line arguments>

So if the user executes in the command-line:

.. code-block:: bash

    pytest -m slow

The actual command line executed is:

.. code-block:: bash

    pytest -ra -q -v -m slow

Note that as usual for other command-line applications, in case of conflicting options the last one wins, so the example
above will show verbose output because :option:`-v` overwrites :option:`-q`.


.. _request example:

Pass different values to a test function, depending on command line options
----------------------------------------------------------------------------

.. regendoc:wipe

Suppose we want to write a test that depends on a command line option.
Here is a basic pattern to achieve this:

.. code-block:: python

    # content of test_sample.py
    def test_answer(cmdopt):
        if cmdopt == "type1":
            print("first")
        elif cmdopt == "type2":
            print("second")
        assert 0  # to see what was printed


For this to work we need to add a command line option and
provide the ``cmdopt`` through a :ref:`fixture function <fixture>`:

.. code-block:: python

    # content of conftest.py
    import pytest


    def pytest_addoption(parser):
        parser.addoption(
            "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
        )


    @pytest.fixture
    def cmdopt(request):
        return request.config.getoption("--cmdopt")

Let's run this without supplying our new option:

.. code-block:: pytest

    $ pytest -q test_sample.py
    F                                                                    [100%]
    ================================= FAILURES =================================
    _______________________________ test_answer ________________________________

    cmdopt = 'type1'

        def test_answer(cmdopt):
            if cmdopt == "type1":
                print("first")
            elif cmdopt == "type2":
                print("second")
    >       assert 0  # to see what was printed
            ^^^^^^^^
    E       assert 0

    test_sample.py:6: AssertionError
    --------------------------- Captured stdout call ---------------------------
    first
    ========================= short test summary info ==========================
    FAILED test_sample.py::test_answer - assert 0
    1 failed in 0.12s

And now with supplying a command line option:

.. code-block:: pytest

    $ pytest -q --cmdopt=type2
    F                                                                    [100%]
    ================================= FAILURES =================================
    _______________________________ test_answer ________________________________

    cmdopt = 'type2'

        def test_answer(cmdopt):
            if cmdopt == "type1":
                print("first")
            elif cmdopt == "type2":
                print("second")
    >       assert 0  # to see what was printed
            ^^^^^^^^
    E       assert 0

    test_sample.py:6: AssertionError
    --------------------------- Captured stdout call ---------------------------
    second
    ========================= short test summary info ==========================
    FAILED test_sample.py::test_answer - assert 0
    1 failed in 0.12s

You can see that the command line option arrived in our test.

We could add simple validation for the input by listing the choices:

.. code-block:: python

    # content of conftest.py
    import pytest


    def pytest_addoption(parser):
        parser.addoption(
            "--cmdopt",
            action="store",
            default="type1",
            help="my option: type1 or type2",
            choices=("type1", "type2"),
        )

Now we'll get feedback on a bad argument:

.. code-block:: pytest

    $ pytest -q --cmdopt=type3
    ERROR: usage: pytest [options] [file_or_dir] [file_or_dir] [...]
    pytest: error: argument --cmdopt: invalid choice: 'type3' (choose from 'type1', 'type2')
      inifile: None
      rootdir: /home/sweet/project


If you need to provide more detailed error messages, you can use the
``type`` parameter and raise :exc:`pytest.UsageError`:

.. code-block:: python

    # content of conftest.py
    import pytest


    def type_checker(value):
        msg = "cmdopt must specify a numeric type as typeNNN"
        if not value.startswith("type"):
            raise pytest.UsageError(msg)
        try:
            int(value[4:])
        except ValueError:
            raise pytest.UsageError(msg)

        return value


    def pytest_addoption(parser):
        parser.addoption(
            "--cmdopt",
            action="store",
            default="type1",
            help="my option: type1 or type2",
            type=type_checker,
        )

This completes the basic pattern.  However, one often rather wants to
process command line options outside of the test and rather pass in
different or more complex objects.

Dynamically adding command line options
--------------------------------------------------------------

.. regendoc:wipe

Through :confval:`addopts` you can statically add command line
options for your project.  You can also dynamically modify
the command line arguments before they get processed:

.. code-block:: python

    # installable external plugin
    import sys


    def pytest_load_initial_conftests(args):
        if "xdist" in sys.modules:  # pytest-xdist plugin
            import multiprocessing

            num = max(multiprocessing.cpu_count() / 2, 1)
            args[:] = ["-n", str(num)] + args

If you have the :pypi:`xdist plugin <pytest-xdist>` installed
you will now always perform test runs using a number
of subprocesses close to your CPU. Running in an empty
directory with the above conftest.py:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 0 items

    ========================== no tests ran in 0.12s ===========================

.. _`excontrolskip`:

Control skipping of tests according to command line option
--------------------------------------------------------------

.. regendoc:wipe

Here is a ``conftest.py`` file adding a ``--runslow`` command
line option to control skipping of ``pytest.mark.slow`` marked tests:

.. code-block:: python

    # content of conftest.py

    import pytest


    def pytest_addoption(parser):
        parser.addoption(
            "--runslow", action="store_true", default=False, help="run slow tests"
        )


    def pytest_configure(config):
        config.addinivalue_line("markers", "slow: mark test as slow to run")


    def pytest_collection_modifyitems(config, items):
        if config.getoption("--runslow"):
            # --runslow given in cli: do not skip slow tests
            return
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

We can now write a test module like this:

.. code-block:: python

    # content of test_module.py
    import pytest


    def test_func_fast():
        pass


    @pytest.mark.slow
    def test_func_slow():
        pass

and when running it will see a skipped "slow" test:

.. code-block:: pytest

    $ pytest -rs    # "-rs" means report details on the little 's'
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    test_module.py .s                                                    [100%]

    ========================= short test summary info ==========================
    SKIPPED [1] test_module.py:8: need --runslow option to run
    ======================= 1 passed, 1 skipped in 0.12s =======================

Or run it including the ``slow`` marked test:

.. code-block:: pytest

    $ pytest --runslow
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    test_module.py ..                                                    [100%]

    ============================ 2 passed in 0.12s =============================

.. _`__tracebackhide__`:

Writing well integrated assertion helpers
-----------------------------------------

.. regendoc:wipe

If you have a test helper function called from a test you can
use the ``pytest.fail`` marker to fail a test with a certain message.
The test support function will not show up in the traceback if you
set the ``__tracebackhide__`` option somewhere in the helper function.
Example:

.. code-block:: python

    # content of test_checkconfig.py
    import pytest


    def checkconfig(x):
        __tracebackhide__ = True
        if not hasattr(x, "config"):
            pytest.fail(f"not configured: {x}")


    def test_something():
        checkconfig(42)

The ``__tracebackhide__`` setting influences ``pytest`` showing
of tracebacks: the ``checkconfig`` function will not be shown
unless the :option:`--full-trace` command line option is specified.
Let's run our little function:

.. code-block:: pytest

    $ pytest -q test_checkconfig.py
    F                                                                    [100%]
    ================================= FAILURES =================================
    ______________________________ test_something ______________________________

        def test_something():
    >       checkconfig(42)
    E       Failed: not configured: 42

    test_checkconfig.py:11: Failed
    ========================= short test summary info ==========================
    FAILED test_checkconfig.py::test_something - Failed: not configured: 42
    1 failed in 0.12s

If you only want to hide certain exceptions, you can set ``__tracebackhide__``
to a callable which gets the ``ExceptionInfo`` object. You can for example use
this to make sure unexpected exception types aren't hidden:

.. code-block:: python

    import operator

    import pytest


    class ConfigException(Exception):
        pass


    def checkconfig(x):
        __tracebackhide__ = operator.methodcaller("errisinstance", ConfigException)
        if not hasattr(x, "config"):
            raise ConfigException(f"not configured: {x}")


    def test_something():
        checkconfig(42)

This will avoid hiding the exception traceback on unrelated exceptions (i.e.
bugs in assertion helpers).


Detect if running from within a pytest run
--------------------------------------------------------------

.. regendoc:wipe

Usually it is a bad idea to make application code
behave differently if called from a test.  But if you
absolutely must find out if your application code is
running from a test you can do this:

.. code-block:: python

    import os


    if os.environ.get("PYTEST_VERSION") is not None:
        # Things you want to do if your code is called by pytest.
        ...
    else:
        # Things you want to do if your code is not called by pytest.
        ...


Adding info to test report header
--------------------------------------------------------------

.. regendoc:wipe

It's easy to present extra information in a ``pytest`` run:

.. code-block:: python

    # content of conftest.py


    def pytest_report_header(config):
        return "project deps: mylib-1.1"

which will add the string to the test header accordingly:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    project deps: mylib-1.1
    rootdir: /home/sweet/project
    collected 0 items

    ========================== no tests ran in 0.12s ===========================

.. regendoc:wipe

It is also possible to return a list of strings which will be considered as several
lines of information. You may consider ``config.getoption('verbose')`` in order to
display more information if applicable:

.. code-block:: python

    # content of conftest.py


    def pytest_report_header(config):
        if config.get_verbosity() > 0:
            return ["info1: did you know that ...", "did you?"]

which will add info only when run with "--v":

.. code-block:: pytest

    $ pytest -v
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    info1: did you know that ...
    did you?
    rootdir: /home/sweet/project
    collecting ... collected 0 items

    ========================== no tests ran in 0.12s ===========================

and nothing when run plainly:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 0 items

    ========================== no tests ran in 0.12s ===========================

Profiling test duration
--------------------------

.. regendoc:wipe

.. versionadded: 2.2

If you have a slow running large test suite you might want to find
out which tests are the slowest. Let's make an artificial test suite:

.. code-block:: python

    # content of test_some_are_slow.py
    import time


    def test_funcfast():
        time.sleep(0.1)


    def test_funcslow1():
        time.sleep(0.2)


    def test_funcslow2():
        time.sleep(0.3)

Now we can profile which test functions execute the slowest:

.. code-block:: pytest

    $ pytest --durations=3
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 3 items

    test_some_are_slow.py ...                                            [100%]

    =========================== slowest 3 durations ============================
    0.30s call     test_some_are_slow.py::test_funcslow2
    0.20s call     test_some_are_slow.py::test_funcslow1
    0.10s call     test_some_are_slow.py::test_funcfast
    ============================ 3 passed in 0.12s =============================

Incremental testing - test steps
---------------------------------------------------

.. regendoc:wipe

Sometimes you may have a testing situation which consists of a series
of test steps.  If one step fails it makes no sense to execute further
steps as they are all expected to fail anyway and their tracebacks
add no insight.  Here is a simple ``conftest.py`` file which introduces
an ``incremental`` marker which is to be used on classes:

.. code-block:: python

    # content of conftest.py

    import pytest

    # store history of failures per test class name and per index in parametrize (if parametrize used)
    _test_failed_incremental: dict[str, dict[tuple[int, ...], str]] = {}


    def pytest_runtest_makereport(item, call):
        if "incremental" in item.keywords:
            # incremental marker is used
            if call.excinfo is not None:
                # the test has failed
                # retrieve the class name of the test
                cls_name = str(item.cls)
                # retrieve the index of the test (if parametrize is used in combination with incremental)
                parametrize_index = (
                    tuple(item.callspec.indices.values())
                    if hasattr(item, "callspec")
                    else ()
                )
                # retrieve the name of the test function
                test_name = item.originalname or item.name
                # store in _test_failed_incremental the original name of the failed test
                _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                    parametrize_index, test_name
                )


    def pytest_runtest_setup(item):
        if "incremental" in item.keywords:
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # check if a previous test has failed for this class
            if cls_name in _test_failed_incremental:
                # retrieve the index of the test (if parametrize is used in combination with incremental)
                parametrize_index = (
                    tuple(item.callspec.indices.values())
                    if hasattr(item, "callspec")
                    else ()
                )
                # retrieve the name of the first test function to fail for this class name and index
                test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
                # if name found, test has failed for the combination of class name & test name
                if test_name is not None:
                    pytest.xfail(f"previous test failed ({test_name})")


These two hook implementations work together to abort incremental-marked
tests in a class.  Here is a test module example:

.. code-block:: python

    # content of test_step.py

    import pytest


    @pytest.mark.incremental
    class TestUserHandling:
        def test_login(self):
            pass

        def test_modification(self):
            assert 0

        def test_deletion(self):
            pass


    def test_normal():
        pass

If we run this:

.. code-block:: pytest

    $ pytest -rx
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 4 items

    test_step.py .Fx.                                                    [100%]

    ================================= FAILURES =================================
    ____________________ TestUserHandling.test_modification ____________________

    self = <test_step.TestUserHandling object at 0xdeadbeef0001>

        def test_modification(self):
    >       assert 0
    E       assert 0

    test_step.py:11: AssertionError
    ========================= short test summary info ==========================
    XFAIL test_step.py::TestUserHandling::test_deletion - previous test failed (test_modification)
    ================== 1 failed, 2 passed, 1 xfailed in 0.12s ==================

We'll see that ``test_deletion`` was not executed because ``test_modification``
failed.  It is reported as an "expected failure".


Package/Directory-level fixtures (setups)
-------------------------------------------------------

If you have nested test directories, you can have per-directory fixture scopes
by placing fixture functions in a ``conftest.py`` file in that directory.
You can use all types of fixtures including :ref:`autouse fixtures
<autouse fixtures>` which are the equivalent of xUnit's setup/teardown
concept.  It's however recommended to have explicit fixture references in your
tests or test classes rather than relying on implicitly executing
setup/teardown functions, especially if they are far away from the actual tests.

Here is an example for making a ``db`` fixture available in a directory:

.. code-block:: python

    # content of a/conftest.py
    import pytest


    class DB:
        pass


    @pytest.fixture(scope="package")
    def db():
        return DB()

and then a test module in that directory:

.. code-block:: python

    # content of a/test_db.py
    def test_a1(db):
        assert 0, db  # to show value

another test module:

.. code-block:: python

    # content of a/test_db2.py
    def test_a2(db):
        assert 0, db  # to show value

and then a module in a sister directory which will not see
the ``db`` fixture:

.. code-block:: python

    # content of b/test_error.py
    def test_root(db):  # no db here, will error out
        pass

We can run this:

.. code-block:: pytest

    $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 7 items

    a/test_db.py F                                                       [ 14%]
    a/test_db2.py F                                                      [ 28%]
    b/test_error.py E                                                    [ 42%]
    test_step.py .Fx.                                                    [100%]

    ================================== ERRORS ==================================
    _______________________ ERROR at setup of test_root ________________________
    file /home/sweet/project/b/test_error.py, line 1
      def test_root(db):  # no db here, will error out
    E       fixture 'db' not found
    >       available fixtures: cache, capfd, capfdbinary, caplog, capsys, capsysbinary, capteesys, doctest_namespace, monkeypatch, pytestconfig, record_property, record_testsuite_property, record_xml_attribute, recwarn, subtests, tmp_path, tmp_path_factory, tmpdir, tmpdir_factory
    >       use 'pytest --fixtures [testpath]' for help on them.

    /home/sweet/project/b/test_error.py:1
    ================================= FAILURES =================================
    _________________________________ test_a1 __________________________________

    db = <conftest.DB object at 0xdeadbeef0002>

        def test_a1(db):
    >       assert 0, db  # to show value
            ^^^^^^^^^^^^
    E       AssertionError: <conftest.DB object at 0xdeadbeef0002>
    E       assert 0

    a/test_db.py:2: AssertionError
    _________________________________ test_a2 __________________________________

    db = <conftest.DB object at 0xdeadbeef0002>

        def test_a2(db):
    >       assert 0, db  # to show value
            ^^^^^^^^^^^^
    E       AssertionError: <conftest.DB object at 0xdeadbeef0002>
    E       assert 0

    a/test_db2.py:2: AssertionError
    ____________________ TestUserHandling.test_modification ____________________

    self = <test_step.TestUserHandling object at 0xdeadbeef0003>

        def test_modification(self):
    >       assert 0
    E       assert 0

    test_step.py:11: AssertionError
    ========================= short test summary info ==========================
    FAILED a/test_db.py::test_a1 - AssertionError: <conftest.DB object at 0x7...
    FAILED a/test_db2.py::test_a2 - AssertionError: <conftest.DB object at 0x...
    FAILED test_step.py::TestUserHandling::test_modification - assert 0
    ERROR b/test_error.py::test_root
    ============= 3 failed, 2 passed, 1 xfailed, 1 error in 0.12s ==============

The two test modules in the ``a`` directory see the same ``db`` fixture instance
while the one test in the sister-directory ``b`` doesn't see it.  We could of course
also define a ``db`` fixture in that sister directory's ``conftest.py`` file.
Note that each fixture is only instantiated if there is a test actually needing
it (unless you use "autouse" fixtures which are always executed ahead of the first test
executing).


Post-process test reports / failures
---------------------------------------

If you want to postprocess test reports and need access to the executing
environment you can implement a hook that gets called when the test
"report" object is about to be created.  Here we write out all failing
test calls and also access a fixture (if it was used by the test) in
case you want to query/look at it during your post processing.  In our
case we just write some information out to a ``failures`` file:

.. code-block:: python

    # content of conftest.py

    import os.path

    import pytest


    @pytest.hookimpl(wrapper=True, tryfirst=True)
    def pytest_runtest_makereport(item, call):
        # execute all other hooks to obtain the report object
        rep = yield

        # we only look at actual failing test calls, not setup/teardown
        if rep.when == "call" and rep.failed:
            mode = "a" if os.path.exists("failures") else "w"
            with open("failures", mode, encoding="utf-8") as f:
                # let's also access a fixture for the fun of it
                if "tmp_path" in item.fixturenames:
                    extra = " ({})".format(item.funcargs["tmp_path"])
                else:
                    extra = ""

                f.write(rep.nodeid + extra + "\n")

        return rep


if you then have failing tests:

.. code-block:: python

    # content of test_module.py
    def test_fail1(tmp_path):
        assert 0


    def test_fail2():
        assert 0

and run them:

.. code-block:: pytest

    $ pytest test_module.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    test_module.py FF                                                    [100%]

    ================================= FAILURES =================================
    ________________________________ test_fail1 ________________________________

    tmp_path = PosixPath('PYTEST_TMPDIR/test_fail10')

        def test_fail1(tmp_path):
    >       assert 0
    E       assert 0

    test_module.py:2: AssertionError
    ________________________________ test_fail2 ________________________________

        def test_fail2():
    >       assert 0
    E       assert 0

    test_module.py:6: AssertionError
    ========================= short test summary info ==========================
    FAILED test_module.py::test_fail1 - assert 0
    FAILED test_module.py::test_fail2 - assert 0
    ============================ 2 failed in 0.12s =============================

you will have a "failures" file which contains the failing test ids:

.. code-block:: bash

    $ cat failures
    test_module.py::test_fail1 (PYTEST_TMPDIR/test_fail10)
    test_module.py::test_fail2

Making test result information available in fixtures
-----------------------------------------------------------

.. regendoc:wipe

If you want to make test result reports available in fixture finalizers
here is a little example implemented via a local plugin:

.. code-block:: python

    # content of conftest.py
    import pytest
    from pytest import StashKey, CollectReport

    phase_report_key = StashKey[dict[str, CollectReport]]()


    @pytest.hookimpl(wrapper=True, tryfirst=True)
    def pytest_runtest_makereport(item, call):
        # execute all other hooks to obtain the report object
        rep = yield

        # store test results for each phase of a call, which can
        # be "setup", "call", "teardown"
        item.stash.setdefault(phase_report_key, {})[rep.when] = rep

        return rep


    @pytest.fixture
    def something(request):
        yield
        # request.node is an "item" because we use the default
        # "function" scope
        report = request.node.stash[phase_report_key]
        if report["setup"].failed:
            print("setting up a test failed", request.node.nodeid)
        elif report["setup"].skipped:
            print("setting up a test skipped", request.node.nodeid)
        elif ("call" not in report) or report["call"].failed:
            print("executing test failed or skipped", request.node.nodeid)


if you then have failing tests:

.. code-block:: python

    # content of test_module.py

    import pytest


    @pytest.fixture
    def other():
        assert 0


    def test_setup_fails(something, other):
        pass


    def test_call_fails(something):
        assert 0


    def test_fail2():
        assert 0

and run it:

.. code-block:: pytest

    $ pytest -s test_module.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 3 items

    test_module.py Esetting up a test failed test_module.py::test_setup_fails
    Fexecuting test failed or skipped test_module.py::test_call_fails
    F

    ================================== ERRORS ==================================
    ____________________ ERROR at setup of test_setup_fails ____________________

        @pytest.fixture
        def other():
    >       assert 0
    E       assert 0

    test_module.py:7: AssertionError
    ================================= FAILURES =================================
    _____________________________ test_call_fails ______________________________

    something = None

        def test_call_fails(something):
    >       assert 0
    E       assert 0

    test_module.py:15: AssertionError
    ________________________________ test_fail2 ________________________________

        def test_fail2():
    >       assert 0
    E       assert 0

    test_module.py:19: AssertionError
    ========================= short test summary info ==========================
    FAILED test_module.py::test_call_fails - assert 0
    FAILED test_module.py::test_fail2 - assert 0
    ERROR test_module.py::test_setup_fails - assert 0
    ======================== 2 failed, 1 error in 0.12s ========================

You'll see that the fixture finalizers could use the precise reporting
information.

.. _pytest current test env:

``PYTEST_CURRENT_TEST`` environment variable
--------------------------------------------



Sometimes a test session might get stuck and there might be no easy way to figure out
which test got stuck, for example if pytest was run in quiet mode (:option:`-q`) or you don't have access to the console
output. This is particularly a problem if the problem happens only sporadically, the famous "flaky" kind of tests.

``pytest`` sets the :envvar:`PYTEST_CURRENT_TEST` environment variable when running tests, which can be inspected
by process monitoring utilities or libraries like :pypi:`psutil` to discover which test got stuck if necessary:

.. code-block:: python

    import psutil

    for pid in psutil.pids():
        environ = psutil.Process(pid).environ()
        if "PYTEST_CURRENT_TEST" in environ:
            print(f'pytest process {pid} running: {environ["PYTEST_CURRENT_TEST"]}')

During the test session pytest will set ``PYTEST_CURRENT_TEST`` to the current test
:ref:`nodeid <nodeids>` and the current stage, which can be ``setup``, ``call``,
or ``teardown``.

For example, when running a single test function named ``test_foo`` from ``foo_module.py``,
``PYTEST_CURRENT_TEST`` will be set to:

#. ``foo_module.py::test_foo (setup)``
#. ``foo_module.py::test_foo (call)``
#. ``foo_module.py::test_foo (teardown)``

In that order.

.. note::

    The contents of ``PYTEST_CURRENT_TEST`` is meant to be human readable and the actual format
    can be changed between releases (even bug fixes) so it shouldn't be relied on for scripting
    or automation.

.. _freezing-pytest:

Freezing pytest
---------------

If you freeze your application using a tool like
`PyInstaller <https://pyinstaller.readthedocs.io>`_
in order to distribute it to your end-users, it is a good idea to also package
your test runner and run your tests using the frozen application. This way packaging
errors such as dependencies not being included into the executable can be detected early
while also allowing you to send test files to users so they can run them in their
machines, which can be useful to obtain more information about a hard to reproduce bug.

Fortunately recent ``PyInstaller`` releases already have a custom hook
for pytest, but if you are using another tool to freeze executables
such as ``cx_freeze`` or ``py2exe``, you can use ``pytest.freeze_includes()``
to obtain the full list of internal pytest modules. How to configure the tools
to find the internal modules varies from tool to tool, however.

Instead of freezing the pytest runner as a separate executable, you can make
your frozen program work as the pytest runner by some clever
argument handling during program startup. This allows you to
have a single executable, which is usually more convenient.
Please note that the mechanism for plugin discovery used by pytest (:ref:`entry
points <pip-installable plugins>`) doesn't work with frozen executables so pytest
can't find any third party plugins automatically. To include third party plugins
like ``pytest-timeout`` they must be imported explicitly and passed on to pytest.main.

.. code-block:: python

    # contents of app_main.py
    import sys

    import pytest_timeout  # Third party plugin

    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        import pytest

        sys.exit(pytest.main(sys.argv[2:], plugins=[pytest_timeout]))
    else:
        # normal application execution: at this point argv can be parsed
        # by your argument-parsing library of choice as usual
        ...


This allows you to execute tests using the frozen
application with standard ``pytest`` command-line options:

.. code-block:: bash

    ./app_main --pytest --verbose --tb=long --junit=xml=results.xml test-suite/

# Parametrizing tests
Source: https://docs.pytest.org/en/stable/example/parametrize.html

.. _paramexamples:

Parametrizing tests
=================================================

``pytest`` allows you to easily parametrize test functions.
For basic docs, see :ref:`parametrize-basics`.

In the following we provide some examples using
the builtin mechanisms.

Generating parameters combinations, depending on command line
----------------------------------------------------------------------------

.. regendoc:wipe

Let's say we want to execute a test with different computation
parameters and the parameter range shall be determined by a command
line argument.  Let's first write a simple (do-nothing) computation test:

.. code-block:: python

    # content of test_compute.py


    def test_compute(param1):
        assert param1 < 4

Now we add a test configuration like this:

.. code-block:: python

    # content of conftest.py


    def pytest_addoption(parser):
        parser.addoption("--all", action="store_true", help="run all combinations")


    def pytest_generate_tests(metafunc):
        if "param1" in metafunc.fixturenames:
            if metafunc.config.getoption("all"):
                end = 5
            else:
                end = 2
            metafunc.parametrize("param1", range(end))

This means that we only run 2 tests if we do not pass ``--all``:

.. code-block:: pytest

    $ pytest -q test_compute.py
    ..                                                                   [100%]
    2 passed in 0.12s

We run only two computations, so we see two dots.
let's run the full monty:

.. code-block:: pytest

    $ pytest -q --all
    ....F                                                                [100%]
    ================================= FAILURES =================================
    _____________________________ test_compute[4] ______________________________

    param1 = 4

        def test_compute(param1):
    >       assert param1 < 4
    E       assert 4 < 4

    test_compute.py:4: AssertionError
    ========================= short test summary info ==========================
    FAILED test_compute.py::test_compute[4] - assert 4 < 4
    1 failed, 4 passed in 0.12s

As expected when running the full range of ``param1`` values
we'll get an error on the last one.


Different options for test IDs
------------------------------------

pytest will build a string that is the test ID for each set of values in a
parametrized test. These IDs can be used with :option:`-k` to select specific cases
to run, and they will also identify the specific case when one is failing.
Running pytest with :option:`--collect-only` will show the generated IDs.

Numbers, strings, booleans and None will have their usual string representation
used in the test ID. For other objects, pytest will make a string based on
the argument name:

.. code-block:: python

    # content of test_time.py

    from datetime import datetime, timedelta

    import pytest

    testdata = [
        (datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1)),
        (datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1)),
    ]


    @pytest.mark.parametrize("a,b,expected", testdata)
    def test_timedistance_v0(a, b, expected):
        diff = a - b
        assert diff == expected


    @pytest.mark.parametrize("a,b,expected", testdata, ids=["forward", "backward"])
    def test_timedistance_v1(a, b, expected):
        diff = a - b
        assert diff == expected


    def idfn(val):
        if isinstance(val, (datetime,)):
            # note this wouldn't show any hours/minutes/seconds
            return val.strftime("%Y%m%d")


    @pytest.mark.parametrize("a,b,expected", testdata, ids=idfn)
    def test_timedistance_v2(a, b, expected):
        diff = a - b
        assert diff == expected


    @pytest.mark.parametrize(
        "a,b,expected",
        [
            pytest.param(
                datetime(2001, 12, 12), datetime(2001, 12, 11), timedelta(1), id="forward"
            ),
            pytest.param(
                datetime(2001, 12, 11), datetime(2001, 12, 12), timedelta(-1), id="backward"
            ),
        ],
    )
    def test_timedistance_v3(a, b, expected):
        diff = a - b
        assert diff == expected

In ``test_timedistance_v0``, we let pytest generate the test IDs.

In ``test_timedistance_v1``, we specified ``ids`` as a list of strings which were
used as the test IDs. These are succinct, but can be a pain to maintain.

In ``test_timedistance_v2``, we specified ``ids`` as a function that can generate a
string representation to make part of the test ID. So our ``datetime`` values use the
label generated by ``idfn``, but because we didn't generate a label for ``timedelta``
objects, they are still using the default pytest representation:

.. code-block:: pytest

    $ pytest test_time.py --collect-only
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 8 items

    <Dir parametrize.rst-215>
      <Module test_time.py>
        <Function test_timedistance_v0[a0-b0-expected0]>
        <Function test_timedistance_v0[a1-b1-expected1]>
        <Function test_timedistance_v1[forward]>
        <Function test_timedistance_v1[backward]>
        <Function test_timedistance_v2[20011212-20011211-expected0]>
        <Function test_timedistance_v2[20011211-20011212-expected1]>
        <Function test_timedistance_v3[forward]>
        <Function test_timedistance_v3[backward]>

    ======================== 8 tests collected in 0.12s ========================

In ``test_timedistance_v3``, we used ``pytest.param`` to specify the test IDs
together with the actual data, instead of listing them separately.

A quick port of "testscenarios"
------------------------------------

Here is a quick port to run tests configured with :pypi:`testscenarios`,
an add-on from Robert Collins for the standard unittest framework. We
only have to work a bit to construct the correct arguments for pytest's
:py:func:`Metafunc.parametrize <pytest.Metafunc.parametrize>`:

.. code-block:: python

    # content of test_scenarios.py


    def pytest_generate_tests(metafunc):
        idlist = []
        argvalues = []
        for scenario in metafunc.cls.scenarios:
            idlist.append(scenario[0])
            items = scenario[1].items()
            argnames = [x[0] for x in items]
            argvalues.append([x[1] for x in items])
        metafunc.parametrize(argnames, argvalues, ids=idlist, scope="class")


    scenario1 = ("basic", {"attribute": "value"})
    scenario2 = ("advanced", {"attribute": "value2"})


    class TestSampleWithScenarios:
        scenarios = [scenario1, scenario2]

        def test_demo1(self, attribute):
            assert isinstance(attribute, str)

        def test_demo2(self, attribute):
            assert isinstance(attribute, str)

this is a fully self-contained example which you can run with:

.. code-block:: pytest

    $ pytest test_scenarios.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 4 items

    test_scenarios.py ....                                               [100%]

    ============================ 4 passed in 0.12s =============================

If you just collect tests you'll also nicely see 'advanced' and 'basic' as variants for the test function:

.. code-block:: pytest

    $ pytest --collect-only test_scenarios.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 4 items

    <Dir parametrize.rst-215>
      <Module test_scenarios.py>
        <Class TestSampleWithScenarios>
          <Function test_demo1[basic]>
          <Function test_demo2[basic]>
          <Function test_demo1[advanced]>
          <Function test_demo2[advanced]>

    ======================== 4 tests collected in 0.12s ========================

Note that we told ``metafunc.parametrize()`` that your scenario values
should be considered class-scoped.  With pytest-2.3 this leads to a
resource-based ordering.

Deferring the setup of parametrized resources
---------------------------------------------------

.. regendoc:wipe

The parametrization of test functions happens at collection
time.  It is a good idea to setup expensive resources like DB
connections or subprocess only when the actual test is run.
Here is a simple example how you can achieve that. This test
requires a ``db`` object fixture:

.. code-block:: python

    # content of test_backends.py

    import pytest


    def test_db_initialized(db):
        # a dummy test
        if db.__class__.__name__ == "DB2":
            pytest.fail("deliberately failing for demo purposes")

We can now add a test configuration that generates two invocations of
the ``test_db_initialized`` function and also implements a factory that
creates a database object for the actual test invocations:

.. code-block:: python

    # content of conftest.py
    import pytest


    def pytest_generate_tests(metafunc):
        if "db" in metafunc.fixturenames:
            metafunc.parametrize("db", ["d1", "d2"], indirect=True)


    class DB1:
        "one database object"


    class DB2:
        "alternative database object"


    @pytest.fixture
    def db(request):
        if request.param == "d1":
            return DB1()
        elif request.param == "d2":
            return DB2()
        else:
            raise ValueError("invalid internal test config")

Let's first see how it looks like at collection time:

.. code-block:: pytest

    $ pytest test_backends.py --collect-only
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    <Dir parametrize.rst-215>
      <Module test_backends.py>
        <Function test_db_initialized[d1]>
        <Function test_db_initialized[d2]>

    ======================== 2 tests collected in 0.12s ========================

And then when we run the test:

.. code-block:: pytest

    $ pytest -q test_backends.py
    .F                                                                   [100%]
    ================================= FAILURES =================================
    _________________________ test_db_initialized[d2] __________________________

    db = <conftest.DB2 object at 0xdeadbeef0001>

        def test_db_initialized(db):
            # a dummy test
            if db.__class__.__name__ == "DB2":
    >           pytest.fail("deliberately failing for demo purposes")
    E           Failed: deliberately failing for demo purposes

    test_backends.py:8: Failed
    ========================= short test summary info ==========================
    FAILED test_backends.py::test_db_initialized[d2] - Failed: deliberately f...
    1 failed, 1 passed in 0.12s

The first invocation with ``db == "DB1"`` passed while the second with ``db == "DB2"`` failed.  Our ``db`` fixture function has instantiated each of the DB values during the setup phase while the ``pytest_generate_tests`` generated two according calls to the ``test_db_initialized`` during the collection phase.

Indirect parametrization
---------------------------------------------------

Using the ``indirect=True`` parameter when parametrizing a test allows one to
parametrize a test with a fixture receiving the values before passing them to a
test:

.. code-block:: python

    import pytest


    @pytest.fixture
    def fixt(request):
        return request.param * 3


    @pytest.mark.parametrize("fixt", ["a", "b"], indirect=True)
    def test_indirect(fixt):
        assert len(fixt) == 3


This can be used, for example, to do more expensive setup at test run time in
the fixture, rather than having to run those setup steps at collection time.

.. note::

    The ``request`` argument used by the fixture is pytest's built-in
    :py:class:`FixtureRequest <pytest.FixtureRequest>` fixture. For indirect
    parametrization, the value supplied to the test parameter is passed to the
    fixture and made available as ``request.param``.

    For more information, see :ref:`fixture-parametrize`.

.. regendoc:wipe

Apply indirect on particular arguments
---------------------------------------------------

Very often parametrization uses more than one argument name. There is opportunity to apply ``indirect``
parameter on particular arguments. It can be done by passing list or tuple of
arguments' names to ``indirect``. In the example below there is a function ``test_indirect`` which uses
two fixtures: ``x`` and ``y``. Here we give to indirect the list, which contains the name of the
fixture ``x``. The indirect parameter will be applied to this argument only, and the value ``a``
will be passed to respective fixture function:

.. code-block:: python

    # content of test_indirect_list.py

    import pytest


    @pytest.fixture(scope="function")
    def x(request):
        return request.param * 3


    @pytest.fixture(scope="function")
    def y(request):
        return request.param * 2


    @pytest.mark.parametrize("x, y", [("a", "b")], indirect=["x"])
    def test_indirect(x, y):
        assert x == "aaa"
        assert y == "b"

The result of this test will be successful:

.. code-block:: pytest

    $ pytest -v test_indirect_list.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 1 item

    test_indirect_list.py::test_indirect[a-b] PASSED                     [100%]

    ============================ 1 passed in 0.12s =============================

.. regendoc:wipe

Parametrizing test methods through per-class configuration
--------------------------------------------------------------

.. _`unittest parametrizer`: https://github.com/testing-cabal/unittest-ext/blob/master/params.py


Here is an example ``pytest_generate_tests`` function implementing a
parametrization scheme similar to Michael Foord's `unittest
parametrizer`_ but in a lot less code:

.. code-block:: python

    # content of ./test_parametrize.py
    import pytest


    def pytest_generate_tests(metafunc):
        # called once per each test function
        funcarglist = metafunc.cls.params[metafunc.function.__name__]
        argnames = sorted(funcarglist[0])
        metafunc.parametrize(
            argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
        )


    class TestClass:
        # a map specifying multiple argument sets for a test method
        params = {
            "test_equals": [dict(a=1, b=2), dict(a=3, b=3)],
            "test_zerodivision": [dict(a=1, b=0)],
        }

        def test_equals(self, a, b):
            assert a == b

        def test_zerodivision(self, a, b):
            with pytest.raises(ZeroDivisionError):
                a / b

Our test generator looks up a class-level definition which specifies which
argument sets to use for each test function.  Let's run it:

.. code-block:: pytest

    $ pytest -q
    F..                                                                  [100%]
    ================================= FAILURES =================================
    ________________________ TestClass.test_equals[1-2] ________________________

    self = <test_parametrize.TestClass object at 0xdeadbeef0002>, a = 1, b = 2

        def test_equals(self, a, b):
    >       assert a == b
    E       assert 1 == 2

    test_parametrize.py:21: AssertionError
    ========================= short test summary info ==========================
    FAILED test_parametrize.py::TestClass::test_equals[1-2] - assert 1 == 2
    1 failed, 2 passed in 0.12s

Parametrization with multiple fixtures
--------------------------------------

Here is a stripped down real-life example of using parametrized
testing for testing serialization of objects between different python
interpreters.  We define a ``test_basic_objects`` function which
is to be run with different sets of arguments for its three arguments:

* ``python1``: first python interpreter, run to pickle-dump an object to a file
* ``python2``: second interpreter, run to pickle-load an object from a file
* ``obj``: object to be dumped/loaded

.. literalinclude:: multipython.py

Running it results in some skips if we don't have all the python interpreters installed and otherwise runs all combinations (3 interpreters times 3 interpreters times 3 objects to serialize/deserialize):

.. code-block:: pytest

   . $ pytest -rs -q multipython.py
   ssssssssssss......sss......                                          [100%]
   ========================= short test summary info ==========================
   SKIPPED [15] multipython.py:67: 'python3.11' not found
   12 passed, 15 skipped in 0.12s

Parametrization of optional implementations/imports
---------------------------------------------------

If you want to compare the outcomes of several implementations of a given
API, you can write test functions that receive the already imported implementations
and get skipped in case the implementation is not importable/available.  Let's
say we have a "base" implementation and the other (possibly optimized ones)
need to provide similar results:

.. code-block:: python

    # content of conftest.py

    import pytest


    @pytest.fixture(scope="session")
    def basemod(request):
        return pytest.importorskip("base")


    @pytest.fixture(scope="session", params=["opt1", "opt2"])
    def optmod(request):
        return pytest.importorskip(request.param)

And then a base implementation of a simple function:

.. code-block:: python

    # content of base.py
    def func1():
        return 1

And an optimized version:

.. code-block:: python

    # content of opt1.py
    def func1():
        return 1.0001

And finally a little test module:

.. code-block:: python

    # content of test_module.py


    def test_func1(basemod, optmod):
        assert round(basemod.func1(), 3) == round(optmod.func1(), 3)


If you run this with reporting for skips enabled:

.. code-block:: pytest

    $ pytest -rs test_module.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 2 items

    test_module.py .s                                                    [100%]

    ========================= short test summary info ==========================
    SKIPPED [1] test_module.py:3: could not import 'opt2': No module named 'opt2'
    ======================= 1 passed, 1 skipped in 0.12s =======================

You'll see that we don't have an ``opt2`` module and thus the second test run
of our ``test_func1`` was skipped.  A few notes:

- the fixture functions in the ``conftest.py`` file are "session-scoped" because we
  don't need to import more than once

- if you have multiple test functions and a skipped import, you will see
  the ``[1]`` count increasing in the report

- you can put :ref:`@pytest.mark.parametrize <@pytest.mark.parametrize>` style
  parametrization on the test functions to parametrize input/output
  values as well.


Set marks or test ID for individual parametrized test
--------------------------------------------------------------------

Use ``pytest.param`` to apply marks or set test ID to individual parametrized test.
For example:

.. code-block:: python

    # content of test_pytest_param_example.py
    import pytest


    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ("3+5", 8),
            pytest.param("1+7", 8, marks=pytest.mark.basic),
            pytest.param("2+4", 6, marks=pytest.mark.basic, id="basic_2+4"),
            pytest.param(
                "6*9", 42, marks=[pytest.mark.basic, pytest.mark.xfail], id="basic_6*9"
            ),
        ],
    )
    def test_eval(test_input, expected):
        assert eval(test_input) == expected

In this example, we have 4 parametrized tests. Except for the first test,
we mark the rest three parametrized tests with the custom marker ``basic``,
and for the fourth test we also use the built-in mark ``xfail`` to indicate this
test is expected to fail. For explicitness, we set test ids for some tests.

Then run ``pytest`` with verbose mode and with only the ``basic`` marker:

.. code-block:: pytest

    $ pytest -v -m basic
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 24 items / 21 deselected / 3 selected

    test_pytest_param_example.py::test_eval[1+7-8] PASSED                [ 33%]
    test_pytest_param_example.py::test_eval[basic_2+4] PASSED            [ 66%]
    test_pytest_param_example.py::test_eval[basic_6*9] XFAIL             [100%]

    =============== 2 passed, 21 deselected, 1 xfailed in 0.12s ================

As the result:

- Four tests were collected
- One test was deselected because it doesn't have the ``basic`` mark.
- Three tests with the ``basic`` mark were selected.
- The test ``test_eval[1+7-8]`` passed, but the name is autogenerated and confusing.
- The test ``test_eval[basic_2+4]`` passed.
- The test ``test_eval[basic_6*9]`` was expected to fail and did fail.

.. _`parametrizing_conditional_raising`:

Parametrizing conditional raising
--------------------------------------------------------------------

Use :func:`pytest.raises` with the
:ref:`pytest.mark.parametrize ref` decorator to write parametrized tests
in which some tests raise exceptions and others do not.

``contextlib.nullcontext`` can be used to test cases that are not expected to
raise exceptions but that should result in some value. The value is given as the
``enter_result`` parameter, which will be available as the ``with`` statement’s
target (``e`` in the example below).

For example:

.. code-block:: python

    from contextlib import nullcontext

    import pytest


    @pytest.mark.parametrize(
        "example_input,expectation",
        [
            (3, nullcontext(2)),
            (2, nullcontext(3)),
            (1, nullcontext(6)),
            (0, pytest.raises(ZeroDivisionError)),
        ],
    )
    def test_division(example_input, expectation):
        """Test how much I know division."""
        with expectation as e:
            assert (6 / example_input) == e

In the example above, the first three test cases should run without any
exceptions, while the fourth should raise a ``ZeroDivisionError`` exception,
which is expected by pytest.

# Working with custom markers
Source: https://docs.pytest.org/en/stable/example/markers.html

.. _`mark examples`:

Working with custom markers
=================================================

Here are some examples using the :ref:`mark` mechanism.

.. _`mark run`:

Marking test functions and selecting them for a run
----------------------------------------------------

You can "mark" a test function with custom metadata like this:

.. code-block:: python

    # content of test_server.py

    import pytest


    @pytest.mark.webtest
    def test_send_http():
        pass  # perform some webtest test for your app


    @pytest.mark.device(serial="123")
    def test_something_quick():
        pass


    @pytest.mark.device(serial="abc")
    def test_another():
        pass


    class TestClass:
        def test_method(self):
            pass



You can then restrict a test run to only run tests marked with ``webtest``:

.. code-block:: pytest

    $ pytest -v -m webtest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 4 items / 3 deselected / 1 selected

    test_server.py::test_send_http PASSED                                [100%]

    ===================== 1 passed, 3 deselected in 0.12s ======================

Or the inverse, running all tests except the webtest ones:

.. code-block:: pytest

    $ pytest -v -m "not webtest"
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 4 items / 1 deselected / 3 selected

    test_server.py::test_something_quick PASSED                          [ 33%]
    test_server.py::test_another PASSED                                  [ 66%]
    test_server.py::TestClass::test_method PASSED                        [100%]

    ===================== 3 passed, 1 deselected in 0.12s ======================

.. _`marker_keyword_expression_example`:

Additionally, you can restrict a test run to only run tests matching one or multiple marker
keyword arguments, e.g. to run only tests marked with ``device`` and the specific ``serial="123"``:

.. code-block:: pytest

    $ pytest -v -m "device(serial='123')"
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 4 items / 3 deselected / 1 selected

    test_server.py::test_something_quick PASSED                          [100%]

    ===================== 1 passed, 3 deselected in 0.12s ======================

.. note:: Only keyword argument matching is supported in marker expressions.

.. note:: Only :class:`int`, (unescaped) :class:`str`, :class:`bool` & :data:`None` values are supported in marker expressions.

Selecting tests based on their node ID
--------------------------------------

You can provide one or more :ref:`node IDs <node-id>` as positional
arguments to select only specified tests. This makes it easy to select
tests based on their module, class, method, or function name:

.. code-block:: pytest

    $ pytest -v test_server.py::TestClass::test_method
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 1 item

    test_server.py::TestClass::test_method PASSED                        [100%]

    ============================ 1 passed in 0.12s =============================

You can also select on the class:

.. code-block:: pytest

    $ pytest -v test_server.py::TestClass
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 1 item

    test_server.py::TestClass::test_method PASSED                        [100%]

    ============================ 1 passed in 0.12s =============================

Or select multiple nodes:

.. code-block:: pytest

    $ pytest -v test_server.py::TestClass test_server.py::test_send_http
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 2 items

    test_server.py::TestClass::test_method PASSED                        [ 50%]
    test_server.py::test_send_http PASSED                                [100%]

    ============================ 2 passed in 0.12s =============================

.. _node-id:

.. note::

    Node IDs are of the form ``module.py::class::method`` or
    ``module.py::function``.  Node IDs control which tests are
    collected, so ``module.py::class`` will select all test methods
    on the class.  Nodes are also created for each parameter of a
    parametrized fixture or test, so selecting a parametrized test
    must include the parameter value, e.g.
    ``module.py::function[param]``.

    Node IDs for failing tests are displayed in the test summary info
    when running pytest with the ``-rf`` option.  You can also
    construct Node IDs from the output of ``pytest --collect-only``.

Using ``-k expr`` to select tests based on their name
-------------------------------------------------------

.. versionadded:: 2.0/2.3.4

You can use the :option:`-k` command line option to specify an expression
which implements a substring match on the test names instead of the
exact match on markers that :option:`-m` provides.  This makes it easy to
select tests based on their names:

.. versionchanged:: 5.4

The expression matching is now case-insensitive.

.. code-block:: pytest

    $ pytest -v -k http  # running with the above defined example module
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 4 items / 3 deselected / 1 selected

    test_server.py::test_send_http PASSED                                [100%]

    ===================== 1 passed, 3 deselected in 0.12s ======================

And you can also run all tests except the ones that match the keyword:

.. code-block:: pytest

    $ pytest -k "not send_http" -v
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 4 items / 1 deselected / 3 selected

    test_server.py::test_something_quick PASSED                          [ 33%]
    test_server.py::test_another PASSED                                  [ 66%]
    test_server.py::TestClass::test_method PASSED                        [100%]

    ===================== 3 passed, 1 deselected in 0.12s ======================

Or to select "http" and "quick" tests:

.. code-block:: pytest

    $ pytest -k "http or quick" -v
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project
    collecting ... collected 4 items / 2 deselected / 2 selected

    test_server.py::test_send_http PASSED                                [ 50%]
    test_server.py::test_something_quick PASSED                          [100%]

    ===================== 2 passed, 2 deselected in 0.12s ======================

You can use ``and``, ``or``, ``not`` and parentheses.


In addition to the test's name, :option:`-k` also matches the names of the test's parents (usually, the name of the file and class it's in),
attributes set on the test function, markers applied to it or its parents and any :attr:`extra keywords <_pytest.nodes.Node.extra_keyword_matches>`
explicitly added to it or its parents.


Registering markers
-------------------------------------



.. ini-syntax for custom markers:

Registering markers for your test suite is simple:

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    markers = ["webtest: mark a test as a webtest.", "slow: mark test as slow."]

Multiple custom markers can be registered, by defining each one in its own line, as shown in above example.

You can ask which markers exist for your test suite - the list includes our just defined ``webtest`` and ``slow`` markers:

.. code-block:: pytest

    $ pytest --markers
    @pytest.mark.webtest: mark a test as a webtest.

    @pytest.mark.slow: mark test as slow.

    @pytest.mark.filterwarnings(warning): add a warning filter to the given test. see https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings

    @pytest.mark.skip(reason=None): skip the given test function with an optional reason. Example: skip(reason="no way of currently testing this") skips the test.

    @pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32') skips the test if we are on the win32 platform. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif

    @pytest.mark.xfail(condition, ..., *, reason=..., run=True, raises=None, strict=strict_xfail): mark the test function as an expected failure if any of the conditions evaluate to True. Optionally specify a reason for better reporting and run=False if you don't even want to execute the test function. If only specific exception(s) are expected, you can list them in raises, and if the test fails in other ways, it will be reported as a true failure. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-xfail

    @pytest.mark.parametrize(argnames, argvalues): call a test function multiple times passing in different arguments in turn. argvalues generally needs to be a list of values if argnames specifies only one name or a list of tuples of values if argnames specifies multiple names. Example: @parametrize('arg1', [1,2]) would lead to two calls of the decorated test function, one with arg1=1 and another with arg1=2.see https://docs.pytest.org/en/stable/how-to/parametrize.html for more info and examples.

    @pytest.mark.usefixtures(fixturename1, fixturename2, ...): mark tests as needing all of the specified fixtures. see https://docs.pytest.org/en/stable/explanation/fixtures.html#usefixtures

    @pytest.mark.tryfirst: mark a hook implementation function such that the plugin machinery will try to call it first/as early as possible. DEPRECATED, use @pytest.hookimpl(tryfirst=True) instead.

    @pytest.mark.trylast: mark a hook implementation function such that the plugin machinery will try to call it last/as late as possible. DEPRECATED, use @pytest.hookimpl(trylast=True) instead.


For an example on how to add and work with markers from a plugin, see
:ref:`adding a custom marker from a plugin`.

.. note::

    It is recommended to explicitly register markers so that:

    * There is one place in your test suite defining your markers

    * Asking for existing markers via ``pytest --markers`` gives good output

    * Typos in function markers are treated as an error if you use the :confval:`strict_markers` configuration option.

.. _`scoped-marking`:

Marking whole classes or modules
----------------------------------------------------

You may use ``pytest.mark`` decorators with classes to apply markers to all of
its test methods:

.. code-block:: python

    # content of test_mark_classlevel.py
    import pytest


    @pytest.mark.webtest
    class TestClass:
        def test_startup(self):
            pass

        def test_startup_and_more(self):
            pass

This is equivalent to directly applying the decorator to the
two test functions.

To apply marks at the module level, use the :globalvar:`pytestmark` global variable::

    import pytest
    pytestmark = pytest.mark.webtest

or multiple markers::

    pytestmark = [pytest.mark.webtest, pytest.mark.slowtest]


Due to legacy reasons, before class decorators were introduced, it is possible to set the
:globalvar:`pytestmark` attribute on a test class like this:

.. code-block:: python

    import pytest


    class TestClass:
        pytestmark = pytest.mark.webtest

.. _`marking individual tests when using parametrize`:

Marking individual tests when using parametrize
-----------------------------------------------

When using parametrize, applying a mark will make it apply
to each individual test. However it is also possible to
apply a marker to an individual test instance:

.. code-block:: python

    import pytest


    @pytest.mark.foo
    @pytest.mark.parametrize(
        ("n", "expected"), [(1, 2), pytest.param(1, 3, marks=pytest.mark.bar), (2, 3)]
    )
    def test_increment(n, expected):
        assert n + 1 == expected

In this example the mark "foo" will apply to each of the three
tests, whereas the "bar" mark is only applied to the second test.
Skip and xfail marks can also be applied in this way, see :ref:`skip/xfail with parametrize`.

.. _`adding a custom marker from a plugin`:

Custom marker and command line option to control test runs
----------------------------------------------------------

.. regendoc:wipe

Plugins can provide custom markers and implement specific behaviour
based on it. This is a self-contained example which adds a command
line option and a parametrized test function marker to run tests
specified via named environments:

.. code-block:: python

    # content of conftest.py

    import pytest


    def pytest_addoption(parser):
        parser.addoption(
            "-E",
            action="store",
            metavar="NAME",
            help="only run tests matching the environment NAME.",
        )


    def pytest_configure(config):
        # register an additional marker
        config.addinivalue_line(
            "markers", "env(name): mark test to run only on named environment"
        )


    def pytest_runtest_setup(item):
        envnames = [mark.args[0] for mark in item.iter_markers(name="env")]
        if envnames:
            if item.config.getoption("-E") not in envnames:
                pytest.skip(f"test requires env in {envnames!r}")

A test file using this local plugin:

.. code-block:: python

    # content of test_someenv.py

    import pytest


    @pytest.mark.env("stage1")
    def test_basic_db_operation():
        pass

and an example invocation specifying a different environment than what
the test needs:

.. code-block:: pytest

    $ pytest -E stage2
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_someenv.py s                                                    [100%]

    ============================ 1 skipped in 0.12s ============================

and here is one that specifies exactly the environment needed:

.. code-block:: pytest

    $ pytest -E stage1
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 1 item

    test_someenv.py .                                                    [100%]

    ============================ 1 passed in 0.12s =============================

The :option:`--markers` option always gives you a list of available markers:

.. code-block:: pytest

    $ pytest --markers
    @pytest.mark.env(name): mark test to run only on named environment

    @pytest.mark.filterwarnings(warning): add a warning filter to the given test. see https://docs.pytest.org/en/stable/how-to/capture-warnings.html#pytest-mark-filterwarnings

    @pytest.mark.skip(reason=None): skip the given test function with an optional reason. Example: skip(reason="no way of currently testing this") skips the test.

    @pytest.mark.skipif(condition, ..., *, reason=...): skip the given test function if any of the conditions evaluate to True. Example: skipif(sys.platform == 'win32') skips the test if we are on the win32 platform. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-skipif

    @pytest.mark.xfail(condition, ..., *, reason=..., run=True, raises=None, strict=strict_xfail): mark the test function as an expected failure if any of the conditions evaluate to True. Optionally specify a reason for better reporting and run=False if you don't even want to execute the test function. If only specific exception(s) are expected, you can list them in raises, and if the test fails in other ways, it will be reported as a true failure. See https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-xfail

    @pytest.mark.parametrize(argnames, argvalues): call a test function multiple times passing in different arguments in turn. argvalues generally needs to be a list of values if argnames specifies only one name or a list of tuples of values if argnames specifies multiple names. Example: @parametrize('arg1', [1,2]) would lead to two calls of the decorated test function, one with arg1=1 and another with arg1=2.see https://docs.pytest.org/en/stable/how-to/parametrize.html for more info and examples.

    @pytest.mark.usefixtures(fixturename1, fixturename2, ...): mark tests as needing all of the specified fixtures. see https://docs.pytest.org/en/stable/explanation/fixtures.html#usefixtures

    @pytest.mark.tryfirst: mark a hook implementation function such that the plugin machinery will try to call it first/as early as possible. DEPRECATED, use @pytest.hookimpl(tryfirst=True) instead.

    @pytest.mark.trylast: mark a hook implementation function such that the plugin machinery will try to call it last/as late as possible. DEPRECATED, use @pytest.hookimpl(trylast=True) instead.


.. _`passing callables to custom markers`:

Passing a callable to custom markers
--------------------------------------------

.. regendoc:wipe

Below is the config file that will be used in the next examples:

.. code-block:: python

    # content of conftest.py
    import sys


    def pytest_runtest_setup(item):
        for marker in item.iter_markers(name="my_marker"):
            print(marker)
            sys.stdout.flush()

A custom marker can have its argument set, i.e. ``args`` and ``kwargs`` properties, defined by either invoking it as a callable or using ``pytest.mark.MARKER_NAME.with_args``. These two methods achieve the same effect most of the time.

However, if there is a callable as the single positional argument with no keyword arguments, using the ``pytest.mark.MARKER_NAME(c)`` will not pass ``c`` as a positional argument but decorate ``c`` with the custom marker (see :ref:`MarkDecorator <mark>`). Fortunately, ``pytest.mark.MARKER_NAME.with_args`` comes to the rescue:

.. code-block:: python

    # content of test_custom_marker.py
    import pytest


    def hello_world(*args, **kwargs):
        return "Hello World"


    @pytest.mark.my_marker.with_args(hello_world)
    def test_with_args():
        pass

The output is as follows:

.. code-block:: pytest

    $ pytest -q -s
    Mark(name='my_marker', args=(<function hello_world at 0xdeadbeef0001>,), kwargs={})
    .
    1 passed in 0.12s

We can see that the custom marker has its argument set extended with the function ``hello_world``. This is the key difference between creating a custom marker as a callable, which invokes ``__call__`` behind the scenes, and using ``with_args``.


Reading markers which were set from multiple places
----------------------------------------------------

.. versionadded: 2.2.2

.. regendoc:wipe

If you are heavily using markers in your test suite you may encounter the case where a marker is applied several times to a test function.  From plugin
code you can read over all such settings.  Example:

.. code-block:: python

    # content of test_mark_three_times.py
    import pytest

    pytestmark = pytest.mark.glob("module", x=1)


    @pytest.mark.glob("class", x=2)
    class TestClass:
        @pytest.mark.glob("function", x=3)
        def test_something(self):
            pass

Here we have the marker "glob" applied three times to the same
test function.  From a conftest file we can read it like this:

.. code-block:: python

    # content of conftest.py
    import sys


    def pytest_runtest_setup(item):
        for mark in item.iter_markers(name="glob"):
            print(f"glob args={mark.args} kwargs={mark.kwargs}")
            sys.stdout.flush()

Let's run this without capturing output and see what we get:

.. code-block:: pytest

    $ pytest -q -s
    glob args=('function',) kwargs={'x': 3}
    glob args=('class',) kwargs={'x': 2}
    glob args=('module',) kwargs={'x': 1}
    .
    1 passed in 0.12s

Marking platform specific tests with pytest
--------------------------------------------------------------

.. regendoc:wipe

Consider you have a test suite which marks tests for particular platforms,
namely ``pytest.mark.darwin``, ``pytest.mark.win32`` etc. and you
also have tests that run on all platforms and have no specific
marker.  If you now want to have a way to only run the tests
for your particular platform, you could use the following plugin:

.. code-block:: python

    # content of conftest.py
    #
    import sys

    import pytest

    ALL = set("darwin linux win32".split())


    def pytest_runtest_setup(item):
        supported_platforms = ALL.intersection(mark.name for mark in item.iter_markers())
        plat = sys.platform
        if supported_platforms and plat not in supported_platforms:
            pytest.skip(f"cannot run on platform {plat}")

then tests will be skipped if they were specified for a different platform.
Let's do a little test file to show how this looks like:

.. code-block:: python

    # content of test_plat.py

    import pytest


    @pytest.mark.darwin
    def test_if_apple_is_evil():
        pass


    @pytest.mark.linux
    def test_if_linux_works():
        pass


    @pytest.mark.win32
    def test_if_win32_crashes():
        pass


    def test_runs_everywhere():
        pass

then you will see two tests skipped and two executed tests as expected:

.. code-block:: pytest

    $ pytest -rs # this option reports skip reasons
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 4 items

    test_plat.py s.s.                                                    [100%]

    ========================= short test summary info ==========================
    SKIPPED [2] conftest.py:13: cannot run on platform linux
    ======================= 2 passed, 2 skipped in 0.12s =======================

Note that if you specify a platform via the marker-command line option like this:

.. code-block:: pytest

    $ pytest -m linux
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 4 items / 3 deselected / 1 selected

    test_plat.py .                                                       [100%]

    ===================== 1 passed, 3 deselected in 0.12s ======================

then the unmarked-tests will not be run.  It is thus a way to restrict the run to the specific tests.

Automatically adding markers based on test names
--------------------------------------------------------

.. regendoc:wipe

If you have a test suite where test function names indicate a certain
type of test, you can implement a hook that automatically defines
markers so that you can use the :option:`-m` option with it. Let's look
at this test module:

.. code-block:: python

    # content of test_module.py


    def test_interface_simple():
        assert 0


    def test_interface_complex():
        assert 0


    def test_event_simple():
        assert 0


    def test_something_else():
        assert 0

We want to dynamically define two markers and can do it in a
``conftest.py`` plugin:

.. code-block:: python

    # content of conftest.py

    import pytest


    def pytest_collection_modifyitems(items):
        for item in items:
            if "interface" in item.nodeid:
                item.add_marker(pytest.mark.interface)
            elif "event" in item.nodeid:
                item.add_marker(pytest.mark.event)

We can now use the ``-m option`` to select one set:

.. code-block:: pytest

    $ pytest -m interface --tb=short
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 4 items / 2 deselected / 2 selected

    test_module.py FF                                                    [100%]

    ================================= FAILURES =================================
    __________________________ test_interface_simple ___________________________
    test_module.py:4: in test_interface_simple
        assert 0
    E   assert 0
    __________________________ test_interface_complex __________________________
    test_module.py:8: in test_interface_complex
        assert 0
    E   assert 0
    ========================= short test summary info ==========================
    FAILED test_module.py::test_interface_simple - assert 0
    FAILED test_module.py::test_interface_complex - assert 0
    ===================== 2 failed, 2 deselected in 0.12s ======================

or to select both "event" and "interface" tests:

.. code-block:: pytest

    $ pytest -m "interface or event" --tb=short
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    collected 4 items / 1 deselected / 3 selected

    test_module.py FFF                                                   [100%]

    ================================= FAILURES =================================
    __________________________ test_interface_simple ___________________________
    test_module.py:4: in test_interface_simple
        assert 0
    E   assert 0
    __________________________ test_interface_complex __________________________
    test_module.py:8: in test_interface_complex
        assert 0
    E   assert 0
    ____________________________ test_event_simple _____________________________
    test_module.py:12: in test_event_simple
        assert 0
    E   assert 0
    ========================= short test summary info ==========================
    FAILED test_module.py::test_interface_simple - assert 0
    FAILED test_module.py::test_interface_complex - assert 0
    FAILED test_module.py::test_event_simple - assert 0
    ===================== 3 failed, 1 deselected in 0.12s ======================

# A session-fixture which can look at all collected tests
Source: https://docs.pytest.org/en/stable/example/special.html

A session-fixture which can look at all collected tests
----------------------------------------------------------------

A session-scoped fixture effectively has access to all
collected test items.  Here is an example of a fixture
function which walks all collected tests and looks
if their test class defines a ``callme`` method and
calls it:

.. code-block:: python

    # content of conftest.py

    import pytest


    @pytest.fixture(scope="session", autouse=True)
    def callattr_ahead_of_alltests(request):
        print("callattr_ahead_of_alltests called")
        seen = {None}
        session = request.node
        for item in session.items:
            cls = item.getparent(pytest.Class)
            if cls not in seen:
                if hasattr(cls.obj, "callme"):
                    cls.obj.callme()
                seen.add(cls)

test classes may now define a ``callme`` method which
will be called ahead of running any tests:

.. code-block:: python

    # content of test_module.py


    class TestHello:
        @classmethod
        def callme(cls):
            print("callme called!")

        def test_method1(self):
            print("test_method1 called")

        def test_method2(self):
            print("test_method2 called")


    class TestOther:
        @classmethod
        def callme(cls):
            print("callme other called")

        def test_other(self):
            print("test other")


    # works with unittest as well ...
    import unittest


    class SomeTest(unittest.TestCase):
        @classmethod
        def callme(self):
            print("SomeTest callme called")

        def test_unit1(self):
            print("test_unit1 method called")

If you run this without output capturing:

.. code-block:: pytest

    $ pytest -q -s test_module.py
    callattr_ahead_of_alltests called
    callme called!
    callme other called
    SomeTest callme called
    test_method1 called
    .test_method2 called
    .test other
    .test_unit1 method called
    .
    4 passed in 0.12s

# Changing standard (Python) test discovery
Source: https://docs.pytest.org/en/stable/example/pythoncollection.html

Changing standard (Python) test discovery
===============================================

Ignore paths during test collection
-----------------------------------

You can easily ignore certain test directories and modules during collection
by passing the :option:`--ignore=path` option on the cli. ``pytest`` allows multiple
``--ignore`` options. Example:

.. code-block:: text

    tests/
    |-- example
    |   |-- test_example_01.py
    |   |-- test_example_02.py
    |   '-- test_example_03.py
    |-- foobar
    |   |-- test_foobar_01.py
    |   |-- test_foobar_02.py
    |   '-- test_foobar_03.py
    '-- hello
        '-- world
            |-- test_world_01.py
            |-- test_world_02.py
            '-- test_world_03.py

Now if you invoke ``pytest`` with ``--ignore=tests/foobar/test_foobar_03.py --ignore=tests/hello/``,
you will see that ``pytest`` only collects test-modules, which do not match the patterns specified:

.. code-block:: pytest

    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-5.x.y, py-1.x.y, pluggy-0.x.y
    rootdir: $REGENDOC_TMPDIR, inifile:
    collected 5 items

    tests/example/test_example_01.py .                                   [ 20%]
    tests/example/test_example_02.py .                                   [ 40%]
    tests/example/test_example_03.py .                                   [ 60%]
    tests/foobar/test_foobar_01.py .                                     [ 80%]
    tests/foobar/test_foobar_02.py .                                     [100%]

    ========================= 5 passed in 0.02 seconds =========================

The :option:`--ignore-glob` option allows to ignore test file paths based on Unix shell-style wildcards.
If you want to exclude test-modules that end with ``_01.py``, execute ``pytest`` with :option:`--ignore-glob='*_01.py'`.

Deselect tests during test collection
-------------------------------------

Tests can individually be deselected during collection by passing the :option:`--deselect=item` option.
For example, say ``tests/foobar/test_foobar_01.py`` contains ``test_a`` and ``test_b``.
You can run all of the tests within ``tests/`` *except* for ``tests/foobar/test_foobar_01.py::test_a``
by invoking ``pytest`` with ``--deselect=tests/foobar/test_foobar_01.py::test_a``.
``pytest`` allows multiple ``--deselect`` options.

.. _duplicate-paths:

Keeping duplicate paths specified from command line
----------------------------------------------------

Default behavior of ``pytest`` is to ignore duplicate paths specified from the command line.
Example:

.. code-block:: pytest

    pytest path_a path_a

    ...
    collected 1 item
    ...

Just collect tests once.

To collect duplicate tests, use the :option:`--keep-duplicates` option on the cli.
Example:

.. code-block:: pytest

    pytest --keep-duplicates path_a path_a

    ...
    collected 2 items
    ...


Changing directory recursion
-----------------------------------------------------

You can set the :confval:`norecursedirs` option in a configuration file:

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    norecursedirs = [".svn", "_build", "tmp*"]

This would tell ``pytest`` to not recurse into typical subversion or sphinx-build directories or into any ``tmp`` prefixed directory.

.. _`change naming conventions`:

Changing naming conventions
-----------------------------------------------------

You can configure different naming conventions by setting
the :confval:`python_files`, :confval:`python_classes` and
:confval:`python_functions` in your :ref:`configuration file <config file formats>`.
Here is an example:

.. code-block:: toml

    # content of pytest.toml
    # Example 1: have pytest look for "check" instead of "test"
    [pytest]
    python_files = ["check_*.py"]
    python_classes = ["Check"]
    python_functions = ["*_check"]

This would make ``pytest`` look for tests in files that match the ``check_*
.py`` glob-pattern, ``Check`` prefixes in classes, and functions and methods
that match ``*_check``. For example, if we have:

.. code-block:: python

    # content of check_myapp.py
    class CheckMyApp:
        def simple_check(self):
            pass

        def complex_check(self):
            pass

The test collection would look like this:

.. code-block:: pytest

    $ pytest --collect-only
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    configfile: pytest.toml
    collected 2 items

    <Dir pythoncollection.rst-216>
      <Module check_myapp.py>
        <Class CheckMyApp>
          <Function simple_check>
          <Function complex_check>

    ======================== 2 tests collected in 0.12s ========================

You can check for multiple glob patterns by adding a space between the patterns:

.. code-block:: toml

    # content of pytest.toml
    # Example 2: have pytest look for files with "test" and "example"
    [pytest]
    python_files = ["test_*.py", "example_*.py"]

.. note::

   the ``python_functions`` and ``python_classes`` options have no effect
   for ``unittest.TestCase`` test discovery because pytest delegates
   discovery of test case methods to unittest code.

Interpreting cmdline arguments as Python packages
-----------------------------------------------------

You can use the :option:`--pyargs` option to make ``pytest`` try
interpreting arguments as python package names, deriving
their file system path and then running the test. For
example if you have unittest2 installed you can type:

.. code-block:: bash

    pytest --pyargs unittest2.test.test_skipping -q

which would run the respective test module.  Like with
other options, through a configuration file and the :confval:`addopts` option you
can make this change more permanently:

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    addopts = ["--pyargs"]

Now a simple invocation of ``pytest NAME`` will check
if NAME exists as an importable package/module and otherwise
treat it as a filesystem path.

Finding out what is collected
-----------------------------------------------

You can always peek at the collection tree without running tests like this:

.. code-block:: pytest

    . $ pytest --collect-only pythoncollection.py
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    configfile: pytest.toml
    collected 3 items

    <Dir pythoncollection.rst-216>
      <Dir CWD>
        <Module pythoncollection.py>
          <Function test_function>
          <Class TestClass>
            <Function test_method>
            <Function test_anothermethod>

    ======================== 3 tests collected in 0.12s ========================

.. _customizing-test-collection:

Customizing test collection
---------------------------

.. regendoc:wipe

You can easily instruct ``pytest`` to discover tests from every Python file:

.. code-block:: toml

    # content of pytest.toml
    [pytest]
    python_files = ["*.py"]

However, many projects will have a ``setup.py`` which they don't want to be
imported. Moreover, there may be files only importable by a specific python
version. For such cases you can dynamically define files to be ignored by
listing them in a ``conftest.py`` file:

.. code-block:: python

    # content of conftest.py
    import sys

    collect_ignore = ["setup.py"]
    if sys.version_info[0] > 2:
        collect_ignore.append("pkg/module_py2.py")

and then if you have a module file like this:

.. code-block:: python

    # content of pkg/module_py2.py
    def test_only_on_python2():
        try:
            assert 0
        except Exception, e:
            pass

and a ``setup.py`` dummy file like this:

.. code-block:: python

    # content of setup.py
    0 / 0  # will raise exception if imported

If you run with a Python 2 interpreter then you will find the one test and will
leave out the ``setup.py`` file:

.. code-block:: pytest

    #$ pytest --collect-only
    ====== test session starts ======
    platform linux2 -- Python 2.7.10, pytest-2.9.1, py-1.4.31, pluggy-0.3.1
    rootdir: $REGENDOC_TMPDIR, inifile: pytest.ini
    collected 1 items
    <Module 'pkg/module_py2.py'>
      <Function 'test_only_on_python2'>

    ====== 1 tests found in 0.04 seconds ======

If you run with a Python 3 interpreter both the one test and the ``setup.py``
file will be left out:

.. code-block:: pytest

    $ pytest --collect-only
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project
    configfile: pytest.toml
    collected 0 items

    ======================= no tests collected in 0.12s ========================

It's also possible to ignore files based on Unix shell-style wildcards by adding
patterns to :globalvar:`collect_ignore_glob`.

The following example ``conftest.py`` ignores the file ``setup.py`` and in
addition all files that end with ``*_py2.py`` when executed with a Python 3
interpreter:

.. code-block:: python

    # content of conftest.py
    import sys

    collect_ignore = ["setup.py"]
    if sys.version_info[0] > 2:
        collect_ignore_glob = ["*_py2.py"]

Since Pytest 2.6, users can prevent pytest from discovering classes that start
with ``Test`` by setting a boolean ``__test__`` attribute to ``False``.

.. code-block:: python

    # Will not be discovered as a test
    class TestClass:
        __test__ = False

.. note::

   If you are working with abstract test classes and want to avoid manually setting
   the ``__test__`` attribute for subclasses, you can use a mixin class to handle
   this automatically. For example:

   .. code-block:: python

       # Mixin to handle abstract test classes
       class NotATest:
           def __init_subclass__(cls):
               cls.__test__ = NotATest not in cls.__bases__


       # Abstract test class
       class AbstractTest(NotATest):
           pass


       # Subclass that will be collected as a test
       class RealTest(AbstractTest):
           def test_example(self):
               assert 1 + 1 == 2

   This approach ensures that subclasses of abstract test classes are automatically
   collected without needing to explicitly set the ``__test__`` attribute.

# Working with non-python tests
Source: https://docs.pytest.org/en/stable/example/nonpython.html

.. _`non-python tests`:

Working with non-python tests
====================================================

.. _`yaml plugin`:

A basic example for specifying tests in Yaml files
--------------------------------------------------------------

.. _`pytest-yamlwsgi`: https://pypi.org/project/pytest-yamlwsgi/

Here is an example ``conftest.py`` (extracted from Ali Afshar's special purpose `pytest-yamlwsgi`_ plugin).   This ``conftest.py`` will  collect ``test*.yaml`` files and will execute the yaml-formatted content as custom tests:

.. include:: nonpython/conftest.py
    :literal:

You can create a simple example file:

.. include:: nonpython/test_simple.yaml
    :literal:

and if you installed :pypi:`PyYAML` or a compatible YAML-parser you can
now execute the test specification:

.. code-block:: pytest

    nonpython $ pytest test_simple.yaml
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project/nonpython
    collected 2 items

    test_simple.yaml F.                                                  [100%]

    ================================= FAILURES =================================
    ______________________________ usecase: hello ______________________________
    usecase execution failed
       spec failed: 'some': 'other'
       no further details known at this point.
    ========================= short test summary info ==========================
    FAILED test_simple.yaml::hello - usecase execution failed
    ======================= 1 failed, 1 passed in 0.12s ========================

.. regendoc:wipe

You get one dot for the passing ``sub1: sub1`` check and one failure.
Obviously in the above ``conftest.py`` you'll want to implement a more
interesting interpretation of the yaml-values.  You can easily write
your own domain-specific testing language this way.

.. note::

    ``repr_failure(excinfo)`` is called for representing test failures.
    If you create custom collection nodes you can return an error
    representation string of your choice.  It
    will be reported as a (red) string.

``reportinfo()`` is used for representing the test location and is also
consulted when reporting in ``verbose`` mode. It should return a tuple
``(path, lineno, description)``, where:

* ``path`` is the path shown in reports (usually ``self.path`` or ``self.fspath``).
* ``lineno`` is a zero-based line number, or ``0`` when no specific line applies.
* ``description`` is a short label shown for the collected item:

.. code-block:: pytest

    nonpython $ pytest -v
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y -- $PYTHON_PREFIX/bin/python
    cachedir: .pytest_cache
    rootdir: /home/sweet/project/nonpython
    collecting ... collected 2 items

    test_simple.yaml::hello FAILED                                       [ 50%]
    test_simple.yaml::ok PASSED                                          [100%]

    ================================= FAILURES =================================
    ______________________________ usecase: hello ______________________________
    usecase execution failed
       spec failed: 'some': 'other'
       no further details known at this point.
    ========================= short test summary info ==========================
    FAILED test_simple.yaml::hello - usecase execution failed
    ======================= 1 failed, 1 passed in 0.12s ========================

.. regendoc:wipe

While developing your custom test collection and execution it's also
interesting to look at the collection tree:

.. code-block:: pytest

    nonpython $ pytest --collect-only
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project/nonpython
    collected 2 items

    <Package nonpython>
      <YamlFile test_simple.yaml>
        <YamlItem hello>
        <YamlItem ok>

    ======================== 2 tests collected in 0.12s ========================

# Using a custom directory collector
Source: https://docs.pytest.org/en/stable/example/customdirectory.html

.. _`custom directory collectors`:

Using a custom directory collector
====================================================

By default, pytest collects directories using :class:`pytest.Package`, for directories with ``__init__.py`` files,
and :class:`pytest.Dir` for other directories.
If you want to customize how a directory is collected, you can write your own :class:`pytest.Directory` collector,
and use :hook:`pytest_collect_directory` to hook it up.

.. _`directory manifest plugin`:

A basic example for a directory manifest file
--------------------------------------------------------------

Suppose you want to customize how collection is done on a per-directory basis.
Here is an example ``conftest.py`` plugin that allows directories to contain a ``manifest.json`` file,
which defines how the collection should be done for the directory.
In this example, only a simple list of files is supported,
however you can imagine adding other keys, such as exclusions and globs.

.. include:: customdirectory/conftest.py
    :literal:

You can create a ``manifest.json`` file and some test files:

.. include:: customdirectory/tests/manifest.json
    :literal:

.. include:: customdirectory/tests/test_first.py
    :literal:

.. include:: customdirectory/tests/test_second.py
    :literal:

.. include:: customdirectory/tests/test_third.py
    :literal:

And you can now execute the test specification:

.. code-block:: pytest

    customdirectory $ pytest
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project/customdirectory
    configfile: pytest.ini
    collected 2 items

    tests/test_first.py .                                                [ 50%]
    tests/test_second.py .                                               [100%]

    ============================ 2 passed in 0.12s =============================

.. regendoc:wipe

Notice how ``test_three.py`` was not executed, because it is not listed in the manifest.

You can verify that your custom collector appears in the collection tree:

.. code-block:: pytest

    customdirectory $ pytest --collect-only
    =========================== test session starts ============================
    platform linux -- Python 3.x.y, pytest-9.x.y, pluggy-1.x.y
    rootdir: /home/sweet/project/customdirectory
    configfile: pytest.ini
    collected 2 items

    <Dir customdirectory>
      <ManifestDirectory tests>
        <Module test_first.py>
          <Function test_1>
        <Module test_second.py>
          <Function test_2>

    ======================== 2 tests collected in 0.12s ========================
