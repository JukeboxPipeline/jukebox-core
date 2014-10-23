Configuration
=============

Inside the the pipeline user directory there is a config dir. You can edit the ``.ini`` -files inside there.
There is also a tool called Configer, that lets you edit these files in an special editor that validates your input.
Some plugins and tools might provide own interfaces for editing their config data. They might also override some stuff while they are running (e.g. to save the last selection).
To edit these files, start ``Configer`` via::

  $ jukebox launch Configer

The most importent section to configure might be the ``jukedj``-section under ``core.ini``.
For more information see :ref:`Connect to an existing Database <connect_db>`.

The Configer Tool will show you, if your settings are acceptable by displaying them either in green or red.
If you want to enter a string with a lot of special characters, try to put them in double quotes.
The reset button on the lower right cornor will reset the selected field to its default.


.. NOTE:: All keys that ask for paths should be a list of paths seperated by either ``:`` on linux or ``;`` on windows.
