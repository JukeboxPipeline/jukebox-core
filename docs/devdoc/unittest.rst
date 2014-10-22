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

This is a little overview for every file and directory involved in the testing process.

.. _conf:

++++
conf
++++

The conf directory in root holds templates for the different configuration files.
Depending on your configuration in :ref:`setup.cfg <setupcfg>` these files are processed by a tempalte engine
and placed inside the root directory. See :ref:`bootstrap.py <bootstrap>` below for more information.

.. _setupcfg:

+++++++++
setup.cfg
+++++++++

This file has different sections for all kind of unittest related actions:

  :flake8: This section is used for the flake8 tool that checks if the python code is conform to the python conventions.
	   There is a special tox environment :ref:`check <check>` which will do that.
  :pytest: Here are some general settings for pytest, like what dirs to ignore or what arguments to use
           by default when executing ``pytest``.
  :matrix: This is a special section for :ref:`bootstrap.py <bootstrap>` and the config templates inside :ref:`conf <conf>`.
           You can define a test matrix so tox tests with multiple python versions or different dependency versions.


.. _bootstrap:

++++++++++++
bootstrap.py
++++++++++++

bootstrap.py parses the matrix section of :ref:`setup.cfg <setupcfg>` and uses the configuration for rendering all
templates inside :ref:`conf <conf>`. Execute the script and all the config files you had templates for should be updated.

+++++++
tox.ini
+++++++

This is where the magic happens. Here you can define all test environments, their dependencies and the commands to use for testing.
See this `documentation <https://testrun.org/tox/latest/config.html>`_ on how to write these config files.
This file has a template inside :ref:`conf <conf>`.
So rather than changing this file directly edit the template and use :ref:`bootstrap.py <bootstrap>`.
Here is a brief overview for the most common sections:

~~~
tox
~~~

The main section defines global settings. It might be worth noting that i changed the toxworkdir to a folder outside the actual package.
The reason for this was that the ``.tox`` dir that tox creates during testing got really heavy (over 40k files). This slowed down the building
process and therefore also the testing.
The envlist is a collection of environments that are used by default if no other environments are specified.

~~~~~~~
testenv
~~~~~~~

The most common options for all testenvironments gatherd. Other environments might override some of the settings again.
But basically they all share this one. Note that all other environments have the ``testenv:`` prefix.

~~~~~
spell
~~~~~

Spell checking for the documentation.

~~~~
docs
~~~~

This env tests building the documentation. It invokes sphinx-build two times. The first time it checks all links inside the documentation.
The second time it just tries to build the documentation and reports the result.

~~~~~~~~~
configure
~~~~~~~~~

The same as using :ref:`bootstrap.py <bootstrap>`.

.. _check:

~~~~~
check
~~~~~

Performs multiple checks, e.g. executes flake8 to check conformity of the python code.

~~~~~~~~~
coveralls
~~~~~~~~~

Collects the coverage reports of the tests and submits the result to `coveralls <https://coveralls.io/>`_.

~~~~~~
report
~~~~~~

Combines and reports all coverage reports. This is nice if you have multiple environments with different coverage results.

~~~~~
clean
~~~~~

Erases the old coverage reports by calling::

  $ coverage erase

~~~~~~~~~~~~~~~~~~~~~~~~
python test environments
~~~~~~~~~~~~~~~~~~~~~~~~

The rest of the environments are test the actual python code.
Usually you have two environments for every python version. One with coverage and one without.
Because certain race conditions cannot be tested with coverage as it introduces a slight overhead. 


++++++++++++
localtox.ini
++++++++++++

This is like a mirror of the regular ``tox.ini``. But for the install command it uses a special script called ``localtoxinstall.py``.
The reason why you might want to use this file is the following:

  Sometimes you want more control over your dependencies. Some might be really hard to install on windows or take a long time from source.
  You might also be developing a dependency in parallel or the dependency is not on any package index yet. In this case
  You can use this file as a tox config file. For installation of the dependencies it will execute a shell script ``localtoxinstall``.
  Put in all your special install commands for various dependencies like ``psycopg2``.
  Look at ``localtoxinstall_template`` for examples.

.. Note:: There is a template in the conf_ dir. So instead of editing this file directly edit the template.
          Do not put the ``localtoxinstall`` shell script under version control.


+++++++++++
.travis.yml
+++++++++++

Ignore this file. If somebody manages to make jukeboxcore work on `Travis-CI <https://travis-ci.org/>`_ this might be interesting.
