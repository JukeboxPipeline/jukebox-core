"""A window that can be used for tools that handle the referene workflow."""

from PySide import QtGui
from PySide import QtCore

from jukeboxcore import reftrack
from jukeboxcore.gui.main import JB_MainWindow, get_icon
from jukeboxcore.gui.widgetdelegate import WD_TreeView
from jukeboxcore.gui.widgets.reftrackwidget import ReftrackDelegate
from jukeboxcore.gui.reftrackitemdata import ReftrackSortFilterModel
from reftrackwin_ui import Ui_reftrack_mwin


class ReftrackWin(JB_MainWindow, Ui_reftrack_mwin):
    """Display reftracks in a view that can be filtered, sorted etc.

    You can either add your own :class:`reftrack.Reftrack` objects to the root or
    call :meth:`ReftrackWin.wrap_scene`.
    """

    def __init__(self, refobjinter, root=None, parent=None, flags=0):
        """Initialize a new Reftrack window with the given refobjinter

        :param root: the reftrackroot, if None is given, a default one is created
        :type root: :class:`jukeboxcore.reftrack.ReftrackRoot`
        :param refobjinter: the refobjinterface to use
        :type refobjinter: :class:`reftrack.RefobjInterface`
        :param parent: Optional - the parent of the window - default is None
        :type parent: QWidget
        :param flags: the window flags
        :type flags: QtCore.Qt.WindowFlags
        :raises: None
        """
        super(ReftrackWin, self).__init__(parent, flags)
        self.refobjinter = refobjinter
        """The :class:`reftrack.RefobjInterface` this window uses."""
        self.root = root if root else self.create_root()
        """The :class:`reftrack.ReftrackRoot` this window uses."""
        self.reftrackdelegate = ReftrackDelegate(self)
        self.typecbmap = {}
        """Map a type to a checkboxes that indicates if the type should be shown"""

        self.setupUi(self)

        self.setup_ui()
        self.setup_filter()
        self.setup_signals()

    def create_root(self, ):
        """Create a default reftrack root.

        :returns: a reftrack root
        :rtype: :class:`reftrack.ReftrackRoot`
        :raises: None
        """
        return reftrack.ReftrackRoot()

    def setup_ui(self, ):
        """Setup the general ui

        :returns: None
        :rtype: None
        :raises: None
        """
        w = QtGui.QWidget(self)
        w.setLayout(self.central_widget_vbox)
        self.setCentralWidget(w)
        self.reftrack_treev = WD_TreeView(parent=self)
        self.central_widget_vbox.insertWidget(1, self.reftrack_treev)
        self.setup_icons()
        self.model = self.root.get_model()
        self.proxy = self.create_proxy_model(self.model)
        self.reftrack_treev.setModel(self.proxy)
        self.reftrack_treev.setItemDelegate(self.reftrackdelegate)
        # hide all columns but the first
        cc = self.proxy.columnCount(QtCore.QModelIndex())
        for i in range(1, cc):
            self.reftrack_treev.setColumnHidden(i, True)

    def create_proxy_model(self, model):
        """Create a sort filter proxy model for the given model

        :param model: the model to wrap in a proxy
        :type model: :class:`QtGui.QAbstractItemModel`
        :returns: a new proxy model that can be used for sorting and filtering
        :rtype: :class:`QtGui.QAbstractItemModel`
        :raises: None
        """
        proxy = ReftrackSortFilterModel(self)
        proxy.setSourceModel(model)
        model.rowsInserted.connect(self.sort_model)
        return proxy

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
        self.showfilter_tb.toggled.connect(self.switch_showfilter_icon)
        self.addnew_tb.clicked.connect(self.open_addnew_win)
        self.search_le.editingFinished.connect(self.update_filter)
        for cb in (self.loaded_checkb, self.unloaded_checkb, self.imported_checkb, self.empty_checkb,
                   self.newest_checkb, self.old_checkb, self.alien_checkb):
            cb.toggled.connect(self.update_filter)

    def setup_icons(self, ):
        """Set all icons on buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        plus_icon = get_icon('glyphicons_433_plus.png', asicon=True)
        self.addnew_tb.setIcon(plus_icon)

    def setup_filter(self, ):
        """Create a checkbox for every reftrack type so one can filter them

        :returns: None
        :rtype: None
        :raises: None
        """
        types = self.refobjinter.types.keys()
        for i, t in enumerate(types):
            cb = QtGui.QCheckBox("%s" % t)
            cb.setChecked(True)
            cb.toggled.connect(self.update_filter)
            self.typecbmap[t] = cb
            self.typefilter_grid.addWidget(cb, int(i / 4), i % 4)

    def switch_showfilter_icon(self, toggled):
        """Switch the icon on the showfilter_tb

        :param toggled: the state of the button
        :type toggled: :class:`bool`
        :returns: None
        :rtype: None
        :raises: None
        """
        at = QtCore.Qt.DownArrow if toggled else QtCore.Qt.RightArrow
        self.showfilter_tb.setArrowType(at)

    def open_addnew_win(self, *args, **kwargs):
        """Open a new window so the use can choose to add new reftracks

        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def update_filter(self, *args, **kwargs):
        """Update the filter

        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        forbidden_statuses = []
        if not self.loaded_checkb.isChecked():
            forbidden_statuses.append(reftrack.Reftrack.LOADED)
        if not self.unloaded_checkb.isChecked():
            forbidden_statuses.append(reftrack.Reftrack.UNLOADED)
        if not self.imported_checkb.isChecked():
            forbidden_statuses.append(reftrack.Reftrack.IMPORTED)
        if not self.empty_checkb.isChecked():
            forbidden_statuses.append(None)
        self.proxy.set_forbidden_statuses(forbidden_statuses)

        forbidden_types = []
        for typ, cb in self.typecbmap.items():
            if not cb.isChecked():
                forbidden_types.append(typ)
        self.proxy.set_forbidden_types(forbidden_types)

        forbidden_uptodate = []
        if not self.old_checkb.isChecked():
            forbidden_uptodate.append(False)
        if not self.newest_checkb.isChecked():
            forbidden_uptodate.append(True)
        self.proxy.set_forbidden_uptodate(forbidden_uptodate)

        forbidden_alien = [] if self.alien_checkb.isChecked() else [True]
        self.proxy.set_forbidden_alien(forbidden_alien)

    def sort_model(self, *args, **kwargs):
        """Sort the proxy model

        :returns: None
        :rtype: None
        :raises: None
        """
        self.proxy.sort(17)  # sort the identifier
        self.proxy.sort(2)  # sort the element
        self.proxy.sort(1)  # sort the elementgrp
        self.proxy.sort(0)  # sort the types

    def wrap_scene(self, ):
        """Wrap all reftracks in the scenen and get suggestions and display it in the view

        :returns: None
        :rtype: None
        :raises: None
        """
        reftrack.Reftrack.wrap_scene(self.root, self.refobjinter)
