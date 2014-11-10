from PySide import QtGui

from jukeboxcore import djadapter
from jukeboxcore.release import Release
from jukeboxcore.action import ActionCollection
from jukeboxcore.filesys import TaskFileInfo
from jukeboxcore.gui.main import JB_MainWindow, get_icon
from jukeboxcore.gui.widgets.filebrowser import FileBrowser
from jukeboxcore.gui.widgets.textedit import JB_PlainTextEdit
from releasewin_ui import Ui_release_mwin


class ReleaseWin(JB_MainWindow, Ui_release_mwin):
    """A window with a file browser and controls to create a new release.
    """

    def __init__(self, filetype, parent=None, flags=0):
        """Constructs a new Release Window with the given parent

        :param filetype: the filetype the browser should display from :data:`djadapter.FILETYPES`
        :type filetypes: str
        :param parent: Optional - the parent of the window - default is None
        :type parent: QWidget
        :param flags: the window flags
        :type flags: QtCore.Qt.WindowFlags
        :raises: None
        """
        super(ReleaseWin, self).__init__(parent, flags)
        self.filetype = filetype
        self.setupUi(self)
        self.setup_ui()
        self.setup_signals()
        self.browser.init_selection()
        self.release_actions = None

    def setup_ui(self, ):
        """Create the browsers and all necessary ui elements for the tool

        :returns: None
        :rtype: None
        :raises: None
        """
        w = QtGui.QWidget(self)
        w.setLayout(self.central_vbox)
        self.setCentralWidget(w)
        releasetypes= [djadapter.RELEASETYPES["work"]]
        self.browser = FileBrowser(self.filetype, releasetypes, None, self)
        self.central_vbox.insertWidget(0, self.browser)

        self.comment_pte = self.create_comment_edit()
        self.central_vbox.addWidget(self.comment_pte)
        self.option_gb.setVisible(False)

        self.setup_icons()

    def setup_icons(self, ):
        """Set all icons on buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        floppy_icon = get_icon('glyphicons_446_floppy_save.png', asicon=True)
        self.release_pb.setIcon(floppy_icon)

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
        self.release_pb.clicked.connect(self.release_callback)

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

    def release_callback(self, *args, **kwargs):
        """Create a new release

        :returns: None
        :rtype: None
        :raises: None
        """
        tf = self.browser.get_current_selection()
        if not tf:
            self.statusbar.showMessage("Select a file to release, please!")
            return
        tfi = TaskFileInfo(tf.task, tf.version, tf.releasetype, tf.typ, tf.descriptor)
        checks = self.get_checks()
        cleanups = self.get_cleanups()
        comment = self.get_comment()
        r = Release(tfi, checks, cleanups, comment)
        self.statusbar.showMessage("Release in progress...")
        success = r.release()
        if success:
            self.statusbar.showMessage("Success!")
        else:
            self.statusbar.showMessage("Release canceled by user!")

    def set_release_actions(self, actions):
        """Set the widget that gives users options about the release, e.g. importing references

        :param actions: Release actions that define the sanity checks and cleanup actions
        :type actions: :class:`jukeboxcore.release.ReleaseActions`
        :returns: None
        :rtype: None
        :raises: None
        """
        self.release_actions = actions
        self.option_widget = self.release_actions.option_widget()
        if self.option_widget:
            self.option_vbox.addWidget(self.option_widget)
            self.option_gb.setVisible(True)

    def get_checks(self, ):
        """Get the sanity checks for the release from the release option widget

        :returns: the sanity checks
        :rtype: :class:`jukeboxcore.action.ActionCollection`
        :raises: None
        """
        if self.release_actions:
            return self.release_actions.get_checks()
        else:
            return ActionCollection([])

    def get_cleanups(self, ):
        """Get the cleanup actions for the release from the release option widget

        :returns: the cleanup actions
        :rtype: :class:`jukeboxcore.action.ActionCollection`
        :raises: None
        """
        if self.release_actions:
            return self.release_actions.get_cleanups()
        else:
            return ActionCollection([])

    def get_comment(self, ):
        """Return the comment for the release from the UI

        :returns: the comment
        :rtype: str
        :raises: None
        """
        return self.comment_pte.toPlainText()
