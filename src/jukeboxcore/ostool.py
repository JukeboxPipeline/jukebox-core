""" Module for platform specific operations

There are 3 important parts:

  :func:`jukeboxcore.ostool.detect_sys` detects the platform you are working on.

  :class:`jukeboxcore.ostool.PlatformInterface` is an abstract class that defines a set of methods
  To support a special plattform, subclass it and implement the abstract methods.
  Then put your Class inside :data:`jukeboxcore.ostool.interfaces`. The system should be the key for the dict.

  :func:`jukeboxcore.ostool.get_interface` will detect your system, then searches inside :data:`jukeboxcore.ostool.interfaces` for a match.

"""
import abc
import os
import platform

from jukeboxcore import errors
from jukeboxcore.constants import MAYA_VERSION, MAYA_REG_KEY


def detect_sys():
    """Tries to identify your python platform

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
    """An abstract class that has platform specific methods

    Sublcasses have to implement those methods!
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_maya_location(self, ):
        """Return the installation path to maya

        :returns: path to maya
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass

    @abc.abstractmethod
    def get_maya_sitepackage_dir(self):
        """Return the sitepackage dir for maya

        :returns: path to the maya sitepackages
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass

    @abc.abstractmethod
    def get_maya_bin(self):
        """Return the path to the maya bin dir

        :returns: path to maya bin dir
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass

    @abc.abstractmethod
    def get_maya_python(self, ):
        """Return the path to the mayapy executable

        :returns: path to the maya python intepreter
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass

    @abc.abstractmethod
    def get_maya_exe(self, ):
        """Return the path to the maya executable

        :returns: path to the maya exe
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        pass

    @abc.abstractmethod
    def get_maya_envpath(self):
        """Return the PYTHONPATH neccessary for running mayapy

        :returns: the PYTHONPATH that is used for running mayapy
        :rtype: str
        :raises: None
        """
        pass


class WindowsInterface(PlatformInterface):
    """Interface for all windows related operations

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
        # the last flag is needed, if we want to test with 32 bit python!
        # Because Maya is an 64 bit key!
        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
                                  MAYA_REG_KEY, 0,
                                  _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY)
            value = _winreg.QueryValueEx(key, "MAYA_INSTALL_LOCATION")[0]
        except WindowsError:
            raise errors.SoftwareNotFoundError('Maya %s installation not found in registry!' % MAYA_VERSION)
        return value

    def get_maya_sitepackage_dir(self, ):
        """Return the sitepackage dir for maya

        :returns: path to the maya sitepackages
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        mayaloc = self.get_maya_location()
        return os.path.join(mayaloc, 'Python', 'Lib', 'site-packages')

    def get_maya_bin(self):
        """Return the path to the maya bin dir

        :returns: path to maya bin dir
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        mayaloc = self.get_maya_location()
        return os.path.join(mayaloc, 'bin')

    def get_maya_python(self, ):
        """Return the path to the mayapy executable

        :returns: path to the maya python intepreter
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        mayabin = self.get_maya_bin()
        return os.path.join(mayabin, 'mayapy.exe')

    def get_maya_exe(self, ):
        """Return the path to the maya executable

        :returns: path to the maya exe
        :rtype: str
        :raises: errors.SoftwareNotFoundError
        """
        mayabin = self.get_maya_bin()
        return os.path.join(mayabin, 'maya.exe')

    def get_maya_envpath(self):
        """Return the PYTHONPATH neccessary for running mayapy

        If you start native mayapy, it will setup these paths.
        You might want to prepend this to your path if running from
        an external intepreter.

        :returns: the PYTHONPATH that is used for running mayapy
        :rtype: str
        :raises: None
        """
        opj = os.path.join
        ml = self.get_maya_location()
        mb = self.get_maya_bin()
        msp = self.get_maya_sitepackage_dir()
        pyzip = opj(mb, "python27.zip")
        pydir = opj(ml, "Python")
        pydll = opj(pydir, "DLLs")
        pylib = opj(pydir, "lib")
        pyplat = opj(pylib, "plat-win")
        pytk = opj(pylib, "lib-tk")
        path = os.pathsep.join((pyzip, pydll, pylib, pyplat, pytk, mb, pydir, msp))
        return path


interfaces = {'Windows': WindowsInterface}
""" Dictionary for platforminterfaces.
Values are PlatformInterface subclasses and
keys are values of detect_sys()['system'] """


def get_interface():
    """Return the appropriate PlatformInterface implementation for your platform

    :returns: the appropriate platform interface for my platform
    :rtype: :class:`PlatformInterface``
    :raises: errors.UnsupportedPlatformError
    """
    plat = detect_sys()['system']
    try:
        return interfaces[plat]()
    except KeyError:
        raise errors.UnsupportedPlatformError("%s is not supported. \
        Implement an interface for it in jukeboxcore.ostool!" % plat)
