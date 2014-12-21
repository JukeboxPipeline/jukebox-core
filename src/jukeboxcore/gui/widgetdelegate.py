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


class MouseEditMixin(object):
    """Mixin for views to allow editing with mouseclicks,
    if there is a widgetdelegate.

    On a mouse click event, try to edit the index at click position.
    Then take the editor widget and issue the same click on that widget.
    """

    def index_at_event(self, event):
        """Get the index under the position of the given MouseEvent

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: the index
        :rtype: :class:`QtCore.QModelIndex`
        :raises: None
        """
        # find index at mouse position
        globalpos = event.globalPos()
        viewport = self.viewport()
        pos = viewport.mapFromGlobal(globalpos)
        return self.indexAt(pos)

    def get_pos_in_delegate(self, index, globalpos):
        """Map the global position to the position relative to the
        given index

        :param index: the index to map to
        :type index: :class:`QtCore.QModelIndex`
        :param globalpos: the global position
        :type globalpos: :class:`QtCore.QPoint`
        :returns: The position relative to the given index
        :rtype: :class:`QtCore.QPoint`
        :raises: None
        """
        rect = self.visualRect(index)  # rect of the index
        p = self.viewport().mapToGlobal(rect.topLeft())
        return globalpos - p

    def propagate_event_to_delegate(self, event, eventhandler):
        """Propagate the given Mouse event to the widgetdelegate

        Enter edit mode, get the editor widget and issue an event on that widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :param eventhandler: the eventhandler to use. E.g. ``"mousePressEvent"``
        :type eventhandler: str
        :returns: None
        :rtype: None
        :raises: None
        """
        # find index at mouse position
        i = self.index_at_event(event)

        # if the index is not valid, we don't care
        # handle it the default way
        if not i.isValid():
            return getattr(super(MouseEditMixin, self), eventhandler)(event)
        # get the widget delegate. if there is None, handle it the default way
        delegate = self.itemDelegate(i)
        if not isinstance(delegate, WidgetDelegate):
            return getattr(super(MouseEditMixin, self), eventhandler)(event)

        # if we are not editing, start editing now
        if self.state() != self.EditingState:
            self.edit(i)
            # check if we are in edit state now. if not, return
            if self.state() != self.EditingState:
                return

        # get the editor widget. if there is None, there is nothing to do so return
        widget = delegate.edit_widget()
        if not widget:
            return getattr(super(MouseEditMixin, self), eventhandler)(event)

        # try to find the relative position to the widget
        clickpos = self.get_pos_in_delegate(i, event.globalPos())

        # create a new event for the editor widget.
        e = QtGui.QMouseEvent(event.type(),
                              clickpos,
                              event.button(),
                              event.buttons(),
                              event.modifiers())
        getattr(widget, eventhandler)(e)
        # make sure to accept the event. If the widget does not accept the event
        # it would be propagated to the view, and we would end in a recursion.
        e.accept()

    def mouseDoubleClickEvent(self, event):
        """If a widgetdelegate is double clicked,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        return self.propagate_event_to_delegate(event, "mouseDoubleClickEvent")

    def mousePressEvent(self, event):
        """If the mouse is presses on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        return self.propagate_event_to_delegate(event, "mousePressEvent")

    def mouseReleaseEvent(self, event):
        """If the mouse is released on a widgetdelegate,
        enter edit mode and propagate the event to the editor widget.

        :param event: the mouse event
        :type event: :class:`QtGui.QMouseEvent`
        :returns: None
        :rtype: None
        :raises: None
        """
        return self.propagate_event_to_delegate(event, "mouseReleaseEvent")


class WD_AbstractItemView(QtGui.QAbstractItemView, MouseEditMixin):
    """A abstract item view that that when clicked, tries to issue
    a left click to the widget delegate.
    """
    pass


class WD_ListView(QtGui.QListView, MouseEditMixin):
    """A list view that that when clicked, tries to issue
    a left click to the widget delegate.
    """
    pass


class WD_TableView(QtGui.QTableView, MouseEditMixin):
    """A table view that that when clicked, tries to issue
    a left click to the widget delegate.
    """
    pass


class WD_TreeView(QtGui.QTreeView, MouseEditMixin):
    """A tree view that that when clicked, tries to issue
    a left click to the widget delegate.
    """
    pass
