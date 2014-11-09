""" Here we provide standard loggers for our pipeline. It is advised to use them instead of the print function. """
import logging
import sys

from jukeboxcore.constants import DEFAULT_LOGGING_LEVEL


def setup_root_logger():
    """Setup the root logger with handlers

    The logger default level is defined in the constants :data:`jukeboxcore.constants.DEFAULT_LOGGING_LEVEL` but can be overwritten by the environment variable \"JUKEBOX_LOG_LEVEL\"

    :returns: None
    :rtype: None
    :raises: None
    """
    log = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    level = DEFAULT_LOGGING_LEVEL
    log.setLevel(level)


def get_logger(name, level=None):
    """ Return a setup logger for the given name

    :param name: The name for the logger. It is advised to use __name__.
    :type name: str
    :param level: the logging level, e.g. logging.DEBUG, logging.INFO etc
    :type level: int
    :returns: Logger
    :rtype: logging.Logger
    :raises: None

    The logger default level is defined in the constants :data:`jukeboxcore.constants.DEFAULT_LOGGING_LEVEL` but can be overwritten by the environment variable \"JUKEBOX_LOG_LEVEL\"

    """
    log = logging.getLogger(name)
    if level is not None:
        log.setLevel(level)
    return log


setup_root_logger()
