from functools import partial

from PySide import QtGui, QtCore

from jukeboxcore.gui.widgets.reftrackwidget_ui import Ui_ReftrackWidget
from jukeboxcore.gui.widgets.optionselector_ui import Ui_OptionSelector
from jukeboxcore.gui.widgets.browser import ComboBoxBrowser
from jukeboxcore.gui.widgetdelegate import WidgetDelegate
from jukeboxcore.gui.main import JB_Dialog, get_icon
from jukeboxcore.gui.reftrackitemdata import REFTRACK_OBJECT_ROLE


class OptionSelector(JB_Dialog, Ui_OptionSelector):
    """Widget to select options when importing or referencing
    """

    def __init__(self, reftrack, parent=None):
        """Initialize a new OptionSelector

        :param reftrack: the reftrack to show options for
        :type reftrack: :class:`jukeboxcore.reftrack.Reftrack`
        :param parent: the parent widget
        :type parent: :class:`QtGui.QWidget`
        :raises: None
        """
        super(OptionSelector, self).__init__(parent)
        self.setupUi(self)
        self.selected = None
        self.reftrack = reftrack
        self.setup_ui()
        self.setup_signals()
        options = reftrack.get_options()
        self.browser.set_model(options)
        columns = self.reftrack.get_option_columns()
        for i, c in enumerate(columns):
            self.browser.get_level(i).setModelColumn(c)
        self.adjustSize()

    def setup_ui(self, ):
        """Setup the ui

        :returns: None
        :rtype: None
        :raises: None
        """
        labels = self.reftrack.get_option_labels()
        self.browser = ComboBoxBrowser(len(labels), headers=labels)
        self.browser_vbox.addWidget(self.browser)

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
        self.select_pb.clicked.connect(self.select)

    def select(self, ):
        """Store the selected taskfileinfo self.selected and accept the dialog

        :returns: None
        :rtype: None
        :raises: None
        """
        s = self.browser.selected_indexes(self.browser.get_depth()-1)
        if not s:
            return
        i = s[0].internalPointer()
        if i:
            tfi = i.internal_data()
            self.selected = tfi
            self.accept()


class ReftrackWidget(Ui_ReftrackWidget, QtGui.QFrame):
    """Widget to display Reftracks in a Widgetdelegate
    """

    def __init__(self, parent=None):
        """Initialize a new ReftrackWidget

        :param parent: widget parent
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(ReftrackWidget, self).__init__(parent)
        self.setupUi(self)
        self.reftrack = None
        self.setup_ui()
        self.setup_signals()

        self.upper_fr_default_bg_color = self.upper_fr.palette().color(QtGui.QPalette.Window)

    def setup_ui(self, ):
        """Setup the ui

        :returns: None
        :rtype: None
        :raises: None
        """
        self.setup_icons()

    def setup_icons(self, ):
        """Setup the icons of the ui

        :returns: None
        :rtype: None
        :raises: None
        """
        iconbtns = [("menu_border_24x24.png", self.menu_tb),
                    ("duplicate_border_24x24.png", self.duplicate_tb),
                    ("delete_border_24x24.png", self.delete_tb),
                    ("reference_border_24x24.png", self.reference_tb),
                    ("load_border_24x24.png", self.load_tb),
                    ("unload_border_24x24.png", self.unload_tb),
                    ("replace_border_24x24.png", self.replace_tb),
                    ("import_border_24x24.png", self.importref_tb),
                    ("import_border_24x24.png", self.importtf_tb),
                    ("alien.png", self.alien_tb),
                    ("imported.png", self.imported_tb)]
        for iconname, btn in iconbtns:
            i = get_icon(iconname, asicon=True)
            btn.setIcon(i)

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
        self.duplicate_tb.clicked.connect(self.duplicate)
        self.delete_tb.clicked.connect(self.delete)
        self.load_tb.clicked.connect(self.load)
        self.unload_tb.clicked.connect(self.unload)
        self.reference_tb.clicked.connect(self.reference)
        self.importtf_tb.clicked.connect(self.import_file)
        self.importref_tb.clicked.connect(self.import_reference)
        self.replace_tb.clicked.connect(self.replace)
        self.imported_tb.clicked.connect(partial(self.toggle_tbstyle, button=self.imported_tb))
        self.alien_tb.clicked.connect(partial(self.toggle_tbstyle, button=self.alien_tb))

    def set_index(self, index):
        """Display the data of the given index

        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self.index = index
        self.reftrack = index.model().index(index.row(), 18, index.parent()).data(REFTRACK_OBJECT_ROLE)
        self.set_maintext(self.index)
        self.set_identifiertext(self.index)
        self.set_type_icon(self.index)
        self.disable_restricted()
        self.hide_restricted()
        self.set_top_bar_color(self.index)
        self.set_status_buttons()
        self.set_menu()

    def set_maintext(self, index):
        """Set the maintext_lb to display text information about the given reftrack

        :param index: the index
        :type index: :class:`QtGui.QModelIndex`
        :returns: None
        :rtype: None
        :raises: None
        """
        dr = QtCore.Qt.DisplayRole
        text = ""
        model = index.model()
        for i in (1, 2, 3, 5, 6):
            new = model.index(index.row(), i, index.parent()).data(dr)
            if new is not None:
                text = " | ".join((text, new)) if text else new

        self.maintext_lb.setText(text)

    def set_identifiertext(self, index):
        """Set the identifier text on the identifier_lb

        :param index: the index
        :type index: :class:`QtGui.QModelIndex`
        :returns: None
        :rtype: None
        :raises: None
        """
        dr = QtCore.Qt.DisplayRole
        t = index.model().index(index.row(), 17, index.parent()).data(dr)
        if t is None:
            t = -1
        else:
            t = t+1
        self.identifier_lb.setText("#%s" % t)

    def set_type_icon(self, index):
        """Set the type icon on type_icon_lb

        :param index: the index
        :type index: :class:`QtGui.QModelIndex`
        :returns: None
        :rtype: None
        :raises: None
        """
        icon = index.model().index(index.row(), 0, index.parent()).data(QtCore.Qt.DecorationRole)
        if icon:
            pix = icon.pixmap(self.type_icon_lb.size())
            self.type_icon_lb.setPixmap(pix)
        else:
            self.type_icon_lb.setPixmap(None)

    def disable_restricted(self, ):
        """Disable the restricted buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        todisable = [(self.reftrack.duplicate, self.duplicate_tb),
                     (self.reftrack.delete, self.delete_tb),
                     (self.reftrack.reference, self.reference_tb),
                     (self.reftrack.replace, self.replace_tb),]
        for action, btn in todisable:
            res = self.reftrack.is_restricted(action)
            btn.setDisabled(res)

    def hide_restricted(self, ):
        """Hide the restricted buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        tohide = [((self.reftrack.unload, self.unload_tb),
                   (self.reftrack.load, self.load_tb)),
                  ((self.reftrack.import_file, self.importtf_tb),
                   (self.reftrack.import_reference, self.importref_tb))]
        for (action1, btn1), (action2, btn2) in tohide:
            res1 = self.reftrack.is_restricted(action1)
            res2 = self.reftrack.is_restricted(action2)
            if res1 != res2:
                btn1.setEnabled(True)
                btn1.setHidden(res1)
                btn2.setHidden(res2)
            else:  # both are restricted, then show one but disable it
                btn1.setDisabled(True)
                btn1.setVisible(True)
                btn2.setVisible(False)

    def set_top_bar_color(self, index):
        """Set the color of the upper frame to the background color of the reftrack status

        :param index: the index
        :type index: :class:`QtGui.QModelIndex`
        :returns: None
        :rtype: None
        :raises: None
        """
        dr = QtCore.Qt.ForegroundRole
        c = index.model().index(index.row(), 8, index.parent()).data(dr)
        if not c:
            c = self.upper_fr_default_bg_color
        self.upper_fr.setStyleSheet('background-color: rgb(%s, %s, %s)' % (c.red(), c.green(), c.blue()))

    def set_status_buttons(self, ):
        """Depending on the status of the reftrack, enable or disable
        the status buttons, for imported/alien status buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        imported = self.reftrack.status() == self.reftrack.IMPORTED
        alien = self.reftrack.alien()

        for btn, enable in [(self.imported_tb, imported),
                            (self.alien_tb, alien)]:
            btn.setEnabled(enable)
            btn.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

    def toggle_tbstyle(self, button):
        """Toogle the ToolButtonStyle of the given button between :data:`ToolButtonIconOnly` and :data:`ToolButtonTextBesideIcon`

        :param button: a tool button
        :type button: :class:`QtGui.QToolButton`
        :returns: None
        :rtype: None
        :raises: None
        """
        old = button.toolButtonStyle()
        if old == QtCore.Qt.ToolButtonIconOnly:
            new = QtCore.Qt.ToolButtonTextBesideIcon
        else:
            new = QtCore.Qt.ToolButtonIconOnly
        button.setToolButtonStyle(new)

    def set_menu(self, ):
        """Setup the menu that the menu_tb button uses

        :returns: None
        :rtype: None
        :raises: None
        """
        self.menu = QtGui.QMenu(self)
        actions = self.reftrack.get_additional_actions()
        self.actions = []
        for a in actions:
            if a.icon:
                qaction = QtGui.QAction(a.icon, a.name, self)
            else:
                qaction = QtGui.QAction(a.name, self)
            qaction.setCheckable(a.checkable)
            qaction.setChecked(a.checked)
            qaction.setEnabled(a.enabled)
            qaction.triggered.connect(a.action)
            self.actions.append(qaction)
            self.menu.addAction(qaction)
        self.menu_tb.setMenu(self.menu)

    def get_taskfileinfo_selection(self, ):
        """Return a taskfileinfo that the user chose from the available options

        :returns: the chosen taskfileinfo
        :rtype: :class:`jukeboxcore.filesys.TaskFileInfo`
        :raises: None
        """
        sel = OptionSelector(self.reftrack)
        sel.exec_()
        return sel.selected

    def duplicate(self, ):
        """Duplicate the current reftrack

        :returns: None
        :rtype: None
        :raises: None
        """
        self.reftrack.duplicate()

    def delete(self, ):
        """Delete the current reftrack

        :returns: None
        :rtype: None
        :raises: None
        """
        self.reftrack.delete()

    def load(self):
        """Load the current reftrack

        :returns: None
        :rtype: None
        :raises: None
        """
        self.reftrack.load()

    def unload(self, ):
        """Unload the current reftrack

        :returns: None
        :rtype: None
        :raises: None
        """
        self.reftrack.unload()

    def reference(self, ):
        """Reference a file

        :returns: None
        :rtype: None
        :raises: None
        """
        tfi = self.get_taskfileinfo_selection()
        if tfi:
            self.reftrack.reference(tfi)

    def import_file(self, ):
        """Import a file

        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        tfi = self.get_taskfileinfo_selection()
        if tfi:
            self.reftrack.import_file(tfi)

    def import_reference(self, ):
        """Import the referenec of the current reftrack

        :returns: None
        :rtype: None
        :raises: None
        """
        self.reftrack.import_reference()

    def replace(self, ):
        """Replace the current reftrack

        :returns: None
        :rtype: None
        :raises: None
        """
        tfi = self.get_taskfileinfo_selection()
        if tfi:
            self.reftrack.replace(tfi)


class ReftrackDelegate(WidgetDelegate):
    """A delegate for drawing a :class:`jukeboxcore.gui.reftrackitemdata.ReftrackItemData`
    """

    def __init__(self, parent=None):
        """Initialize a new ReftrackDelegate

        :param parent:
        :type parent:
        :raises: None
        """
        super(ReftrackDelegate, self).__init__(parent)

    def create_widget(self, parent=None):
        """Return a widget that should get painted by the delegate

        You might want to use this in :meth:`WidgetDelegate.createEditor`

        :returns: The created widget | None
        :rtype: QtGui.QWidget | None
        :raises: None
        """
        return ReftrackWidget(parent)

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
        :returns: None
        :rtype: None
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
