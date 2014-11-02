from PySide import QtCore, QtGui

from jukeboxcore.gui.widgets.commentwidget import CommentWidget


class WidgetDelegate(QtGui.QStyledItemDelegate):
    """A delegate for drawing a arbitrary QWidget

    When subclassing, reimplement set_widget_index, create_widget, createEditor, setEditorData, setModelData
    to your liking.
    Make sure that the model returns the ItemIsEditable flag!
    I recommend using one of the views in this module, because they issue a left click, when
    an index is clicked.
    """

    def __init__(self, parent=None):
        """Create a new abstract widget delegate that draws the given widget.

        :param widget: the widget to draw. If None, it behaves like a :class:`QtGui.QStyledItemDelegate`
        :type widget: :class:`QtGui.QWidget` | None
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :raises: None
        """
        super(WidgetDelegate, self).__init__(parent)
        self._widget = self.create_widget(parent)
        self._widget.setVisible(False)

    @property
    def widget(self):
        """Return the widget that is used by the delegate for drawing

        :returns: widget
        :rtype: :class:`QtGui.QWidget`
        :raises: None
        """
        return self._widget

    def paint(self, painter, option, index):
        """Use the painter and style option to render the item specified by the item index.

        :param painter: the painter to paint
        :type painter: :class:`QtGui.QPainter`
        :param option: the options for painting
        :type option: :class:`QtGui.QStyleOptionViewItem`
        :param index: the index to paint
        :type index: :class:`QtCore.QModelIndex`
        :returns: None
        :rtype: None
        :raises: None
        """
        if self._widget is None:
            return super(WidgetDelegate, self).paint(painter, option, index)

        self.set_widget_index(index)
        painter.save()
        painter.translate(option.rect.topLeft())
        self._widget.resize(option.rect.size())
        self._widget.render(painter, QtCore.QPoint())
        painter.restore()

    def sizeHint(self, option, index):
        """Return the appropriate amount for the size of the widget

        The widget will always be expanded to at least the size of the viewport.

        :param option: the options for painting
        :type option: :class:`QtGui.QStyleOptionViewItem`
        :param index: the index to paint
        :type index: :class:`QtCore.QModelIndex`
        :returns: None
        :rtype: None
        :raises: None
        """
        if self._widget is None:
            return super(WidgetDelegate, self).sizeHint(option, index)

        self.set_widget_index(index)
        self._widget.resize(option.rect.size())
        sh = self._widget.sizeHint()
        return sh

    def set_widget_index(self, index):
        """Set the index for the widget. The widget should retrieve data from the index and display it.

        You might want use the same function as for :meth:`WidgetDelegate.setEditorData`.

        :param index: the index to paint
        :type index: :class:`QtCore.QModelIndex`
        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    def create_widget(self, parent=None):
        """Return a widget that should get painted by the delegate

        You might want to use this in :meth:`WidgetDelegate.createEditor`

        :param parent: the parent widget
        :type parent: :class:`QtGui.QWidget` | None
        :returns: The created widget | None
        :rtype: :class:`QtGui.QWidget` | None
        :raises: None
        """
        return None

    def commit_close_editor(self, editor, endedithint=QtGui.QAbstractItemDelegate.NoHint):
        """Commit and close the editor

        Call this method whenever the user finished editing.

        :param editor: The editor to close
        :type editor: :class:`QtGui.QWidget`
        :param endedithint: Hints that the delegate can give the model and view to make editing data comfortable for the user
        :type endedithint: :data:`QtGui.QAbstractItemDelegate.EndEditHint`
        :returns: None
        :rtype: None
        :raises: None
        """
        self.commitData.emit(editor)
        self.closeEditor.emit(editor, endedithint)


class CommentDelegate(WidgetDelegate):
    """A delegate for drawing a :class:`jukeboxcore.gui.djitemdata.NoteItemData`.
    """

    def __init__(self, parent=None):
        """

        :param parent: the parent object
        :type parent: QObject
        :raises: None
        """
        super(CommentDelegate, self).__init__(parent)

    def create_widget(self, parent=None):
        """Return a widget that should get painted by the delegate

        You might want to use this in :meth:`WidgetDelegate.createEditor`

        :returns: The created widget | None
        :rtype: QtGui.QWidget | None
        :raises: None
        """
        return CommentWidget(parent)

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


class WD_AbstractItemView(QtGui.QAbstractItemView):
    """A abstract item view that that when clicked, tries to issue
    a left click to the widget delegate.
    """

    def __init__(self, parent):
        """Initialize a new abstract item view

        :raises: None
        """
        super(WD_AbstractItemView, self).__init__(parent)
        self.clicked.connect(self.clicked_cb)

    def clicked_cb(self, index):
        """When the view is clicked, tries to edit the clicked index.
        If the clicked index has a widget delegate, then issue a left click on the widget.

        :param index: the clicked index
        :type index: :class:`QtCore.QModelIndex`
        :returns: None
        :raises: None
        """
        if self.state() == self.EditingState:
            return
        delegate = self.itemDelegate(index)
        if not isinstance(delegate, WidgetDelegate):
            return
        self.edit(index)
        widget = delegate.widget
        # try to find the relative position to the widget
        rect = self.visualRect(index)  # rect of the index
        p = self.viewport().mapToGlobal(rect.topLeft())
        pos = self.cursor().pos() - p

        # issue two mouse clicks because e.g. a button only will be activated
        # if it is pressed and released
        e1 = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                               pos,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.NoModifier)
        e2 = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease,
                               pos,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.NoModifier)
        QtCore.QCoreApplication.sendEvent(widget, e1)
        QtCore.QCoreApplication.sendEvent(widget, e2)


class WD_ListView(QtGui.QListView):
    """A list view that that when clicked, tries to issue
    a left click to the widget delegate.
    """

    def __init__(self, parent):
        """Initialize a new list view

        :raises: None
        """
        super(WD_ListView, self).__init__(parent)
        self.clicked.connect(self.clicked_cb)

    def clicked_cb(self, index):
        """When the view is clicked, tries to edit the clicked index.
        If the clicked index has a widget delegate, then issue a left click on the widget.

        :param index: the clicked index
        :type index: :class:`QtCore.QModelIndex`
        :returns: None
        :raises: None
        """
        if self.state() == self.EditingState:
            return
        delegate = self.itemDelegate(index)
        if not isinstance(delegate, WidgetDelegate):
            return
        self.edit(index)
        widget = delegate.widget
        # try to find the relative position to the widget
        rect = self.visualRect(index)  # rect of the index
        p = self.viewport().mapToGlobal(rect.topLeft())
        pos = self.cursor().pos() - p

        # issue two mouse clicks because e.g. a button only will be activated
        # if it is pressed and released
        e1 = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                               pos,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.NoModifier)
        e2 = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease,
                               pos,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.NoModifier)
        QtCore.QCoreApplication.sendEvent(widget, e1)
        QtCore.QCoreApplication.sendEvent(widget, e2)


class WD_TableView(QtGui.QTableView):
    """A table view that that when clicked, tries to issue
    a left click to the widget delegate.
    """

    def __init__(self, parent):
        """Initialize a new table view

        :raises: None
        """
        super(WD_TableView, self).__init__(parent)
        self.clicked.connect(self.clicked_cb)

    def clicked_cb(self, index):
        """When the view is clicked, tries to edit the clicked index.
        If the clicked index has a widget delegate, then issue a left click on the widget.

        :param index: the clicked index
        :type index: :class:`QtCore.QModelIndex`
        :returns: None
        :raises: None
        """
        if self.state() == self.EditingState:
            return
        delegate = self.itemDelegate(index)
        if not isinstance(delegate, WidgetDelegate):
            return
        self.edit(index)
        widget = delegate.widget
        # try to find the relative position to the widget
        rect = self.visualRect(index)  # rect of the index
        p = self.viewport().mapToGlobal(rect.topLeft())
        pos = self.cursor().pos() - p

        # issue two mouse clicks because e.g. a button only will be activated
        # if it is pressed and released
        e1 = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                               pos,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.NoModifier)
        e2 = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease,
                               pos,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.NoModifier)
        QtCore.QCoreApplication.sendEvent(widget, e1)
        QtCore.QCoreApplication.sendEvent(widget, e2)


class WD_TreeView(QtGui.QTreeView):
    """A tree view that that when clicked, tries to issue
    a left click to the widget delegate.
    """

    def __init__(self, parent):
        """Initialize a new tree view

        :raises: None
        """
        super(WD_TableView, self).__init__(parent)
        self.clicked.connect(self.clicked_cb)

    def clicked_cb(self, index):
        """When the view is clicked, tries to edit the clicked index.
        If the clicked index has a widget delegate, then issue a left click on the widget.

        :param index: the clicked index
        :type index: :class:`QtCore.QModelIndex`
        :returns: None
        :raises: None
        """
        if self.state() == self.EditingState:
            return
        delegate = self.itemDelegate(index)
        if not isinstance(delegate, WidgetDelegate):
            return
        self.edit(index)
        widget = delegate.widget
        # try to find the relative position to the widget
        rect = self.visualRect(index)  # rect of the index
        p = self.viewport().mapToGlobal(rect.topLeft())
        pos = self.cursor().pos() - p

        # issue two mouse clicks because e.g. a button only will be activated
        # if it is pressed and released
        e1 = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress,
                               pos,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.NoModifier)
        e2 = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease,
                               pos,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.LeftButton,
                               QtCore.Qt.NoModifier)
        QtCore.QCoreApplication.sendEvent(widget, e1)
        QtCore.QCoreApplication.sendEvent(widget, e2)
