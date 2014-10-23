.. _environment_variables:

Environment Variables
=====================

Here is a list of important environment variables you can set/override:

  :JUKEBOX_PLUGIN_PATHS: In addition to adding the plugin paths for the pipeline to your user config you can use this environment variable
                         to include additional directories. If plugins in this path have the same name as built-in plugins or plugins from the user
			 config, then they override them.
  :JUKEBOX_LOG_LEVEL: The logging level of the pipeline. Choose from ``"NOTSET"``, ``"Debug"``, ``"INFO"``, ``"WARNING"``, ``"ERROR"``, ``"CRITICAL"``.
