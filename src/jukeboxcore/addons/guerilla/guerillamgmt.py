from PySide import QtGui

from jukeboxcore.log import get_logger
log = get_logger(__name__)

from jukeboxcore import ostool
from jukeboxcore import djadapter
from jukeboxcore.gui.main import JB_MainWindow, JB_Dialog, dt_to_qdatetime
from jukeboxcore.gui import treemodel
from jukeboxcore.gui import djitemdata
from jukeboxcore.plugins import JB_CoreStandaloneGuiPlugin
from jukeboxcore.gui.widgets.guerillamgmt_ui import Ui_guerillamgmt_mwin
from jukeboxcore.gui.widgets.guerilla.projectcreator_ui import Ui_projectcreator_dialog
from jukeboxcore.gui.widgets.guerilla.prjadder_ui import Ui_prjadder_dialog
from jukeboxcore.gui.widgets.guerilla.seqcreator_ui import Ui_seqcreator_dialog
from jukeboxcore.gui.widgets.guerilla.atypecreator_ui import Ui_atypecreator_dialog
from jukeboxcore.gui.widgets.guerilla.atypeadder_ui import Ui_atypeadder_dialog
from jukeboxcore.gui.widgets.guerilla.depcreator_ui import Ui_depcreator_dialog
from jukeboxcore.gui.widgets.guerilla.depadder_ui import Ui_depadder_dialog
from jukeboxcore.gui.widgets.guerilla.usercreator_ui import Ui_usercreator_dialog
from jukeboxcore.gui.widgets.guerilla.useradder_ui import Ui_useradder_dialog
from jukeboxcore.gui.widgets.guerilla.shotcreator_ui import Ui_shotcreator_dialog
from jukeboxcore.gui.widgets.guerilla.assetcreator_ui import Ui_assetcreator_dialog
from jukeboxcore.gui.widgets.guerilla.assetadder_ui import Ui_assetadder_dialog
from jukeboxcore.gui.widgets.guerilla.taskcreator_ui import Ui_taskcreator_dialog


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


class ProjectAdderDialog(JB_Dialog, Ui_prjadder_dialog):
    """A Dialog to add project to a project
    """

    def __init__(self, atype=None, department=None, user=None, parent=None, flags=0):
        """Initialize a new project creator dialog

        :param atype: the atype to add the project to
        :type atype: :class:`djadapter.models.Atype`
        :param department: the department to add the project to
        :type department: :class:`djadapter.models.Department`
        :param parent: the parent object
        :param user: the user to tadd the project to
        :type user: :class:`djadapter.models.User`
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(ProjectAdderDialog, self).__init__(parent, flags)
        self._atype = atype
        self._dep = department
        self._user = user
        self.projects = []
        self.setupUi(self)
        self.add_pb.clicked.connect(self.add_project)

        rootdata = treemodel.ListItemData(["Name", "Description"])
        rootitem = treemodel.TreeItem(rootdata)

        if atype:
            projects = djadapter.projects.exclude(pk__in = atype.projects.all())
        elif department:
            projects = djadapter.projects.exclude(pk__in = department.projects.all())
        else:
            projects = djadapter.projects.exclude(users=user)
        for project in projects:
            projectdata = djitemdata.ProjectItemData(project)
            treemodel.TreeItem(projectdata, rootitem)
        self.model = treemodel.TreeModel(rootitem)
        self.prj_tablev.setModel(self.model)

    def add_project(self, ):
        """Add a project and store it in the self.projects

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.prj_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            project = item.internal_data()
            if self._atype:
                self._atype.projects.add(project)
            elif self._dep:
                self._dep.projects.add(project)
            else:
                project.users.add(self._user)
            self.projects.append(project)
            item.set_parent(None)


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


class UserCreatorDialog(JB_Dialog, Ui_usercreator_dialog):
    """A Dialog to create a user
    """

    def __init__(self, projects=None, tasks=None, parent=None, flags=0):
        """Initialize a new user creator dialog

        :param projects: The projects for the user
        :type projects: list of :class:`jukeboxcore.djadapter.models.Project`
        :param tasks: The tasks for the user
        :type tasks: list of :class:`jukeboxcore.djadapter.models.Task`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(UserCreatorDialog, self).__init__(parent, flags)
        self.projects = projects or []
        self.tasks = tasks or []
        self.user = None
        self.setupUi(self)
        self.create_pb.clicked.connect(self.create_user)

    def create_user(self, ):
        """Create a user and store it in the self.user

        :returns: None
        :rtype: None
        :raises: None
        """
        name = self.username_le.text()
        if not name:
            self.username_le.setPlaceholderText("Please provide a username.")
            return
        first = self.first_le.text()
        last = self.last_le.text()
        email = self.email_le.text()
        try:
            user = djadapter.models.User(username=name, first_name=first, last_name=last, email=email)
            user.save()
            for prj in self.projects:
                prj.users.add(user)
            for task in self.tasks:
                task.users.add(user)
            self.user = user
            self.accept()
        except:
            log.exception("Could not create new assettype")


class UserAdderDialog(JB_Dialog, Ui_useradder_dialog):
    """A Dialog to add user to a project
    """

    def __init__(self, project=None, task=None, parent=None, flags=0):
        """Initialize a new user creator dialog

        :param project: The project for the users
        :type project: :class:`jukeboxcore.djadapter.models.Project`
        :param task: The task for the users
        :type task: :class:`jukeboxcore.djadapter.models.Task`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(UserAdderDialog, self).__init__(parent, flags)
        self._project = project
        self._task = task
        self.users = []
        self.setupUi(self)
        self.add_pb.clicked.connect(self.add_user)

        rootdata = treemodel.ListItemData(["Name", "Description"])
        rootitem = treemodel.TreeItem(rootdata)
        if project:
            users = djadapter.users.exclude(project = project)
        else:
            users = djadapter.users.exclude(task = task)
        for user in users:
            userdata = djitemdata.UserItemData(user)
            treemodel.TreeItem(userdata, rootitem)
        self.model = treemodel.TreeModel(rootitem)
        self.user_tablev.setModel(self.model)

    def add_user(self, ):
        """Add a user and store it in the self.users

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.user_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            user = item.internal_data()
            if self._project:
                self._project.users.add(user)
            else:
                self._task.users.add(user)
            self.users.append(user)
            item.set_parent(None)


class ShotCreatorDialog(JB_Dialog, Ui_shotcreator_dialog):
    """A Dialog to create a shot
    """

    def __init__(self, sequence, parent=None, flags=0):
        """Initialize a new shot creator dialog

        :param sequence: the sequence for the shot
        :type sequence: :class:`jukeboxcore.djadapter.models.Shot`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(ShotCreatorDialog, self).__init__(parent, flags)
        self.sequence = sequence
        self.shot = None
        self.setupUi(self)
        self.create_pb.clicked.connect(self.create_shot)

    def create_shot(self, ):
        """Create a shot and store it in the self.shot

        :returns: None
        :rtype: None
        :raises: None
        """
        name = self.name_le.text()
        if not name:
            self.name_le.setPlaceholderText("Please enter a name!")
            return
        desc = self.desc_pte.toPlainText()
        try:
            shot = djadapter.models.Shot(sequence=self.sequence, project=self.sequence.project, name=name, description=desc)
            shot.save()
            self.shot = shot
            self.accept()
        except:
            log.exception("Could not create new shot")


class AssetCreatorDialog(JB_Dialog, Ui_assetcreator_dialog):
    """A Dialog to create a asset
    """

    def __init__(self, project=None, atype=None, parent=None, flags=0):
        """Initialize a new asset creator dialog

        :param project: the project of the asset
        :type project: :class:`jukeboxcore.djadapter.models.Project`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(AssetCreatorDialog, self).__init__(parent, flags)
        self.project = project
        self.atype = atype
        self.asset = None
        self.setupUi(self)

        if not self.atype:
            self.atypes = list(project.atype_set.all())
            atrootdata = treemodel.ListItemData(["Name"])
            atrootitem = treemodel.TreeItem(atrootdata)
            for at in self.atypes:
                data = djitemdata.AtypeItemData(at)
                treemodel.TreeItem(data, atrootitem)
            self.atypemodel = treemodel.TreeModel(atrootitem)
            self.atype_cb.setModel(self.atypemodel)
            self.prj_cb.setVisible(False)
            self.prj_lb.setVisible(False)
        else:
            self.projects = list(self.atype.projects.all())
            prjrootdata = treemodel.ListItemData(['Name', 'Short', 'Path', 'Created', 'Semester', 'Status', 'Resolution', 'FPS', 'Scale'])
            prjrootitem = treemodel.TreeItem(prjrootdata)
            for prj in self.projects:
                prjdata = djitemdata.ProjectItemData(prj)
                treemodel.TreeItem(prjdata, prjrootitem)
            self.prjmodel = treemodel.TreeModel(prjrootitem)
            self.prj_cb.setModel(self.prjmodel)
            self.atype_cb.setVisible(False)
            self.atype_lb.setVisible(False)
        self.create_pb.clicked.connect(self.create_asset)

    def create_asset(self, ):
        """Create a asset and store it in the self.asset

        :returns: None
        :rtype: None
        :raises: None
        """
        name = self.name_le.text()
        if not name:
            self.name_le.setPlaceholderText("Please enter a name!")
            return
        desc = self.desc_pte.toPlainText()
        if self.project:
            atypei = self.atype_cb.currentIndex()
            assert atypei >= 0
            self.atype = self.atypes[atypei]
        else:
            prji = self.prj_cb.currentIndex()
            assert prji >= 0
            self.project = self.projects[prji]
        try:
            asset = djadapter.models.Asset(atype=self.atype, project=self.project, name=name, description=desc)
            asset.save()
            self.asset = asset
            self.accept()
        except:
            log.exception("Could not create new asset")


class AssetAdderDialog(JB_Dialog, Ui_assetadder_dialog):
    """A Dialog to add asset to a project
    """

    def __init__(self, shot=None, asset=None, parent=None, flags=0):
        """Initialize a new asset creator dialog

        :param shot: The shot for the assets
        :type shot: :class:`jukeboxcore.djadapter.models.Shot`
        :param asset: The asset for the assets
        :type asset: :class:`jukeboxcore.djadapter.models.Asset`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(AssetAdderDialog, self).__init__(parent, flags)
        self._shot = shot
        self._asset = asset
        self.assets = []
        self.setupUi(self)
        self.add_pb.clicked.connect(self.add_asset)

        rootdata = treemodel.ListItemData(["Name"])
        rootitem = treemodel.TreeItem(rootdata)
        self.model = treemodel.TreeModel(rootitem)
        self.asset_treev.setModel(self.model)
        atypes = {}
        if shot:
            assets = djadapter.assets.exclude(pk__in = shot.assets.all()).filter(project=shot.project)
        else:
            assets = djadapter.assets.exclude(pk__in = asset.assets.all()).filter(project=asset.project)
        for asset in assets:
            atype = asset.atype
            atypeitem = atypes.get(atype)
            if not atypeitem:
                atypedata = djitemdata.AtypeItemData(atype)
                atypeitem = treemodel.TreeItem(atypedata, rootitem)
                atypes[atype] = atypeitem
            assetdata = djitemdata.AssetItemData(asset)
            treemodel.TreeItem(assetdata, atypeitem)

    def add_asset(self, ):
        """Add a asset and store it in the self.assets

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.asset_treev.currentIndex()
        item = i.internalPointer()
        if item:
            asset = item.internal_data()
            if not isinstance(asset, djadapter.models.Asset):
                return
            if self._shot:
                self._shot.assets.add(asset)
            else:
                self._asset.assets.add(asset)
            self.assets.append(asset)
            item.set_parent(None)


class TaskCreatorDialog(JB_Dialog, Ui_taskcreator_dialog):
    """A Dialog to create a task
    """

    def __init__(self, element, parent=None, flags=0):
        """Initialize a new task creator dialog

        :param element: the element for the task
        :type element: :class:`jukeboxcore.djadapter.models.Asset` | :class:`jukeboxcore.djadapter.models.Shot`
        :param parent: the parent object
        :type parent: :class:`QtCore.QObject`
        :param flags: the window flags
        :type flags: :data:`QtCore.Qt.WindowFlags`
        :raises: None
        """
        super(TaskCreatorDialog, self).__init__(parent, flags)
        self.element = element
        self.task = None
        self.setupUi(self)
        self.create_pb.clicked.connect(self.create_task)

        qs = djadapter.departments.filter(projects=element.project).exclude(pk__in = element.tasks.all().values_list('department', flat=True))
        qs = qs.filter(assetflag=isinstance(element, djadapter.models.Asset))
        self.deps = list(qs)

        atrootdata = treemodel.ListItemData(["Name"])
        atrootitem = treemodel.TreeItem(atrootdata)
        for dep in self.deps:
            data = djitemdata.DepartmentItemData(dep)
            treemodel.TreeItem(data, atrootitem)
        self.model = treemodel.TreeModel(atrootitem)
        self.dep_cb.setModel(self.model)

    def create_task(self, ):
        """Create a task and store it in the self.task

        :returns: None
        :rtype: None
        :raises: None
        """
        depi = self.dep_cb.currentIndex()
        assert depi >= 0
        dep = self.deps[depi]
        deadline = self.deadline_de.dateTime().toPython()
        try:
            task = djadapter.models.Task(department=dep, project=self.element.project, element=self.element, deadline=deadline)
            task.save()
            self.task = task
            self.accept()
        except:
            log.exception("Could not create new task")


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
        self.prj_user_remove_pb.clicked.connect(self.prj_remove_user)
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
        self.seq_prj_view_pb.clicked.connect(self.seq_view_prj)
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
        self.shot_asset_view_pb.clicked.connect(self.shot_view_asset)
        self.shot_asset_create_pb.clicked.connect(self.shot_create_asset)
        self.shot_asset_add_pb.clicked.connect(self.shot_add_asset)
        self.shot_asset_remove_pb.clicked.connect(self.shot_remove_asset)
        self.shot_task_view_pb.clicked.connect(self.shot_view_task)
        self.shot_task_create_pb.clicked.connect(self.shot_create_task)
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
        self.atype_asset_view_pb.clicked.connect(self.atype_view_asset)
        self.atype_asset_create_pb.clicked.connect(self.atype_create_asset)
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
        self.users_user_create_pb.clicked.connect(self.create_user)

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
        self.user_username_le.editingFinished.connect(self.user_save)
        self.user_first_le.editingFinished.connect(self.user_save)
        self.user_last_le.editingFinished.connect(self.user_save)
        self.user_email_le.editingFinished.connect(self.user_save)

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
            self.view_prj(prj)

    def prjs_create_prj(self, *args, **kwargs):
        """Create a new project

        :returns: None
        :rtype: None
        :raises: None
        """
        self.create_prj()

    def view_prj(self, prj):
        """View the given project on the project page

        :param prj: the project to view
        :type prj: :class:`jukeboxcore.djadapter.models.Project`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing project %s', prj.name)
        self.cur_prj = None
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
        self.cur_prj = prj

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
        if prj:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, self.prjs_model.root)
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
        self.cur_seq = None
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
        self.cur_seq = seq

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
        self.cur_atype = None
        self.pages_tabw.setCurrentIndex(4)
        self.atype_name_le.setText(atype.name)
        self.atype_desc_pte.setPlainText(atype.description)

        prjrootdata = treemodel.ListItemData(['Name', 'Short', 'Path', 'Created', 'Semester', 'Status', 'Resolution', 'FPS', 'Scale'])
        prjrootitem = treemodel.TreeItem(prjrootdata)
        prjs = atype.projects.all()
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, prjrootitem)
        self.atype_prj_model = treemodel.TreeModel(prjrootitem)
        self.atype_prj_tablev.setModel(self.atype_prj_model)

        assetrootdata = treemodel.ListItemData(['Name', 'Description'])
        assetrootitem = treemodel.TreeItem(assetrootdata)
        self.atype_asset_model = treemodel.TreeModel(assetrootitem)
        self.atype_asset_treev.setModel(self.atype_asset_model)
        prjs = atype.projects.all()
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            prjitem = treemodel.TreeItem(prjdata, assetrootitem)
            for a in djadapter.assets.filter(project=prj, atype=atype):
                assetdata = djitemdata.AssetItemData(a)
                treemodel.TreeItem(assetdata, prjitem)

        self.cur_atype = atype

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
        self.cur_dep = None
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

        self.cur_dep = dep

    def prj_view_user(self, *args, **kwargs):
        """View the, in the user table view selected, user.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        i = self.prj_user_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            user = item.internal_data()
            self.view_user(user)

    def prj_add_user(self, *args, **kwargs):
        """Add more users to the project.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        dialog = UserAdderDialog(project=self.cur_prj)
        dialog.exec_()
        users = dialog.users
        for user in users:
            userdata = djitemdata.UserItemData(user)
            treemodel.TreeItem(userdata, self.prj_user_model.root)
        self.cur_prj.save()

    def prj_remove_user(self, *args, **kwargs):
        """Remove the, in the user table view selected, user.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        i = self.prj_user_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            user = item.internal_data()
            log.debug("Removing user %s.", user.username)
            item.set_parent(None)
            self.cur_prj.users.remove(user)

    def prj_create_user(self, *args, **kwargs):
        """Create a new project

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return
        user = self.create_user(projects=[self.cur_prj])
        if user:
            userdata = djitemdata.UserItemData(user)
            treemodel.TreeItem(userdata, self.prj_user_model.root)

    def create_user(self, projects=None, tasks=None):
        """Create and return a new user

        :param projects: the projects for the user
        :type projects: list of :class:`jukeboxcore.djadapter.models.Project`
        :param tasks: the tasks for the user
        :type tasks: list of :class:`jukeboxcore.djadapter.models.Task`
        :returns: The created user or None
        :rtype: None | :class:`jukeboxcore.djadapter.models.User`
        :raises: None
        """
        projects = projects or []
        tasks = tasks or []
        dialog = UserCreatorDialog(projects=projects, tasks=tasks, parent=self)
        dialog.exec_()
        user = dialog.user
        if user:
            userdata = djitemdata.UserItemData(user)
            treemodel.TreeItem(userdata, self.users_model.root)
        return user

    def view_user(self, user):
        """View the given user on the user page

        :param user: the user to view
        :type user: :class:`jukeboxcore.djadapter.models.User`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing user %s', user.username)
        self.cur_user = None
        self.pages_tabw.setCurrentIndex(9)
        self.user_username_le.setText(user.username)
        self.user_first_le.setText(user.first_name)
        self.user_last_le.setText(user.last_name)
        self.user_email_le.setText(user.email)

        prjrootdata = treemodel.ListItemData(['Name', 'Short', 'Path', 'Created', 'Semester', 'Status', 'Resolution', 'FPS', 'Scale'])
        prjrootitem = treemodel.TreeItem(prjrootdata)
        prjs = djadapter.projects.filter(users=user)
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, prjrootitem)
        self.user_prj_model = treemodel.TreeModel(prjrootitem)
        self.user_prj_tablev.setModel(self.user_prj_model)

        taskrootdata = treemodel.ListItemData(['Name'])
        taskrootitem = treemodel.TreeItem(taskrootdata)
        self.user_task_model = treemodel.TreeModel(taskrootitem)
        self.user_task_treev.setModel(self.user_task_model)
        tasks = djadapter.tasks.filter(users=user)
        assets = {}
        shots = {}
        atypes = {}
        seqs = {}
        prjs = {}
        for t in tasks:
            tdata = djitemdata.TaskItemData(t)
            titem = treemodel.TreeItem(tdata)
            e = t.element
            if isinstance(e, djadapter.models.Asset):
                eitem = assets.get(e)
                if not eitem:
                    edata = djitemdata.AssetItemData(e)
                    eitem = treemodel.TreeItem(edata)
                    assets[e] = eitem
                egrp = e.atype
                egrpitem = atypes.get(egrp)
                if not egrpitem:
                    egrpdata = djitemdata.AtypeItemData(egrp)
                    egrpitem = treemodel.TreeItem(egrpdata)
                    atypes[egrp] = egrpitem
            else:
                eitem = shots.get(e)
                if not eitem:
                    edata = djitemdata.ShotItemData(e)
                    eitem = treemodel.TreeItem(edata)
                    shots[e] = eitem
                egrp = e.sequence
                egrpitem = seqs.get(egrp)
                if not egrpitem:
                    egrpdata = djitemdata.SequenceItemData(egrp)
                    egrpitem = treemodel.TreeItem(egrpdata)
                    seqs[egrp] = egrpitem
            if eitem not in egrpitem.childItems:
                eitem.set_parent(egrpitem)
            prj = egrp.project
            prjitem = prjs.get(prj)
            if not prjitem:
                prjdata = djitemdata.ProjectItemData(prj)
                prjitem = treemodel.TreeItem(prjdata, taskrootitem)
                prjs[prj] = prjitem
                assetdata = treemodel.ListItemData(["Asset"])
                assetitem = treemodel.TreeItem(assetdata, prjitem)
                shotdata = treemodel.ListItemData(["Shot"])
                shotitem = treemodel.TreeItem(shotdata, prjitem)
            else:
                assetitem = prjitem.child(0)
                shotitem = prjitem.child(1)
            if isinstance(egrp, djadapter.models.Atype) and egrpitem not in assetitem.childItems:
                egrpitem.set_parent(assetitem)
            elif isinstance(egrp, djadapter.models.Sequence) and egrpitem not in shotitem.childItems:
                egrpitem.set_parent(shotitem)
            titem.set_parent(eitem)

        self.cur_user = user

    def prj_show_path(self, ):
        """Show the dir in the a filebrowser of the project

        :returns: None
        :rtype: None
        :raises: None
        """
        f = self.prj_path_le.text()
        osinter = ostool.get_interface()
        osinter.open_path(f)

    def prj_save(self):
        """Save the current project

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_prj:
            return

        desc = self.prj_desc_pte.toPlainText()
        semester = self.prj_semester_le.text()
        fps = self.prj_fps_dsb.value()
        resx = self.prj_res_x_sb.value()
        resy = self.prj_res_y_sb.value()
        scale = self.prj_scale_cb.currentText()
        self.cur_prj.description = desc
        self.cur_prj.semester = semester
        self.cur_prj.framerate = fps
        self.cur_prj.resx = resx
        self.cur_prj.resy = resy
        self.cur_prj.scale = scale
        self.cur_prj.save()

    def seq_save(self):
        """Save the current sequence

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_seq:
            return

        desc = self.seq_desc_pte.toPlainText()
        self.cur_seq.description = desc
        self.cur_seq.save()

    def seq_view_prj(self, ):
        """View the project or the current sequence

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_seq:
            return
        self.view_prj(self.cur_seq.project)

    def seq_view_shot(self, ):
        """View the shot that is selected in the table view of the sequence page

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_seq:
            return
        i = self.seq_shot_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            shot = item.internal_data()
            self.view_shot(shot)

    def seq_create_shot(self, *args, **kwargs):
        """Create a new shot

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_seq:
            return
        shot = self.create_shot(sequence=self.cur_seq)
        if shot:
            shotdata = djitemdata.ShotItemData(shot)
            treemodel.TreeItem(shotdata, self.seq_shot_model.root)

    def view_shot(self, shot):
        """View the given shot

        :param shot: the shot to view
        :type shot: :class:`jukeboxcore.djadapter.models.Shot`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing shot %s', shot.name)
        self.cur_shot = None
        self.pages_tabw.setCurrentIndex(3)
        self.shot_name_le.setText(shot.name)
        self.shot_prj_le.setText(shot.project.name)
        self.shot_seq_le.setText(shot.sequence.name)
        self.shot_start_sb.setValue(shot.startframe)
        self.shot_end_sb.setValue(shot.endframe)
        self.shot_handle_sb.setValue(shot.handlesize)
        self.shot_desc_pte.setPlainText(shot.description)

        assetsrootdata = treemodel.ListItemData(["Name", "Description"])
        assetsrootitem = treemodel.TreeItem(assetsrootdata)
        self.shot_asset_model = treemodel.TreeModel(assetsrootitem)
        self.shot_asset_treev.setModel(self.shot_asset_model)
        atypes = {}
        assets = shot.assets.all()
        for a in assets:
            atype = a.atype
            atypeitem = atypes.get(atype)
            if not atypeitem:
                atypedata = djitemdata.AtypeItemData(atype)
                atypeitem = treemodel.TreeItem(atypedata, assetsrootitem)
                atypes[atype] = atypeitem
            assetdata = djitemdata.AssetItemData(a)
            treemodel.TreeItem(assetdata, atypeitem)

        tasksrootdata = treemodel.ListItemData(["Name", "Short"])
        tasksrootitem = treemodel.TreeItem(tasksrootdata)
        self.shot_task_model = treemodel.TreeModel(tasksrootitem)
        self.shot_task_tablev.setModel(self.shot_task_model)
        tasks = shot.tasks.all()
        for t in tasks:
            tdata = djitemdata.TaskItemData(t)
            treemodel.TreeItem(tdata, tasksrootitem)

        self.cur_shot = shot

    def create_shot(self, sequence):
        """Create and return a new shot

        :param sequence: the sequence for the shot
        :type sequence: :class:`jukeboxcore.djadapter.models.Sequence`
        :returns: The created shot or None
        :rtype: None | :class:`jukeboxcore.djadapter.models.Shot`
        :raises: None
        """
        dialog = ShotCreatorDialog(sequence=sequence, parent=self)
        dialog.exec_()
        shot = dialog.shot
        return shot

    def shot_view_prj(self, ):
        """View the project of the current shot

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return

        self.view_prj(self.cur_shot.project)

    def shot_view_seq(self, ):
        """View the sequence of the current shot

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return

        self.view_seq(self.cur_shot.sequence)

    def shot_view_task(self, ):
        """View the task that is currently selected on the shot page

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return

        i = self.shot_task_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            task = item.internal_data()
            self.view_task(task)

    def shot_view_asset(self, ):
        """View the task that is currently selected on the shot page

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return

        i = self.shot_asset_treev.currentIndex()
        item = i.internalPointer()
        if item:
            asset = item.internal_data()
            if isinstance(asset, djadapter.models.Asset):
                self.view_asset(asset)

    def shot_create_task(self, *args, **kwargs):
        """Create a new task

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return
        task = self.create_task(element=self.cur_shot)
        if task:
            taskdata = djitemdata.TaskItemData(task)
            treemodel.TreeItem(taskdata, self.shot_task_model.root)

    def create_task(self, element):
        """Create a new task for the given element

        :param element: the element for the task
        :type element: :class:`jukeboxcore.djadapter.models.Shot` | :class:`jukeboxcore.djadapter.models.Asset`
        :returns: None
        :rtype: None
        :raises: None
        """
        dialog = TaskCreatorDialog(element=element, parent=self)
        dialog.exec_()
        task = dialog.task
        return task

    def view_asset(self, asset):
        """View the given asset

        :param asset: the asset to view
        :type asset: :class:`jukeboxcore.djadapter.models.Asset`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing asset %s', asset.name)
        self.cur_asset = None
        self.pages_tabw.setCurrentIndex(5)

        name = asset.name
        prj = asset.project.name
        atype = asset.atype.name
        desc = asset.description
        self.asset_name_le.setText(name)
        self.asset_prj_le.setText(prj)
        self.asset_atype_le.setText(atype)
        self.asset_desc_pte.setPlainText(desc)

        assetsrootdata = treemodel.ListItemData(["Name", "Description"])
        assetsrootitem = treemodel.TreeItem(assetsrootdata)
        self.asset_asset_model = treemodel.TreeModel(assetsrootitem)
        self.asset_asset_treev.setModel(self.asset_asset_model)
        atypes = {}
        assets = asset.assets.all()
        for a in assets:
            atype = a.atype
            atypeitem = atypes.get(atype)
            if not atypeitem:
                atypedata = djitemdata.AtypeItemData(atype)
                atypeitem = treemodel.TreeItem(atypedata, assetsrootitem)
            assetdata = djitemdata.AssetItemData(a)
            treemodel.TreeItem(assetdata, atypeitem)

        tasksrootdata = treemodel.ListItemData(["Name", "Short"])
        tasksrootitem = treemodel.TreeItem(tasksrootdata)
        self.asset_task_model = treemodel.TreeModel(tasksrootitem)
        self.asset_task_tablev.setModel(self.asset_task_model)
        tasks = asset.tasks.all()
        for t in tasks:
            tdata = djitemdata.TaskItemData(t)
            treemodel.TreeItem(tdata, tasksrootitem)

        self.cur_asset = asset

    def shot_add_asset(self, *args, **kwargs):
        """Add more assets to the shot.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return
        dialog = AssetAdderDialog(shot=self.cur_shot)
        dialog.exec_()
        assets = dialog.assets
        atypes = {}
        for c in self.shot_asset_model.root.childItems:
            atypes[c.internal_data()] = c
        for asset in assets:
            atypeitem = atypes.get(asset.atype)
            if not atypeitem:
                atypedata = djitemdata.AtypeItemData(asset.atype)
                atypeitem = treemodel.TreeItem(atypedata, self.shot_asset_model.root)
                atypes[asset.atype] = atypeitem
            assetdata = djitemdata.AssetItemData(asset)
            treemodel.TreeItem(assetdata, atypeitem)
        self.cur_shot.save()

    def shot_remove_asset(self, *args, **kwargs):
        """Remove the, in the asset table view selected, asset.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return
        i = self.shot_asset_treev.currentIndex()
        item = i.internalPointer()
        if item:
            asset = item.internal_data()
            if not isinstance(asset, djadapter.models.Asset):
                return
            log.debug("Removing asset %s.", asset.name)
            item.set_parent(None)
            self.cur_shot.assets.remove(asset)

    def shot_create_asset(self, *args, **kwargs):
        """Create a new shot

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return
        asset = self.create_asset(shot=self.cur_shot)
        if not asset:
            return
        atypes = {}
        for c in self.shot_asset_model.root.childItems:
            atypes[c.internal_data()] = c
        atypeitem = atypes.get(asset.atype)
        if not atypeitem:
            atypedata = djitemdata.AtypeItemData(asset.atype)
            atypeitem = treemodel.TreeItem(atypedata, self.shot_asset_model.root)
            atypes[asset.atype] = atypeitem
        assetdata = djitemdata.AssetItemData(asset)
        treemodel.TreeItem(assetdata, atypeitem)

    def create_asset(self, atype=None, shot=None, asset=None):
        """Create and return a new asset

        :param project: the project for the asset
        :type project: :class:`jukeboxcore.djadapter.models.Project`
        :returns: The created asset or None
        :rtype: None | :class:`jukeboxcore.djadapter.models.Asset`
        :raises: None
        """
        if atype:
            dialog = AssetCreatorDialog(atype=atype, parent=self)
        else:
            element = shot or asset
            project = element.project
            dialog = AssetCreatorDialog(project=project, parent=self)
        dialog.exec_()
        asset = dialog.asset
        if not atype:
            element.assets.add(asset)
        return asset

    def view_task(self, task):
        """View the given task

        :param task: the task to view
        :type task: :class:`jukeboxcore.djadapter.models.Task`
        :returns: None
        :rtype: None
        :raises: None
        """
        log.debug('Viewing task %s', task.name)
        self.cur_task = None
        self.pages_tabw.setCurrentIndex(7)

        self.task_dep_le.setText(task.name)
        statusmap = {"New": 0, "Open": 1, "Done":2}
        self.task_status_cb.setCurrentIndex(statusmap.get(task.status, -1))
        dt = dt_to_qdatetime(task.deadline) if task.deadline else None
        self.task_deadline_de.setDateTime(dt)

        self.task_link_le.setText(task.element.name)

        userrootdata = treemodel.ListItemData(['Username', 'First', 'Last', 'Email'])
        userrootitem = treemodel.TreeItem(userrootdata)
        for user in task.users.all():
            userdata = djitemdata.UserItemData(user)
            treemodel.TreeItem(userdata, userrootitem)
        self.task_user_model = treemodel.TreeModel(userrootitem)
        self.task_user_tablev.setModel(self.task_user_model)

        self.cur_task = task

    def shot_save(self, ):
        """Save the current shot

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_shot:
            return

        desc = self.shot_desc_pte.toPlainText()
        start = self.shot_start_sb.value()
        end = self.shot_end_sb.value()
        handle = self.shot_handle_sb.value()
        self.cur_shot.description = desc
        self.cur_shot.startframe = start
        self.cur_shot.endframe = end
        self.cur_shot.handlesize = handle
        self.cur_shot.save()

    def asset_view_prj(self, ):
        """View the project of the current asset

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return

        prj = self.cur_asset.project
        self.view_prj(prj)

    def asset_view_atype(self, ):
        """View the project of the current atype

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return

        atype = self.cur_asset.atype
        self.view_atype(atype)

    def atype_view_prj(self, ):
        """View the project of the current assettype

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_atype:
            return

        i = self.atype_prj_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            prj = item.internal_data()
            self.view_prj(prj)

    def atype_create_prj(self, *args, **kwargs):
        """Create a new project

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_atype:
            return
        prj = self.create_prj()
        if prj:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, self.atype_prj_model.root)

    def atype_add_prj(self, *args, **kwargs):
        """Add project to assettype

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_atype:
            return

        dialog = ProjectAdderDialog(atype=self.cur_atype)
        dialog.exec_()
        prjs = dialog.projects
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, self.atype_prj_model.root)

    def atype_view_asset(self, ):
        """View the project of the current assettype

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_atype:
            return

        i = self.atype_asset_treev.currentIndex()
        item = i.internalPointer()
        if item:
            asset = item.internal_data()
            if isinstance(asset, djadapter.models.Asset):
                self.view_asset(asset)

    def atype_create_asset(self, ):
        """Create a new asset

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_atype:
            return

        asset = self.create_asset(atype=self.cur_atype)

        if not asset:
            return
        prjs = {}
        for c in self.atype_asset_model.root.childItems:
            prjs[c.internal_data()] = c
        prjitem = prjs.get(asset.project)
        if not prjitem:
            prjdata = djitemdata.ProjectItemData(asset.project)
            prjitem = treemodel.TreeItem(prjdata, self.atype_asset_model.root)
            prjs[asset.project] = prjitem
        assetdata = djitemdata.AssetItemData(asset)
        treemodel.TreeItem(assetdata, prjitem)

    def atype_save(self):
        """Save the current atype

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_atype:
            return

        desc = self.atype_desc_pte.toPlainText()
        self.cur_atype.description = desc
        self.cur_atype.save()

    def asset_view_asset(self, ):
        """View the task that is currently selected on the asset page

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return

        i = self.asset_asset_treev.currentIndex()
        item = i.internalPointer()
        if item:
            asset = item.internal_data()
            if isinstance(asset, djadapter.models.Asset):
                self.view_asset(asset)

    def asset_add_asset(self, *args, **kwargs):
        """Add more assets to the asset.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return
        dialog = AssetAdderDialog(asset=self.cur_asset)
        dialog.exec_()
        assets = dialog.assets
        atypes = {}
        for c in self.asset_asset_model.root.childItems:
            atypes[c.internal_data()] = c
        for asset in assets:
            atypeitem = atypes.get(asset.atype)
            if not atypeitem:
                atypedata = djitemdata.AtypeItemData(asset.atype)
                atypeitem = treemodel.TreeItem(atypedata, self.asset_asset_model.root)
                atypes[asset.atype] = atypeitem
            assetdata = djitemdata.AssetItemData(asset)
            treemodel.TreeItem(assetdata, atypeitem)
        self.cur_asset.save()

    def asset_remove_asset(self, *args, **kwargs):
        """Remove the, in the asset table view selected, asset.

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return
        i = self.asset_asset_treev.currentIndex()
        item = i.internalPointer()
        if item:
            asset = item.internal_data()
            if not isinstance(asset, djadapter.models.Asset):
                return
            log.debug("Removing asset %s.", asset.name)
            item.set_parent(None)
            self.cur_asset.assets.remove(asset)

    def asset_create_asset(self, *args, **kwargs):
        """Create a new asset

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return
        asset = self.create_asset(asset=self.cur_asset)
        if not asset:
            return
        atypes = {}
        for c in self.asset_asset_model.root.childItems:
            atypes[c.internal_data()] = c
        atypeitem = atypes.get(asset.atype)
        if not atypeitem:
            atypedata = djitemdata.AtypeItemData(asset.atype)
            atypeitem = treemodel.TreeItem(atypedata, self.asset_asset_model.root)
            atypes[asset.atype] = atypeitem
        assetdata = djitemdata.AssetItemData(asset)
        treemodel.TreeItem(assetdata, atypeitem)

    def asset_view_task(self, ):
        """View the task that is currently selected on the asset page

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return

        i = self.asset_task_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            task = item.internal_data()
            self.view_task(task)

    def asset_create_task(self, *args, **kwargs):
        """Create a new task

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return
        task = self.create_task(element=self.cur_asset)
        if task:
            taskdata = djitemdata.TaskItemData(task)
            treemodel.TreeItem(taskdata, self.asset_task_model.root)

    def asset_save(self):
        """Save the current asset

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_asset:
            return

        desc = self.asset_desc_pte.toPlainText()
        self.cur_asset.description = desc
        self.cur_asset.save()

    def dep_view_prj(self, ):
        """View the project that is currently selected

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_dep:
            return
        i = self.dep_prj_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            prj = item.internal_data()
            self.view_prj(prj)

    def dep_add_prj(self, *args, **kwargs):
        """Add projects to the current department

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_dep:
            return

        dialog = ProjectAdderDialog(department=self.cur_dep)
        dialog.exec_()
        prjs = dialog.projects
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, self.dep_prj_model.root)

    def dep_remove_prj(self, *args, **kwargs):
        """Remove the selected project from the department

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_dep:
            return
        i = self.dep_prj_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            prj = item.internal_data()
            self.cur_dep.projects.remove(prj)
            item.set_parent(None)

    def dep_save(self, ):
        """Save the current department

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_dep:
            return
        ordervalue = self.dep_ordervalue_sb.value()
        desc = self.dep_desc_pte.toPlainText()
        self.cur_dep.ordervalue = ordervalue
        self.cur_dep.description = desc
        self.cur_dep.save()

    def task_view_user(self, ):
        """View the user that is currently selected

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_task:
            return
        i = self.task_user_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            user = item.internal_data()
            self.view_user(user)

    def task_add_user(self, *args, **kwargs):
        """Add users to the current task

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_task:
            return

        dialog = UserAdderDialog(task=self.cur_task)
        dialog.exec_()
        users = dialog.users
        for user in users:
            userdata = djitemdata.UserItemData(user)
            treemodel.TreeItem(userdata, self.task_user_model.root)

    def task_remove_user(self, *args, **kwargs):
        """Remove the selected user from the task

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_task:
            return
        i = self.task_user_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            user = item.internal_data()
            self.cur_task.users.remove(user)
            item.set_parent(None)

    def task_view_dep(self, ):
        """View the departmetn of the current task

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_task:
            return
        self.view_dep(self.cur_task.department)

    def task_view_link(self, ):
        """View the link of the current task

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_task:
            return
        e = self.cur_task.element
        if isinstance(e, djadapter.models.Asset):
            self.view_asset(e)
        else:
            self.view_shot(e)

    def task_save(self, ):
        """Save the current task

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_task:
            return
        deadline = self.task_deadline_de.dateTime().toPython()
        status = self.task_status_cb.currentText()
        self.cur_task.deadline = deadline
        self.cur_task.status = status
        self.cur_task.save()

    def users_view_user(self, ):
        """View the user that is currently selected

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.users_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            user = item.internal_data()
            self.view_user(user)

    def user_view_task(self, ):
        """View the task that is selected

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_user:
            return
        i = self.user_task_treev.currentIndex()
        item = i.internalPointer()
        if item:
            task = item.internal_data()
            if isinstance(task, djadapter.models.Task):
                self.view_task(task)

    def user_view_prj(self, ):
        """View the project that is currently selected

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.user_prj_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            prj = item.internal_data()
            self.view_prj(prj)

    def user_add_prj(self, *args, **kwargs):
        """Add projects to the current user

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_user:
            return

        dialog = ProjectAdderDialog(user=self.cur_user)
        dialog.exec_()
        prjs = dialog.projects
        for prj in prjs:
            prjdata = djitemdata.ProjectItemData(prj)
            treemodel.TreeItem(prjdata, self.user_prj_model.root)

    def user_remove_prj(self, *args, **kwargs):
        """Remove the selected project from the user

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_user:
            return
        i = self.user_prj_tablev.currentIndex()
        item = i.internalPointer()
        if item:
            prj = item.internal_data()
            prj.users.remove(self.cur_user)
            item.set_parent(None)

    def user_save(self):
        """Save the current user

        :returns: None
        :rtype: None
        :raises: None
        """
        if not self.cur_user:
            return

        username = self.user_username_le.text()
        first = self.user_first_le.text()
        last = self.user_last_le.text()
        email = self.user_email_le.text()
        self.cur_user.username = username
        self.cur_user.first_name = first
        self.cur_user.last_name = last
        self.cur_user.email = email
        self.cur_user.save()


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
