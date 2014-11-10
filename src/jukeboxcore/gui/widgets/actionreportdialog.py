"""A Dialog Window to display the result of a :class:`jukeboxcore.action.ActionCollection`."""
import abc

from PySide import QtGui, QtCore

from jukeboxcore.gui.main import JB_Dialog, JB_MainWindow
from jukeboxcore.gui.actionreport import create_action_model
from jukeboxcore.gui.widgetdelegate import WidgetDelegate, WD_TableView
from actionreportdialog_ui import Ui_ActionReportDialog


class TextPopupButton(QtGui.QPushButton):
    """A abstract push button that will show a textedit as popup when you click on it

    Intended to be used in the :class:`jukeboxcore.gui.widgetdelegate.WidgetDelegate`.
    Subclass it and reimplement :meth:`TextPopupButton.get_popup_text`
    """

    def __init__(self, popuptitle, text, parent=None):
        """

        :param popuptitle: Title for the popup. shown in the titlebar of the popup
        :type popuptitle: str
        :param text: Text on the button. Not in the popup.
        :type text: str
        :param parent: widget parent
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(TextPopupButton, self).__init__(text, parent)
        self.popuptitle = popuptitle
        self.setAutoFillBackground(True)
        self.setText(text)
        self.clicked.connect(self.show_popup)

    def show_popup(self, *args, **kwargs):
        """Show a popup with a textedit

        :returns: None
        :rtype: None
        :raises: None
        """
        self.mw = JB_MainWindow(flags=QtCore.Qt.Dialog)
        self.mw.setWindowTitle(self.popuptitle)
        self.mw.setWindowModality(QtCore.Qt.ApplicationModal)
        w = QtGui.QWidget()
        self.mw.setCentralWidget(w)
        vbox = QtGui.QVBoxLayout(w)
        pte = QtGui.QPlainTextEdit()
        pte.setPlainText(self.get_popup_text())
        vbox.addWidget(pte)
        # move window to cursor position
        d = self.cursor().pos() - self.mw.mapToGlobal(self.mw.pos())
        self.mw.move(d)
        self.mw.show()

    @abc.abstractmethod
    def get_popup_text(self):
        """Return a text for the popup

        :returns: some text
        :rtype: str
        :raises: None
        """
        pass


class TracebackButton(TextPopupButton):
    """A push button that will show the traceback of an :class:`jukeboxcore.action.ActionUnit`.

    Intended to be used in the :class:`jukeboxcore.gui.widgetdelegate.ActionUnitDelegate`.
    """

    def __init__(self, parent=None):
        """Initialize a new TracebackButton

        :param parent: widget parent
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(TracebackButton, self).__init__("Traceback", "Show Traceback", parent)
        self.actionunit = None  # the current action unit

    def set_index(self, index):
        """Display the data of the given index

        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        item = index.internalPointer()
        self.actionunit = item.internal_data()
        self.setEnabled(bool(self.actionunit.status.traceback))

    @abc.abstractmethod
    def get_popup_text(self):
        """Return a text for the popup

        :returns: some text
        :rtype: str
        :raises: None
        """
        if self.actionunit:
            return self.actionunit.status.traceback
        else:
            return ""


class MessageButton(TextPopupButton):
    """A push button that will show the message of an :class:`jukeboxcore.action.ActionUnit`.

    Intended to be used in the :class:`jukeboxcore.gui.widgetdelegate.ActionUnitDelegate`.
    """

    def __init__(self, parent=None):
        """Initialize a new MessageButton

        :param parent: widget parent
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(MessageButton, self).__init__("Message", "Show Message", parent)
        self.actionunit = None  # the current action unit

    def set_index(self, index):
        """Display the data of the given index

        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        item = index.internalPointer()
        self.actionunit = item.internal_data()
        self.setEnabled(bool(self.actionunit.status.message))

    @abc.abstractmethod
    def get_popup_text(self):
        """Return a text for the popup

        :returns: some text
        :rtype: str
        :raises: None
        """
        if self.actionunit:
            return self.actionunit.status.message
        else:
            return ""


class ActionUnitTracebackDelegate(WidgetDelegate):
    """A delegate for drawing the tracebackcolumn of a :class:`jukeboxcore.gui.actionreport.ActionItenData`.
    """

    def __init__(self, parent=None):
        """

        :param parent: the parent object
        :type parent: QObject
        :raises: None
        """
        super(ActionUnitTracebackDelegate, self).__init__(parent)

    def create_widget(self, parent=None):
        """Return a widget that should get painted by the delegate

        You might want to use this in :meth:`WidgetDelegate.createEditor`

        :returns: The created widget | None
        :rtype: QtGui.QWidget | None
        :raises: None
        """
        return TracebackButton(parent)

    def set_widget_index(self, index):
        """Set the index for the widget. The widget should retrieve data from the index and display it.

        You might want use the same function as for :meth:`WidgetDelegate.setEditorData`.

        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self.widget.set_index(index)

    def create_editor_widget(self, parent, option, index):
        """Return the editor to be used for editing the data item with the given index.

        Note that the index contains information about the model being used.
        The editor's parent widget is specified by parent, and the item options by option.

        :param parent: the parent widget
        :type parent: QtGui.QWidget
        :param option: the options for painting
        :type option: QtGui.QStyleOptionViewItem
        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: Widget
        :rtype: :class:`QtGui.QWidget`
        :raises: None
        """
        return self.create_widget(parent)

    def setEditorData(self, editor, index):
        """Sets the contents of the given editor to the data for the item at the given index.

         Note that the index contains information about the model being used.

        :param editor: the editor widget
        :type editor: QtGui.QWidget
        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        editor.set_index(index)


class ActionUnitMessageDelegate(WidgetDelegate):
    """A delegate for drawing the tracebackcolumn of a :class:`jukeboxcore.gui.actionreport.ActionItenData`.
    """

    def __init__(self, parent=None):
        """

        :param parent: the parent object
        :type parent: QObject
        :raises: None
        """
        super(ActionUnitMessageDelegate, self).__init__(parent)

    def create_widget(self, parent=None):
        """Return a widget that should get painted by the delegate

        You might want to use this in :meth:`WidgetDelegate.createEditor`

        :returns: The created widget | None
        :rtype: QtGui.QWidget | None
        :raises: None
        """
        return MessageButton(parent)

    def set_widget_index(self, index):
        """Set the index for the widget. The widget should retrieve data from the index and display it.

        You might want use the same function as for :meth:`WidgetDelegate.setEditorData`.

        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self.widget.set_index(index)

    def create_editor_widget(self, parent, option, index):
        """Return the editor to be used for editing the data item with the given index.

        Note that the index contains information about the model being used.
        The editor's parent widget is specified by parent, and the item options by option.

        :param parent: the parent widget
        :type parent: QtGui.QWidget
        :param option: the options for painting
        :type option: QtGui.QStyleOptionViewItem
        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: Widget
        :rtype: :class:`QtGui.QWidget`
        :raises: None
        """
        return self.create_widget(parent)

    def setEditorData(self, editor, index):
        """Sets the contents of the given editor to the data for the item at the given index.

         Note that the index contains information about the model being used.

        :param editor: the editor widget
        :type editor: QtGui.QWidget
        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        editor.set_index(index)


class ActionReportDialog(JB_Dialog, Ui_ActionReportDialog):
    """A dialog that can show the result of a :class:`jukeboxcore.action.ActionCollection`

    The dialog will ask the user to confirm the report or cancel.

    The dialog uses the actionreportdialog.ui for it's layout.
    """

    def __init__(self, actioncollection, parent=None, flags=0):
        """Construct a new dialog for the given action collection

        :param actioncollection: the action collection to report
        :type actioncollection: :class:`jukeboxcore.action.ActionCollection`
        :param parent: Optional - the parent of the window - default is None
        :type parent: QWidget
        :param flags: the window flags
        :type flags: QtCore.Qt.WindowFlags
        :raises: None
        """
        super(ActionReportDialog, self).__init__(parent, flags)
        self.setupUi(self)
        self._actioncollection = actioncollection
        self._parent = parent
        self._flags = flags

        status = self._actioncollection.status()
        self.status_lb.setText(status.value)
        self.message_lb.setText(status.message)
        self.traceback_pte.setPlainText(status.traceback)

        self.traceback_pte.setVisible(False)

        model = create_action_model(self._actioncollection)
        self.actions_tablev = WD_TableView(self)
        self.actions_tablev.setModel(model)
        self.verticalLayout.insertWidget(1, self.actions_tablev)

        self.msgdelegate = ActionUnitMessageDelegate(self)
        self.tbdelegate = ActionUnitTracebackDelegate(self)
        self.actions_tablev.setItemDelegateForColumn(3, self.msgdelegate)
        self.actions_tablev.setItemDelegateForColumn(4, self.tbdelegate)

        self.actions_tablev.horizontalHeader().setStretchLastSection(True)
