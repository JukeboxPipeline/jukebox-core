from PySide import QtGui

from jukeboxcore.gui.widgets import commentwidget_ui
from jukeboxcore.gui.main import dt_to_qdatetime, get_icon


class CommentWidget(commentwidget_ui.Ui_CommentWidget, QtGui.QFrame):
    """A widget to display comments
    """

    def __init__(self, parent=None):
        """Create a new CommentWidget

        :param parent: widget parent
        :type parent: QtGui.QWidget
        :raises: None
        """
        super(CommentWidget, self).__init__(parent)
        self.setupUi(self)
        self.setAutoFillBackground(True)
        self.setFrameShadow(self.Sunken)
        self.setFrameStyle(self.StyledPanel)
        self.setFrameShadow(self.Sunken)

        user_pix = get_icon('glyphicons_003_user.png', aspix=True)
        self.user_lb.setPixmap(user_pix)

    def set_index(self, index):
        """Display the data of the given index

        :param index: the index to paint
        :type index: QtCore.QModelIndex
        :returns: None
        :rtype: None
        :raises: None
        """
        item = index.internalPointer()
        note = item.internal_data()
        self.content_lb.setText(note.content)
        self.created_dte.setDateTime(dt_to_qdatetime(note.date_created))
        self.updated_dte.setDateTime(dt_to_qdatetime(note.date_updated))
        self.username_lb.setText(note.user.username)
