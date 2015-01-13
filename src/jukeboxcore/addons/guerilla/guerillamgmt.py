from PySide import QtGui

from jukeboxcore.log import get_logger
log = get_logger(__name__)

from jukeboxcore.gui.main import JB_MainWindow
from jukeboxcore.plugins import JB_CoreStandaloneGuiPlugin
from jukeboxcore.gui.widgets.guerillamgmt_ui import Ui_guerillamgmt_mwin


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
        super(GuerillaMGMTWin, self).__init__(parent)
        self.setupUi(self)
        self.setup_ui()
        self.setup_signals()

    def setup_ui(self, ):
        """Create all necessary ui elements for the tool

        :returns: None
        :rtype: None
        :raises: None
        """
        pass

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
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

    def setup_prjs_signals(self, ):
        """Setup the signals for the projects page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.prjs_prj_view_pb.clicked.connect(self.prjs_view_prj)
        self.prjs_prj_create_pb.clicked.connect(self.prjs_create_prj)

    def setup_prj_signals(self, ):
        """Setup the signals for the project page

        :returns: None
        :rtype: None
        :raises: None
        """
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
        self.users_user_view_pb.clicked.connect(self.users_view_user)
        self.users_user_create_pb.clicked.connect(self.users_create_user)

    def setup_user_signals(self, ):
        """Setup the signals for the user page

        :returns: None
        :rtype: None
        :raises: None
        """
        self.user_task_view_pb.clicked.connect(self.user_view_task)
        self.user_prj_view_pb.clicked.connect(self.user_view_prj)
        self.user_prj_add_pb.clicked.connect(self.user_add_prj)
        self.user_prj_remove_pb.clicked.connect(self.user_remove_prj)
        self.user_username_le.editingFinished.connect(self.users_save)
        self.user_first_le.editingFinished.connect(self.users_save)
        self.user_last_le.editingFinished.connect(self.users_save)
        self.user_email_le.editingFinished.connect(self.users_save)


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
