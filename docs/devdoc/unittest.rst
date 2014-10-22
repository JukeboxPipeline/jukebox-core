.. _unittests:

=========
Unittests
=========

Unittesting is a way to automatically test the functionality of your code.
There are numerous ways for unittesting. This is a description of the current test setup

  "Something that is always appropriate, regardless of general style, is when you get a bug report. ALWAYS create a test case first & run your tests. Make sure it demonstrates the failure, THEN go fix the bug. If your fix is correct, that new test should pass! It's an excellent way to sanity check yourself & is a great way to get started with testing to boot."

  -- Daniel Lindsley on his ToastDriven blog.

Organisation
------------

We use `tox <https://pypi.python.org/pypi/tox>`_ for running a whole array of unittests.
Tox as is a generic virtualenv management and test command line tool you can use for:

    - checking your package installs correctly with different Python versions and interpreters
    - running your tests in each of the environments, configuring your test tool of choice
    - acting as a frontend to Continuous Integration servers, greatly reducing boilerplate and merging CI and shell-based testing.

Because all jukebox products are packages it is important to test them in their installed configuration and not in your development environment.
Tox lets you configure multiple environments with different dependencies and executes the tests in these environments. So you could test your code
with python 2.7, 3.3, 3.4, pypy etc. There are numerous environments already configured. Some have special usecases, e.g. they test building the documentation.

Tox itselfs basically invokes any command you tell it to. So for the unittesting itself we use `pytest <http://pytest.org/latest/>`_.
Pytest is a tool for testing in python. It helps you with writing your tests, collects them, executes them and reports the results.
So for testing our package, tox invokes the pytest command.
If you are familiar with other test frameworks like nose or unittest, pytest is really easy. Pytest even understands a good amount of nose,
and unittest. So some tests are already portable.

All tests for the jukebox-core package are inside the ``test`` directory. So in most cases it might be enough to just throw your tests in there and
execute the tox command. The next sections will teach you more in depth about the purpose of every file involved in the testsetup, how to
setup environments, how to have a special local test system and some tips when using tox.


--------
Overview
--------

This is a little overview for every file and directory involved in the testing process:
