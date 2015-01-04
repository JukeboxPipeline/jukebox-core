from PySide import QtGui, QtCore

from jukeboxcore.gui.widgets.reftrackwidget_ui import Ui_ReftrackWidget
from jukeboxcore.gui.Widgets.optionselector_ui import Ui_OptionSelector
from jukeboxcore.gui.widgets.browser import ComboBoxBrowser
from jukeboxcore.gui.widgetdelegate import WidgetDelegate
from jukeboxcore.gui.main import JB_Dialog


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
        i = s.internalPointer()
        if i:
            d = i.internal_data()
            tfi = d.internal_data()
            self.selected = tfi
            self.accept()


class ReftrackWidget(Ui_ReftrackWidget, QtGui.QWidget):
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
        self.item = None
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self, ):
        """Setup the ui

        :returns: None
        :rtype: None
        :raises: None
        """
        self.setup_icons

    def setup_icons(self, ):
        """Setup the icons of the ui

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

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

    def set_index(self, index):
        """Display the data of the given index

        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self.item = index.internalPointer()
        self.reftrack = self.item.internal_data()
        self.set_maintext(self.item)
        self.set_type_icon(self.item)
        self.hide_restricted()

    def set_maintext(self, item):
        """Set the maintext_lb to display text information about the given reftrack

        :param item: the item to represent
        :type item: :class:`jukeboxcore.gui.treemodel.TreeItem`
        :returns: None
        :rtype: None
        :raises: None
        """
        dr = QtCore.Qt.DisplayRole
        text = ""
        for i in (1, 2, 3, 5):
            new = item.data(i, dr)
            if new is not None:
                text = " | ".join((text, new)) if text else new

    def set_type_icon(self, item):
        """Set the type icon on type_icon_lb

        :param item: the item to represent
        :type item: :class:`jukeboxcore.gui.treemodel.TreeItem`
        :returns: None
        :rtype: None
        :raises: None
        """
        icon = item.data(0, QtCore.Qt.DecorationRole)
        if icon:
            pix = icon.pixmap(self.type_icon_lb.size())
            self.type_icon_lb.setPixmap(pix)
        else:
            self.type_icon_lb.setPixmap(None)

    def hide_restricted(self, ):
        """Hide the restricted buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        dupres = self.reftrack.is_restricted(self.reftrack.duplicate)
        self.duplicate_tb.setVisible(not dupres)
        delres = self.reftrack.is_restricted(self.reftrack.delete)
        self.delete_tb.setVisible(not delres)
        refres = self.reftrack.is_restricted(self.reftrack.reference)
        self.reference_tb.setVisible(not refres)
        loadres = self.reftrack.is_restricted(self.reftrack.load)
        self.load_tb.setVisible(not loadres)
        unloadres = self.reftrack.is_restricted(self.reftrack.unload)
        self.unload_tb.setVisible(not unloadres)
        ifres = self.reftrack.is_restricted(self.reftrack.import_file)
        self.importtf_tb.setVisible(not ifres)
        irefres = self.reftrack.is_restricted(self.reftrack.import_reference)
        self.importref_tb.setVisible(not irefres)
        repres = self.reftrack.is_restricted(self.reftrack.replace)
        self.replace_tb.setVisible(not repres)

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
        :raises: NotImplementedError
        """
        sel = OptionSelector(self.reftrack)
        sel.exec_()
        tfi = sel.selected
        if o:
            self.reftrack.reference(tfi)

    def import_file(self, ):
        """Import a file

        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        sel = OptionSelector(self.reftrack)
        sel.exec_()
        tfi = sel.selected
        if o:
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
        :raises: NotImplementedError
        """
        raise NotImplementedError


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
