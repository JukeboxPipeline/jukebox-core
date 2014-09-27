Python
======

We use almost only python code for our pipeline. So here are a few infos to you should know.

Third Party Packages
--------------------

For 'Users'
+++++++++++

Third party python packages that are needed for every pipeline user, not just devs, are located in a directory described by :data:`jukebox.core.constants.THIRD_PARTY_PATH`. In this directory is a whole subtree of dirs for the different platform and python versions. You can generate yourself a path with::

  import jukebox.loaders.thirdparty as tp
  tp.make_third_party_path()

You can also include this path automatically by just calling::

  tp.include_libs()

.. seealso:: :mod:`jukebox.core.thirdparty`

For 'Devs'
++++++++++

Third party python packages that are only needed for development (Sphinx, Nose, Lettuce etc.) have to be installed for your python distribution. To make things easy, I recommend to install these packages on your lokal python distribution. Here is a little guide on how to use a special setup.py, that will install all required libs automatically with only one command.

First of all: you need setuptools! Setuptools should be already installed on the computers in the CA-Pool. Unfortunately you have to add the script path manually to your ``PATH`` environment variable.

Then you can use the ``esay_install`` command to install the packages. There is a premade package for your convinience that installs all required packages. So just call::

  easy_install /L/pipeline/dev/Installation/jukebox_env-1.0.zip

and you are setup!

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
