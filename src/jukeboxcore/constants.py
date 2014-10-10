""" Define constant values that matter for the whole pipeline here

The paths for data are relative paths from the package dir. To get the path to the actual data
that is installed use::

   pgk_resources.resource_filename('jukeboxcore', <data_path>)
"""

import os
import logging

from pkg_resources import resource_filename

_norm = os.path.normpath  # make it shorter

here = os.path.abspath(os.path.dirname(__file__))

DEFAULT_LOGGING_LEVEL = logging.DEBUG
"""All loggers should use this level by default. When you obtain a logger with :func:`jukebox.core.log.get_logger`, it will have this level."""

BUILTIN_PLUGIN_PATH = _norm(os.path.join(here, 'addons'))
"""Path to all builtin plugins. The pluginmanager will load these by default."""

user_home = os.path.expanduser('~')
USERDIR = _norm(os.path.join(user_home, '.jukebox'))
"""The pipeline userdirectory. Here the pipeline can store or load userpreferences etc."""

CONFIG_EXT = 'ini'
"""All config files should have this extension."""

CONFIG_DIR = _norm(os.path.join(USERDIR, 'config'))
"""The directory where user configs are stored."""

PLUGIN_CONFIG_DIR = _norm(os.path.join(CONFIG_DIR, 'plugins'))
"""The directory where plugins store their configs."""

CORE_CONFIG_PATH = _norm(os.path.join(CONFIG_DIR, 'core.ini'))
"""The filepath of the core config."""

DATA_DIR = 'data'
"""Location of the data directory of this package."""

_core_config_speq_data_path = os.path.join(DATA_DIR, 'corespec.ini')
CORE_CONFIG_SPEC_PATH = resource_filename('jukeboxcore', _core_config_speq_data_path)
"""The filepath to the configspec of core.ini"""

ICON_PATH = os.path.join(DATA_DIR, 'icons')
"""Data path to the icons."""

STYLESHEET_PATH = os.path.join(DATA_DIR, 'stylesheets')
"""Data path to the stylesheet directory"""

_main_stylesheet_data_path = os.path.join(STYLESHEET_PATH, 'main.qss')
MAIN_STYLESHEET = resource_filename('jukeboxcore', _main_stylesheet_data_path)
"""The default or main stylesheet that should be used by all our guis. Usually :func:`jukebox.core.gui.main.set_main_style` will do that for standalone apps."""

MAYA_VERSION = "2015"
"""The supported maya version for jukebox."""

MAYA_REG_KEY = "Software\\Autodesk\\Maya\\%s\\Setup\\InstallPath" % MAYA_VERSION
"""Registry key on windows to access maya install path"""

#TODO GET RID OF THIS!
TEST_PROJECTS_DIR = _norm(os.path.join('//ca-fs-01/ca-script/pipeline/testprojectdir', os.environ['USERNAME']))
"""A path to a location where a developer can put his test project."""
