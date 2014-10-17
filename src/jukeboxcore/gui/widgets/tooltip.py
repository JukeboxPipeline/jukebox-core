from functools import partial
from collections import OrderedDict

try:
    import shiboken
except ImportError:
    from PySide import shiboken
from PySide import QtGui, QtCore

from jukeboxcore.gui.main import JB_MainWindow


class WidgetToolTip(QtGui.QWidget):
    """A ToolTip that can be installed on a widget via :meth:`WidgetToolTip.install_tooltip`

    The tooltip is a selector for added widgets. The widgets are rendered to icons that are placed onto Buttons.
    If a button is clicked the widget receives focus.

    .. Warning:: Setting the layout after initialisation has no effect at the moment.

    There are a few properties and setters that can be changed. The affect might only take place after calling :meth:`WidgetToolTip.show`.
    Properties and setters:

      ::meth:`WidgetToolTip.alignment`: property for the alignment relative to the mouse
      ::meth:`WidgetToolTip.offset`: property for the offset relativ to the alignment
      ::meth:`WidgetToolTip.triggerevent`: property for the event that triggers the tooltip
      ::meth:`WidgetToolTip.setup_size`: setter for the size of one cell/button
      ::meth:`WidgetToolTip.setup_cyatimer`: setter for the time the widget waits before closing

    To use this tooltip for any widget that triggers a ToolTip event:

      1. Create the WidgetToolTip widget
      2. Install it on a widget
      3. Add Widgets to the WidgetToolTip

    Example::

      mainwidget = QtGui.QWidget()
      widget1 = QtGui.QWidget()
      widget2 = QtGui.QWidget()
      # Step 1 with the default parameters
      tooltip = WidgetToolTip(orientation=QtCore.Qt.Horizontal,
                              alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter,
                              offset=20,
                              parent=None,
                              flags=QtCore.Qt.CustomizeWindowHint)
      # Step 2
      tooltip.install_tooltip(mainwidget)
      # Step 3
      tooltip.add_widget(widget1)
      tooltip.add_widget(widget2)

    """

    def __init__(self, orientation=QtCore.Qt.Horizontal,
                 alignment=None,
                 offset=20,
                 interval=1000,
                 size=QtCore.QSize(160, 90),
                 triggerevent=QtCore.QEvent.ToolTip,
                 parent=None,
                 flags=QtCore.Qt.CustomizeWindowHint):  # hides title bar but gives a frames
        """Initialize the ToolTip in the given orientation with an optional parent and windowflags.

        :param orientation: the orientation of the tooltip. horizontal or vertical
        :type orientation: QtCore.Qt.Orientation
        :param parent: the parent of the widget
        :param alignment: affcts the positon of the popup relative to the mouse. If None, align left and vcenter is chosen
                          Use left, right, hcenter, top, bottom and vcenter only. Everything else will be ignored.
        :type alignment: QtCore.Qt.Alignment | None
        :param offset: The offset to the alignment in pixels
        :type offset: int
        :param interval: The time to wait for the tooltip to close in miliseconds
        :type interval: int
        :param size: The size of one cell/button
        :type size: QtCore.QSize
        :param triggerevent: The event that triggers the tooltip
        :type triggerevent: QtCore.QEvent.Type
        :type parent: QtGui.QWidget
        :param flags: the windowflags
        :type flags: QtCore.QtWindowFlags
        :raises: TypeError
        """
        super(WidgetToolTip, self).__init__(parent, flags)
        self._buttons = OrderedDict()
        self._triggerevent = triggerevent
        self._alignment = alignment
        self._offset = 20
        if alignment is None:
            self._alignment = QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        self.setup_layout(orientation)
        self.setup_size(size.width(), size.height())
        self.setup_cyatimer(interval)

    def setup_layout(self, orientation=None):
        """Setup the layout for the tooltip in the given orientation

        :param layout: the orentation of the layout
        :type layout: QtCore.Qt.Orientation | None
        :returns: None
        :rtype: None
        :raises: None
        """
        if orientation == QtCore.Qt.Horizontal or orientation is None:
            layout = QtGui.QHBoxLayout()
        elif orientation == QtCore.Qt.Vertical:
            layout = QtGui.QVBoxLayout()
        else:
            raise TypeError('Orientation is of wrong type! Allowed is QtCore.Qt.Horizontal and QtCore.Qt.Vertical. Given: %s' % orientation)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def setup_size(self, width, height):
        """Set the width and height for one cell in the tooltip

        This is inderectly acomplished by setting the iconsizes for the buttons.

        :param width: the width of one cell, min. is 7 -> icon width = 0
        :type width: int
        :param height: the height of one cell, min. is 6 -> icon height = 0
        :type height: int
        :returns: None
        :rtype: None
        :raises: None
        """
        self._iconw = max(0, width - 7)
        self._iconh = max(0, height - 6)
        self.update_all_buttons()

    def setup_cyatimer(self, interval):
        """Setup the timer that will close the widget after the mouse left the widget for the time of interval

        :param interval: the time that the tooltip waits before it dissapears in milliseconds
        :type interval: int
        :returns: None
        :rtype: None
        :raises: None
        """
        self.cyatimer = QtCore.QTimer(self)
        self.cyatimer.setSingleShot(True)
        self.cyatimer.timeout.connect(self.hide)
        self._interval = interval

    def event(self, event):
        """Reimplementation of QWidget.event

        The widget is closed, when the window is deactivated.
        The widget is closed after the set interval if the mouse leaves the widget.
        The timer is stops when the mouse enters the widget before the interval ends.
        On show, the added widgets are rendered for the tooltip into buttons. The buttons
        are used to set the widget in focus.
        """
        if event.type() == QtCore.QEvent.WindowDeactivate:  # hide the tooltip
            self.cyatimer.stop()
            self.hide()
            return True
        if event.type() == QtCore.QEvent.Leave:  # start timer
            self.cyatimer.start(self._interval)
            return True
        if event.type() == QtCore.QEvent.Enter:  # reset/stop timer
            self.cyatimer.stop()
            return True
        if event.type() == QtCore.QEvent.Show:  # render the widgets
            self.cyatimer.stop()
            return True
        return super(WidgetToolTip, self).event(event)

    def create_button(self, widget):
        """Create a button that has the given widget rendered as an icon

        :param widget: the widget to render as icon
        :type widget: QtGui.QWidget
        :returns: the created button
        :rtype: QtGui.QAbstractButton
        :raises: None
        """
        btn = QtGui.QToolButton(self)
        btn.setIconSize(QtCore.QSize(self._iconw, self._iconh))
        self.update_button(btn, widget)
        return btn

    def update_button(self, button, widget):
        """Update the icon of the button with the given widget

        if the widget does not is invalid, it is deleted from the tooltip automatically.

        :param button: the button to update
        :type button: QtGui.QAbstractButton
        :param widget: the widget to render as icon
        :type widget: QtGui.QWidget
        :returns: None
        :rtype: None
        :raises: None
        """
        if not shiboken.isValid(widget):
            self.remove_widget(widget)
            return
        button.setIconSize(QtCore.QSize(self._iconw, self._iconh))
        pix = QtGui.QPixmap(widget.size())
        widget.render(pix)
        icon = QtGui.QIcon(pix)
        button.setIcon(icon)

    def update_all_buttons(self, ):
        """Update all buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        for widget, button in self._buttons.items():
            self.update_button(button, widget)
        self.adjustSize()

    def focus_widget(self, checked=None, w=None):
        """Focus the given widget. Checked is ignored and only used as a slot for QAbstractButton.clicked.

        :param checked: The checked state of the button that was clicked
        :type checked: bool
        :param w: the widget to focus
        :type w: QtGui.QWidget
        :returns: None
        :raises: None
        """
        if w is None:
            return
        w.show()
        w.activateWindow()
        w.setFocus()

    def add_widget(self, widget):
        """Add the given widget to the tooltip

        :param widget: the widget to add
        :type widget: QtGui.QWidget
        :returns: None
        :rtype: None
        :raises: None
        """
        if self._buttons.get(widget):
            return
        btn = self.create_button(widget)
        cb = partial(self.focus_widget, w=widget)
        btn.clicked.connect(cb)
        self.layout().addWidget(btn)
        self._buttons[widget] = btn

    def remove_widget(self, widget):
        """Remove the given widget from the tooltip

        :param widget: the widget to remove
        :type widget: QtGui.QWidget
        :returns: None
        :rtype: None
        :raises: KeyError
        """
        button = self._buttons.pop(widget)
        self.layout().removeWidget(button)
        button.deleteLater()

    def eventFilter(self, watched, event):
        """Filter ToolTip events and display this tooltip widget, if watched requests a tooltip.

        :param watched: The watched object
        :type watched: QtCore.QObject
        :param event: The event sent by watched
        :type event: QtCore.QEvent
        :returns: True if the event was processed. False if the event should be passed on.
        :rtype: bool
        :raises: None
        """
        if event.type() == self._triggerevent:
            self.show()
            return True
        else:
            return False

    def get_position(self, ):
        """Return a recommended position for this widget to appear

        This implemenation returns a position so that the widget is vertically centerd on the mouse
        and 10 pixels left of the mouse

        :returns: the position
        :rtype: QPoint
        :raises: None
        """
        pos = QtGui.QCursor.pos()
        if self._alignment & QtCore.Qt.AlignLeft == QtCore.Qt.AlignLeft:
            pos.setX(pos.x() - self._offset)
        elif self._alignment & QtCore.Qt.AlignRight == QtCore.Qt.AlignRight:
            pos.setX(pos.x() - self.frameGeometry().width() + self._offset)
        elif self._alignment & QtCore.Qt.AlignHCenter == QtCore.Qt.AlignHCenter:
            pos.setX(pos.x() - self.frameGeometry().width()/2)
        if self._alignment & QtCore.Qt.AlignTop == QtCore.Qt.AlignTop:
            pos.setY(pos.y() - self._offset)
        elif self._alignment & QtCore.Qt.AlignBottom == QtCore.Qt.AlignBottom:
            pos.setY(pos.y() - self.frameGeometry().height() + self._offset)
        elif self._alignment & QtCore.Qt.AlignVCenter == QtCore.Qt.AlignVCenter:
            pos.setY(pos.y() - self.frameGeometry().height()/2)
        return pos

    def install_tooltip(self, parent):
        """Intall the tooltip on the parent so that it is shown when parent requests a tooltip

        :param parent: the parent object
        :type parent: QObject
        :returns: None
        :rtype: None
        :raises: None
        """
        parent.installEventFilter(self)

    @property
    def alignment(self):
        """Get the alginment of the tooltip relative to the mouse

        :returns: alignment
        :rtype: QtCore.Qt.Alignment
        :raises: None
        """
        return self._alignment

    @alignment.setter
    def alignment(self, alignment):
        """Set the alginment of the tooltip relative to the mouse

        :param alignment: The value for alignment
        :type alignment: QtCore.Qt.Alignment
        :raises: None
        """
        self._alignment = alignment

    @property
    def offset(self):
        """Return offset to the alignment in pixels

        :returns: offset
        :rtype: int
        :raises: None
        """
        return self._offset

    @offset.setter
    def offset(self, offset):
        """Set offset to the alginment in pixels

        :param offset: The value for offset
        :type offset: int
        :raises: None
        """
        self._offset = offset

    @property
    def triggerevent(self):
        """Return triggerevent

        :returns: triggerevent
        :rtype: QtCore.QEvent.Type
        :raises: None
        """
        return self._triggerevent

    @triggerevent.setter
    def triggerevent(self, eventtype):
        """Set triggerevent

        :param eventtype: The value for triggerevent
        :type eventtype: QtCore.QEvent.Type
        :raises: None
        """
        self._triggerevent = eventtype

    def get_widgets(self, ):
        """Return all registered Widgets

        :returns: list of widgets
        :rtype: list
        :raises: None
        """
        return self._buttons.keys()

    def show(self, ):
        """Reimplementation that moves the tooltip and updates the buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        self.update_all_buttons()
        pos = self.get_position()
        self.move(pos)
        super(WidgetToolTip, self).show()


class JB_WindowToolTip(WidgetToolTip):

    def show(self, ):
        """Reimplementation of show to update all currently available JB_MainWindows

        :returns: None
        :rtype: None
        :raises: None
        """
        wins = set(JB_MainWindow.instances())
        widgets = set(self.get_widgets())
        for w in wins - widgets:
            self.add_widget(w)
        super(JB_WindowToolTip, self).show()
