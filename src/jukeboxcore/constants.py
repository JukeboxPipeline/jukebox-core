""" Define constant values that matter for the whole pipeline here """

import os
import logging

_norm = os.path.normpath  # make it shorter

here = os.path.abspath(os.path.dirname(__file__))

DEFAULT_LOGGING_LEVEL = logging.DEBUG
"""All loggers should use this level by default. When you obtain a logger with :func:`jukebox.core.log.get_logger`, it will have this level."""

BUILTIN_PLUGIN_PATH = _norm(os.path.join(here, 'addons'))
"""Path to all builtin plugins. The pluginmanager will load these by default."""

user_home = os.path.expanduser('~')
USERDIR = _norm(os.path.join(user_home, 'pipeline'))
"""The pipeline userdirectory. Here the pipeline can store or load userpreferences etc."""

CONFIG_EXT = 'ini'
"""All config files should have this extension."""

CONFIG_DIR = _norm(os.path.join(USERDIR, 'config'))
"""The directory where user configs are stored."""

PLUGIN_CONFIG_DIR = _norm(os.path.join(CONFIG_DIR, 'plugins'))
"""The directory where plugins store their configs."""

CORE_CONFIG_PATH = _norm(os.path.join(CONFIG_DIR, 'core.ini'))
"""The filepath of the core config."""

CORE_CONFIG_SPEC_PATH =_norm(os.path.join(here, 'corespec.ini'))
"""The filepath to the configspec of core.ini"""

#TODO
#ICON_PATH = _norm(os.path.join(SOURCE_PATH, 'images/icons'))
#"""Path to the icons"""

STYLESHEET_PATH = _norm(os.path.join(here, 'gui', 'stylesheets'))
"""Inside this dir is a colleciton of stylesheets."""

MAIN_STYLESHEET = _norm(os.path.join(STYLESHEET_PATH, 'main.qss'))
"""The default or main stylesheet that should be used by all our guis. Usually :func:`jukebox.core.gui.main.set_main_style` will do that for standalone apps."""


#TODO PUT IN USERCONV
TEST_PROJECTS_DIR = _norm(os.path.join('//ca-fs-01/ca-script/pipeline/testprojectdir', os.environ['USERNAME']))
"""A path to a location where a developer can put his test project."""
