import os
import fnmatch

from PySide import QtGui

from jukeboxcore.log import get_logger
log = get_logger(__name__)
from jukeboxcore import iniconf
from jukeboxcore.constants import PLUGIN_CONFIG_DIR
from jukeboxcore.errors import ConfigError
from jukeboxcore.plugins import JB_CoreStandaloneGuiPlugin
from jukeboxcore.gui.configeditor import ConfigObjModel, InifilesModel
from jukeboxcore.gui.main import JB_MainWindow
from configer_ui import Ui_configer_mwin


class ConfigerWin(JB_MainWindow, Ui_configer_mwin):
    """A Configeditor window

    The window uses the configer.ui for it's Layout.
    It has a main editor treeview to edit the ConfigObjs.
    Next to it is a listview to select the configs.
    There are also two buttons. One is for saving, the other for reseting a value to its default.

    the get_configs method is used to gather all the config files in the userfolder and finding the corresponding configspec
    in any of the plugin folders.
    """

    def __init__(self, parent=None):
        """Constructs a new ConfigerWin

        :param parent: Optional - the parent of the window - default is None
        :type parent: QWidget
        :returns: None
        :rtype: None
        :raises: None

        This will also load all configs and display the first one.
        """
        super(ConfigerWin, self).__init__(parent)
        self.setupUi(self)

        self.confobjmodel = None
        self.inimodel = InifilesModel(self.get_configs())
        self.files_lv.setModel(self.inimodel)

        self.sm = self.files_lv.selectionModel()  #.currentChanged.connect(self.set_inifile)
        self.sm.currentChanged.connect(self.set_inifile)

        self.reset_pb.clicked.connect(self.reset_current_row)
        self.save_pb.clicked.connect(self.save_current_config)

    def reset_current_row(self, *args, **kwargs):
        """Reset the selected rows value to its default value

        :returns: None
        :rtype: None
        :raises: None
        """
        i = self.configobj_treev.currentIndex()
        m = self.configobj_treev.model()
        m.restore_default(i)

    def get_configs(self):
        """Load all config files and return the configobjs

        :returns: a list of configobjs
        :raises: None

        It always loads the coreconfig.
        Then it looks for all configs inside the PLUGIN_CONFIG_DIR.
        It will find the corresponding spec of the plugins.
        If there is a spec, but no ini, it will also be loaded!
        """
        # all loaded configs are stored in confs
        confs = []
        # always load core config. it is not part of the plugin configs
        try:
            confs.append(iniconf.get_core_config())
        except ConfigError, e:
            log.error("Could not load Core config! Reason was: %s" % e)

        # get config specs that lie in the plugin path
        # we have to watch the order we gather the specs
        # plugins can override each other, so can config specs
        # it depends on the order of the JUKEBOX_PLUGIN_PATH
        specs = {}
        pathenv = os.environ.get('JUKEBOX_PLUGIN_PATH', '')
        paths = pathenv.split(';')
        for p in reversed(paths):
            if p:
                files = self.find_inifiles(p)
                for ini in files:
                    base = os.path.basename(ini)
                    specs[base] = ini

        configs = {}
        files = self.find_inifiles(PLUGIN_CONFIG_DIR)
        for ini in files:
            base = os.path.basename(ini)
            configs[base] = ini

        # find matching pairs of configs and specs
        # and load them
        for k in configs:
            spec = specs.pop(k, None)
            conf = configs[k]
            try:
                confs.append(iniconf.load_config(conf, spec))
            except ConfigError, e:
                log.error("Could not load config %s, Reason was: %s" % (k ,e))

        # the remaining configspecs can be used to create
        # empty configs
        for k in specs:
            spec = specs[k]
            conf = os.path.join(PLUGIN_CONFIG_DIR, k)
            try:
                confs.append(iniconf.load_config(conf, spec))
            except ConfigError, e:
                log.error("Could not load config %s, Reason was: %s" % (k ,e))

        return confs

    def find_inifiles(self, path):
        """Return all ini-files in the directory of path and below

        :param path: a path to a directory
        :type path: str
        :returns: list of configfiles
        :rtype: list of str
        :raises: None
        """
        matches = []
        for root, dirnames, filenames in os.walk(path):
            for filename in fnmatch.filter(filenames, '*.ini'):
                matches.append(os.path.join(root, filename))
        return matches

    def set_inifile(self, current, previous):
        """Set the configobj to the current index of the files_lv

        This is a slot for the currentChanged signal

        :param current: the modelindex of a inifilesmodel that should be set for the configobj_treev
        :type current: QModelIndex
        :param previous: the previous selected index
        :type previous: QModelIndex
        :returns: None
        :raises: None
        """
        c = self.inimodel.data(current, self.inimodel.confobjRole)
        self.confobjmodel = ConfigObjModel(c)
        self.configobj_treev.setModel(self.confobjmodel)
        self.configobj_treev.expandAll()
        self.confobjmodel.dataChanged.connect(self.iniedited)

    def iniedited(self, *args, **kwargs):
        """Set the current index of inimodel to modified

        :returns: None
        :rtype: None
        :raises: None
        """
        self.inimodel.set_index_edited(self.files_lv.currentIndex(), True)

    def closeEvent(self, event):
        """Handles closing of the window. If configs were edited, ask user to continue.

        :param event: the close event
        :type event: QCloseEvent
        :returns: None
        :rtype: None
        :raises: None
        """
        if self.inimodel.get_edited():
            r = self.doc_modified_prompt()
            if r == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def doc_modified_prompt(self, ):
        """Create a message box, that asks the user to continue although files have been modified

        :returns: value of the standard button of qmessagebox that has been pressed. Either Yes or Cancel.
        :rtype: QtGui.QMessageBox.StandardButton
        :raises: None
        """
        msgbox = QtGui.QMessageBox()
        msgbox.setWindowTitle("Discard changes?")
        msgbox.setText("Documents have been modified.")
        msgbox.setInformativeText("Do you really want to exit? Changes will be lost!")
        msgbox.setStandardButtons(msgbox.Yes | msgbox.Cancel)
        msgbox.setDefaultButton(msgbox.Cancel)
        msgbox.exec_()
        return msgbox.result()

    def invalid_prompt(self, ):
        """Create a message box, that asks the user to continue although files are invalid

        :returns: value of the standard button of qmessagebox that has been pressed. Either Yes or Cancel.
        :rtype: QtGui.QMessageBox.StandardButton
        :raises: None
        """
        msgbox = QtGui.QMessageBox()
        msgbox.setWindowTitle("Invalid Config!")
        msgbox.setText("Invalid Configs!")
        msgbox.setInformativeText("Do you really want to continue? Invalid values will be replaced by their default!")
        msgbox.setStandardButtons(msgbox.Yes | msgbox.Cancel)
        msgbox.setDefaultButton(msgbox.Cancel)
        msgbox.exec_()
        return msgbox.result()

    def save_current_config(self, ):
        """Saves the currently displayed config

        :returns: None
        :rtype: None
        :raises: None

        This resets the edited status of the file to False.
        Also asks the user to continue if config is invalid.

        """
        # check if all configs validate correctly
        btn = None
        for row in range(self.inimodel.rowCount()):
            i = self.inimodel.index(row, 0)
            r = self.inimodel.validate(i)
            if r is not True:
                btn = self.invalid_prompt()
                break

        if btn == QtGui.QMessageBox.Cancel:
            return
        current = self.files_lv.currentIndex()
        c = self.inimodel.data(current, self.inimodel.confobjRole)
        c.write()
        self.inimodel.set_index_edited(current, False)


class Configer(JB_CoreStandaloneGuiPlugin):
    """A plugin that can run a ConfigEditor

    This can be used as a standalone plugin.
    Before you call run, make sure that there is a running
    QApplication running. See :mod:`jukeboxcore.gui.main` for helpful functions.

    """

    author = "David Zuber"
    copyright = "2014"
    version = "0.1"
    description = "A tool for editing config files"

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

    def run(self, ):
        """Start the configeditor

        :returns: None
        :rtype: None
        :raises: None
        """
        self.cw = ConfigerWin()
        self.cw.show()
