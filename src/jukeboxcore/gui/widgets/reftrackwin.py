"""A window that can be used for tools that handle the referene workflow."""

from PySide import QtGui

from jukeboxcore.gui.main import JB_MainWindow, get_icon
from reftrackwin_ui import Ui_reftrack_mwin


class ReftrackWin(JB_MainWindow, Ui_reftrack_mwin):
    """Display reftracks in a view that can be filtered, sorted etc.
    """

    def __init__(self, refobjinter, parent=None, flags=0):
        """Initialize a new Reftrack window with the given refobjinter

        :param parent: Optional - the parent of the window - default is None
        :type parent: QWidget
        :param flags: the window flags
        :type flags: QtCore.Qt.WindowFlags
        :raises: None
        """
        super(ReftrackWin, self).__init__(parent, flags)
        self.refobjinter = refobjinter

        self.setupUi(self)
        self.setup_ui()
        self.setup_signals()
        self.setup_icons()
