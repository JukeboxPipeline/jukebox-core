"""A Dialog Window to display the result of a :class:`jukeboxcore.action.ActionCollection`."""
from jukeboxcore.gui.main import JB_Dialog
from jukeboxcore.gui.actionreport import create_action_model
from actionreportdialog_ui import Ui_ActionReportDialog


class ActionReportDialog(JB_Dialog, Ui_ActionReportDialog):
    """A dialog that can show the result of a :class:`jukeboxcore.action.ActionCollection`

    The dialog will ask the user to confirm the report or cancel.

    The dialog uses the actionreportdialog.ui for it's layout.
    """

    def __init__(self, actioncollection, parent=None, flags=0):
        """Construct a new dialog for the given action collection

        :param actioncollection: the action collection to report
        :type actioncollection: :class:`jukeboxcore.action.ActionCollection`
        :param parent: Optional - the parent of the window - default is None
        :type parent: QWidget
        :param flags: the window flags
        :type flags: QtCore.Qt.WindowFlags
        :raises: None
        """
        super(ActionReportDialog, self).__init__(parent, flags)
        self.setupUi(self)
        self._actioncollection = actioncollection
        self._parent = parent
        self._flags = flags

        status = self._actioncollection.status()
        self.status_lb.setText(status.value)
        self.message_lb.setText(status.message)
        self.traceback_pte.setPlainText(status.traceback)

        self.traceback_pte.setVisible(False)

        model = create_action_model(self._actioncollection)
        self.actions_tablev.setModel(model)
