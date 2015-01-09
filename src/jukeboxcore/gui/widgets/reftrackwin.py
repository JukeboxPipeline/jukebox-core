"""A window that can be used for tools that handle the referene workflow."""

from PySide import QtGui
from PySide import QtCore

from jukeboxcore import reftrack
from jukeboxcore import djadapter
from jukeboxcore.gui.main import JB_MainWindow, get_icon
from jukeboxcore.gui import treemodel
from jukeboxcore.gui import djitemdata
from jukeboxcore.gui.widgetdelegate import WD_TreeView
from jukeboxcore.gui.widgets.reftrackwidget import ReftrackDelegate
from jukeboxcore.gui.widgets.browser import ListBrowser
from jukeboxcore.gui.reftrackitemdata import ReftrackSortFilterModel
from reftrackwin_ui import Ui_reftrack_mwin
from reftrackadder_ui import Ui_reftrackadder_mwin


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
        self.reftrackadderwin = None  # the window to add new reftracks to the root

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
        self.reftrack_treev.setHeaderHidden(True)
        self.central_widget_vbox.insertWidget(1, self.reftrack_treev)
        self.setup_icons()
        self.model = self.root.get_model()
        self.proxy = self.create_proxy_model(self.model)
        self.proxy.setFilterKeyColumn(-1)  # filter all columns
        self.proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
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
        plus_icon = get_icon('glyphicons_433_plus_bright.png', asicon=True)
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
        if self.reftrackadderwin:
            self.reftrackadderwin.close()
        self.reftrackadderwin = ReftrackAdderWin(self.refobjinter, self.root, parent=self)
        self.reftrackadderwin.destroyed.connect(self.addnewwin_destroyed)
        self.reftrackadderwin.show()

    def addnewwin_destroyed(self, *args, **kwargs):
        """Delete the internal reference to the reftrackadderwin

        :returns: None
        :rtype: None
        :raises: None
        """
        self.reftrackadderwin = None

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

        self.proxy.setFilterWildcard(self.search_le.text())

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


class ReftrackAdderWin(JB_MainWindow, Ui_reftrackadder_mwin):
    """A window for adding new reftracks to reftrack treemodel.
    """

    def __init__(self, refobjinter, root, parent=None, flags=0):
        """Initialize a new ReftrackAdder window with the given refobjinter that
        will add new reftracks to the given root.

        :param refobjinter:
        :type refobjinter:
        :param root:
        :type root:
        :param parent:
        :type parent:
        :param flags:
        :type flags:
        :raises: None
        """
        super(ReftrackAdderWin, self).__init__(parent, flags)
        self.refobjinter = refobjinter
        self.root = root

        self.setupUi(self)
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self, ):
        """Setup the general ui

        :returns: None
        :rtype: None
        :raises: None
        """
        plus_icon = get_icon('glyphicons_433_plus_bright.png', asicon=True)
        self.add_tb.setIcon(plus_icon)

        self.shot_browser = ListBrowser(4, parent=self, headers=["Project", "Sequence", "Shot", "Type"])
        self.asset_browser = ListBrowser(4, parent=self, headers=["Project", "Assettype", "Asset", "Type"])

        self.shotmodel = self.create_shot_model()
        self.assetmodel = self.create_asset_model()

        self.shot_browser.set_model(self.shotmodel)
        self.asset_browser.set_model(self.assetmodel)

        self.shot_vbox.addWidget(self.shot_browser)
        self.asset_vbox.addWidget(self.asset_browser)

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
        self.add_tb.clicked.connect(self.add_selected)

    def create_shot_model(self, ):
        """Return a treemodel with the levels: project, sequence, shot and reftrack type

        :returns: a treemodel
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        rootdata = treemodel.ListItemData(['Name'])
        rootitem = treemodel.TreeItem(rootdata)
        prjs = djadapter.projects.all()
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            prjitem = treemodel.TreeItem(prjdata, rootitem)
            for seq in prj.sequence_set.all():
                seqdata = djitemdata.SequenceItemData(seq)
                seqitem = treemodel.TreeItem(seqdata, prjitem)
                for shot in seq.shot_set.all():
                    shotdata = djitemdata.ShotItemData(shot)
                    shotitem = treemodel.TreeItem(shotdata, seqitem)
                    for typ in self.refobjinter.get_available_types_for_scene(shot):
                        typdata = treemodel.ListItemData([typ])
                        treemodel.TreeItem(typdata, shotitem)

        return treemodel.TreeModel(rootitem)

    def create_asset_model(self, ):
        """Return a treemodel with the levels: project, assettype, asset and reftrack type

        :returns: a treemodel
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        rootdata = treemodel.ListItemData(['Name'])
        rootitem = treemodel.TreeItem(rootdata)
        prjs = djadapter.projects.all()
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            prjitem = treemodel.TreeItem(prjdata, rootitem)
            for atype in prj.atype_set.all():
                atypedata = djitemdata.AtypeItemData(atype)
                atypeitem = treemodel.TreeItem(atypedata, prjitem)
                for asset in atype.asset_set.filter(project=prj):
                    assetdata = djitemdata.AssetItemData(asset)
                    assetitem = treemodel.TreeItem(assetdata, atypeitem)
                    for typ in self.refobjinter.get_available_types_for_scene(asset):
                        typdata = treemodel.ListItemData([typ])
                        treemodel.TreeItem(typdata, assetitem)

        return treemodel.TreeModel(rootitem)

    def add_selected(self, ):
        """Create a new reftrack with the selected element and type and add it to the root.

        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        browser = self.shot_browser if self.browser_tabw.currentIndex() == 0 else self.asset_browser
        selelements = browser.selected_indexes(2)
        if not selelements:
            return
        seltypes = browser.selected_indexes(3)
        if not seltypes:
            return
        elementi = selelements[0]
        typi = seltypes[0]
        if not elementi.isValid() or not typi.isValid():
            return
        element = elementi.internalPointer().internal_data()
        typ = typi.internalPointer().internal_data()[0]

        reftrack.Reftrack(self.root, self.refobjinter, typ=typ, element=element)
