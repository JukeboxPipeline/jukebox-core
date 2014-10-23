import os
from functools import partial

from PySide import QtCore
from PySide import QtGui
from django.core.exceptions import ValidationError

from jukeboxcore.log import get_logger
log = get_logger(__name__)

from jukeboxcore import djadapter
from jukeboxcore.filesys import JB_File, TaskFileInfo
from jukeboxcore.plugins import JB_CorePlugin
from jukeboxcore.gui.main import JB_MainWindow, get_icon
from jukeboxcore.gui import treemodel, djitemdata
from jukeboxcore.gui.widgets.browser import ComboBoxBrowser, ListBrowser, CommentBrowser
from jukeboxcore.gui.widgets.textedit import JB_PlainTextEdit
import genesis_ui


class GenesisWin(JB_MainWindow, genesis_ui.Ui_genesis_mwin):
    """The abstract genesis tool window

    The window uses the genesis.ui for it's layout.
    It has a tab widget with two browsers to select shots and assets.
    There is a field to write a comment and buttons for opening and saving.

    This is should be subclassed and :meth:`GenesisWin.open_shot`, :meth:`GenesisWin.open_asset`,
    :meth:`GenesisWin.save_shot`, :meth:`GenesisWin.save_asset`, :meth:`GenesisWin.get_current_file` should be reimplemented.

    Before creating an instance, call :meth:`GenesisWin.set_filetype` at least once.
    """

    _filetype = None

    def __init__(self, parent=None, flags=0):
        """Constructs a new GenesisWin with the given parent

        :param parent: Optional - the parent of the window - default is None
        :type parent: QWidget
        :param flags: the window flags
        :type flags: QtCore.Qt.WindowFlags
        :raises: None
        """
        super(GenesisWin, self).__init__(parent, flags)

        self.setupUi(self)
        self.setup_ui()
        self.setup_signals()

        if not self._filetype:
            log.warning('No Filetypes are allowed. Genesis will not show any files! Call set_filetype before instancing!')
        self.prjbrws.set_model(self.create_prj_model())
        self.set_to_current()

        # init the buttons (determine if they are enabled)
        # when there are no versions at the beginning, the buttons are still enabled
        si = self.shotverbrws.selected_indexes(0)
        if si:
            self.shot_ver_sel_changed(si[0])
        else:
            self.shot_ver_sel_changed(QtCore.QModelIndex())
        ai = self.assetverbrws.selected_indexes(0)
        if ai:
            self.asset_ver_sel_changed(ai[0])
        else:
            self.asset_ver_sel_changed(QtCore.QModelIndex())

    @classmethod
    def set_filetype(cls, filetype):
        """Set the allowed filetypes for the taskfiles that should be handled by Genesis

        :param filetype: the filetype from :data:`djadapter.FILETYPES`
        :type filetypes: str
        :returns: None
        :rtype: None
        :raises: None
        """
        cls._filetype = filetype

    @classmethod
    def get_filetype(cls, ):
        """Return the allowed filetype

        :returns:  filetype from :data:`djadapter.FILETYPES`
        :rtype: str
        :raises: None
        """
        return cls.filetype

    def setup_ui(self, ):
        """Create the browsers and all necessary ui elements for the tool

        :returns: None
        :rtype: None
        :raises: None
        """
        w = QtGui.QWidget(self)
        w.setLayout(self.central_vbox)
        self.setCentralWidget(w)

        self.prjbrws = self.create_prj_browser()
        self.shotbrws = self.create_shot_browser()
        self.shotverbrws = self.create_ver_browser(self.shot_browser_vbox)
        self.shotcommentbrws = self.create_comment_browser(self.shot_info_hbox)
        self.assetbrws = self.create_asset_browser()
        self.assetverbrws = self.create_ver_browser(self.asset_browser_vbox)
        self.assetcommentbrws = self.create_comment_browser(self.asset_info_hbox)
        self.current_pb = self.create_current_pb()
        self.asset_comment_pte = self.create_comment_edit()
        self.asset_vbox.addWidget(self.asset_comment_pte)
        self.shot_comment_pte = self.create_comment_edit()
        self.shot_vbox.addWidget(self.shot_comment_pte)

        ph = "Enter New Descriptor"
        self.asset_descriptor_le.setPlaceholderText(ph)
        self.shot_descriptor_le.setPlaceholderText(ph)

        self.shot_info_mapper = QtGui.QDataWidgetMapper()
        self.asset_info_mapper = QtGui.QDataWidgetMapper()
        self.setup_icons()

    def setup_icons(self, ):
        """Set all icons on buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        folder_icon = get_icon('glyphicons_144_folder_open.png', asicon=True)
        self.asset_open_path_tb.setIcon(folder_icon)
        self.shot_open_path_tb.setIcon(folder_icon)
        self.asset_open_pb.setIcon(folder_icon)
        self.shot_open_pb.setIcon(folder_icon)

        floppy_icon = get_icon('glyphicons_446_floppy_save.png', asicon=True)
        self.asset_save_pb.setIcon(floppy_icon)
        self.shot_save_pb.setIcon(floppy_icon)

        current_icon = get_icon('glyphicons_181_download_alt.png', asicon=True)
        self.current_pb.setIcon(current_icon)

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
        prjlvl = self.prjbrws.get_level(0)
        prjlvl.new_root.connect(self.update_browsers)
        self.work_rb.toggled.connect(self.update_browsers)

        shotdesclvl = self.shotbrws.get_level(3)
        shotselcb = partial(self.selection_changed,
                            source=self.shotbrws,
                            update=self.shotverbrws,
                            commentbrowser=self.shotcommentbrws,
                            mapper=self.shot_info_mapper)
        shotdesclvl.new_root.connect(shotselcb)
        shotverlvl = self.shotverbrws.get_level(0)
        shotverlvl.new_root.connect(self.shot_ver_sel_changed)
        shotmappercb = partial(self.set_mapper_index, mapper=self.shot_info_mapper)
        shotverlvl.new_root.connect(shotmappercb)
        shotverlvl.new_root.connect(partial(self.shotcommentbrws.set_root, 0))

        assetdesclvl = self.assetbrws.get_level(3)
        assetselcb = partial(self.selection_changed,
                             source=self.assetbrws,
                             update=self.assetverbrws,
                             commentbrowser=self.assetcommentbrws,
                             mapper=self.asset_info_mapper)
        assetdesclvl.new_root.connect(assetselcb)
        assetverlvl = self.assetverbrws.get_level(0)
        assetverlvl.new_root.connect(self.asset_ver_sel_changed)
        assetmappercb = partial(self.set_mapper_index, mapper=self.asset_info_mapper)
        assetverlvl.new_root.connect(assetmappercb)
        assetverlvl.new_root.connect(partial(self.assetcommentbrws.set_root, 0))

        self.shot_open_pb.clicked.connect(self.shot_open_callback)
        self.asset_open_pb.clicked.connect(self.asset_open_callback)
        self.shot_save_pb.clicked.connect(self.shot_save_callback)
        self.asset_save_pb.clicked.connect(self.asset_save_callback)

        self.current_pb.clicked.connect(self.set_to_current)

    def create_prj_browser(self, ):
        """Create the project browser

        This creates a combobox brower for projects
        and adds it to the ui

        :returns: the created combo box browser
        :rtype: :class:`jukeboxcore.gui.widgets.browser.ComboBoxBrowser`
        :raises: None
        """
        prjbrws = ComboBoxBrowser(1, headers=['Project:'])
        self.central_vbox.insertWidget(1, prjbrws)
        return prjbrws

    def create_shot_browser(self, ):
        """Create the shot browser

        This creates a list browser for shots
        and adds it to the ui

        :returns: the created borwser
        :rtype: :class:`jukeboxcore.gui.widgets.browser.ListBrowser`
        :raises: None
        """
        shotbrws = ListBrowser(4, headers=['Sequence', 'Shot', 'Task', 'Descriptor'])
        self.shot_browser_vbox.insertWidget(0, shotbrws)
        return shotbrws

    def create_asset_browser(self, ):
        """Create the asset browser

        This creates a list browser for assets
        and adds it to the ui

        :returns: the created borwser
        :rtype: :class:`jukeboxcore.gui.widgets.browser.ListBrowser`
        :raises: None
        """
        assetbrws = ListBrowser(4, headers=['Assettype', 'Asset', 'Task', 'Descriptor'])
        self.asset_browser_vbox.insertWidget(0, assetbrws)
        return assetbrws

    def create_ver_browser(self, layout):
        """Create a version browser and insert it into the given layout

        :param layout: the layout to insert the browser into
        :type layout: QLayout
        :returns: the created browser
        :rtype: :class:`jukeboxcore.gui.widgets.browser.ComboBoxBrowser`
        :raises: None
        """
        brws = ComboBoxBrowser(1, headers=['Version:'])
        layout.insertWidget(1, brws)
        return brws

    def create_comment_browser(self, layout):
        """Create a comment browser and insert it into the given layout

        :param layout: the layout to insert the browser into
        :type layout: QLayout
        :returns: the created browser
        :rtype: :class:`jukeboxcore.gui.widgets.browser.ListBrowser`
        :raises: None
        """
        brws = CommentBrowser(1, headers=['Comments:'])
        layout.insertWidget(1, brws)
        return brws

    def create_current_pb(self, ):
        """Create a push button and place it in the corner of the tabwidget

        :returns: the created button
        :rtype: :class:`QtGui.QPushButton`
        :raises: None
        """
        pb = QtGui.QPushButton("Set to current")
        self.selection_tabw.setCornerWidget(pb)
        return pb

    def create_prj_model(self, ):
        """Create and return a tree model that represents a list of projects

        :returns: the creeated model
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        prjs = djadapter.projects.all()
        rootdata = treemodel.ListItemData(['Name', 'Short', 'Rootpath'])
        prjroot = treemodel.TreeItem(rootdata)
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, prjroot)
        prjmodel = treemodel.TreeModel(prjroot)
        return prjmodel

    def create_shot_model(self, project, releasetype):
        """Create and return a new tree model that represents shots til descriptors

        The tree will include sequences, shots, tasks and descriptors of the given releaetype.

        :param releasetype: the releasetype for the model
        :type releasetype: :data:`djadapter.RELEASETYPES`
        :param project: the project of the shots
        :type project: :class:`djadapter.models.Project`
        :returns: the created tree model
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        rootdata = treemodel.ListItemData(['Name'])
        rootitem = treemodel.TreeItem(rootdata)
        for seq in project.sequence_set.all():
            seqdata = djitemdata.SequenceItemData(seq)
            seqitem = treemodel.TreeItem(seqdata, rootitem)
            for shot in seq.shot_set.all():
                shotdata = djitemdata.ShotItemData(shot)
                shotitem = treemodel.TreeItem(shotdata, seqitem)
                for task in shot.tasks.all():
                    taskdata = djitemdata.TaskItemData(task)
                    taskitem = treemodel.TreeItem(taskdata, shotitem)
                    #get all mayafiles
                    taskfiles = task.taskfile_set.filter(releasetype=releasetype, typ=self._filetype)
                    # get all descriptor values as a list. disctinct eliminates duplicates.
                    for d in taskfiles.order_by('descriptor').values_list('descriptor', flat=True).distinct():
                        ddata = treemodel.ListItemData([d,])
                        treemodel.TreeItem(ddata, taskitem)
        shotmodel = treemodel.TreeModel(rootitem)
        return shotmodel

    def create_comment_edit(self, ):
        """Create a text edit for comments

        :returns: the created text edit
        :rtype: :class:`jukeboxcore.gui.widgets.textedit.JB_PlainTextEdit`
        :raises: None
        """
        pte = JB_PlainTextEdit(parent=self)
        pte.set_placeholder("Enter a comment before saving...")
        pte.setMaximumHeight(120)
        return pte

    def create_asset_model(self, project, releasetype):
        """Create and return a new tree model that represents assets til descriptors

        The tree will include assettypes, assets, tasks and descriptors of the given releaetype.

        :param releasetype: the releasetype for the model
        :type releasetype: :data:`djadapter.RELEASETYPES`
        :param project: the project of the assets
        :type project: :class:`djadapter.models.Project`
        :returns: the created tree model
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        rootdata = treemodel.ListItemData(['Name'])
        rootitem = treemodel.TreeItem(rootdata)
        for atype in project.atype_set.all():
            atypedata = djitemdata.AtypeItemData(atype)
            atypeitem = treemodel.TreeItem(atypedata, rootitem)
            for asset in atype.asset_set.filter(project=project):
                assetdata = djitemdata.AssetItemData(asset)
                assetitem = treemodel.TreeItem(assetdata, atypeitem)
                for task in asset.tasks.all():
                    taskdata = djitemdata.TaskItemData(task)
                    taskitem = treemodel.TreeItem(taskdata, assetitem)
                    taskfiles = task.taskfile_set.filter(releasetype=releasetype, typ=self._filetype)
                    # get all descriptor values as a list. disctinct eliminates duplicates.
                    for d in taskfiles.order_by('descriptor').values_list('descriptor', flat=True).distinct():
                        ddata = treemodel.ListItemData([d,])
                        treemodel.TreeItem(ddata, taskitem)
        assetmodel = treemodel.TreeModel(rootitem)
        return assetmodel

    def create_version_model(self, task, releasetype, descriptor):
        """Create and return a new model that represents taskfiles for the given task, releasetpye and descriptor

        :param task: the task of the taskfiles
        :type task: :class:`djadapter.models.Task`
        :param releasetype: the releasetype
        :type releasetype: str
        :param descriptor: the descirptor
        :type descriptor: str|None
        :returns: the created tree model
        :rtype: :class:`jukeboxcore.gui.treemodel.TreeModel`
        :raises: None
        """
        rootdata = treemodel.ListItemData(['Version', 'Releasetype', 'Path'])
        rootitem = treemodel.TreeItem(rootdata)
        for tf in task.taskfile_set.filter(releasetype=releasetype, descriptor=descriptor).order_by('-version'):
            tfdata = djitemdata.TaskFileItemData(tf)
            tfitem = treemodel.TreeItem(tfdata, rootitem)
            for note in tf.notes.all():
                notedata = djitemdata.NoteItemData(note)
                treemodel.TreeItem(notedata, tfitem)
        versionmodel = treemodel.TreeModel(rootitem)
        return versionmodel

    def update_shot_browser(self, project, releasetype):
        """Update the shot browser to the given project

        :param releasetype: the releasetype for the model
        :type releasetype: :data:`djadapter.RELEASETYPES`
        :param project: the project of the shots
        :type project: :class:`djadapter.models.Project`
        :returns: None
        :rtype: None
        :raises: None
        """
        if project is None:
            self.shotbrws.set_model(None)
            return
        shotmodel = self.create_shot_model(project, releasetype)
        self.shotbrws.set_model(shotmodel)

    def update_asset_browser(self, project, releasetype):
        """update the assetbrowser to the given project

        :param releasetype: the releasetype for the model
        :type releasetype: :data:`djadapter.RELEASETYPES`
        :param project: the project of the assets
        :type project: :class:`djadapter.models.Project`
        :returns: None
        :rtype: None
        :raises: None
        """
        if project is None:
            self.shotbrws.set_model(None)
            return
        assetmodel = self.create_asset_model(project, releasetype)
        self.assetbrws.set_model(assetmodel)

    def update_browsers(self, *args, **kwargs):
        """Update the shot and the assetbrowsers

        :returns: None
        :rtype: None
        :raises: None
        """
        sel = self.prjbrws.selected_indexes(0)
        if not sel:
            return
        prjindex = sel[0]
        if not prjindex.isValid():
            prj = None
        else:
            prjitem = prjindex.internalPointer()
            prj = prjitem.internal_data()
        self.set_project_banner(prj)
        releasetype = self.get_releasetype()
        self.update_shot_browser(prj, releasetype)
        self.update_asset_browser(prj, releasetype)

    def update_version_descriptor(self, task, releasetype, descriptor,
                                  verbrowser, commentbrowser):
        """Update the versions in the given browser

        :param task: the task of the taskfiles
        :type task: :class:`djadapter.models.Task` | None
        :param releasetype: the releasetype
        :type releasetype: str|None
        :param descriptor: the descirptor
        :type descriptor: str|None
        :param verbrowser: the browser to update (the version browser)
        :type verbrowser: :class:`jukeboxcore.gui.widgets.browser.AbstractTreeBrowser`
        :param commentbrowser: the comment browser to update
        :type commentbrowser: :class:`jukeboxcore.gui.widgets.browser.AbstractTreeBrowser`
        :returns: None
        :rtype: None
        :raises: None
        """
        if task is None:
            null = treemodel.TreeItem(None)
            verbrowser.set_model(treemodel.TreeModel(null))
            return
        m = self.create_version_model(task, releasetype, descriptor)
        verbrowser.set_model(m)
        commentbrowser.set_model(m)

    def selection_changed(self, index, source, update, commentbrowser, mapper):
        """Callback for when the asset or shot browser changed its selection

        :param index: the modelindex with the descriptor tree item as internal data
        :type index: QtCore.QModelIndex
        :param source: the shot or asset browser to that changed its selection
        :type source: :class:`jukeboxcore.gui.widgets.browser.AbstractTreeBrowser`
        :param update: the browser to update
        :type update: :class:`jukeboxcore.gui.widgets.browser.AbstractTreeBrowser`
        :param browser: the comment browser to update
        :type browser: :class:`jukeboxcore.gui.widgets.browser.AbstractTreeBrowser`
        :param mapper: the data widget mapper to update
        :type mapper: :class:`QtGui.QDataWidgetMapper`
        :returns: None
        :rtype: None
        :raises: None
        """
        if not index.isValid():  # no descriptor selected
            self.update_version_descriptor(None, None, None, update, commentbrowser)
            self.set_info_mapper_model(mapper, None)
            return

        descitem  = index.internalPointer()
        descriptor = descitem.internal_data()[0]
        taskdata = source.selected_indexes(2)[0].internalPointer()
        task = taskdata.internal_data()
        releasetype = self.get_releasetype()
        self.update_version_descriptor(task, releasetype, descriptor, update, commentbrowser)

        self.set_info_mapper_model(mapper, update.model)
        sel = update.selected_indexes(0)
        if sel:
            self.set_mapper_index(sel[0], mapper)

    def set_info_mapper_model(self, mapper, model):
        """Set the model for the info mapper

        :param mapper: the mapper to update
        :type mapper: QtGui.QDataWidgetMapper
        :param model: The model to set
        :type model: QtGui.QAbstractItemModel | None
        :returns: None
        :rtype: None
        :raises: None
        """
        mapper.setModel(model)
        if mapper is self.asset_info_mapper:
            if model is None:
                self.asset_path_le.setText("")
                self.asset_created_by_le.setText("")
                self.asset_created_dte.findChild(QtGui.QLineEdit).setText('')
                self.asset_updated_dte.findChild(QtGui.QLineEdit).setText('')
            else:
                mapper.addMapping(self.asset_path_le, 2)
                mapper.addMapping(self.asset_created_by_le, 3)
                mapper.addMapping(self.asset_created_dte, 4)
                mapper.addMapping(self.asset_updated_dte, 5)
        else:
            if model is None:
                self.shot_path_le.setText("")
                self.shot_created_by_le.setText("")
                self.shot_created_dte.findChild(QtGui.QLineEdit).setText('')
                self.shot_updated_dte.findChild(QtGui.QLineEdit).setText('')
            else:
                mapper.addMapping(self.shot_path_le, 2)
                mapper.addMapping(self.shot_created_by_le, 3)
                mapper.addMapping(self.shot_created_dte, 4)
                mapper.addMapping(self.shot_updated_dte, 5)

    def set_mapper_index(self, index, mapper):
        """Set the mapper to the given index

        :param index: the index to set
        :type index: QtCore.QModelIndex
        :param mapper: the mapper to set
        :type mapper: QtGui.QDataWidgetMapper
        :returns: None
        :rtype: None
        :raises: None
        """
        parent = index.parent()
        mapper.setRootIndex(parent)
        mapper.setCurrentModelIndex(index)

    def get_releasetype(self, ):
        """Return the currently selected releasetype

        :returns: the selected releasetype
        :rtype: str
        :raises: None
        """
        if self.work_rb.isChecked():
            releasetype = djadapter.RELEASETYPES['work']
        else:
            releasetype = djadapter.RELEASETYPES['release']
        return releasetype

    def asset_ver_sel_changed(self, index):
        """Callback for when the version selection has changed

        :param index: the selected index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self.asset_open_pb.setEnabled(index.isValid())
        # only allow new, when there is an asset. if there is an asset, there should always be a task
        enablenew = bool(self.assetbrws.selected_indexes(1)) and self.get_releasetype() == djadapter.RELEASETYPES['work']
        self.asset_save_pb.setEnabled(enablenew)
        self.asset_descriptor_le.setEnabled(enablenew)
        self.asset_comment_pte.setEnabled(enablenew)
        self.update_descriptor_le(self.asset_descriptor_le, index)

    def shot_ver_sel_changed(self, index):
        """Callback for when the version selection has changed

        :param index: the selected index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        self.shot_open_pb.setEnabled(index.isValid())
        # only allow new, if the releasetype is work
        # only allow new, if there is a shot. if there is a shot, there should always be a task.
        enablenew = bool(self.shotbrws.selected_indexes(1)) and self.get_releasetype() == djadapter.RELEASETYPES['work']
        self.shot_save_pb.setEnabled(enablenew)
        self.shot_descriptor_le.setEnabled(enablenew)
        self.shot_comment_pte.setEnabled(enablenew)
        self.update_descriptor_le(self.shot_descriptor_le, index)

    def update_descriptor_le(self, lineedit, index):
        """Update the given line edit to show the descriptor that is stored in the index

        :param lineedit: the line edit to update with the descriptor
        :type lineedit: QLineEdit
        :param index: the selected index of the treemodel that has a taskfileitem as internal pointer
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        if index.isValid():
            item = index.internalPointer()
            taskfile = item.internal_data()
            descriptor = taskfile.descriptor
            lineedit.setText(descriptor)
        else:
            lineedit.setText("")

    def set_to_current(self, ):
        """Set the selection to the currently open one

        :returns: None
        :rtype: None
        :raises: None
        """
        cur = self.get_current_file()
        if cur is not None:
            self.set_selection(cur)

    def set_selection(self, taskfile):
        """Set the selection to the given taskfile

        :param taskfile: the taskfile to set the selection to
        :type taskfile: :class:`djadapter.models.TaskFile`
        :returns: None
        :rtype: None
        :raises: None
        """
        self.set_project(taskfile.task.project)
        self.set_releasetype(taskfile.releasetype)
        if taskfile.task.department.assetflag:
            browser = self.assetbrws
            verbrowser = self.assetverbrws
            tabi = 0
            rootobj = taskfile.task.element.atype
        else:
            browser = self.shotbrws
            verbrowser = self.shotverbrws
            tabi = 1
            rootobj = taskfile.task.element.sequence

        self.set_level(browser, 0, rootobj)
        self.set_level(browser, 1, taskfile.task.element)
        self.set_level(browser, 2, taskfile.task)
        self.set_level(browser, 3, [taskfile.descriptor])
        self.set_level(verbrowser, 0, taskfile)

        self.selection_tabw.setCurrentIndex(tabi)

    def set_project(self, project):
        """Set the project selection to the given project

        :param project: the project to select
        :type project: :class:`djadapter.models.Project`
        :returns: None
        :rtype: None
        :raises: ValueError
        """
        prjroot = self.prjbrws.model.root
        prjitems = prjroot.childItems
        for row, item in enumerate(prjitems):
            prj = item.internal_data()
            if prj == project:
                prjindex = self.prjbrws.model.index(row, 0)
                break
        else:
            raise ValueError("Could not select the given taskfile. No project %s found." % project.name)
        self.prjbrws.set_index(0, prjindex)

    def set_releasetype(self, releasetype):
        """Set the releasetype to either work or release

        :param releasetype: the release type to set
        :type releasetype: :data:`djadapter.RELEASETYPES`
        :returns: None
        :rtype: None
        :raises: None
        """
        if releasetype == djadapter.RELEASETYPES['work']:
            self.work_rb.setChecked(True)
        else:
            self.release_rb.setChecked(True)

    def set_level(self, browser, lvl, obj):
        """Set the given browser level selection to the one that matches with obj

        This is going to compare the internal_data of the model with the obj

        :param browser:
        :type browser:
        :param lvl: the depth level to set
        :type lvl: int
        :param obj: the object to compare the indexes with
        :type obj: object
        :returns: None
        :rtype: None
        :raises: None
        """
        if lvl == 0:
            index = QtCore.QModelIndex()
            root = browser.model.root
            items = root.childItems
        else:
            index = browser.selected_indexes(lvl-1)[0]
            item = index.internalPointer()
            items = item.childItems
        for row, item in enumerate(items):
            data = item.internal_data()
            if data == obj:
                newindex = browser.model.index(row, 0, index)
                break
        else:
            raise ValueError("Could not select the given object in the browser. %s not found." % obj)
        browser.set_index(lvl, newindex)

    def get_current_file(self, ):
        """Return the taskfile that is currently open or None if no taskfile is open

        :returns: the open taskfile or None if no taskfile is open
        :rtype: :class:`djadapter.models.TaskFile` | None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def set_project_banner(self, project):
        """Set the banner labels pixmap to the project banner

        :param project: the project with the banner
        :type project: :class:`djadapter.models.Project` | None
        :returns: None
        :rtype: None
        :raises: None
        """
        if project is None:
            self.prj_banner_lb.setText("No Project")
        else:
            self.prj_banner_lb.setText("%s banner placeholder" % project.name)

    def shot_open_callback(self, *args, **kwargs):
        """Callback for the shot open button

        :returns: None
        :rtype: None
        :raises: None
        """
        si = self.shotverbrws.selected_indexes(0)
        if not si:
            return
        item = si[0].internalPointer()
        taskfile = item.internal_data()
        if not os.path.exists(taskfile.path):
            msg = 'The selected shot does not exist: %s' % taskfile.path
            log.error(msg)
            self.statusbar.showMessage(msg)
            return
        self.open_shot(taskfile)

    def asset_open_callback(self, *args, **kwargs):
        """Callback for the shot open button

        :returns: None
        :rtype: None
        :raises: None
        """
        si = self.assetverbrws.selected_indexes(0)
        if not si:
            return
        item = si[0].internalPointer()
        taskfile = item.internal_data()
        if not os.path.exists(taskfile.path):
            msg = 'The selected asset does not exist: %s' % taskfile.path
            log.error(msg)
            self.statusbar.showMessage(msg)
            return
        self.open_asset(taskfile)

    def shot_save_callback(self, *args, **kwargs):
        """Callback for the shot open button

        :returns: None
        :rtype: None
        :raises: None
        """
        tasksel = self.shotbrws.selected_indexes(2)
        if not tasksel:
            self.statusbar.showMessage('No task selected! Cannot save!')
            return

        taskitem = tasksel[0].internalPointer()
        task = taskitem.internal_data()
        rtype = djadapter.RELEASETYPES['work']
        descriptor = self.shot_descriptor_le.text()
        if not self.check_selection_for_save(task, descriptor):
            return

        tfi = TaskFileInfo.get_next(task=task, releasetype=rtype,
                                    typ=self._filetype, descriptor=descriptor)
        self._save_tfi(tfi)

    def asset_save_callback(self, *args, **kwargs):
        """Callback for the shot open button

        :returns: None
        :rtype: None
        :raises: None
        """
        tasksel = self.assetbrws.selected_indexes(2)
        if not tasksel:
            self.statusbar.showMessage('No task selected! Cannot save!')
            return

        taskitem = tasksel[0].internalPointer()
        task = taskitem.internal_data()
        rtype = djadapter.RELEASETYPES['work']
        descriptor = self.asset_descriptor_le.text()
        if not self.check_selection_for_save(task, descriptor):
            return

        tfi = TaskFileInfo.get_next(task=task, releasetype=rtype,
                                    typ=self._filetype, descriptor=descriptor)
        self._save_tfi(tfi)

    def _save_tfi(self, tfi):
        """Save currently open scene with the information in the given taskfile info

        :param tfi: taskfile info
        :type tfi: :class:`TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        jbfile = JB_File(tfi)
        self.create_dir(jbfile)

        tf, note = self.create_db_entry(tfi)

        try:
            self.save_shot(jbfile, tf)
        except:
            tf.delete()
            note.delete()
            self.statusbar.showMessage('Saving failed!')
            log.exception("Saving failed!")
            return
        self.update_model(tfi)

    def update_model(self, tfi):
        """Update the model for the given tfi

        :param tfi: taskfile info
        :type tfi: :class:`TaskFileInfo`
        :returns: None
        :rtype: None
        :raises: None
        """
        if tfi.task.department.assetflag:
            browser = self.assetbrws
        else:
            browser = self.shotbrws

        if tfi.version == 1:  # add descriptor
            parent = browser.selected_indexes(2)[0]
            ddata = treemodel.ListItemData([tfi.descriptor])
            ditem = treemodel.TreeItem(ddata)
            browser.model.addRow(0, ditem, parent)
        self.set_level(browser, 3, [tfi.descriptor])

    def create_dir(self, jbfile):
        """Create a dir for the given dirfile and display an error message, if it fails.

        :param jbfile: the jb file to make the directory for
        :type jbfile: class:`JB_File`
        :returns: None
        :rtype: None
        :raises: None
        """
        try:
            jbfile.create_directory()
        except os.error:
            self.statusbar.showMessage('Could not create path: %s' % jbfile.get_path())

    def open_shot(self, taskfile):
        """Open the given taskfile

        :param taskfile: the taskfile for the shot
        :type taskfile: :class:`djadapter.models.TaskFile`
        :returns: True if opening was successful
        :rtype: bool
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def save_shot(self, jbfile):
        """Save the shot to the location of jbfile

        :param jbfile: the jbfile that can be used to query the location
        :type jbfile: :class:`jukeboxcore.filesys.JB_File`
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def open_asset(self, taskfile):
        """Open the given taskfile

        :param taskfile: the taskfile for the asset
        :type taskfile: :class:`djadapter.models.TaskFile`
        :returns: True if opening was successful
        :rtype: bool
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def save_asset(self, taskfile):
        """Save the shot to the location of jbfile

        :param jbfile: the jbfile that can be used to query the location
        :type jbfile: :class:`jukeboxcore.filesys.JB_File`
        :returns: None
        :rtype: None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def check_selection_for_save(self, task, descriptor):
        """Emit warnings if the descriptor is None or the current file
        is of a different task.

        :param task: the selected task
        :type task: :class:`djadapter.models.Task`
        :param descriptor: the descriptor
        :type descriptor: str
        :returns: True if check was successfull.
        :rtype: bool
        :raises: None
        """
        if not descriptor:
            self.statusbar.showMessage("Please provide a descriptor!")
            return False
        try:
            djadapter.validators.alphanum_vld(descriptor)
        except ValidationError:
            self.statusbar.showMessage("Descriptor contains characters other than alphanumerical ones.")
            return False
        cur = self.get_current_file()
        if cur and task != cur.task:
            self.statusbar.showMessage("Task is different. Not supperoted atm!")
            return False
        return True

    def create_db_entry(self, tfi):
        """Create a db entry for the given task file info

        :param tfi: the info for a TaskFile entry in the db
        :type tfi: :class:`jukeboxcore.filesys.TaskFileInfo`
        :returns: the created taskfile and note
        :rtype: tuple
        :raises: ValidationError
        """
        jbfile = JB_File(tfi)
        p = jbfile.get_fullpath()
        user = djadapter.get_current_user()
        tf = djadapter.models.TaskFile(path=p, task=tfi.task, version=tfi.version,
                                       releasetype=tfi.releasetype, descriptor=tfi.descriptor,
                                       typ=tfi.typ, user=user)
        tf.full_clean()
        tf.save()
        if tfi.task.department.assetflag:
            comment = self.asset_comment_pte.toPlainText()
        else:
            comment = self.shot_comment_pte.toPlainText()

        try:
            note = djadapter.models.Note(user=user, parent=tf, content=comment)
            note.full_clean()
            note.save()
        except Exception, e:
            tf.delete()
            raise e
        return tf, note


class Genesis(JB_CorePlugin):
    """Core plugin for all tools that implement opening and saving shots and assets in a software.
    """

    author = "David Zuber"
    copyright = "2014"
    version =  "0.1"
    description = "A abstract tool for saving and opening shots and assets."

    def init(self, ):
        """Do nothing

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    def uninit(self):
        """Do nothing

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    @property
    def GenesisWin(self, ):
        """Return the GenesisWin class

        :returns: the genesis win class
        :rtype: :class:`GenesisWin`
        :raises: None
        """
        return GenesisWin
