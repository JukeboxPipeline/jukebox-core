.. _unittests:

=========
Unittests
=========

We use nose for unittesting. There is a executable ``runtest.py`` file inside the source root. Just execute it and the test will run.
Please write unittests whenever possible. It makes the code much easier to maintain.

  "Something that is always appropriate, regardless of general style, is when you get a bug report. ALWAYS create a test case first & run your tests. Make sure it demonstrates the failure, THEN go fix the bug. If your fix is correct, that new test should pass! It's an excellent way to sanity check yourself & is a great way to get started with testing to boot."

  -- Daniel Lindsley on his ToastDriven blog.

Organisation
------------

Here is a short description of what happens when you execute ``runtest.py``.

:mod:`jukebox.tests` has several lists of arguments. :data:`jukebox.tests.ALL_TEST_ARGS` gets loaded here. Then we call :func:`jukebox.core.main.init_test_env` to initialize some Environment Variables. This will set the environment variable ``TESTING`` to ``'True'``. This might have impact on some functions in the souce code. An example would be :class:`jukebox.maya3d.menu.Menu` that will not call the commands to create the gui, because while we are testing, maya does not support those commands. See :ref:`mayatests` for more information.
Now we can run ``nose``.
Nose will look for all tests inside the testdirectory and runs them. There are also tests for maya inside this directory, which leads to a problem. Mayatests depend on ``maya.cmds`` which is not available at the moment, except you execute the test in maya. But what happens if we add tests for Nuke etc.

.. _mayatests:

Mayatests
+++++++++

To work around that, the :data:`jukebox.tests.ALL_TEST_ARGS` exclude these directories. The tests will not run by this nose process.
Instead there is a test :mod:`jukebox.tests.test_mayatests`. This function will test maya in a seperate nose process. To test maya functions correctly we need to find the maya installation and execute nose via the special python intepreter of maya. This can be easily done by getting ``mayapy.exe`` via :meth:`jukebox.core.ostool.PlatformInterface.get_maya_python`. 

So again, we execute a file similar to ``runtest.py`` only this time via ``mayapy.exe`` and this time we initialize a maya standalone.
With this maya standalone we can execute almost every ``maya.cmds`` command except for the ones that handle the GUI. Thats the reason for why we need a ``TESTING`` env variable. Without that we could not test the MenuManager for example. So all ``maya.cmds`` commands regarding GUIs should be handled with care.

.. _djangotests:

Djangotests
+++++++++++

When a test requires access to a database, that means it requires django, then we use a test database. The :mod:`jukebox.tests.test_django` is responsible for these tests. Put Django tests inside here. The jukedj-django project is also tested that way.
The testdatabase is only temorary for the unittest. When chaning models it is required to call ``manage.py makemigrations <appname>`` so migrationfiles get generated. These are applied to the testdb. If you forget to do that, the testdb does not represent your current models.
