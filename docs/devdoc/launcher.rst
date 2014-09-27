.. _launcher:

========
Launcher
========

Whenever we want to start a script or an application that uses the pipeline we should use the :mod:`jukebox.launcher.baselauncher` script or a script derived from it. Look at its documentation for more information.
The launchers are independent from the rest of the source. Their job is to load environments, load the source and setup the pipeline. The launcher will load the source code from the ``SOURCE_PATH`` environment variable.


Environment Files
-----------------

Launcher load environmentfiles before they launch. First the global environment of the user is loaded. If the user did not specify any, the
default one is loaded afterwards. If environments are specified, these are loaded instead of the default one.
The global one is always loaded.

The standard location for these files is :data:`jukebox.launcher.baselauncher.USERENV_DIR`. All files should be ordinary python files.

As a dev it is adviced to create something like a dev_env.py::

  import os
  
  os.environ['SOURCE_PATH'] = 'path/to/your/sandbox/repository'

When launching the prelauncher you provide ``--env default_env.py`` as argument to load it.
The launcher will always try to load a global_env.py and if no env is specified, also a default_env.py.

Because you normally use your sandbox source as a dev, putting the code in the default_env and using special envs for live and beta might
be more convenient.
