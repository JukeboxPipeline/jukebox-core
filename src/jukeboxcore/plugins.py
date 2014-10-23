"""A collection of classes, metaclasses and functions for Plugins

As a plugin developer: Subclass from one of the JB_Plugin classes and implement the abstract functions.
The plugin managers load and hold plugins.
"""
import abc
import inspect
import os
import sys
import traceback
from collections import OrderedDict

from jukeboxcore.log import get_logger
log = get_logger(__name__)
from jukeboxcore import errors
from jukeboxcore.constants import PLUGIN_CONFIG_DIR, CONFIG_EXT, BUILTIN_PLUGIN_PATH
from jukeboxcore.iniconf import load_config, get_core_config


class JB_Plugin(object):
    """Abstract Base Class for jukebox plugins.

    Subclass this to create your own types of plugins. The name of the subclass will be the name
    of the plugin itself, so be sure to pick a unique one.
    Else you will override an existing plugin (maybe that is your intend, then do it).
    If you write a plugin, always subclass from a subclass of JB_Plugin
    but not JB_Plugin directly!

    For subclassing: you have to implement **init** and **uninit**!

    Metadata:

      This class has a few public attributes. Override them to supply metadata for your plugin.

    User Config:

      Every Plugin can have its own userpreference file.
      The user preferences are ini-files that lie in the config folder
      inside the pipeline user directory.
      As a plugin developer, create a configspec file in the same folder as your plugin module.
      Do it only, if you need to use get_config().

    """

    __metaclass__ = abc.ABCMeta

    __UNLOADED = False
    __LOADED = True

    required = ()
    """The plugins required to run this one successfully.
    Set this to a list of strings with the required classnames."""
    author = None
    """The author of the plugin."""
    copyright = None
    """Copyright information."""
    license = None
    """ License information."""
    version = None
    """The version of the plugin."""
    description = None
    """A descriptive text for the plugin."""

    def __init__(self):
        """Constructs a new Plugin

        :returns: None
        :rtype: None
        :raises: None
        """
        self.__status = self.__UNLOADED

    def _load(self, ):
        """Loads the plugin

        :raises: errors.PluginInitError
        """
        try:
            self.init()
        except Exception as e:
            log.exception("Load failed!")
            raise errors.PluginInitError('%s' % e)
        self.__status = self.__LOADED

    def _unload(self, ):
        """Unloads the plugin

        :raises: errors.PluginUninitError
        """
        try:
            self.uninit()
        except Exception as e:
            log.exception("Unload failed!")
            raise errors.PluginUninitError('%s' % e)
        self.__status = self.__UNLOADED

    @abc.abstractmethod
    def init(self, ):
        """Initialize the plugin

        This function gets called when the plugin is loaded by the plugin manager.
        It is abstract and has to be implemented in a subclass

        :returns:
        :rtype:
        :raises:
        """
        pass

    @abc.abstractmethod
    def uninit(self, ):
        """Uninitialize the plugin

        This function gets called when the plugin is unloaded by the plugin manager.
        It is abstract and has to be implemented in a subclass

        :returns:
        :rtype:
        :raises:
        """
        pass

    def is_loaded(self, ):
        """Return True if the plugin is loaded

        :returns: Returns False if the plugin is not loaded
        :rtype: bool
        :raises: None
        """
        return self.__status

    def get_config(self, ):
        """Return the user config for this plugin

        You have to provide a configspec,
        put the configspec file in the same folder as your plugin.
        Name it like your class and put 'ini' as extension.
        """
        # get the module of the plugin class
        mod = sys.modules[self.__module__]
        # get the file from where it was imported
        modfile = mod.__file__
        # get the module directory
        specdir = os.path.dirname(modfile)
        # get the classname
        cname = self.__class__.__name__
        # add the extension
        confname = os.extsep.join((cname, CONFIG_EXT))

        specpath = os.path.join(specdir, confname)
        if not os.path.exists(specpath):
            return None
        confpath = os.path.join(PLUGIN_CONFIG_DIR, confname)
        return load_config(confpath, specpath)


class JB_CorePlugin(JB_Plugin):
    """Core plugin class

    Core plugins should be loadable at all times and not require a
    specific software to run.

    For subclassing: you have to implement **init** and **uninit**!
    """
    pass


class JB_CoreStandalonePlugin(JB_CorePlugin):
    """Core plugin for standalone addons.

    Standalone addons feature a special run method an
    can be run with the jukebox launcher.
    The launcher will first initialize the plugin and then
    call the run method.

    For subclassing: you have to implement **init**, **unit** and **run**!
    """

    @abc.abstractmethod
    def run(self, ):
        """Start the plugin. This method is also called by
        the jukebox launcher.

        :returns: None
        :rtype: None
        :raises: None
        """
        pass


class JB_CoreStandaloneGuiPlugin(JB_CoreStandalonePlugin):
    """Core plugin for standalone addons that also need a gui.

    Standalone addons feature a special run method an
    can be run with the jukebox launcher.
    The launcher will first initialize the plugin and then
    call the run method.

    For subclassing: you have to implement **init**, **unit** and **run**!
    """
    pass


class PluginManager(object):
    """Loads and unloads core plugins.

    A plugin manager scanns the plugin directories for plugins.
    Only plugins types that are supported can be loaded.
    If you need special plugins for a software, subclass JB_Plugin.
    Then create a subclass of this plugin manager and override
    supportedTypes. Core plugins should always be supported.

    The gathering of plugins is done during initialisation.
    To load the plugins, call load_plugins(). This will load
    all found plugins.
    """

    instance = None
    """PluginManager instance when using PluginManager.get() """

    supportedTypes = [JB_CorePlugin, JB_CoreStandalonePlugin, JB_CoreStandaloneGuiPlugin]
    """ A list of plugin classes, the manager can load.
    Override this list in a subclass if you want to support more than just core plugins,
    e.g. plugins that are meant for a specific software.
    """

    builtinpluginpath = BUILTIN_PLUGIN_PATH
    """String of Paths for builtin plugins, seperated by os.pathsep"""

    @classmethod
    def get(cls):
        """Return a PluginManager Instance.

        This will always return the same instance. If the instance is not available
        it will be created and returned.
        There should only be one pluginmanager at a time. If you create a PluginManager with get()
        and use get() on for example a MayaPluginManager,
        the PluginManager instance is returned (not a MayaPluginManager).

        :returns: always the same PluginManager
        :rtype: PluginManager
        :raises: None
        """
        if not cls.instance:
            PluginManager.instance = cls()
        return cls.instance

    def __init__(self, ):
        """Constructs a new PluginManager, use the get method in 99% of cases!

        :raises: None
        """
        pluginclasses = self.gather_plugins()
        self.__plugins = OrderedDict()
        for p in pluginclasses:
            self.__plugins[p.__name__] = p()

    def find_plugins(self, path):
        """Return a list with all plugins found in path

        :param path: the directory with plugins
        :type path: str
        :returns: list of JB_Plugin subclasses
        :rtype: list
        :raises: None
        """
        ext = os.extsep+'py'
        files = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            files.extend([os.path.join(dirpath, x) for x in filenames if x.endswith(ext)])
        plugins = []
        for f in files:
            try:
                mod = self.__import_file(f)
            except Exception:
                tb = traceback.format_exc()
                log.debug("Importing plugin from %s failed!\n%s" % (f, tb))
                continue
            # get all classes in the imported file
            members = inspect.getmembers(mod, lambda x: inspect.isclass(x))
            classes = [m[1] for m in members]  # get the classes
            for c in classes:
                # if the class is derived from a supported type append it
                # we test if it is a subclass of a supported type but not a supported type itself
                # because that might be the abstract class
                if any(issubclass(c, supported) for supported in self.supportedTypes)\
                   and c not in self.supportedTypes:
                    plugins.append(c)
        return plugins

    def gather_plugins(self):
        """Return all plugins that are found in the plugin paths

        Looks in the .. :data:`PluginManager.builtinpluginpath`
        Then in the envvar ``JUKEBOX_PLUGIN_PATH``.

        :returns:
        :rtype:
        :raises:
        """
        plugins = []
        cfg = get_core_config()
        pathenv =  os.environ.get("JUKEBOX_PLUGIN_PATHS", "")
        pathenv = os.pathsep.join((pathenv, cfg['jukebox']['pluginpaths']))
        pathenv = os.pathsep.join((pathenv, self.builtinpluginpath))
        paths = pathenv.split(os.pathsep)
        # first find built-ins then the ones in the config, then the one from the environment
        # so user plugins can override built-ins
        for p in reversed(paths):
            if p and os.path.exists(p):  # in case of an empty string, we do not search!
                plugins.extend(self.find_plugins(p))
        return plugins

    def load_plugins(self, ):
        """Loads all found plugins

        :returns: None
        :rtype: None
        :raises: None
        """
        for p in self.__plugins.values():
            try:
                self.load_plugin(p)
            except errors.PluginInitError:
                log.exception('Initializing the plugin: %s failed.' % p)

    def load_plugin(self, p):
        """Load the specified plugin

        :param p: The plugin to load
        :type p: Subclass of JB_Plugin
        :returns: None
        :rtype: None
        :raises: errors.PluginInitError
        """
        if p.is_loaded():
            return
        # load required plugins first
        reqnames = p.required
        reqplugins = []
        for name in reqnames:
            try:
                reqplugins.append(self.__plugins[name])
            except KeyError as e:
                log.error("Required Plugin %s not found. Cannot load %s." % (name, p))
                raise errors.PluginInitError('Required Plugin %s not found. Cannot load %s. Reason: %s' % (name, p, e))
        for plug in reqplugins:
            try:
                self.load_plugin(plug)
            except errors.PluginInitError as e:
                log.error("Required Plugin %s could not be loaded. Cannot load %s" % (plug, p))
                raise errors.PluginInitError('Required Plugin %s could not be loaded. Cannot load %s. Reason: %s' % (plug,p, e))
        # load the actual plugin
        p._load()
        log.info('Initialized the plugin: %s' % p)

    def unload_plugins(self, ):
        """ Unloads all loaded plugins

        :returns: None
        :rtype: None
        :raises: None
        """
        for p in self.__plugins.values():
            if p.is_loaded():
                try:
                    p._unload()
                    log.info('Uninitialized the plugin: %s' % p)
                except errors.PluginUninitError:
                    log.error('Uninitialization of the plugin: %s failed.' % p)

    def __import_file(self, f):
        """Import the specified file and return the imported module

        :param f: the file to import
        :type f: str
        :returns: The imported module
        :rtype: module
        :raises: None
        """
        directory, module_name = os.path.split(f)
        module_name = os.path.splitext(module_name)[0]

        path = list(sys.path)
        sys.path.insert(0, directory)
        try:
            module = __import__(module_name)
        finally:
            sys.path[:] = path # restore
        return module

    def get_plugin(self, plugin):
        """Return the plugin instance for the given pluginname

        :param plugin: Name of the plugin class
        :type plugin: str
        :returns: the plugin that matches the name
        :rtype: JB_Plugin like
        :raises: None
        """
        return self.__plugins[plugin]

    def get_all_plugins(self, ):
        """Return all plugins

        :returns: a list of all plugins found by the manager
        """
        return self.__plugins.values()
