from PySide import QtGui

from jukeboxcore.log import get_logger
log = get_logger(__name__)

from jukeboxcore import djadapter
from jukeboxcore.gui.main import JB_MainWindow, JB_Dialog, dt_to_qdatetime
from jukeboxcore.gui import treemodel
from jukeboxcore.gui import djitemdata
from jukeboxcore.plugins import JB_CoreStandaloneGuiPlugin
from jukeboxcore.gui.widgets.guerillamgmt_ui import Ui_guerillamgmt_mwin
from jukeboxcore.gui.widgets.guerilla.projectcreator_ui import Ui_projectcreator_dialog
from jukeboxcore.gui.widgets.guerilla.seqcreator_ui import Ui_seqcreator_dialog
from jukeboxcore.gui.widgets.guerilla.atypecreator_ui import Ui_atypecreator_dialog
from jukeboxcore.gui.widgets.guerilla.atypeadder_ui import Ui_atypeadder_dialog
from jukeboxcore.gui.widgets.guerilla.depcreator_ui import Ui_depcreator_dialog
from jukeboxcore.gui.widgets.guerilla.depadder_ui import Ui_depadder_dialog


class ProjectCreatorDialog(JB_Dialog, Ui_projectcreator_dialog):
    """A Dialog to create a project
    """

    def __init__(self, parent=None, flags=0):
        """Initialize a new project creator dialog

        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(ProjectCreatorDialog, self).__init__(parent, flags)
        self.project = None
        self.setupUi(self)
        self.create_pb.clicked.connect(self.create_prj)

    def create_prj(self, ):
        """Create a project and store it in the self.project

        :returns: None
        :rtype: None
        :raises: None
        """
        name = self.name_le.text()
        short = self.short_le.text()
        path = self.path_le.text()
        semester = self.semester_le.text()
        try:
            prj = djadapter.models.Project(name=name, short=short, path=path, semester=semester)
            prj.save()
            self.project = prj
            self.accept()
        except:
            log.exception("Could not create new project")


class SequenceCreatorDialog(JB_Dialog, Ui_seqcreator_dialog):
    """A Dialog to create a sequence
    """

    def __init__(self, project, parent=None, flags=0):
        """Initialize a new sequence creator dialog

        :param project: The project for the sequence
        :type project: :class:`jukeboxcore.djadapter.models.Project`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(SequenceCreatorDialog, self).__init__(parent, flags)
        self._project = project
        self.sequence = None
        self.setupUi(self)
        self.create_pb.clicked.connect(self.create_seq)

    def create_seq(self, ):
        """Create a sequence and store it in the self.sequence

        :returns: None
        :rtype: None
        :raises: None
        """
        name = self.name_le.text()
        desc = self.desc_pte.toPlainText()
        try:
            seq = djadapter.models.Sequence(name=name, project=self._project, description=desc)
            seq.save()
            self.sequence = seq
            self.accept()
        except:
            log.exception("Could not create new sequence")


class AtypeCreatorDialog(JB_Dialog, Ui_atypecreator_dialog):
    """A Dialog to create a atype
    """

    def __init__(self, projects=None, parent=None, flags=0):
        """Initialize a new atype creator dialog

        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(AtypeCreatorDialog, self).__init__(parent, flags)
        self.projects = projects or []
        self.atype = None
        self.setupUi(self)
        self.create_pb.clicked.connect(self.create_atype)

    def create_atype(self, ):
        """Create a atype and store it in the self.atype

        :returns: None
        :rtype: None
        :raises: None
        """
        name = self.name_le.text()
        desc = self.desc_pte.toPlainText()
        try:
            atype = djadapter.models.Atype(name=name, description=desc)
            atype.save()
            for prj in self.projects:
                atype.projects.add(prj)
            self.atype = atype
            self.accept()
        except:
            log.exception("Could not create new assettype")


class AtypeAdderDialog(JB_Dialog, Ui_atypeadder_dialog):
    """A Dialog to add atype to a project
    """

    def __init__(self, project, parent=None, flags=0):
        """Initialize a new atype creator dialog

        :param project: The project for the atypes
        :type project: :class:`jukeboxcore.djadapter.models.Project`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(AtypeAdderDialog, self).__init__(parent, flags)
        self._project = project
        self.atypes = []
        self.setupUi(self)
        self.add_pb.clicked.connect(self.add_atype)

        rootdata = treemodel.ListItemData(["Name", "Description"])
        rootitem = treemodel.TreeItem(rootdata)
        atypes = djadapter.atypes.exclude(projects=project)
        for atype in atypes:
            atypedata = djitemdata.AtypeItemData(atype)
            treemodel.TreeItem(atypedata, rootitem)
        self.model = treemodel.TreeModel(rootitem)
        self.atype_tablev.setModel(self.model)

    def add_atype(self, ):
        """Add a atype and store it in the self.atypes

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.atype_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            atype = item.internal_data()
            atype.projects.add(self._project)
            self.atypes.append(atype)
            item.set_parent(None)


class DepCreatorDialog(JB_Dialog, Ui_depcreator_dialog):
    """A Dialog to create a dep
    """

    def __init__(self, projects=None, parent=None, flags=0):
        """Initialize a new dep creator dialog

        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(DepCreatorDialog, self).__init__(parent, flags)
        self.projects = projects or []
        self.dep = None
        self.setupUi(self)
        self.create_pb.clicked.connect(self.create_dep)

    def create_dep(self, ):
        """Create a dep and store it in the self.dep

        :returns: None
        :rtype: None
        :raises: None
        """
        name = self.name_le.text()
        short = self.short_le.text()
        assetflag = self.asset_rb.isChecked()
        ordervalue = self.ordervalue_sb.value()
        desc = self.desc_pte.toPlainText()
        try:
            dep = djadapter.models.Department(name=name, short=short, assetflag=assetflag, ordervalue=ordervalue, description=desc)
            dep.save()
            for prj in self.projects:
                dep.projects.add(prj)
            self.dep = dep
            self.accept()
        except:
            log.exception("Could not create new department.")


class DepAdderDialog(JB_Dialog, Ui_depadder_dialog):
    """A Dialog to add departments to a project
    """

    def __init__(self, project, parent=None, flags=0):
        """Initialize a new dep creator dialog

        :param project: The project for the deps
        :type project: :class:`jukeboxcore.djadapter.models.Project`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(DepAdderDialog, self).__init__(parent, flags)
        self._project = project
        self.deps = []
        self.setupUi(self)
        self.add_pb.clicked.connect(self.add_dep)

        rootdata = treemodel.ListItemData(["Name", "Description", "Ordervalue"])
        rootitem = treemodel.TreeItem(rootdata)
        deps = djadapter.departments.exclude(projects=project)
        for dep in deps:
            depdata = djitemdata.DepartmentItemData(dep)
            treemodel.TreeItem(depdata, rootitem)
        self.model = treemodel.TreeModel(rootitem)
        self.dep_tablev.setModel(self.model)

    def add_dep(self, ):
        """Add a dep and store it in the self.deps

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.dep_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            dep = item.internal_data()
            dep.projects.add(self._project)
            self.deps.append(dep)
            item.set_parent(None)


class GuerillaMGMTWin(JB_MainWindow, Ui_guerillamgmt_mwin):
    """A tool for creating entries in the database and a little project management.
    """

    def __init__(self, parent=None, flags=0):
        """Initialize a new GuerillaMGMTwin

        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(GuerillaMGMTWin, self).__init__(parent, flags)
        self.cur_prj = None
        self.cur_seq = None
        self.cur_shot = None
        self.cur_atype = None
        self.cur_asset = None
        self.cur_dep = None
        self.cur_task = None
        self.cur_user = None

        self.setupUi(self)
        self.setup_ui()
        try:
            self.setup_signals()
        except:
            log.exception("Exception setting up signals")

    def setup_ui(self, ):
        """Create all necessary ui elements for the tool

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up the ui")
        self.setup_prjs_page()
        self.setup_prj_page()
        self.setup_seq_page()
        self.setup_shot_page()
        self.setup_atype_page()
        self.setup_asset_page()
        self.setup_dep_page()
        self.setup_task_page()
        self.setup_users_page()
        self.setup_user_page()

    def setup_prjs_page(self, ):
        """Create and set the model on the projects page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.prjs_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        log.debug("Loading projects for projects page.")
        rootdata = treemodel.ListItemData(['Name', 'Short', 'Path', 'Created', 'Semester', 'Status', 'Resolution', 'FPS', 'Scale'])
        rootitem = treemodel.TreeItem(rootdata)
        prjs = djadapter.projects.all()
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, rootitem)
        self.prjs_model = treemodel.TreeModel(rootitem)
        self.prjs_tablev.setModel(self.prjs_model)

    def setup_prj_page(self, ):
        """Create and set the model on the project page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.prj_seq_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.prj_atype_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.prj_dep_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.prj_user_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_seq_page(self, ):
        """Create and set the model on the sequence page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.seq_shot_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_shot_page(self, ):
        """Create and set the model on the shot page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.shot_asset_treev.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.shot_task_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_atype_page(self, ):
        """Create and set the model on the atype page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.atype_prj_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_asset_page(self, ):
        """Create and set the model on the asset page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.asset_asset_treev.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.asset_task_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_dep_page(self, ):
        """Create and set the model on the department page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.dep_prj_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_task_page(self, ):
        """Create and set the model on the task page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.task_user_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_users_page(self, ):
        """Create and set the model on the users page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.users_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        log.debug("Loading users for users page.")
        rootdata = treemodel.ListItemData(['Username', 'First', 'Last', 'Email'])
        rootitem = treemodel.TreeItem(rootdata)
        users = djadapter.users.all()
        for usr in users:
            usrdata = djitemdata.UserItemData(usr)
            treemodel.TreeItem(usrdata, rootitem)
        self.users_model = treemodel.TreeModel(rootitem)
        self.users_tablev.setModel(self.users_model)

    def setup_user_page(self, ):
        """Create and set the model on the user page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.user_prj_tablev.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.user_task_treev.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up signals.")
        self.setup_prjs_signals()
        self.setup_prj_signals()
        self.setup_seq_signals()
        self.setup_shot_signals()
        self.setup_atype_signals()
        self.setup_asset_signals()
        self.setup_dep_signals()
        self.setup_task_signals()
        self.setup_users_signals()
        self.setup_user_signals()
        log.debug("Signals are set up.")

    def setup_prjs_signals(self, ):
        """Setup the signals for the projects page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up projects page signals.")
        self.prjs_prj_view_pb.clicked.connect(self.prjs_view_prj)
        self.prjs_prj_create_pb.clicked.connect(self.prjs_create_prj)

    def setup_prj_signals(self, ):
        """Setup the signals for the project page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up project page signals.")
        self.prj_seq_view_pb.clicked.connect(self.prj_view_seq)
        self.prj_seq_create_pb.clicked.connect(self.prj_create_seq)
        self.prj_atype_view_pb.clicked.connect(self.prj_view_atype)
        self.prj_atype_add_pb.clicked.connect(self.prj_add_atype)
        self.prj_atype_create_pb.clicked.connect(self.prj_create_atype)
        self.prj_dep_view_pb.clicked.connect(self.prj_view_dep)
        self.prj_dep_add_pb.clicked.connect(self.prj_add_dep)
        self.prj_dep_create_pb.clicked.connect(self.prj_create_dep)
        self.prj_user_view_pb.clicked.connect(self.prj_view_user)
        self.prj_user_add_pb.clicked.connect(self.prj_add_user)
        self.prj_user_create_pb.clicked.connect(self.prj_create_user)
        self.prj_path_view_pb.clicked.connect(self.prj_show_path)
        self.prj_desc_pte.textChanged.connect(self.prj_save)
        self.prj_semester_le.editingFinished.connect(self.prj_save)
        self.prj_fps_dsb.valueChanged.connect(self.prj_save)
        self.prj_res_x_sb.valueChanged.connect(self.prj_save)
        self.prj_res_y_sb.valueChanged.connect(self.prj_save)
        self.prj_scale_cb.currentIndexChanged.connect(self.prj_save)

    def setup_seq_signals(self, ):
        """Setup the signals for the sequence page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up sequence page signals.")
        self.seq_project_view_pb.clicked.connect(self.seq_view_prj)
        self.seq_shot_view_pb.clicked.connect(self.seq_view_shot)
        self.seq_shot_create_pb.clicked.connect(self.seq_create_shot)
        self.seq_desc_pte.textChanged.connect(self.seq_save)

    def setup_shot_signals(self, ):
        """Setup the signals for the shot page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up shot page signals.")
        self.shot_prj_view_pb.clicked.connect(self.shot_view_prj)
        self.shot_seq_view_pb.clicked.connect(self.shot_view_seq)
        self.shot_task_view_pb.clicked.connect(self.shot_view_task)
        self.shot_task_create_pb.clicked.connect(self.shot_create_task)
        self.shot_asset_view_pb.clicked.connect(self.shot_view_asset)
        self.shot_asset_create_pb.clicked.connect(self.shot_create_asset)
        self.shot_asset_add_pb.clicked.connect(self.shot_add_asset)
        self.shot_asset_remove_pb.clicked.connect(self.shot_remove_asset)
        self.shot_start_sb.valueChanged.connect(self.shot_save)
        self.shot_end_sb.valueChanged.connect(self.shot_save)
        self.shot_handle_sb.valueChanged.connect(self.shot_save)
        self.shot_desc_pte.textChanged.connect(self.shot_save)

    def setup_atype_signals(self, ):
        """Setup the signals for the assettype page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up atype page signals.")
        self.asset_prj_view_pb.clicked.connect(self.asset_view_prj)
        self.asset_atype_view_pb.clicked.connect(self.asset_view_atype)
        self.atype_prj_view_pb.clicked.connect(self.atype_view_prj)
        self.atype_prj_add_pb.clicked.connect(self.atype_add_prj)
        self.atype_prj_create_pb.clicked.connect(self.atype_create_prj)
        self.atype_desc_pte.textChanged.connect(self.atype_save)

    def setup_asset_signals(self, ):
        """Setup the signals for the asset page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up asset signals.")
        self.asset_asset_view_pb.clicked.connect(self.asset_view_asset)
        self.asset_asset_create_pb.clicked.connect(self.asset_create_asset)
        self.asset_asset_add_pb.clicked.connect(self.asset_add_asset)
        self.asset_asset_remove_pb.clicked.connect(self.asset_remove_asset)
        self.asset_task_view_pb.clicked.connect(self.asset_view_task)
        self.asset_task_create_pb.clicked.connect(self.asset_create_task)
        self.asset_desc_pte.textChanged.connect(self.asset_save)

    def setup_dep_signals(self, ):
        """Setup the signals for the department page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up department page signals.")
        self.dep_prj_view_pb.clicked.connect(self.dep_view_prj)
        self.dep_prj_add_pb.clicked.connect(self.dep_add_prj)
        self.dep_prj_remove_pb.clicked.connect(self.dep_remove_prj)
        self.dep_desc_pte.textChanged.connect(self.dep_save)
        self.dep_ordervalue_sb.valueChanged.connect(self.dep_save)

    def setup_task_signals(self, ):
        """Setup the signals for the task page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up task page signals.")
        self.task_user_view_pb.clicked.connect(self.task_view_user)
        self.task_user_add_pb.clicked.connect(self.task_add_user)
        self.task_user_remove_pb.clicked.connect(self.task_remove_user)
        self.task_dep_view_pb.clicked.connect(self.task_view_dep)
        self.task_link_view_pb.clicked.connect(self.task_view_link)
        self.task_deadline_de.dateChanged.connect(self.task_save)
        self.task_status_cb.currentIndexChanged.connect(self.task_save)

    def setup_users_signals(self, ):
        """Setup the signals for the users page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up users page signals.")
        self.users_user_view_pb.clicked.connect(self.users_view_user)
        self.users_user_create_pb.clicked.connect(self.users_create_user)

    def setup_user_signals(self, ):
        """Setup the signals for the user page

        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug("Setting up user page signals.")
        self.user_task_view_pb.clicked.connect(self.user_view_task)
        self.user_prj_view_pb.clicked.connect(self.user_view_prj)
        self.user_prj_add_pb.clicked.connect(self.user_add_prj)
        self.user_prj_remove_pb.clicked.connect(self.user_remove_prj)
        self.user_username_le.editingFinished.connect(self.users_save)
        self.user_first_le.editingFinished.connect(self.users_save)
        self.user_last_le.editingFinished.connect(self.users_save)
        self.user_email_le.editingFinished.connect(self.users_save)

    def prjs_view_prj(self, *args, **kwargs):
        """View the, in the projects table view selected, project.

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.prjs_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            prj = item.internal_data()
            self.view_project(prj)

    def prjs_create_prj(self, *args, **kwargs):
        """Create a new project

        :returns: None
        :rtype: None
        :raises: None
        """
        prj = self.create_prj()
        if prj:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, self.prjs_model.root)

    def view_project(self, prj):
        """View the given project on the project page

        :param prj: the project to view
        :type prj: :class:`jukeboxcore.djadapter.models.Project`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing project %s', prj.name)
        self.cur_prj = prj
        self.pages_tabw.setCurrentIndex(1)
        self.prj_name_le.setText(prj.name)
        self.prj_short_le.setText(prj.short)
        self.prj_path_le.setText(prj.path)
        self.prj_desc_pte.setPlainText(prj.description)
        self.prj_created_dte.setDateTime(dt_to_qdatetime(prj.date_created))
        self.prj_semester_le.setText(prj.semester)
        self.prj_fps_dsb.setValue(prj.framerate)
        self.prj_res_x_sb.setValue(prj.resx)
        self.prj_res_y_sb.setValue(prj.resy)
        scalemap = {"m": 2, "meter": 2, "mm": 0, "millimeter": 0, "cm": 1, "centimeter": 1,
                    "km": 3, "kilometer": 3, "inch": 4, "foot": 5, "yard": 6, "mile": 7}
        scaleindex = scalemap.get(prj.scale, -1)
        log.debug("Setting index of project scale combobox to %s. Scale is %s", scaleindex, prj.scale)
        self.prj_scale_cb.setCurrentIndex(scaleindex)

        seqrootdata = treemodel.ListItemData(['Name', "Description"])
        seqrootitem = treemodel.TreeItem(seqrootdata)
        for seq in prj.sequence_set.all():
            seqdata = djitemdata.SequenceItemData(seq)
            treemodel.TreeItem(seqdata, seqrootitem)
        self.prj_seq_model = treemodel.TreeModel(seqrootitem)
        self.prj_seq_tablev.setModel(self.prj_seq_model)

        atyperootdata = treemodel.ListItemData(['Name', "Description"])
        atyperootitem = treemodel.TreeItem(atyperootdata)
        for atype in prj.atype_set.all():
            atypedata = djitemdata.AtypeItemData(atype)
            treemodel.TreeItem(atypedata, atyperootitem)
        self.prj_atype_model = treemodel.TreeModel(atyperootitem)
        self.prj_atype_tablev.setModel(self.prj_atype_model)

        deprootdata = treemodel.ListItemData(['Name', "Description", "Ordervalue"])
        deprootitem = treemodel.TreeItem(deprootdata)
        for dep in prj.department_set.all():
            depdata = djitemdata.DepartmentItemData(dep)
            treemodel.TreeItem(depdata, deprootitem)
        self.prj_dep_model = treemodel.TreeModel(deprootitem)
        self.prj_dep_tablev.setModel(self.prj_dep_model)

        userrootdata = treemodel.ListItemData(['Username', 'First', 'Last', 'Email'])
        userrootitem = treemodel.TreeItem(userrootdata)
        for user in prj.users.all():
            userdata = djitemdata.UserItemData(user)
            treemodel.TreeItem(userdata, userrootitem)
        self.prj_user_model = treemodel.TreeModel(userrootitem)
        self.prj_user_tablev.setModel(self.prj_user_model)

    def create_prj(self, atypes=None, deps=None):
        """Create and return a new project

        :param atypes: add the given atypes to the project
        :type atypes: list | None
        :param deps: add the given departmetns to the project
        :type deps: list | None
        :returns: The created project or None
        :rtype: None | :class:`jukeboxcore.djadapter.models.Project`
        :raises: None
        """
        dialog = ProjectCreatorDialog(parent=self)
        dialog.exec_()
        prj = dialog.project
        if prj and atypes:
            for at in atypes:
                at.projects.add(prj)
                at.save()
        if prj and deps:
            for dep in deps:
                dep.projects.add(prj)
                dep.save()
        return prj

    def prj_view_seq(self, *args, **kwargs):
        """View the, in the prj_seq_tablev selected, sequence.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        i = self.prj_seq_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            seq = item.internal_data()
            self.view_seq(seq)

    def prj_create_seq(self, *args, **kwargs):
        """Create a new Sequence for the current project

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        seq = self.create_seq(project=self.cur_prj)
        if seq:
            seqdata = djitemdata.SequenceItemData(seq)
            treemodel.TreeItem(seqdata, self.prj_seq_model.root)

    def view_seq(self, seq):
        """View the given sequence on the sequence page

        :param seq: the sequence to view
        :type seq: :class:`jukeboxcore.djadapter.models.Sequence`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing sequence %s', seq.name)
        self.cur_seq = seq
        self.pages_tabw.setCurrentIndex(2)
        self.seq_name_le.setText(seq.name)
        self.seq_prj_le.setText(seq.project.name)
        self.seq_desc_pte.setPlainText(seq.description)

        shotrootdata = treemodel.ListItemData(['Name', "Description", "Duration", "Start", "End"])
        shotrootitem = treemodel.TreeItem(shotrootdata)
        for shot in seq.shot_set.all():
            shotdata = djitemdata.ShotItemData(shot)
            treemodel.TreeItem(shotdata, shotrootitem)
        self.seq_shot_model = treemodel.TreeModel(shotrootitem)
        self.seq_shot_tablev.setModel(self.seq_shot_model)

    def create_seq(self, project):
        """Create and return a new sequence

        :param project: the project for the sequence
        :type deps: :class:`jukeboxcore.djadapter.models.Project`
        :returns: The created sequence or None
        :rtype: None | :class:`jukeboxcore.djadapter.models.Sequence`
        :raises: None
        """
        dialog = SequenceCreatorDialog(project=project, parent=self)
        dialog.exec_()
        seq = dialog.sequence
        return seq

    def prj_view_atype(self, *args, **kwargs):
        """View the, in the atype table view selected, assettype.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        i = self.prj_atype_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            atype = item.internal_data()
            self.view_atype(atype)

    def prj_add_atype(self, *args, **kwargs):
        """Add more assettypes to the project.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        dialog = AtypeAdderDialog(project=self.cur_prj)
        dialog.exec_()
        atypes = dialog.atypes
        for atype in atypes:
            atypedata = djitemdata.AtypeItemData(atype)
            treemodel.TreeItem(atypedata, self.prj_atype_model.root)

    def prj_create_atype(self, *args, **kwargs):
        """Create a new project

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        atype = self.create_atype(projects=[self.cur_prj])
        if atype:
            atypedata = djitemdata.AtypeItemData(atype)
            treemodel.TreeItem(atypedata, self.prj_atype_model.root)

    def create_atype(self, projects):
        """Create and return a new atype

        :param projects: the projects for the atype
        :type projects: :class:`jukeboxcore.djadapter.models.Project`
        :returns: The created atype or None
        :rtype: None | :class:`jukeboxcore.djadapter.models.Atype`
        :raises: None
        """
        dialog = AtypeCreatorDialog(projects=projects, parent=self)
        dialog.exec_()
        atype = dialog.atype
        return atype

    def view_atype(self, atype):
        """View the given atype on the atype page

        :param atype: the atype to view
        :type atype: :class:`jukeboxcore.djadapter.models.Atype`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing atype %s', atype.name)
        self.cur_atype = atype
        self.pages_tabw.setCurrentIndex(4)
        self.atype_name_le.setText(atype.name)
        self.atype_desc_pte.setPlainText(atype.description)

        rootdata = treemodel.ListItemData(['Name', 'Short', 'Path', 'Created', 'Semester', 'Status', 'Resolution', 'FPS', 'Scale'])
        rootitem = treemodel.TreeItem(rootdata)
        prjs = atype.projects.all()
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, rootitem)
        self.atype_prj_model = treemodel.TreeModel(rootitem)
        self.atype_prj_tablev.setModel(self.atype_prj_model)

    def prj_view_dep(self, *args, **kwargs):
        """View the, in the dep table view selected, department.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        i = self.prj_dep_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            dep = item.internal_data()
            self.view_dep(dep)

    def prj_add_dep(self, *args, **kwargs):
        """Add more departments to the project.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        dialog = DepAdderDialog(project=self.cur_prj)
        dialog.exec_()
        deps = dialog.deps
        for dep in deps:
            depdata = djitemdata.DepartmentItemData(dep)
            treemodel.TreeItem(depdata, self.prj_dep_model.root)

    def prj_create_dep(self, *args, **kwargs):
        """Create a new project

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        dep = self.create_dep(projects=[self.cur_prj])
        if dep:
            depdata = djitemdata.DepartmentItemData(dep)
            treemodel.TreeItem(depdata, self.prj_dep_model.root)

    def create_dep(self, projects):
        """Create and return a new dep

        :param projects: the projects for the dep
        :type projects: :class:`jukeboxcore.djadapter.models.Project`
        :returns: The created dep or None
        :rtype: None | :class:`jukeboxcore.djadapter.models.Dep`
        :raises: None
        """
        dialog = DepCreatorDialog(projects=projects, parent=self)
        dialog.exec_()
        dep = dialog.dep
        return dep

    def view_dep(self, dep):
        """View the given department on the department page

        :param dep: the dep to view
        :type dep: :class:`jukeboxcore.djadapter.models.Department`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing department %s', dep.name)
        self.cur_dep = dep
        self.pages_tabw.setCurrentIndex(6)
        self.dep_name_le.setText(dep.name)
        self.dep_short_le.setText(dep.short)
        self.dep_shot_rb.setChecked(not dep.assetflag)
        self.dep_asset_rb.setChecked(dep.assetflag)
        self.dep_ordervalue_sb.setValue(dep.ordervalue)
        self.dep_desc_pte.setPlainText(dep.description)

        rootdata = treemodel.ListItemData(['Name', 'Short', 'Path', 'Created', 'Semester', 'Status', 'Resolution', 'FPS', 'Scale'])
        rootitem = treemodel.TreeItem(rootdata)
        prjs = dep.projects.all()
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, rootitem)
        self.dep_prj_model = treemodel.TreeModel(rootitem)
        self.dep_prj_tablev.setModel(self.dep_prj_model)


class GuerillaMGMT(JB_CoreStandaloneGuiPlugin):
    """A plugin that can run a GuerillaMGMT tool

    This can be used as a standalone plugin.
    Before you call run, make sure that there is a running
    QApplication running. See :mod:`jukeboxcore.gui.main` for helpful functions.

    """

    author = "David Zuber"
    copyright = "2015"
    version = "0.1"
    description = "A guerilla tool for projectmanagement and creating entries in the database."

    def init(self, ):
        """Do nothing on init! Call run() if you want to start the configeditor

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    def uninit(self, ):
        """Do nothing on uninit!

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    def run(self, parent=None):
        """Start the configeditor

        :returns: None
        :rtype: None
        :raises: None
        """
        self.gw = GuerillaMGMTWin(parent=parent)
        self.gw.show()
