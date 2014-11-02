"""A Dialog Window to display the result of a :class:`jukeboxcore.action.ActionCollection`."""
from PySide import QtGui, QtCore

from jukeboxcore.gui.main import JB_Dialog, JB_MainWindow
from jukeboxcore.gui.actionreport import create_action_model
from jukeboxcore.gui.widgetdelegate import WidgetDelegate, WD_TableView
from actionreportdialog_ui import Ui_ActionReportDialog


class TracebackButton(QtGui.QPushButton):
    """A push button that will show the traceback of an :class:`jukeboxcore.action.ActionUnit`.

    Intended to be used in the :class:`jukeboxcore.gui.widgetdelegate.ActionUnitDelegate`.
    """

    def __init__(self, parent=None):
        """Create a new TracebackButton

        :param parent: widget parent
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(TracebackButton, self).__init__(parent)
        self.setAutoFillBackground(True)
        self.setText("Show Traceback")
        self.actionunit = None  # the current action unit
        self.clicked.connect(self.show_traceback)

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

    def show_traceback(self, *args, **kwargs):
        """Show the traceback of the action_unit

        :param *args:
        :type *args:
        :param **kwargs:
        :type **kwargs:
        :returns: None
        :rtype: None
        :raises: None
        """
        if self.actionunit:
            self.mw = JB_MainWindow(flags=QtCore.Qt.Dialog)
            self.mw.setWindowTitle("Traceback")
            self.mw.setWindowModality(QtCore.Qt.ApplicationModal)
            w = QtGui.QWidget()
            self.mw.setCentralWidget(w)
            vbox = QtGui.QVBoxLayout(w)
            pte = QtGui.QPlainTextEdit()
            pte.setPlainText(self.actionunit.status.traceback)
            vbox.addWidget(pte)
            # move window to cursor position
            d = self.cursor().pos() - self.mw.mapToGlobal(self.mw.pos())
            self.mw.move(d)
            self.mw.show()


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

    def createEditor(self, parent, option, index):
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

        self.tbdelegate = ActionUnitTracebackDelegate(self)
        self.actions_tablev.setItemDelegateForColumn(4, self.tbdelegate)
        self.actions_tablev.horizontalHeader().setStretchLastSection(True)
