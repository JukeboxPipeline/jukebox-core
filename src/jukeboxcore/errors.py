"""Module for all our custom exceptions"""


class JukeboxException(Exception):
    """Base Exceptions for all our jukebox related Exceptions!

    Subclass this for your own exceptions. Do not recreate the builtin exceptions!
    We still use them. But whenever you want to raise a custom exception, use this as baseclass.
    """
    pass


class PluginInitError(JukeboxException):
    """Jukebox Exception that is raised when a Plugin fails initializing."""
    pass


class PluginUninitError(JukeboxException):
    """Jukebox Exception that is raised when a Plugin fails uninitializing."""
    pass


class UnsupportedPlatformError(JukeboxException):
    """Jukebox Exception that is raised when the platform you are on does not support some actions."""
    pass


class SoftwareNotFoundError(JukeboxException):
    """Jukebox Exception that is raised when the pipeline cannot find a required software."""
    pass


class ConfigError(JukeboxException):
    """Jukebox Exception that is raised when some error occurs concerning Config files."""
    pass


class MenuExistsError(JukeboxException):
    """Jukebox Exception that is raised when a MenuManger tries to create a menu that already exists."""
    pass


class IntegrityError(JukeboxException):
    """Jukebox Exception that is raised when the pipeline cannot execute an action
    because it would affect the integrity of the pipeline.
    """
    pass


class ReftrackIntegrityError(IntegrityError):
    """Jukebox Integrity Exception that is raised when an action concerning the reference workflow
    cannot be executed because it would affect the integrity of the reference workflow.

    You can access a list of :class:`jukeboxcore.reftrack.Reftrack` that would cause the error
    with :data:`ReftrackIntegrityError.reftracks`.
    """
    def __init__(self, msg=None, reftracks=None):
        """Initialize a new exception with a error message and the reftracks that
        would cause an integrity error.

        :param msg: the error message
        :type msg: :class:`str` | None
        :param reftracks: the reftracks that would cause an integrity error
        :type reftracks: list of :class:`jukeboxcore.reftrack.Reftrack` | None
        :raises: None
        """
        super(ReftrackIntegrityError, self).__init__(msg)
        if reftracks is None:
            reftracks = []
        self.reftracks = reftracks
