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
