from PySide import QtGui

from jukeboxcore.release import Release
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
        self.setupUi(self)
        self.setup_ui()
        self.setup_signals()
        self.browser.init_selection()
        self.filetype = filetype

    def setup_ui(self, ):
        """Create the browsers and all necessary ui elements for the tool

        :returns: None
        :rtype: None
        :raises: None
        """
        w = QtGui.QWidget(self)
        w.setLayout(self.central_vbox)
        self.setCentralWidget(w)
        self.browser = FileBrowser(self.filetype, self.get_current_file, self)
        self.central_vbox.insertWidget(0, self.browser)

        self.comment_pte = self.create_comment_edit()
        self.central_vbox.addWidget(self.comment_pte)

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
        checks = self.get_checks()
        cleanups = self.get_cleanups()
        comment = self.get_comment()
        r = Release(tf, checks, cleanups, comment)
        r.release()
