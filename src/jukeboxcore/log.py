""" Here we provide standard loggers for our pipeline. It is advised to use them instead of the print function. """
import logging
import sys

from jukeboxcore.constants import DEFAULT_LOGGING_LEVEL


def setup_jukebox_logger():
    """Setup the jukebox top-level logger with handlers

    The logger has the name ``jukebox`` and is the top-level logger for all other loggers of jukebox.
    It does not propagate to the root logger, because it also has a StreamHandler and that might cause double output.

    The logger default level is defined in the constants :data:`jukeboxcore.constants.DEFAULT_LOGGING_LEVEL` but can be overwritten by the environment variable \"JUKEBOX_LOG_LEVEL\"

    :returns: None
    :rtype: None
    :raises: None
    """
    log = logging.getLogger("jb")
    log.propagate = False
    handler = logging.StreamHandler(sys.stdout)
    fmt = "%(levelname)-8s:%(name)s:'%(message)s'"
    formatter = logging.Formatter(fmt)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    level = DEFAULT_LOGGING_LEVEL
    log.setLevel(level)


def get_logger(name, level=None):
    """ Return a setup logger for the given name

    :param name: The name for the logger. It is advised to use __name__. The logger name will be prepended by \"jb.\".
    :type name: str
    :param level: the logging level, e.g. logging.DEBUG, logging.INFO etc
    :type level: int
    :returns: Logger
    :rtype: logging.Logger
    :raises: None

    The logger default level is defined in the constants :data:`jukeboxcore.constants.DEFAULT_LOGGING_LEVEL` but can be overwritten by the environment variable \"JUKEBOX_LOG_LEVEL\"

    """
    log = logging.getLogger("jb.%s" % name)
    if level is not None:
        log.setLevel(level)
    return log


setup_jukebox_logger()
