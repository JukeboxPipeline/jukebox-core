""" Here we provide standard loggers for our pipeline. It is advised to use them instead of the print function. """

import logging

from jukeboxcore.constants import DEFAULT_LOGGING_LEVEL

logging.basicConfig()


def get_logger(name):
    """ Return a setup logger for the given name

    :param name: The name for the logger. It is advised to use __name__.
    :type name: str
    :returns: Logger
    :rtype: logging.Logger
    :raises: None

    The logger default level is defined in the constants  :data:`jukebox.core.constants.DEFAULT_LOGGING_LEVEL`

    """
    log = logging.getLogger(name)
    log.setLevel(DEFAULT_LOGGING_LEVEL)
    return log
