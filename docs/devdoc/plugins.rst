=======
Plugins
=======

The pipeline is extensible via plugins. Plugins are simple python scripts that implement a certain class (:class:`jukeboxcore.plugins.JB_Plugin`).
In order to load the plugin, you have to put the script to a accessible location. Now you have two options.

--------------------
Environment variable
--------------------

Set the ``JUKEBOX_PLUGIN_PATH`` environment variable. You can add multiple paths if seperated by ``;`` on Windows and ``:`` on Linux. E.g. your plugin scripts live in ``~/myjukeboxplugins`` and ``/jukeboxplugins/`` then set the ``JUKEBOX_PLUGIN_PATH`` to ``~/myjukeboxplugins;/jukeboxplugins/``.

.. Important:: The order is important. Plugins in can overwrite other Plugins with the same name. The overriding Plugin has to live on a path that comes before the overridden Plugin. If you have two Plugins on the same path with the same name, there is no guarantee which one is loaded first.

--------
Settings
--------

You can also add paths to plugins in the core settings file. See `<configuration>`.


------------
Plugin types
------------

There are different plugin types. All plugin(type)s are subclasses from :class:`jukeboxcore.plugins.JB_Plugin`.
You can only load a certain set of plugin classes depending on the context.

Plugins might require a certain software suite like Maya or nuke. If your plugin needs Maya, the :mod:`jukeboxmaya.plugins` module has a collection of plugin classes that require maya to run. They only get loaded in Maya. If a plugin is of general purpose it should subclass from either :class:`jukeboxcore.plugins.JB_CorePlugin`, :class:`jukeboxcore.plugins.JB_CoreStandalonePlugin`, :class:`jukeboxcore.plugins.JB_CoreStandaloneGuiPlugin`.

Plugin classes with standalone in their name are like little seperate programms. For example the editor for the preferences can be launched on it's own via the :mod:`jukeboxcore.launcher`. StanaloneGui plugins require a QApplication to run.

Maya has it's own set of plugin types which are derived from the core ones.

Confused??? Good. Me too. So here are some examples when to use which plugin subclass.

+++++++++++++
JB_CorePlugin
+++++++++++++

A :class:`jukeboxcore.plugins.JB_CorePlugin` does extend the pipeline and does not require a software suite.
It could be a logging plugins, which logs all database access. It does not just run a procedure but extends the existing ones.

+++++++++++++++++++++++
JB_CoreStandalonePlugin
+++++++++++++++++++++++

A :class:`jukeboxcore.plugins.JB_CoreStandalonePlugin` does not require a software suite. It can be launched on its own or from
within any software suite. It could be a plugin that does database migrations. Basically it runs some procedure (without a gui).

++++++++++++++++++++++++++
JB_CoreStandaloneGuiPlugin
++++++++++++++++++++++++++

A :class:`jukeboxcore.plugins.JB_CoreStandaloneGuiPlugin` is similar to the previous one. But it wants to run a GUI.
For example the prefernce editor is a subclass of this class. It can run on its own or from within a software suite like maya and has a gui.

+++++++++++++
JB_MayaPlugin
+++++++++++++


:class:`jukeboxmaya.plugins.JB_MayaPlugin` is part of the jukeboxmaya package. It requires maya in order to work.
It could override the save command in maya or create a menu in maya etc.

+++++++++++++++++++++++
JB_MayaStandalonePlugin
+++++++++++++++++++++++

:class:`jukeboxmaya.plugins.JB_MayaStandalonePlugin` also requires maya. It can either run inside maya or in a maya standalone process (A maya without a gui). The plugin could open all scene files of a project and import all references automatically when run.

++++++++++++++++++++++++++
JB_MayaStandaloneGuiPlugin
++++++++++++++++++++++++++

:class:`jukeboxmaya.plugins.JB_MayaStandaloneGuiPlugin` requires maya, can run on its own and needs a gui. The release tool of the maya pipeline is such an example. In order to release a maya scene file, a maya standalone instance is sufficient. But it also requires a GUI so the user can select a file to release.

--------------
Minimal Plugin
--------------

Here is an example of a minimal plugin::

  from jukeboxcore import plugins
  
  class MinimalPlugin(plugins.JB_Plugin):
  
      required = ()  # a list of class names of other plugins that should be loaded beforehand
  
      # 'useless' metadata
      author = 'David Zuber'
      copyright = '2015'
      license = 'BSD'
      version='0.1.0'
      description='Does exactly nothing.'
  
      def init(self):
          # gets called when the plugin is loaded
  	print 'loaded my useless plugin'
  
      def uninit(self):
          print 'unloaded my useless plugin'

--------------
Plugin Configs
--------------

Some plugins might want to allow configuration by the user.
If a plugin wants such a configuration, it needs a configspec file. This file specifies the values the user can modify and the valid values. The name of the config file has to be exactly like the plugin class but the ending is ``ini``.
For a tutorial on how to write configspecs see: `Configobj documentation <https://configobj.readthedocs.org/en/latest/configobj.html#configspec>`_.

Example config spec for our ``MinimalPlugin``::

  # contents of MinimalPlugin.ini
  port = integer(0, 100)
  user = string(max=25)
  mode = option('quiet', 'loud', 'silent')
