from PySide import QtCore, QtGui

from jukeboxcore.gui.widgets.commentwidget import CommentWidget


class WidgetDelegate(QtGui.QStyledItemDelegate):
    """A delegate for drawing a arbitrary QWidget

    When subclassing, reimplement set_widget_index, create_widget, create_editor_widget, setEditorData, setModelData
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
        self._edit_widget = None

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

        You might want to use this in :meth:`WidgetDelegate.create_editor_widget`

        :param parent: the parent widget
        :type parent: :class:`QtGui.QWidget` | None
        :returns: The created widget | None
        :rtype: :class:`QtGui.QWidget` | None
        :raises: None
        """
        return None

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
        :returns: The created widget | None
        :rtype: :class:`QtGui.QWidget` | None
        :raises: None
        """
        self._edit_widget = self.create_editor_widget(parent, option, index)
        if self._edit_widget:
            self._edit_widget.destroyed.connect(self.editor_destroyed)
        return self._edit_widget

    def create_editor_widget(self, parent, option, index):
        """Return a editor widget for the given index.

        :param parent: the parent widget
        :type parent: QtGui.QWidget
        :param option: the options for painting
        :type option: QtGui.QStyleOptionViewItem
        :param index: the index to paint
        :type index: QtCore.QModelIndex
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
        self._edit_widget = None

    def edit_widget(self, ):
        """Return the current edit widget if there is one

        :returns: The editor widget | None
        :rtype: :class:`QtGui.QWidget` | None
        :raises: None
        """
        return self._edit_widget

    def editor_destroyed(self, *args, **kwargs):
        """Callback for when the editor widget gets destroyed. Set edit_widget to None

        :returns: None
        :rtype: None
        :raises: None
        """
        self._edit_widget = None


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


class WD_AbstractItemView(QtGui.QAbstractItemView):
    """A abstract item view that that when clicked, tries to issue
    a left click to the widget delegate.
    """

    def __init__(self, parent):
        """Initialize a new abstract item view

        :raises: None
        """
        super(WD_AbstractItemView, self).__init__(parent)

    def mouseDoubleClickEvent(self, event):
        """If a widgetdelegate is double clicked,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_AbstractItemView, self).mouseDoubleClickEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_AbstractItemView, self).mouseDoubleClickEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_AbstractItemView, self).mouseDoubleClickEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mouseDoubleClickEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mousePressEvent(self, event):
        """If the mouse is presses on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_AbstractItemView, self).mousePressEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_AbstractItemView, self).mousePressEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_AbstractItemView, self).mousePressEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mousePressEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mouseReleaseEvent(self, event):
        """If the mouse is released on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_AbstractItemView, self).mouseReleaseEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_AbstractItemView, self).mouseReleaseEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_AbstractItemView, self).mouseReleaseEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mouseReleaseEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()


class WD_ListView(QtGui.QListView):
    """A list view that that when clicked, tries to issue
    a left click to the widget delegate.
    """

    def __init__(self, parent):
        """Initialize a new list view

        :raises: None
        """
        super(WD_ListView, self).__init__(parent)

    def mouseDoubleClickEvent(self, event):
        """If a widgetdelegate is double clicked,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_ListView, self).mouseDoubleClickEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_ListView, self).mouseDoubleClickEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_ListView, self).mouseDoubleClickEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mouseDoubleClickEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mousePressEvent(self, event):
        """If the mouse is presses on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_ListView, self).mousePressEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_ListView, self).mousePressEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_ListView, self).mousePressEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mousePressEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mouseReleaseEvent(self, event):
        """If the mouse is released on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_ListView, self).mouseReleaseEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_ListView, self).mouseReleaseEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_ListView, self).mouseReleaseEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mouseReleaseEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()


class WD_TableView(QtGui.QTableView):
    """A table view that that when clicked, tries to issue
    a left click to the widget delegate.
    """

    def __init__(self, parent):
        """Initialize a new table view

        :raises: None
        """
        super(WD_TableView, self).__init__(parent)

    def mouseDoubleClickEvent(self, event):
        """If a widgetdelegate is double clicked,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_TableView, self).mouseDoubleClickEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_TableView, self).mouseDoubleClickEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_TableView, self).mouseDoubleClickEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mouseDoubleClickEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mousePressEvent(self, event):
        """If the mouse is presses on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_TableView, self).mousePressEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_TableView, self).mousePressEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_TableView, self).mousePressEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mousePressEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mouseReleaseEvent(self, event):
        """If the mouse is released on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_TableView, self).mouseReleaseEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_TableView, self).mouseReleaseEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_TableView, self).mouseReleaseEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mouseReleaseEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()


class WD_TreeView(QtGui.QTreeView):
    """A tree view that that when clicked, tries to issue
    a left click to the widget delegate.
    """

    def __init__(self, parent):
        """Initialize a new tree view

        :raises: None
        """
        super(WD_TableView, self).__init__(parent)

    def mouseDoubleClickEvent(self, event):
        """If a widgetdelegate is double clicked,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_TreeView, self).mouseDoubleClickEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_TreeView, self).mouseDoubleClickEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_TreeView, self).mouseDoubleClickEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mouseDoubleClickEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mousePressEvent(self, event):
        """If the mouse is presses on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_TreeView, self).mousePressEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_TreeView, self).mousePressEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_TreeView, self).mousePressEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mousePressEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mouseReleaseEvent(self, event):
        """If the mouse is released on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        i = self.indexAt(pos)

        # if the index is not valid, we don't care
        if not i.isValid():
            return super(WD_TreeView, self).mouseReleaseEvent(event)
        # get the widget delegate. if there is None, return
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return super(WD_TreeView, self).mouseReleaseEvent(event)
        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return
        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return super(WD_TreeView, self).mouseReleaseEvent(event)

        # try to find the relative position to the widget
        rect = self.visualRect(i)  # rect of the index
        p = viewport.mapToGlobal(rect.topLeft())
        clickpos = globalpos - p
        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        widget.mouseReleaseEvent(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()
