""" Module for platform specific operations

There are 3 important parts:

  :func:`jukebox.core.ostool.detect_sys` detects the platform you are working on.

  :py:class:`jukebox.core.ostool.PlatformInterface` is an abstract class that defines a set of methods
  To support a special plattform, subclass it and implement the abstract methods.
  Then put your Class inside :data:`jukebox.core.ostool.interfaces`. The system should be the key for the dict.

  :func:`jukebox.core.ostool.get_interface` will detect your system, then searches inside :data:`jukebox.core.ostool.interfaces` for a match.

"""
import abc
import os
import platform

from jukeboxcore import errors
from jukeboxcore.constants import MAYA_VERSION, MAYA_REG_KEY


def detect_sys():
    """ Tries to identify your python platform

    :returns: a dict with the gathered information
    :rtype: dict
    :raises: None

    the returned dict has these keys: 'system', 'bit', 'compiler', 'python_version_tuple'

    eg.::

      {'system':'Windows', 'bit':'32bit', 'compiler':'MSC v.1500 32bit (Intel)', 'python_version_tuple':('2', '7', '6')}

    """
    system = platform.system()
    bit = platform.architecture()[0]
    compiler = platform.python_compiler()
    ver = platform.python_version_tuple()
    return {'system': system, 'bit': bit, 'compiler': compiler, 'python_version_tuple': ver}


class PlatformInterface(object):
    """ An abstract class that has platform specific methods

    Sublcasses have to implement those methods!
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_maya_location(self, ):
        """ Return the installation path to maya

        :returns: path to maya
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass

    @abc.abstractmethod
    def get_maya_sitepackage_dir(self):
        """ Return the sitepackage dir for maya

        :returns: path to the maya sitepackages
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass

    @abc.abstractmethod
    def get_maya_python(self, ):
        """ Return the path to the mayapy executable

        :returns: path to the maya python intepreter
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass

    @abc.abstractmethod
    def get_maya_exe(self, ):
        """ Return the path to the maya executable

        :returns: path to the maya exe
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass


class WindowsInterface(PlatformInterface):
    """ Interface for all windows related operations

    implements all methods of PlatformInterface
    """

    def get_maya_location(self, ):
        """ Return the installation path to maya

        :returns: path to maya
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        import _winreg
        # query winreg entry
        # the last flag is needed, if we want to test with 32 bit python! Because Maya is an 64 bit key!
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                  MAYA_REG_KEY, 0,
                                  _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
            value = _winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")[0]
        except WindowsError:
            raise errors.SoftwareNotFoundError('Maya %s installation not found in registry!' % MAYA_VERSION)
        return value

    def get_maya_sitepackage_dir(self, ):
        """ Return the sitepackage dir for maya

        :returns: path to the maya sitepackages
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        mayaloc = self.get_maya_location()
        return os.path.join(mayaloc, 'Python', 'Lib', 'site-packages')

    def get_maya_python(self, ):
        """ Return the path to the mayapy executable

        :returns: path to the maya python intepreter
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        mayaloc = self.get_maya_location()
        return os.path.join(mayaloc, 'bin', 'mayapy.exe')

    def get_maya_exe(self, ):
        """ Return the path to the maya executable

        :returns: path to the maya exe
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        mayaloc = self.get_maya_location()
        return os.path.join(mayaloc, 'bin', 'maya.exe')


interfaces = {'Windows': WindowsInterface}
""" Dictionary for platforminterfaces.
Values are PlatformInterface subclasses and
keys are values of detect_sys()['system'] """


def get_interface():
    """ Return the appropriate PlatformInterface implementation for your platform

    :returns: the appropriate platform interface for my platform
    :rtype: subclass of PlatformInterface
    :raises: errors.UnsupportedPlatformError
    """
    plat = detect_sys()['system']
    try:
        return interfaces[plat]()
    except KeyError:
        raise errors.UnsupportedPlatformError("%s is not supported. \
        Implement an interface for it in jukebox.ostool!" % plat)
