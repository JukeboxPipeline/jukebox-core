import os

from PySide import QtGui
from django.core.exceptions import ValidationError

from jukeboxcore.log import get_logger
log = get_logger(__name__)

import jukedj
from jukeboxcore import djadapter
from jukeboxcore.filesys import JB_File, TaskFileInfo
from jukeboxcore.plugins import JB_CorePlugin
from jukeboxcore.gui.main import JB_MainWindow, get_icon
from jukeboxcore.gui.widgets.filebrowser import FileBrowser
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
        releasetypes = [djadapter.RELEASETYPES['work'], djadapter.RELEASETYPES['release'], djadapter.RELEASETYPES['handoff']]
        self.browser = FileBrowser(self._filetype, releasetypes, self.get_current_file, self)
        self.central_vbox.insertWidget(0, self.browser)

        self.asset_comment_pte = self.create_comment_edit()
        self.browser.asset_vbox.addWidget(self.asset_open_pb)
        self.asset_new_hbox = QtGui.QHBoxLayout()
        self.asset_new_hbox.addWidget(self.asset_save_pb)
        self.asset_new_hbox.addWidget(self.asset_descriptor_lb)
        self.asset_new_hbox.addWidget(self.asset_descriptor_le)
        self.browser.asset_vbox.addLayout(self.asset_new_hbox)
        self.browser.asset_vbox.addWidget(self.asset_comment_pte)
        self.shot_comment_pte = self.create_comment_edit()
        self.browser.shot_vbox.addWidget(self.shot_open_pb)
        self.shot_new_hbox = QtGui.QHBoxLayout()
        self.shot_new_hbox.addWidget(self.shot_save_pb)
        self.shot_new_hbox.addWidget(self.shot_descriptor_lb)
        self.shot_new_hbox.addWidget(self.shot_descriptor_le)
        self.browser.shot_vbox.addLayout(self.shot_new_hbox)
        self.browser.shot_vbox.addWidget(self.shot_comment_pte)

        ph = "Enter New Descriptor"
        self.asset_descriptor_le.setPlaceholderText(ph)
        self.shot_descriptor_le.setPlaceholderText(ph)

        self.setup_icons()

    def setup_icons(self, ):
        """Set all icons on buttons

        :returns: None
        :rtype: None
        :raises: None
        """
        folder_icon = get_icon('glyphicons_144_folder_open.png', asicon=True)
        self.asset_open_pb.setIcon(folder_icon)
        self.shot_open_pb.setIcon(folder_icon)

        floppy_icon = get_icon('glyphicons_446_floppy_save.png', asicon=True)
        self.asset_save_pb.setIcon(floppy_icon)
        self.shot_save_pb.setIcon(floppy_icon)

    def setup_signals(self, ):
        """Connect the signals with the slots to make the ui functional

        :returns: None
        :rtype: None
        :raises: None
        """
        self.browser.shot_taskfile_sel_changed.connect(self.shot_taskfile_sel_changed)
        self.browser.asset_taskfile_sel_changed.connect(self.asset_taskfile_sel_changed)

        self.shot_open_pb.clicked.connect(self.shot_open_callback)
        self.asset_open_pb.clicked.connect(self.asset_open_callback)
        self.shot_save_pb.clicked.connect(self.shot_save_callback)
        self.asset_save_pb.clicked.connect(self.asset_save_callback)

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

    def asset_taskfile_sel_changed(self, tf):
        """Callback for when the version selection has changed

        :param tf: the selected taskfileinfo
        :type tf: :class:`TaskFileInfo` | None
        :returns: None
        :rtype: None
        :raises: None
        """
        self.asset_open_pb.setEnabled(bool(tf))
        # only allow new, when there is an asset. if there is an asset, there should always be a task
        enablenew = bool(self.browser.assetbrws.selected_indexes(1)) and self.browser.get_releasetype() == djadapter.RELEASETYPES['work']
        self.asset_save_pb.setEnabled(enablenew)
        self.asset_descriptor_le.setEnabled(enablenew)
        self.asset_comment_pte.setEnabled(enablenew)
        self.update_descriptor_le(self.asset_descriptor_le, tf)

    def shot_taskfile_sel_changed(self, tf):
        """Callback for when the version selection has changed

        :param tf: the selected taskfileinfo
        :type tf: :class:`TaskFileInfo` | None
        :returns: None
        :rtype: None
        :raises: None
        """
        self.shot_open_pb.setEnabled(bool(tf))
        # only allow new, if the releasetype is work
        # only allow new, if there is a shot. if there is a shot, there should always be a task.
        enablenew = bool(self.browser.shotbrws.selected_indexes(1)) and self.browser.get_releasetype() == djadapter.RELEASETYPES['work']
        self.shot_save_pb.setEnabled(enablenew)
        self.shot_descriptor_le.setEnabled(enablenew)
        self.shot_comment_pte.setEnabled(enablenew)
        self.update_descriptor_le(self.shot_descriptor_le, tf)

    def update_descriptor_le(self, lineedit, tf):
        """Update the given line edit to show the descriptor that is stored in the index

        :param lineedit: the line edit to update with the descriptor
        :type lineedit: QLineEdit
        :param tf: the selected taskfileinfo
        :type tf: :class:`TaskFileInfo` | None
        :returns: None
        :rtype: None
        :raises: None
        """
        if tf:
            descriptor = tf.descriptor
            lineedit.setText(descriptor)
        else:
            lineedit.setText("")

    def get_current_file(self, ):
        """Return the taskfile that is currently open or None if no taskfile is open

        :returns: the open taskfile or None if no taskfile is open
        :rtype: :class:`djadapter.models.TaskFile` | None
        :raises: NotImplementedError
        """
        raise NotImplementedError

    def shot_open_callback(self, *args, **kwargs):
        """Callback for the shot open button

        :returns: None
        :rtype: None
        :raises: None
        """
        tf = self.browser.get_current_selection(1)
        if not tf:
            return
        if not os.path.exists(tf.path):
            msg = 'The selected shot does not exist: %s' % tf.path
            log.error(msg)
            self.statusbar.showMessage(msg)
            return
        self.open_shot(tf)

    def asset_open_callback(self, *args, **kwargs):
        """Callback for the shot open button

        :returns: None
        :rtype: None
        :raises: None
        """
        tf = self.browser.get_current_selection(0)
        if not tf:
            return
        if not os.path.exists(tf.path):
            msg = 'The selected asset does not exist: %s' % tf.path
            log.error(msg)
            self.statusbar.showMessage(msg)
            return
        self.open_asset(tf)

    def shot_save_callback(self, *args, **kwargs):
        """Callback for the shot open button

        :returns: None
        :rtype: None
        :raises: None
        """
        tasksel = self.browser.shotbrws.selected_indexes(2)
        if not tasksel or not tasksel[0].isValid():
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
        tasksel = self.browser.assetbrws.selected_indexes(2)
        if not tasksel or not tasksel[0].isValid():
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
        self.browser.update_model(tfi)

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
            jukedj.validators.alphanum_vld(descriptor)
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
        if tfi.task.department.assetflag:
            comment = self.asset_comment_pte.toPlainText()
        else:
            comment = self.shot_comment_pte.toPlainText()
        return tfi.create_db_entry(comment)


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
