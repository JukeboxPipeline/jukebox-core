"""Bundles common gui functions and classes

When creating a standalone app, you can use :func:`jukeboxcore.gui.main.init_gui` to
make sure there is a running QApplication. Usually the launcher will do that for you.
Then use set_main_style to apply the main_stylesheet to your app.
That way all the plugins have a consistent look.
"""

import os
import sys
import weakref
import pkg_resources

try:
    import shiboken
except ImportError:
    from PySide import shiboken
from PySide import QtGui, QtCore

from jukeboxcore.constants import MAIN_STYLESHEET, ICON_PATH

app = None
"""The QApplication app instance when using :func:`jukebox.core.gui.main.get_qapp`"""


def get_qapp():
    """Return an instance of QApplication. Creates one if neccessary.

    :returns: a QApplication instance
    :rtype: QApplication
    :raises: None
    """
    global app
    app = QtGui.QApplication.instance()
    if app is None:
        app = QtGui.QApplication(sys.argv)
    return app


def set_main_style(widget):
    """Load the main.qss and apply it to the application

    :param widget: The widget to apply the stylesheet to.
                   Can also be a QApplication. ``setStylesheet`` is called on the widget.
    :type widget: :class:`QtGui.QWidget`
    :returns: None
    :rtype: None
    :raises: None
    """
    with open(MAIN_STYLESHEET, 'r') as qss:
        sheet = qss.read()
    widget.setStyleSheet(sheet)


def init_gui():
    """Initialize a QApplication and apply the main style to it

    :returns: None
    :rtype: None
    :raises: None
    """
    app = get_qapp()
    set_main_style(app)


def wrap(ptr, base=None):
    """Wrap the given pointer with shiboken and return the appropriate QObject

    :returns: if ptr is not None returns a QObject that is cast to the appropriate class
    :rtype: QObject | None
    :raises: None
    """
    if ptr is None:
        return None
    ptr = long(ptr) # Ensure type
    if base is None:
        qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
        metaObj = qObj.metaObject()
        cls = metaObj.className()
        superCls = metaObj.superClass().className()
        if hasattr(QtGui, cls):
            base = getattr(QtGui, cls)
        elif hasattr(QtGui, superCls):
            base = getattr(QtGui, superCls)
        else:
            base = QtGui.QWidget
    return shiboken.wrapInstance(long(ptr), base)


def dt_to_qdatetime(dt):
    """Convert a python datetime.datetime object to QDateTime

    :param dt: the datetime object
    :type dt: :class:`datetime.datetime`
    :returns: the QDateTime conversion
    :rtype: :class:`QtCore.QDateTime`
    :raises: None
    """
    return QtCore.QDateTime(QtCore.QDate(dt.year, dt.month, dt.day),
                            QtCore.QTime(dt.hour, dt.minute, dt.second))


def get_icon(name, aspix=False, asicon=False):
    """Return the real file path to the given icon name
    If aspix is True return as QtGui.QPixmap, if asicon is True return as QtGui.QIcon.

    :param name: the name of the icon
    :type name: str
    :param aspix: If True, return a QtGui.QPixmap.
    :type aspix: bool
    :param asicon: If True, return a QtGui.QIcon.
    :type asicon: bool
    :returns: The real file path to the given icon name.
              If aspix is True return as QtGui.QPixmap, if asicon is True return as QtGui.QIcon.
              If both are True, a QtGui.QIcon is returned.
    :rtype: string
    :raises: None
    """
    datapath = os.path.join(ICON_PATH, name)
    icon = pkg_resources.resource_filename('jukeboxcore', datapath)
    if aspix or asicon:
        icon = QtGui.QPixmap(icon)
        if asicon:
            icon = QtGui.QIcon(icon)
    return icon


class JB_Gui(object):
    """A mixin class for top-level widgets liek main windows, widgets, dialogs etc

    .. Important:

      If you use this widget with a Qt object, make sure that your class will inherit from
      JB_Gui first! Qt objects do not call the super constructor!

    This class tracks its instances. So all classes that use this mixedin are tracked.
    Additionally each class that uses this mixin keeps track of its own instances and
    instances of its own class+subclasses
    """

    _allinstances = weakref.WeakSet()

    def __init__(self, *args, **kwargs):
        """Constructs a new JB_Gui that will be tracked

        :raises: None
        """
        super(JB_Gui, self).__init__(*args, **kwargs)
        self._add_instance()

    def _add_instance(self):
        JB_Gui._allinstances.add(self)

    @classmethod
    def allinstances(cls):
        """Return all instances that inherit from JB_Gui

        :returns: all instances that inherit from JB_Gui
        :rtype: list
        :raises: None
        """
        JB_Gui._allinstances = weakref.WeakSet([i for i in cls._allinstances if shiboken.isValid(i)])
        return list(cls._allinstances)

    @classmethod
    def classinstances(cls):
        """Return all instances of the current class

        JB_Gui will not return the instances of subclasses
        A subclass will only return the instances that have the same
        type as the subclass. So it won\'t return instances of further subclasses.

        :returns: all instnaces of the current class
        :rtype: list
        :raises: None
        """
        l = [i for i in cls.allinstances() if type(i) == cls]
        return l

    @classmethod
    def instances(cls):
        """Return all instances of this class and subclasses

        :returns: all instances of the current class and subclasses
        :rtype: list
        :raises: None
        """
        l = [i for i in cls.allinstances() if isinstance(i, cls)]
        return l


class JB_MainWindow(JB_Gui, QtGui.QMainWindow):
    """A main window class that should be used for all main windows

    It is useful for tracking all main windows and we can already set common
    attributes.
    """

    def __init__(self, *args, **kwargs):
        """Constructs a new JB_MainWindow. Arguments are passed on to QMainWindow

        :raises: None
        """
        super(JB_MainWindow, self).__init__(*args, **kwargs)
        set_main_style(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, on=True)
