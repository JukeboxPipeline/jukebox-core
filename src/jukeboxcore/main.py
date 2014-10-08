"""Bundles common core functions.

There are different init functions to initialize jukebox. Usually the launcher executes a script/software.
Then in your script/software you call one of these inits. Some softwares have special inits.
"""
import sys

from jukeboxcore.plugins import PluginManager


def init_environment():
    """Set environment variables that are important for the pipeline.

    :returns: None
    :rtype: None
    :raises: None
    """
    pass


def init():
    """Initialize the pipeline so everything works

    Include third party libs and load plugins
    """
    init_environment()
    # load plugins
    pmanager = PluginManager.get()
    pmanager.load_plugins()


def unload_modules():
    """ Unload all modules of the jukebox package and all plugin modules

    Python provides the ``reload`` command for reloading modules. The major drawback is, that if this module is loaded in any other module
    the source code will not be resourced!
    If you want to reload the code because you changed the source file, you have to get rid of it completely first.

    :returns: None
    :rtype: None
    :raises: None
    """
    mods = set([])
    for m in sys.modules:
        if m.startswith('jukebox'):
            mods.add(m)
    pm = PluginManager.get()
    for p in pm.get_all_plugins():
        mods.add(p.__module__)
    for m in mods:
        del(sys.modules[m])
