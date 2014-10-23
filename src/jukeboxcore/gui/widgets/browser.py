from functools import partial

from PySide import QtCore, QtGui

from jukeboxcore.gui.widgetdelegate import CommentDelegate


class AbstractLevel(object):
    """Mixin for QtGui.QWidget for a level of a browser

    A level is a widget that should display data of a specific root index
    of its model. So it can be just a regular view, but it can also be a combobox.
    It can also emit a signal to state that the level below this one should have a new
    root index. You are free to emit the signal in whatever case you want.

    When subclassing implement :meth:`AbstractLevel.model_changed`, :meth:`AbstractLevel.set_root`, :meth:`AbstractLevel.selected_indexes`.
    """

    new_root = QtCore.Signal(QtCore.QModelIndex)
    """This signal says that the level under this one
    should update its root index to the one of the signal.
    """

    def __init__(self, *args, **kwargs):
        """Constructs a new level. All arguments will be passed on.

        :raises: None
        """
        super(AbstractLevel, self).__init__(*args, **kwargs)
        self._model = None

    def set_model(self, m):
        """Set the model for the level

        :param m: the model that the level should use
        :type m: QtCore.QAbstractItemModel
        :returns: None
        :rtype: None
        :raises: None
        """
        self._model = m
        self.new_root.emit(QtCore.QModelIndex())
        self.model_changed(m)

    def get_model(self, ):
        """Return the model that the level uses

        :returns: the model
        :rtype: QtCore.QAbstractItemModel|None
        :raises: None
        """
        return self._model

    def model_changed(self, model):
        """Abstract method that should handle the case that someone set the model

        When a level instance is created, the model is None. So it has to be set afterwards.
        Then this method will be called and your level should somehow use the model

        :param model: the model that the level should use | None
        :type model: QtCore.QAbstractItemModel
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def set_root(self, index):
        """Abstract method that should make the level use the given index as root

        The index might also be invalid! In that case show an empty level.
        The index might also be from a different model. In that case change the
        model of the level::

          if self.get_model() != index.model():
              self.set_model(index.model())

        :param index: the new root index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def selected_indexes(self, ):
        """Abstract method that should return the \"selected\" indexes.

        Selected does not mean, selected like Qt refers to the term. It just means
        that this level has some indexes that seam to be of importance right now.
        E.g. your level is a combobox, then the selected indexes would just consit of the
        current index. If your level is a regular view, then you could indeed return the selected
        indexes.

        :returns: the \'selected\' indexes of the level
        :rtype: list of QtCore.QModelIndex
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def set_index(self, index):
        """Set the current index of the level to the given one

        The given index should be the new root for levels below.
        You should make sure that the new_root signal will be emitted.

        :param index: the new index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError


class AbstractTreeBrowser(QtGui.QWidget):
    """A abstract class for a treebrowser

    A tree browser can be compared to a column view.
    The browser uses a tree model and on initialisation
    creates levels up to a certain depth.
    Each level displays on level of hierarchy of the model.

    When subclassing implement :meth:`AbstractTreeBrowser.create_level`,
    :meth:`AbstractTreeBrowser.add_lvl_to_ui`, :meth:`AbstractTreeBrowser.create_level`
    and for headers reimplement :meth:`AbstractTreeBrowser.create_header`
    """

    def __init__(self, depth, parent=None, flags=0):
        """Constructs an AbstractTreeBrowser

        :param depth: the depth of the browser
        :type depth: int
        :param parent: the parent of the widget
        :type parent: QtGui.QWidget
        :param flags: the flags for the widget
        :type flags: QtCore.Qt.WindowFlags
        :raises: None
        """
        super(AbstractTreeBrowser, self).__init__(parent, flags)
        self._depth = depth
        self._levels = []
        self.model = None

    def build_browser(self, ):
        """Creates all levels and adds them to the ui

        :returns: None
        :rtype: None
        :raises: None
        """
        for i in range(self._depth):
            self._new_level(i)

    def create_level(self, depth):
        """Create and return a level for the given depth

        The model and root of the level will be automatically set by the browser.

        :param depth: the depth level that the level should handle
        :type depth: int
        :returns: a new level for the given depth
        :rtype: :class:`jukeboxcore.gui.widgets.browser.AbstractLevel`
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def create_header(self, depth):
        """Create and return a widget that will be used as a header for the given depth

        Override this method if you want to have header widgets.
        The default implementation returns None.
        You can return None if you do not want a header for the given depth

        :param depth: the depth level
        :type depth: int
        :returns: a Widget that is used for the header or None
        :rtype: QtGui.QWidget|None
        :raises: None
        """
        return None

    def add_lvl_to_ui(self, level, header):
        """Abstract method that is responsible for inserting the level and header
        into the ui.

        :param level: a newly created level
        :type level: :class:`jukeboxcore.gui.widgets.browser.AbstractLevel`
        :param header: a newly created header
        :type header: QtCore.QWidget|None
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def set_model(self, model):
        """Set all levels\' model to the given one

        :param m: the model that the levels should use
        :type m: QtCore.QAbstractItemModel
        :returns: None
        :rtype: None
        :raises: None
        """
        # do the set model in reverse!
        # set model might trigger an update for the lower levels
        # but the lower ones have a different model, so it will fail anyways
        # this way the initial state after set_model is correct.
        self.model = model
        self._levels[0].set_model(model)

    def set_root(self, depth, index):
        """Set the level\'s root of the given depth to index

        :param depth: the depth level
        :type depth: int
        :param index: the new root index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        if depth < len(self._levels):
            self._levels[depth].set_root(index)

    def _new_level(self, depth):
        """Create a new level and header and connect signals

        :param depth: the depth level
        :type depth: int
        :returns: None
        :rtype: None
        :raises: None
        """
        l = self.create_level(depth)
        h = self.create_header(depth)
        self.add_lvl_to_ui(l, h)
        l.new_root.connect(partial(self.set_root, depth+1))
        self._levels.append(l)

    def get_level(self, depth):
        """Return the level for the given depth

        :param depth: the hierarchy level
        :type depth: int
        :returns: the level widget
        :rtype: :class:`AbstractLevel`
        :raises: None
        """
        return self._levels[depth]

    def get_depth(self, ):
        """Return the current depth of the browser

        :returns: the hierarchy depth of the browser
        :rtype: int
        :raises: None
        """
        return self._depth

    def selected_indexes(self, depth):
        """Get the selected indexes of a certain depth level

        :param depth: the depth level
        :type depth: int
        :returns: the selected indexes of the given depth level
        :rtype: list of QtCore.QModelIndex
        :raises: None
        """
        return self._levels[depth].selected_indexes()

    def set_index(self, depth, index):
        """Set the level at the given depth to the given index

        :param depth: addresses the level at the given depth
        :type depth: int
        :param index: the index to set the level to
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self._levels[depth].set_index(index)


class CBLevel(AbstractLevel, QtGui.QComboBox):
    """A level that consists of a simple combobox to be used in a TreeBrowser
    """

    def __init__(self, parent=None):
        """Constructs a new cblevel with the given parent

        :param parent: the parent widget
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(CBLevel, self).__init__(parent)
        self.currentIndexChanged.connect(self.current_changed)

    def model_changed(self, model):
        """Apply the model to the combobox

        When a level instance is created, the model is None. So it has to be set afterwards.
        Then this method will be called and your level should somehow use the model

        :param model: the model that the level should use
        :type model: QtCore.QAbstractItemModel
        :returns: None
        :rtype: None
        :raises: None
        """
        self.setModel(model)

    def set_root(self, index):
        """Set the given index as root index of the combobox

        :param index: the new root index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        if not index.isValid():
            self.setCurrentIndex(-1)
            return
        if self.model() != index.model():
            self.setModel(index.model())
        self.setRootModelIndex(index)
        if self.model().rowCount(index):
            self.setCurrentIndex(0)
        else:
            self.setCurrentIndex(-1)

    def selected_indexes(self, ):
        """Return the current index

        :returns: the current index in a list
        :rtype: list of QtCore.QModelIndex
        :raises: None
        """
        i = self.model().index(self.currentIndex(), 0, self.rootModelIndex())
        return [i]

    def current_changed(self, i):
        """Slot for when the current index changes.
        Emits the :data:`AbstractLevel.new_root` signal.

        :param index: the new current index
        :type index: int
        :returns: None
        :rtype: None
        :raises: None
        """
        m = self.model()
        ri = self.rootModelIndex()
        index = m.index(i, 0, ri)
        self.new_root.emit(index)

    def set_index(self, index):
        """Set the current index to the row of the given index

        :param index: the index to set the level to
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self.setCurrentIndex(index.row())


class ComboBoxBrowser(AbstractTreeBrowser):
    """A tree browser that has a combo box for every level
    and a label for every header.
    The header labels will be next to each combobox.
    """

    def __init__(self, depth, parent=None, flags=0, headers=None):
        """Constructs a new ComboBoxBrowser with the given depth

        :param depth: the depth of the browser
        :type depth: int
        :param parent: the parent of the widget
        :type parent: QtGui.QWidget
        :param flags: the flags for the widget
        :type flags: QtCore.Qt.WindowFlags
        :param headers: a list of label texts to put for the labels next to the comboboxes
                        the list does not need to have the length of ``depth``.
                        If the list is None, no headers will be created.
        :type headers: list of str|None
        :raises: None
        """
        super(ComboBoxBrowser, self).__init__(depth, parent, flags)
        self._headertexts = headers
        self.setup_ui()
        self.build_browser()

    def setup_ui(self, ):
        """Create the layouts and set some attributes of the ui

        :returns: None
        :rtype: None
        :raises: None
        """
        grid = QtGui.QGridLayout(self)
        grid.setContentsMargins(0, 0, 0, 0)
        self.setLayout(grid)

    def create_level(self, depth):
        """Create and return a level for the given depth

        The model and root of the level will be automatically set by the browser.

        :param depth: the depth level that the level should handle
        :type depth: int
        :returns: a new level for the given depth
        :rtype: :class:`CBLevel`
        :raises: None
        """
        cb = CBLevel(parent=self)
        return cb

    def create_header(self, depth):
        """Create and return a widget that will be used as a header for the given depth

        Override this method if you want to have header widgets.
        The default implementation returns None.
        You can return None if you do not want a header for the given depth

        :param depth: the depth level
        :type depth: int
        :returns: a Widget that is used for the header or None
        :rtype: QtGui.QWidget|None
        :raises: None
        """
        if not (depth >= 0 and depth < len(self._headertexts)):
            return
        txt = self._headertexts[depth]
        if txt is None:
            return
        lbl = QtGui.QLabel(txt, self)
        return lbl

    def add_lvl_to_ui(self, level, header):
        """Insert the level and header into the ui.

        :param level: a newly created level
        :type level: :class:`jukeboxcore.gui.widgets.browser.AbstractLevel`
        :param header: a newly created header
        :type header: QtCore.QWidget|None
        :returns: None
        :rtype: None
        :raises: None
        """
        lay = self.layout()
        rc = lay.rowCount()
        lay.addWidget(level, rc+1, 1)
        if header is not None:
            lay.addWidget(header, rc+1, 0)
        lay.setColumnStretch(1,1)


class ListLevel(AbstractLevel, QtGui.QListView):
    """A level that consists of a listview to be used in a TreeBrowser
    """

    def __init__(self, parent=None):
        """Constructs a new listlevel with the given parent

        :param parent: the parent widget
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(ListLevel, self).__init__(parent)

    def model_changed(self, model):
        """Apply the model to the combobox

        When a level instance is created, the model is None. So it has to be set afterwards.
        Then this method will be called and your level should somehow use the model

        :param model: the model that the level should use
        :type model: QtCore.QAbstractItemModel
        :returns: None
        :rtype: None
        :raises: None
        """
        self.setModel(model)
        # to update all lists belwo
        # current changed is not triggered by setModel somehow
        if model is not None:
            self.setCurrentIndex(self.model().index(0, 0))

    def set_root(self, index):
        """Set the given index as root index of list

        :param index: the new root index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        if not index.isValid():
            self.setModel(None) # so we will not see toplevel stuff
            self.setCurrentIndex(QtCore.QModelIndex())
            self.new_root.emit(QtCore.QModelIndex())
            return
        if self.model() != index.model():
            self.setModel(index.model())
        self.setRootIndex(index)
        if self.model().hasChildren(index):
            self.setCurrentIndex(self.model().index(0, 0, index))
            self.new_root.emit(self.model().index(0, 0, index))
        else:
            self.new_root.emit(QtCore.QModelIndex())

    def selected_indexes(self, ):
        """Return the current index

        :returns: the current index in a list
        :rtype: list of QtCore.QModelIndex
        :raises: None
        """
        return [self.currentIndex()]

    def currentChanged(self, current, prev):
        """Slot for when the current index changes.
        Emits the :data:`AbstractLevel.new_root` signal.

        :param current: the new current index
        :type current: QtGui.QModelIndex
        :param current: the previous current index
        :type current: QtGui.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        m = self.model()
        p = current.parent()
        index = m.index(current.row(), 0, p)
        self.new_root.emit(index)
        return super(ListLevel, self).currentChanged(current, prev)

    def set_index(self, index):
        """Set the current index to the row of the given index

        :param index: the index to set the level to
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self.setCurrentIndex(index)
        self.new_root.emit(index)
        self.scrollTo(index)

    def resizeEvent(self, event):
        """Schedules an item layout if resize mode is \"adjust\". Somehow this is
        needed for correctly scaling down items.

        The reason this was reimplemented was the CommentDelegate.

        :param event: the resize event
        :type event: QtCore.QEvent
        :returns: None
        :rtype: None
        :raises: None
        """
        if self.resizeMode() == self.Adjust:
            self.scheduleDelayedItemsLayout()
        return super(ListLevel, self).resizeEvent(event)


class ListBrowser(AbstractTreeBrowser):
    """A tree browser that has a list view for every level
    and a label for every header.
    The header labels will be above each list.
    """

    def __init__(self, depth, parent=None, flags=0, headers=None):
        """Constructs a new ListBrowser with the given depth

        :param depth: the depth of the browser
        :type depth: int
        :param parent: the parent of the widget
        :type parent: QtGui.QWidget
        :param flags: the flags for the widget
        :type flags: QtCore.Qt.WindowFlags
        :param headers: a list of label texts to put for the labels above the lists
                        the list does not need to have the length of ``depth``.
                        If the list is None or an element is None, no headers will be created.
        :type headers: list of str|None
        :raises: None
        """
        super(ListBrowser, self).__init__(depth, parent, flags)
        self._headertexts = headers
        self.setup_ui()
        self.build_browser()

    def setup_ui(self, ):
        """Create the layouts and set some attributes of the ui

        :returns: None
        :rtype: None
        :raises: None
        """
        grid = QtGui.QGridLayout(self)
        self.setLayout(grid)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal, self)
        grid.addWidget(self.splitter)
        grid.setContentsMargins(0, 0, 0, 0)

    def create_level(self, depth):
        """Create and return a level for the given depth

        The model and root of the level will be automatically set by the browser.

        :param depth: the depth level that the level should handle
        :type depth: int
        :returns: a new level for the given depth
        :rtype: :class:`jukeboxcore.gui.widgets.browser.AbstractLevel`
        :raises: None
        """
        ll = ListLevel(parent=self)
        return ll

    def create_header(self, depth):
        """Create and return a widget that will be used as a header for the given depth

        Override this method if you want to have header widgets.
        The default implementation returns None.
        You can return None if you do not want a header for the given depth

        :param depth: the depth level
        :type depth: int
        :returns: a Widget that is used for the header or None
        :rtype: QtGui.QWidget|None
        :raises: None
        """
        if not (depth >= 0 and depth < len(self._headertexts)):
            return
        txt = self._headertexts[depth]
        if txt is None:
            return
        lbl = QtGui.QLabel(txt, self)
        return lbl

    def add_lvl_to_ui(self, level, header):
        """Insert the level and header into the ui.

        :param level: a newly created level
        :type level: :class:`jukeboxcore.gui.widgets.browser.AbstractLevel`
        :param header: a newly created header
        :type header: QtCore.QWidget|None
        :returns: None
        :rtype: None
        :raises: None
        """
        w = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        w.setLayout(vbox)
        if header is not None:
            vbox.addWidget(header)
        vbox.addWidget(level)
        self.splitter.addWidget(w)


class CommentBrowser(ListBrowser):
    """A list browser that has a list view for every level
    and a label for every header.
    The header labels will be above each list.
    The lists are designed to display :class:`jukeboxcore.gui.djitemdata.NoteItemData`.
    """

    def create_level(self, depth):
        """Create and return a level for the given depth

        The model and root of the level will be automatically set by the browser.

        :param depth: the depth level that the level should handle
        :type depth: int
        :returns: a new level for the given depth
        :rtype: :class:`jukeboxcore.gui.widgets.browser.AbstractLevel`
        :raises: None
        """
        ll = ListLevel(parent=self)
        ll.setEditTriggers(ll.DoubleClicked | ll.SelectedClicked | ll.CurrentChanged)
        #ll.setSelectionBehavior(ll.SelectRows)
        ll.setResizeMode(ll.Adjust)
        self.delegate = CommentDelegate(ll)
        ll.setItemDelegate(self.delegate)
        ll.setVerticalScrollMode(ll.ScrollPerPixel)
        return ll
