import os
from functools import partial

from PySide import QtCore
from PySide import QtGui

from jukeboxcore.log import get_logger
log = get_logger(__name__)

from jukeboxcore import djadapter
from jukeboxcore.ostool import get_interface
from jukeboxcore.filesys import TaskFileInfo
from jukeboxcore.gui.main import get_icon
from jukeboxcore.gui import treemodel, djitemdata
from jukeboxcore.gui.widgets.browser import ComboBoxBrowser, ListBrowser, CommentBrowser
from filebrowser_ui import Ui_FileBrowser


class FileBrowser(Ui_FileBrowser, QtGui.QWidget):
    """A browser for taskfiles
    """

    shot_taskfile_sel_changed = QtCore.Signal(TaskFileInfo)
    """Signal when the selection changes. Returns a :class:`TaskFileInfo` or None"""

    asset_taskfile_sel_changed = QtCore.Signal(TaskFileInfo)
    """Signal when the selection changes. Returns a :class:`TaskFileInfo` or None"""

    def __init__(self, filetype, releasetypes=None, get_current_file=None, parent=None):
        """Initialize a new file browser widget with the given parent

        :param filetype: the filetype the browser should display from :data:`djadapter.FILETYPES`
        :type filetypes: str
        :param releasetypes: the releasetypes the browser should display.
        :type releasetype: list of :data:`djadapter.RELEASETYPES`
        :param get_current_file: a function that should return the current open file as a :class:`jukeboxcore.filesys.TaskFileInfo`
        :type get_current_file: func|None
        :param parent: Optional - the parent of the window - default is None
        :type parent: QWidget
        :raises: None
        """
        super(FileBrowser, self).__init__(parent)
        self._filetype = filetype
        self._releasetypes = releasetypes
        # Map releasetypes to radiobuttons
        self._releasetype_button_mapping = {}
        self.get_current_file = get_current_file
        self.setupUi(self)
        self.setup_ui()
        self.setup_signals()

        self.prjbrws.set_model(self.create_prj_model())
        if get_current_file:
            self.set_to_current()
        else:
            self.init_selection()

    def init_selection(self):
        """Call selection changed in the beginning, so signals get emitted once

        Emit shot_taskfile_sel_changed signal and asset_taskfile_sel_changed.

        :returns: None
        :raises: None
        """
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

    def setup_ui(self, ):
        """Create the browsers and all necessary ui elements for the tool

        :returns: None
        :rtype: None
        :raises: None
        """
        self.prjbrws = self.create_prj_browser()
        self.shotbrws = self.create_shot_browser()
        self.shotverbrws = self.create_ver_browser(self.shot_browser_vbox)
        self.shotcommentbrws = self.create_comment_browser(self.shot_info_hbox)
        self.assetbrws = self.create_asset_browser()
        self.assetverbrws = self.create_ver_browser(self.asset_browser_vbox)
        self.assetcommentbrws = self.create_comment_browser(self.asset_info_hbox)
        self.current_pb = self.create_current_pb()
        self.current_pb.setVisible(bool(self.get_current_file))
        self.shot_info_mapper = QtGui.QDataWidgetMapper()
        self.asset_info_mapper = QtGui.QDataWidgetMapper()
        self.setup_releasetype_buttons()
        self.setup_icons()

    def setup_releasetype_buttons(self, ):
        """Create a radio button for every releasetype

        :returns: None
        :rtype: None
        :raises: None
        """
        # we insert the radiobuttons instead of adding them
        # because there is already a spacer in the layout to
        # keep the buttons to the left. To maintain the original order
        # we insert them all to position 0 but in reversed order
        for rt in reversed(self._releasetypes):
            rb = QtGui.QRadioButton(rt)
            self.releasetype_hbox.insertWidget(0, rb)
            self._releasetype_button_mapping[rt] = rb
        # set first radiobutton checked
        if self._releasetypes:
            rt = self._releasetypes[0]
            rb = self._releasetype_button_mapping[rt]
            rb.setChecked(True)
        # if there is only one releasetype hide the buttons
        if len(self._releasetypes) == 1:
            self.releasetype_widget.setVisible(False)

    def setup_icons(self, ):
        """Set all icons on buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        folder_icon = get_icon('glyphicons_144_folder_open.png', asicon=True)
        self.asset_open_path_tb.setIcon(folder_icon)
        self.shot_open_path_tb.setIcon(folder_icon)

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
        for rb in self._releasetype_button_mapping.values():
            rb.toggled.connect(self.releasetype_btn_toggled)

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

        self.current_pb.clicked.connect(self.set_to_current)
        self.asset_open_path_tb.clicked.connect(self.open_asset_path)
        self.shot_open_path_tb.clicked.connect(self.open_shot_path)

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
        pb = QtGui.QPushButton("Select current")
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

    def releasetype_btn_toggled(self, checked):
        """Callback for when a certain releasetype is toggled

        If the button is checked, update browsers

        :param checked: the state of the button
        :type checked: bool
        :returns: None
        :rtype: None
        :raises: None
        """
        if checked:
            self.update_browsers()

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
            self.assetbrws.set_model(None)
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
        # nothing changed. we can return.
        # I noticed that when you set the model the very first time to None
        # it printed a message:
        # QObject::connect: Cannot connect (null)::dataChanged(QModelIndex,QModelIndex) to
        # QDataWidgetMapper::_q_dataChanged(QModelIndex,QModelIndex)
        # QObject::connect: Cannot connect (null)::destroyed() to
        # QDataWidgetMapper::_q_modelDestroyed()
        # I don't know exactly why. But these two lines get rid of the message and outcome is the same
        if not mapper.model() and not model:
            return

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
        for rt, rb in self._releasetype_button_mapping.items():
            if rb.isChecked():
                return rt

    def asset_ver_sel_changed(self, index):
        """Callback for when the version selection has changed

        Emit asset_taskfile_sel_changed signal.

        :param index: the selected index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        taskfile = None
        if index.isValid():
            item = index.internalPointer()
            taskfile = item.internal_data()
        self.asset_taskfile_sel_changed.emit(taskfile)

    def shot_ver_sel_changed(self, index):
        """Callback for when the version selection has changed

        Emit shot_taskfile_sel_changed signal.

        :param index: the selected index
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        taskfile = None
        if index.isValid():
            item = index.internalPointer()
            taskfile = item.internal_data()
        self.shot_taskfile_sel_changed.emit(taskfile)

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
        self._releasetype_button_mapping[releasetype].setChecked(True)

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
            browser.model.insertRow(0, ditem, parent)
        self.set_level(browser, 3, [tfi.descriptor])

    def open_asset_path(self, *args, **kwargs):
        """Open the currently selected asset in the filebrowser

        :returns: None
        :rtype: None
        :raises: None
        """
        f = self.asset_path_le.text()
        d = os.path.dirname(f)
        osinter = get_interface()
        osinter.open_path(d)

    def open_shot_path(self, *args, **kwargs):
        """Open the currently selected shot in the filebrowser

        :returns: None
        :rtype: None
        :raises: None
        """
        f = self.shot_path_le.text()
        d = os.path.dirname(f)
        osinter = get_interface()
        osinter.open_path(d)

    def get_current_selection(self, i=None):
        """Get the :class:`TaskFileInfo` for the file selected in the active tab

        :param i: If None, returns selection of active tab. If 0, assetselection. If 1, shotselection
        :type i:
        :returns: The taskfile info in the currently active tab
        :rtype: :class:`TaskFileInfo` | None
        :raises: None
        """
        taskfile = None
        if (i is None and self.selection_tabw.currentIndex() == 0) or (i is not None and i == 0):
            indexes = self.assetverbrws.selected_indexes(0)
            if indexes and indexes[0].isValid():
                item = indexes[0].internalPointer()
                taskfile = item.internal_data()
        elif (i is None and self.selection_tabw.currentIndex() == 1) or (i is not None and i == 1):
            indexes = self.shotverbrws.selected_indexes(0)
            if indexes and indexes[0].isValid():
                item = indexes[0].internalPointer()
                taskfile = item.internal_data()
        return taskfile
