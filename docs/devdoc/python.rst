Python
======

We use almost only python code for our pipeline. So here are a few infos to you should know.
I recommend python 2.7 64-bit because it compatible with the jukebox-maya package.

--------------------
Virtual Environments
--------------------

I recommend using `virtualenv <https://pypi.python.org/pypi/virtualenv>`_ or even better `virtualenvwrapper <https://pypi.python.org/pypi/virtualenvwrapper>`_. To install `virtualenvwrapper <https://pypi.python.org/pypi/virtualenvwrapper>`_ on Windows might be a little hard to do. It is possible by downloading several dependencies and putting them in your Git bin directory. But for that you also need ``msys`` and edit your ``.bashrc``. It might be easier to try `virtualenvwrapper for Windows <https://pypi.python.org/pypi/virtualenvwrapper-win>`_.

Create a new virtual environment for jukecore. Then install `tox <https://pypi.python.org/pypi/tox>`_ for unittesting.
I also recommend to install jukebox-core in edit mode::

  $ pip install -e path/to/jukeboxcorerepository


Coding Conventions
------------------

The general conventions for python are described in these official PEPs: `PEP8 <http://legacy.python.org/dev/peps/pep-0008/>`_, `PEP257 <http://legacy.python.org/dev/peps/pep-0257/>`_.
For writing docstrings, also look at :ref:`Docstring Guide <docstrings>`!

Organize your imports should be in the following order:

  1. standard library imports
  2. related third party imports
  3. local application/library specific imports

PySide
++++++

When writing pyside code it is hard to adhere the peps because PySide follows the C++-Conventions more or less. So if you override a pyside function you have to use camelcase. When defining your own use underscores! That way it is also easier to distinguish between our code and pyside code.

When using the designer, it is important how to name your widgets. Find a name for the widget that describes its function and/or location in the gui and add a suffix that is a abbreviation for the widget, e.g. '_lb' for label.

Here is a list for the most common widgets and layouts:

  :QWidget: _widget
  :QFrame: _fr
  :QMainWindow: _mwin
  :QPushButton: _pb
  :QToolButton: _tb
  :QRadioButton: _rb
  :QCheckBox: _checkb
  :QListView: _lv
  :QTreeView: _treev
  :QTableView: _tablev
  :QGroupBox: _gb
  :QScrollArea: _sa
  :QTabWidget: _tabw
  :QComboBox: _cb
  :QLineEdit: _le
  :QTextEdit: _te
  :QPlainTextEdit: _pte
  :QSpinBox: _sb
  :QDoubleSpinBox: _dsb
  :QScrollBar: _scrollb
  :QLabel: _lb
  :QTextBrowesr: _brw
  :QHBoxLayout: _hbox
  :QVBoxLayout: _vbox
  :QGridLayout: _grid
  :QFormLayout: _form

.. Note:: This list is in alpha stadium and can change!

Some widgets in the designer have internal layouts. These layouts can often be renamed directly in the designer. Especially the ones under ``container``.
